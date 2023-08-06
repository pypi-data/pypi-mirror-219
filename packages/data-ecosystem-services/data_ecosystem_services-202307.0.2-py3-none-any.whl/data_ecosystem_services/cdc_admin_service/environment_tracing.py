""" Module for python tracing for cdc_tech_environment_service with minimal dependencies. """

import os
import sys
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor, SpanExporter, SpanExportResult
from opentelemetry.sdk.trace.export import ReadableSpan
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.trace.status import StatusCode
import opentelemetry.sdk.trace.export as trace_export
import time
from data_ecosystem_services.cdc_admin_service import (
    environment_logging as pade_env_logging
)

# Import from sibling directory ..\cdc_tech_environment_service
OS_NAME = os.name


sys.path.append("..")

ENV_SHARE_FALLBACK_PATH = '/usr/local/share'

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
    TRACE_FILENAME = ENV_SHARE_PATH + "\\data_ecosystem_services_tracing.txt"
else:
    print("environment_logging: non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))
    env_path = os.path.dirname(os.path.abspath(sys.executable + "/.."))
    ENV_SHARE_PATH = env_path + "/share"
    sys.path.append(os.path.dirname(
        os.path.abspath(sys.executable + "/../share")))
    TRACE_FILENAME = ENV_SHARE_PATH + "/data_ecosystem_services_tracing.txt"
    ENV_SHARE_PATH = os.path.expanduser("~") + '/share'

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
            TRACE_FILENAME = ENV_SHARE_FALLBACK_PATH + \
                "/data_ecosystem_services_tracing.txt"

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class FileTraceExporter(SpanExporter):

    def __init__(self):
        self.file_path = TRACE_FILENAME
        os.makedirs(os.path.dirname(ENV_SHARE_PATH), exist_ok=True)

    def to_readable_dict(self, span):
        return {
            "trace_id": str(span.get_span_context().trace_id),
            "span_id": str(span.get_span_context().span_id),
            "parent_id": str(span.parent.span_id) if span.parent else None,
            "name": span.name,
            "status": StatusCode(span.status.status_code).name,
            "kind": span.kind.name,
            "start_time": str(span.start_time),
            "end_time": str(span.end_time),
            "attributes": dict(span.attributes),
        }

    def export(self, spans):
        for span in spans:
            span_dict = self.to_readable_dict(span)
            # TODO export to logger or azure trace
        return SpanExportResult.SUCCESS

    @staticmethod
    def delete_old_files():
        folder_path = ENV_SHARE_PATH
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.getmtime(file_path) < time.time() - 7 * 86400:
                os.remove(file_path)


class TracerSingleton:
    """
    A Python wrapper class around OpenTelemetry Tracer using a 
    singleton design pattern, so that the tracer instance is created 
    only once and the same instance is used throughout the application.

    This class is designed to be a singleton to ensure that there's only
    one tracer instance throughout the application.

    Raises:
        Exception: If an attempt is made to create another instance
                   of this singleton class.

    Returns:
        TracerSingleton: An instance of the TracerSingleton class.
    """

    _instance = None
    log_to_console = False  # Set to False if you want console logging

    @staticmethod
    def instance(calling_namespace_name, calling_service_name):
        """Provides access to the singleton instance of the LoggerSingleton 
        class.

        This method ensures there is only one instance of the LoggerSingleton 
        class in the application.
        If an instance already exists, it returns that instance. If no 
        instance exists, it creates a new one and then returns that.
        """
        if TracerSingleton._instance is None:
            TracerSingleton(calling_namespace_name, calling_service_name)
        return TracerSingleton._instance

    def __init__(self, calling_namespace_name, calling_service_name):
        """Initializes the singleton instance, if it doesn't exist yet.

        This method is responsible for ensuring that only a single instance 
        of the class is created. If an instance doesn't exist at the time of 
        invocation, it will be created. If an instance already exists, 
        the existing instance will be used.
        """
        if TracerSingleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            TracerSingleton._instance = self

        # Define a Resource with your service.name attribute
        resource = Resource.create(
            {ResourceAttributes.SERVICE_NAME: calling_service_name,
             ResourceAttributes.SERVICE_NAMESPACE: calling_namespace_name})

        # Set tracer provider
        trace.set_tracer_provider(TracerProvider(resource=resource))

        # Check if the environment variable is set
        if "APPLICATIONINSIGHTS_CONNECTION_STRING" in os.environ:
            # This is the exporter that sends data to Application Insights
            azure_trace_exporter = AzureMonitorTraceExporter(
                connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
            )
            # Create a BatchSpanProcessor and add the exporter to it
            azure_span_processor = BatchSpanProcessor(azure_trace_exporter)
            # add to the tracer provider
            trace.get_tracer_provider().add_span_processor(azure_span_processor)
        else:
            print(
                "The environment variable APPLICATIONINSIGHTS_CONNECTION_STRING is not set.")

        file_trace_exporter = FileTraceExporter()
        file_span_processor = BatchSpanProcessor(file_trace_exporter)

        trace.get_tracer_provider().add_span_processor(file_span_processor)
        # Add ConsoleSpanExporter if log_to_console is True
        if TracerSingleton.log_to_console:
            trace.get_tracer_provider().add_span_processor(
                SimpleSpanProcessor(ConsoleSpanExporter()))

        # Get tracer
        self.tracer = trace.get_tracer(__name__)

    def get_tracer(self):
        """
        Get the logger instance.

        Returns:
            logging.Logger: The logger instance.
        """
        return self.tracer

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
        trace.get_tracer_provider().force_flush()
