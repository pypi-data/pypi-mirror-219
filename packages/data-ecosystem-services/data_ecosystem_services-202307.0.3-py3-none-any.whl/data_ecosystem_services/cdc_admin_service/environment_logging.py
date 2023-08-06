""" Module for python logging for cdc_tech_environment_service with minimal dependencies. """

import sys  # don't remove required for error handling
import os
import logging
import logging.config
import logging.handlers
from logging.handlers import TimedRotatingFileHandler
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from datetime import datetime
import traceback
import inspect
import platform

from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing
)


from opentelemetry.sdk._logs import (
    LoggingHandler,
    LoggerProvider
)

from opentelemetry._logs import (

    set_logger_provider,
)

from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter


# Import from sibling directory ..\cdc_tech_environment_service
OS_NAME = os.name

ENV_SHARE_FALLBACK_PATH = '/usr/local/share'

sys.path.append("..")
if OS_NAME.lower() == "nt":
    print("environment_logging: windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(
        os.path.abspath(__file__ + "\\..\\..\\..")))
    env_path = os.path.dirname(os.path.abspath(sys.executable + "\\.."))
    ENV_SHARE_PATH = env_path + "\\share"
    sys.path.append(os.path.dirname(
        os.path.abspath(sys.executable + "\\..\\share")))
    LOG_FILENAME = ENV_SHARE_PATH + "\\data_ecosystem_services_logging.txt"
else:
    print("environment_logging: non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))
    env_path = os.path.dirname(os.path.abspath(sys.executable + "/.."))
    ENV_SHARE_PATH = env_path + "/share"
    ENV_SHARE_PATH = os.path.expanduser("~") + '/share'
    sys.path.append(os.path.dirname(
        os.path.abspath(sys.executable + "/../share")))
    LOG_FILENAME = ENV_SHARE_PATH + "/data_ecosystem_services_logging.txt"


try:
    FOLDER_EXISTS = os.path.exists(ENV_SHARE_PATH)
    if not FOLDER_EXISTS:
        # Create a new directory because it does not exist
        os.makedirs(ENV_SHARE_PATH)
except Exception as e:
    FOLDER_EXISTS = os.path.exists(ENV_SHARE_FALLBACK_PATH)
    if not FOLDER_EXISTS:
        if platform.system() != 'Windows':
            # Create a new directory because it does not exist
            os.makedirs(ENV_SHARE_FALLBACK_PATH)
            LOG_FILENAME = ENV_SHARE_FALLBACK_PATH + "/data_ecosystem_services_logging.txt"

print(f"Log files stored at LOG_FILENAME:{LOG_FILENAME}")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s\u001F%(name)s\u001F%(module)s\u001F%(lineno)d\u001F%(levelname)s\u001F%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "%(message)s",
        },
    },
    "handlers": {
        "logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "filename": LOG_FILENAME,
            "formatter": "default",
            "backupCount": 2,

        },
        "verbose_output": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "tryceratops": {
            "level": "INFO",
            "handlers": [
                "verbose_output",
            ],
        },
    },
    "root": {"level": "DEBUG", "handlers": ["logfile"]},
    "ocio_pade_dev": {"level": "DEBUG", "handlers": ["logfile"]},
}


# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class LoggerSingleton:
    """
    A Python wrapper class around OpenTelemetry Logger using a 
    singleton design pattern, so that the logger instance is created 
    only once and the same instance is used throughout the application.

    Raises:
        Exception: If an attempt is made to create another instance
                   of this singleton class.

    Returns:
        LoggerSingleton: An instance of the LoggerSingleton class.
    """
    _instance = None

    @staticmethod
    def instance(calling_namespace_name: str, calling_service_name: str):
        """Provides access to the singleton instance of the LoggerSingleton 
        class.

        This method ensures there is only one instance of the LoggerSingleton 
        class in the application.
        If an instance already exists, it returns that instance. If no 
        instance exists, it creates a new one and then returns that.
        """
        if LoggerSingleton._instance is None:
            LoggerSingleton(calling_namespace_name,
                            calling_service_name)
        return LoggerSingleton._instance

    def __init__(self, calling_namespace_name, calling_service_name):
        """Initializes the singleton instance, if it doesn't exist yet.

        This method is responsible for ensuring that only a single instance 
        of the class is created. If an instance doesn't exist at the time of 
        invocation, it will be created. If an instance already exists, 
        the existing instance will be used.
        """
        if LoggerSingleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            LoggerSingleton._instance = self

        self.calling_namespace_name = calling_namespace_name
        self.calling_service_name = calling_service_name
        logger_provider = LoggerProvider()
        set_logger_provider(logger_provider)

        connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

        if connection_string:
            log_exporter = AzureMonitorLogExporter(
                connection_string=connection_string)
            logger_provider.add_log_record_processor(
                BatchLogRecordProcessor(log_exporter))
        else:
            print(
                "APPLICATIONINSIGHTS_CONNECTION_STRING is not set.")

        # Attach LoggingHandler to root logger
        self.file_path = LOG_FILENAME
        os.makedirs(os.path.dirname(ENV_SHARE_PATH), exist_ok=True)
        # Create a console handler and set its log level to INFO
        format = LOGGING_CONFIG['formatters']['default']['format']
        datefmt = LOGGING_CONFIG['formatters']['default']['datefmt']

        self.azure_handler = LoggingHandler()

        formatter = logging.Formatter(format, datefmt)
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(formatter)
        self.console_handler.setLevel(logging.getLevelName(
            LOGGING_CONFIG['handlers']['verbose_output']['level']))

        self.file_handler = TimedRotatingFileHandler(
            self.file_path, when="midnight", interval=1, backupCount=7)
        # Set formatter for file handler
        self.file_handler.setFormatter(formatter)
        logger_name = f"{calling_namespace_name}:{calling_service_name}"
        self.logger = logging.getLogger(logger_name)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.azure_handler)

        # Set the threshold of logger to INFO
        self.logger.setLevel(logging.INFO)

    def get_exception_info(self, message, exc_info):
        """
        Retrieves detailed information about the most recently handled exception.

        This function should be called inside an 'except' block only. 
        It extracts and formats various details about the exception and its context, 
        such as the type and message of the exception, the filename and line number 
        where the exception occurred, the function name where the exception was raised,
        the current date and time, and the full stack trace.

        Args:
            message (str): Additional message to be included in the exception information.
            exc_info (tuple): The exception information as returned by sys.exc_info().
                The tuple should contain (type, value, traceback).

        Returns:
            dict: A dictionary containing detailed information about the exception. 
            The dictionary includes the following keys:
                - 'filename': The name of the file where the exception occurred.
                - 'lineno': The line number in the file where the exception occurred.
                - 'name': The name of the function where the exception occurred.
                - 'type': The type of the exception.
                - 'message': The exception message.
                - 'date_time': The current date and time when the exception is caught, formatted as 'YYYY-MM-DD HH:MM:SS'.
                - 'full_traceback': A list of strings describing the entire stack trace.

        Raises:
            TypeError: If exc_info is not a tuple or does not have three elements.
        """
        exc_type, exc_value, exc_traceback = exc_info
        message = message or str(exc_value) if message or exc_value else ""

        traceback_details = {
            "namespace": self.calling_namespace_name,
            "service": self.calling_service_name,
            "filename_pade": exc_traceback.tb_frame.f_code.co_filename,
            "lineno_pade": exc_traceback.tb_lineno,
            "name_pade": exc_traceback.tb_frame.f_code.co_name,
            "type_pade": exc_type.__name__,
            # or just str(exc_value) for the message alone
            "message_pade": str(message),
            "date_time_pade": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "full_traceback_pade": traceback.format_exception(exc_type, exc_value, exc_traceback)

        }

        return traceback_details

    def error_with_exception(self, message, exc_info):
        """
        Logs an error message with exception details (if available).

        Args:
            message (str): The error message to be logged.
            exc_info (tuple): The exception information as returned by sys.exc_info().
                The tuple should contain (type, value, traceback).

        Raises:
            TypeError: If exc_info is not a tuple or does not have three elements.
        """
        if not isinstance(exc_info, tuple) or len(exc_info) != 3:
            raise TypeError(
                "exc_info should be a tuple containing (type, value, traceback).")

        exc_type, exc_instance, exc_traceback = exc_info

        # Convert traceback object to a string
        exc_traceback_str = "".join(traceback.format_tb(exc_traceback))

        # Get the calling frame
        frame = inspect.currentframe().f_back

        # Get the parameter values from the calling frame
        args, _, _, values = inspect.getargvalues(frame)

        # Log the exception information
        exception_info = f"{exc_type.__name__}: {exc_instance}: {exc_traceback_str}"
        message = f"{message}: {exception_info}"
        self.logger.error(message)
        properties = self.get_exception_info(message, exc_info)
        # Add each parameter to the properties object
        for arg in args:
            property_name = f"parameter_{str(arg)}"
            properties[property_name] = values[arg]

        message = str(message)
        self.logger.exception(message, extra=properties)

    def truncate_log_file(self):
        """
        Truncate a log file.

        Returns:
        bool: True if the file was successfully truncated, False otherwise.
        """
        try:
            # 'w' mode will truncate the file.
            with open(LOG_FILENAME, 'w'):
                pass
            return 200
        except Exception as e:
            print(f"Unable to truncate file {LOG_FILENAME}. Error: {str(e)}")
            return 500

    def get_logger(self):
        """
        Get the logger instance.

        Returns:
            logging.Logger: The logger instance.
        """
        return self.logger

    def force_flush(self):
        """This method forces an immediate write of all log 
        messages currently in the buffer.

        In normal operation, log messages may be buffered for
        efficiency. This method ensures that all buffered messages 
        are immediately written to their destination. It can be 
        useful in scenarios where you want to ensure that all 
        log messages have been written out, such as before ending 
        a program.
        """
        for h in self.logger.handlers:
            h.flush()

    def get_datetime(self, entry):
        """
        Convert the first field of an entry to a datetime object.

        The log_entries will be sorted based on the datetime values returned by get_datetime.
        If parsing fails for an entry, the first field of that entry will be set to datetime.min.

        Args:
            entry (list): The entry containing datetime information.

        Returns:
            datetime: The datetime object converted from the first field of the entry,
            or datetime.min if parsing fails.
        """
        try:
            if type(entry) is str:
                entry = entry.split('\u001F')
            if len(entry) >= 2:
                date_time_str = entry[0]
                datetime_obj = datetime.strptime(
                    date_time_str, "%Y-%m-%d %H:%M:%S")
                return datetime_obj
            else:
                error_msg = "Could not parse datetime from entry " + str(entry)
                raise ValueError(error_msg)
        except (TypeError, ValueError) as ex:
            print(
                f"Could not parse datetime from entry: { str(entry)}. Error: {str(ex)}")
            return datetime.min

    def get_log_file_tail(self, number_of_lines=100):
        """
        Read the last number_of_lines from the log file, sorted by date in descending order.

        Args:
        file_path (str): The path to the log file.
        number_of_lines (int, optional): The number of lines to read from the end of the file. Defaults to 100.

        Returns:
        tuple: A tuple containing the actual number of lines read and the last number_of_lines of the log file.
        """

        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        try:
            self.force_flush()
            tracer_singleton.force_flush()
            with open(LOG_FILENAME, 'r') as file:

                lines = file.readlines()

                if lines is not None:
                    # Sort the lines by date in descending order
                    lines.sort(key=lambda entry: self.get_datetime(
                        entry), reverse=True)

                    # Get the actual number of lines to read
                    actual_number_of_lines = min(number_of_lines, len(lines))

                    # Get the last number_of_lines
                    last_lines = lines[:actual_number_of_lines]

                    # Combine the lines into a single string
                    log_content = ''.join(last_lines)
                    return 200, actual_number_of_lines, str(log_content)
                else:
                    # Handle the case when lines is None
                    actual_number_of_lines = 0
                    log_content = ""
                    return 500, actual_number_of_lines, str(log_content)

        except FileNotFoundError:
            error_msg = f"File {LOG_FILENAME} not found."
            return 500, 0, str(error_msg)
