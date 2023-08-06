""" Module for spark and os environment for cdc_tech_environment_service with
 minimal dependencies. """

# library management
from importlib import util  # library management
import subprocess

# error handling
from subprocess import check_output, Popen, PIPE, CalledProcessError

import sys  # don't remove required for error handling
import os

# files
import glob
import json
import platform

# http
from urllib.parse import urlparse
import requests

import data_ecosystem_services.cdc_tech_environment_service.repo_core as pade_repo

# azcopy and adls
from azure.identity import DefaultAzureCredential
from azure.identity import ManagedIdentityCredential
from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient
from azure.storage.filedatalake import DataLakeDirectoryClient
from azure.keyvault.secrets import SecretClient

# spark
from pyspark.sql import (SparkSession)
from pyspark.sql.types import (IntegerType, LongType, StringType, StructField,
                               StructType)

from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)


#  data
pyspark_pandas_loader = util.find_spec("pyspark.pandas")
pyspark_pandas_found = pyspark_pandas_loader is not None

if pyspark_pandas_found:
    # import pyspark.pandas  as pd
    # bug - pyspark version will not read local files in the repo
    import pyspark.pandas as pd
else:
    import pandas as pd


# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class EnvironmentFile:
    """ EnvironmentFile class with minimal dependencies for the developer
    service.
    - This class is used to perform file and directory operations.
    """

    # Get the currently running file name
    NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
    # Get the parent folder name of the running file
    SERVICE_NAME = os.path.basename(__file__)

    @staticmethod
    def class_exists() -> bool:
        """Basic check to make sure object is instantiated

        Returns:
            bool: true/false indicating object exists
        """
        return True

    @staticmethod
    def convert_abfss_to_https_path(abfss_path: str) -> str:
        """Converts abfs path to https path

        Args:
            abfss_path (str): abfss path

        Returns:
            str: https path
        """
        hostname = abfss_path.split('/')[2]
        file_system = hostname.split('@')[0]
        print(f"hostname:{hostname}")
        print(f"file_system:{file_system}")
        storage_account = hostname.split('@')[1]
        print(f"storage_account:{storage_account}")
        https_path = abfss_path.replace(
            hostname, storage_account + '/' + file_system)
        https_path = https_path.replace('abfss', 'https')
        return https_path

    @staticmethod
    def delete_directory_files(directory, file_extension='*'):

        # Join the directory and file_extension with glob pattern

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("delete_directory_files"):

            files = glob.glob(os.path.join(directory, f'*.{file_extension}'))
            msg = ""
            for file in files:
                try:
                    os.remove(file)
                    msg = msg + f"{file} has been deleted\n"
                    logger.info(msg)

                except OSError as e:
                    error_msg = f'Error: {file} : {e}'
                    exc_info = sys.exc_info()
                    logger_singleton.error_with_exception(error_msg, exc_info)
                    raise

            return msg

    @classmethod
    def convert_to_current_os_dir(cls, path: str) -> str:
        """Converts path to current os path

        Args:
            path (str): path to convert

        Returns:
            str: converted path
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("convert_to_current_os_dir"):
            logger.info(f"convert_to_current_os_dir: {path}")
            if platform.system() == 'Windows':
                converted_path = cls.convert_to_windows_dir(path)
            else:
                converted_path = cls.convert_to_unix_dir(path)

            logger.info(f"converted_path: {converted_path}")

            # Fix any double slashes
            converted_path = converted_path.replace('//', '/')

            return converted_path

    @staticmethod
    def convert_to_windows_dir(folder_path: str) -> str:
        """Converts to a Windows folder path from bash format

        Args:
            folder_path (str): path to convert

        Returns:
            str: _converted path
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("convert_to_windows_dir"):

            logger.info(f"convert_to_windows_dir: {folder_path}")
            window_dir = "\\"
            unix_dir = '/'

            folder_path = folder_path.replace(unix_dir, window_dir)
            # Replace double backslashes with a single backslash
            folder_path = folder_path.replace('\\\\', '\\')

            converted_path = folder_path.rstrip(window_dir) + window_dir
            logger.info(f"converted_path: {converted_path}")
            return converted_path

    @staticmethod
    def convert_to_unix_dir(folder_path: str) -> str:
        """Converts tp a unix folder path to windows format

        Args:
            folder_path (str): path to convert

        Returns:
            str: _converted path
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("convert_to_unix_dir"):
            logger.info(f"convert_to_unix_dir: {folder_path}")

            window_dir = "\\"
            unix_dir = '/'
            drive_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

            if window_dir in folder_path:
                # Check if a drive letter exists at the start of the string
                if folder_path[0].upper() in drive_letters and folder_path[1] == ":":
                    drive_letter = folder_path[0].lower()
                    # remove the drive letter and the colon
                    folder_path = folder_path[2:]
                    folder_path = '/' + drive_letter + folder_path  # prepend the drive letter
                folder_path = folder_path.replace(window_dir, unix_dir)
            converted_path = folder_path.rstrip(unix_dir) + unix_dir

            converted_path = converted_path.replace('//', '/')

            return converted_path

    @staticmethod
    def execute_script_file(script_path) -> str:
        """
        Executes a script file and returns its output or error message.

        The function first checks the operating system, then uses the corresponding command to run the script.
        If the script execution fails (i.e., if the return code is non-zero), a subprocess.CalledProcessError is raised.

        Args:
            script_path (str): The path to the script to execute.
            shell (bool, optional): If true, the specified command will be executed through the shell. Default is False.

        Raises:
            subprocess.CalledProcessError: If there is an error executing the script. The exception object will contain the return code, command, output, and error message.
            Exception: If there is an unknown error.

        Returns:
            tuple: A tuple containing two elements:
                - int: The status code - 200 for successful execution, 500 for an error.
                - str: The output of the script in case of success, or the error message in case of an error.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("execute_script_file"):

            try:

                result_string = ""

                # Determine the current operating system
                os_name = platform.system()
                if os_name == 'Windows':
                    # In Windows, use cmd to run the script
                    process = subprocess.Popen(
                        ['cmd', '/c', script_path], stderr=subprocess.PIPE)
                elif os_name in ['Linux', 'Darwin']:
                    # In Unix-based systems, use sh to run the script
                    os.chmod(script_path, 0o755)
                    process = subprocess.Popen(
                        ['sh', script_path], stderr=subprocess.PIPE)
                else:
                    raise ValueError("Unsupported platform: %s" % os_name)

                process.wait()  # Wait for the process to complete

                if process.returncode != 0:
                    # Read the error message from stderr
                    error_msg = process.stderr.read().decode('utf-8')
                    raise subprocess.CalledProcessError(
                        process.returncode, process.args, output=process.stdout, stderr=error_msg)
                    # process.stdout contains the output
                result_string = process.stdout
                return 200, result_string

            except Exception as err:
                error_msg = "Error %s", err
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                return 500, error_msg

    @staticmethod
    def execute_script_string(script_string, shell=False) -> str:
        """
        Executes a command represented as a string and returns its output or error message.

        The function runs the command using subprocess.Popen, capturing its output. If the command fails
        (i.e., if the return code is non-zero), a subprocess.CalledProcessError is raised.

        Args:
            script_string (str): The command to execute as a string.
            shell (bool, optional): If true, the specified command will be executed through the shell. Default is False.

        Raises:
            subprocess.CalledProcessError: If there is an error executing the command. The exception object will contain the return code and the command.
            Exception: If there is an unknown error.

        Returns:
            tuple: A tuple containing two elements:
                - int: The status code - 200 for successful execution, 500 for an error.
                - str: The output of the command in case of success, or the error message in case of an error.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("execute_script_string"):

            try:

                result_string = ""

                with Popen(script_string,
                           stdout=PIPE,
                           bufsize=1,
                           universal_newlines=True, shell=shell) as p_output:
                    if p_output is not None:
                        stdout = p_output.stdout
                        if stdout is not None:
                            for line in stdout:
                                # process line here
                                result_string = result_string + line
                    else:
                        result_string = "p_output is None"

                if p_output.returncode != 0:
                    raise CalledProcessError(
                        p_output.returncode, p_output.args)

                return 200, result_string

            except Exception as err:
                error_msg = "Error %s", err
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                return 500, error_msg

    @staticmethod
    def get_local_bin_folder():
        """
        Get the path to the .local/bin folder in the user's home directory.
        If the folder doesn't exist, it will be created.

        Returns:
            str: Path to the .local/bin folder
        """
        # Get the user's home directory
        home_dir = os.path.expanduser("~")

        # Create the .local/bin folder if it doesn't exist
        bin_folder = os.path.join(home_dir, ".local", "bin")
        os.makedirs(bin_folder, exist_ok=True)

        return bin_folder

    @staticmethod
    def set_file_metadata(file_path, key, value):

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("set_file_metadata"):

            try:
                if sys.platform.startswith('win'):
                    import win32api
                    import win32con

                    # Convert the key and value to a null-terminated string
                    key = key + '\x00'
                    value = value + '\x00'

                    # Set the metadata using the Windows API
                    win32api.SetFileAttributes(file_path, win32api.GetFileAttributes(
                        file_path) & ~win32con.FILE_ATTRIBUTE_ARCHIVE)
                    win32api.SetFileExtendedAttribute(file_path, key, value)
                    win32api.SetFileAttributes(file_path, win32api.GetFileAttributes(
                        file_path) | win32con.FILE_ATTRIBUTE_ARCHIVE)

                elif sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
                    import xattr

                    # Convert the key and value to strings
                    key_str = str(key)
                    value_str = str(value)

                    # Encode the key and value as bytes
                    key_bytes = key_str.encode('utf-8')
                    value_bytes = value_str.encode('utf-8')

                    # Set the metadata using the xattr library
                    xattr.setxattr(file_path, key_bytes, value_bytes)

                else:
                    raise ValueError(
                        "Unsupported operating system: {}".format(sys.platform))

            except OSError as os_error:
                logger.warning(
                    "Failed to set file metadata: %s", str(os_error))

            except Exception as ex:
                # Raise all other exceptions
                raise

    @staticmethod
    def download_file(url: str, timeout: int = 60, download_folder: str = "", local_file_name="") -> str:
        """
        Downloads a file from a URL.

        Args:
            url (str): The URL of the file to download.
            timeout (int, optional): The maximum number of seconds to wait for the request to complete. Default is 60 seconds.
            download_folder (str, optional): The folder where the downloaded file will be saved. If the folder doesn't exist, it will be created. Default is the user's .local/bin folder.
            local_file_name (str, optional): The name of the downloaded file. If not provided, the file name in the URL will be used.

        Returns:
            tuple: A tuple consisting of an integer and a string.
                The integer is the HTTP status code - 200 for a successful download, 500 for an error.
                The string is the local file path where the file was saved in case of success, or the error message in case of an error.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("download_file"):
            try:
                logger.info(f"download_file: {url}")
                if local_file_name is None or local_file_name == "":
                    local_file_name = url.split('/')[-1]

                # Get the user's home directory
                home_dir = os.path.expanduser("~")

                # Create the .local/bin folder if it doesn't exist
                bin_folder = os.path.join(home_dir, ".local", "bin")
                os.makedirs(bin_folder, exist_ok=True)

                # Check if download_folder exists and local_file_name doesn't contain a path
                if download_folder and os.path.basename(local_file_name) == local_file_name:
                    local_file_name = os.path.join(
                        download_folder, local_file_name)
                else:
                    local_file_name = os.path.join(bin_folder, local_file_name)

                # NOTE the stream=True parameter below
                with requests.get(url, stream=True, timeout=timeout) as request_result:
                    request_result.raise_for_status()
                    with open(local_file_name, 'wb') as file_result:
                        for chunk in request_result.iter_content(chunk_size=8192):
                            # If you have chunk encoded response uncomment if
                            # and set chunk_size parameter to None.
                            # if chunk:
                            file_result.write(chunk)
                return 200, local_file_name
            except requests.exceptions.HTTPError as errh:
                error_msg = "Http Error: %s", errh
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                return 500, error_msg
            except requests.exceptions.ConnectionError as errc:
                error_msg = "Http connectuion Error: %s", errc
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                return 500, error_msg
            except requests.exceptions.Timeout as errt:
                error_msg = "Http timeout Error: %s", errt
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                return 500, error_msg
            except Exception as err:
                error_msg = "Error: %s", err
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                return 500, error_msg

    @staticmethod
    def scrub_utf_8_text(original_str: str) -> str:
        """
        Scrubs the given text by encoding it as UTF-8 and decoding it back,
        removing any invalid UTF-8 characters in the process.

        Args:
            original_str (str): The original text to be scrubbed.

        Returns:
            str: The scrubbed text.

        """
        encoded_bytes = original_str.encode('utf-8', errors='ignore')
        decoded_string = encoded_bytes.decode('utf-8')
        return decoded_string

    @staticmethod
    def scrub_file_name(original_file_name: str) -> str:
        """Scrubs characters in object to rename

        Args:
            original_file_name (str): original column name

        Returns:
            str: new object name
        """

        if original_file_name is None:
            original_file_name = "object_name_is_missing"

        c_renamed = original_file_name
        c_renamed = c_renamed.replace("†", "_")
        c_renamed = c_renamed.replace(",", "_")
        c_renamed = c_renamed.replace("*", "_")
        c_renamed = c_renamed.replace(" ", "_")
        c_renamed = c_renamed.replace("\r", "_")
        c_renamed = c_renamed.replace("\n", "_")
        c_renamed = c_renamed.replace(";", "")
        c_renamed = c_renamed.replace(".", "")
        c_renamed = c_renamed.replace("}", "")
        c_renamed = c_renamed.replace("{", "")
        c_renamed = c_renamed.replace("(", "")
        c_renamed = c_renamed.replace(")", "")
        c_renamed = c_renamed.replace("?", "")
        c_renamed = c_renamed.replace("-", "")
        c_renamed = c_renamed.replace("/", "")
        c_renamed = c_renamed.replace("//", "")
        c_renamed = c_renamed.replace("=", "_")
        c_renamed = c_renamed.replace("&", "w")
        c_renamed = c_renamed.lower()
        c_renamed = c_renamed.strip()

        return c_renamed

    @classmethod
    def prepend_line_to_file(cls, source_path: str, destination_path: str,
                             line_to_prepend: str) -> str:
        """Add line to the beginning of a file

        Args:
            source_path (str): _description_
            destination_path (str): _description_
            line_to_prepend (str): _description_

        Returns:
            str: Status of operation
        """

        result = "running"
        print(f"source_path: {source_path}")
        print(f"destination_path: {destination_path}")
        with open(source_path,
                  'r',
                  encoding='utf-8') as original:
            data = original.read()
        with open(destination_path,
                  'w',
                  encoding='utf-8') as modified:
            modified.write(f"{line_to_prepend}\n" + data)
        result = "Success"
        return result

    @classmethod
    def combine_files(cls, source_path: str, file_mask: str,
                      destination_path: str) -> str:
        """Joins/combines multilple files

        Args:
            source_path (str): _description_
            file_mask (str): _description_
            destination_path (str): _description_

        Returns:
            str: Status of operation
        """
        result = "running"
        source_files = f"{source_path}{file_mask}"
        all_files = glob.glob(source_files)
        with open(destination_path,
                  'w+',
                  encoding='utf-8',
                  newline='\n') as f_output:
            for filename in all_files:
                print(f"filename:{filename}")
                with open(filename,
                          'r',
                          encoding="utf-8",
                          newline='\n') as f_input:
                    for line in f_input:
                        f_output.write(line)
        result = "Success"
        return result

    @classmethod
    def rename_directory(cls, config: dict, source_path, new_directory_name) -> str:
        """
        Renames a directory in Azure Blob File System Storage (ABFSS).

        Args:
            config (dict): The configuration dictionary containing the necessary Azure parameters.
            source_path (str): The original path of the directory to be renamed in ABFSS.
            new_directory_name (str): The new name for the directory.

        Returns:
            str: A message indicating the status of the rename operation.
        """

        try:
            client_id = config['client_id']
            client_secret = config['client_secret']

            result = "file_adls_copy failed"

            if client_secret is None:
                azure_client_secret_key = str(
                    config["azure_client_secret_key"])
                key = azure_client_secret_key
                client_secret = f"Environment variable: {key} not found"

            os.environ['AZCOPY_SPA_CLIENT_SECRET'] = client_secret
            tenant_id = config['tenant']

            running_local = config['running_local']
            print(f"running_local:{running_local}")
            print(f"source_path:{source_path}")
            print(f"new_directory_name:{new_directory_name}")

            credential = ClientSecretCredential(
                tenant_id, client_id, client_secret)
            storage_account_loc = urlparse(source_path).netloc
            storage_path = urlparse(source_path).path
            storage_path_list = storage_path.split("/")
            storage_container = storage_path_list[1]
            account_url = f"https://{storage_account_loc}"

            service_client = DataLakeServiceClient(account_url=account_url,
                                                   credential=credential)
            file_system_client = service_client.get_file_system_client(
                storage_container)

            dir_path = storage_path.replace(f"{storage_container}" + "/", "")

            is_directory = None
            directory_client: DataLakeDirectoryClient
            try:
                directory_client = file_system_client.get_directory_client(
                    dir_path)
                if directory_client.exists():
                    is_directory = True
                else:
                    is_directory = True

                if is_directory:
                    directory_client.rename_directory(new_directory_name)
                    result = "Success"
                else:
                    result = f"rename_directory failed: {dir_path} does not exist"
            except Exception as ex:
                directory_client = DataLakeDirectoryClient(
                    "empty", "empty", "empty")
                print(ex)
                result = "rename_directory failed"
        except Exception as ex_rename_directory:
            print(ex_rename_directory)
            result = "rename_directory failed"
        result = str(result)
        return result

    @classmethod
    def folder_adls_create(cls, config, dir_path: str, dbutils) -> str:
        """
        Creates a new directory in Azure Data Lake Storage (ADLS).

        Args:
            config (dict): The configuration dictionary containing the necessary Azure parameters.
            dir_path (str): The path of the directory to be created in ADLS.
            dbutils: An instance of Databricks dbutils, used for filesystem operations.

        Returns:
            str: A message indicating the status of the directory creation operation.
        """
        running_local = config['running_local']
        client_id = config['client_id']
        client_secret = config['client_secret']

        if client_secret is None:
            azure_client_secret_key = str(config["azure_client_secret_key"])
            client_secret = f"Environment variable: {azure_client_secret_key} not found"

        os.environ['AZCOPY_SPA_CLIENT_SECRET'] = client_secret
        tenant_id = config['tenant']

        storage_account_loc = urlparse(dir_path).netloc
        storage_path = urlparse(dir_path).path
        storage_path_list = storage_path.split("/")
        storage_container = storage_path_list[1]
        account_url = f"https://{storage_account_loc}"

        credential = ClientSecretCredential(
            tenant_id, client_id, client_secret)
        service_client = DataLakeServiceClient(
            account_url=account_url, credential=credential)
        file_system_client = service_client.get_file_system_client(
            storage_container)
        directory_client = file_system_client.create_directory(dir_path)

        return "True"

    @classmethod
    def file_adls_copy(cls, config, source_path: str, destination_path: str, from_to: str, dbutils) -> str:
        """
        Copies a file from the local filesystem to Azure Data Lake Storage (ADLS), or vice versa.

        Args:
            config (dict): The configuration dictionary containing the necessary Azure and local filesystem parameters.
            source_path (str): The path of the file to be copied.
            destination_path (str): The path where the file will be copied. If 'bytes' is passed, the function will return a byte array instead of performing a copy.
            from_to (str): Indicates the direction of the copy. 'BlobFSLocal' signifies ADLS to local copy, and 'LocalBlobFS' signifies local to ADLS copy.
            dbutils: An instance of Databricks dbutils, used for filesystem operations.

        Returns:
            str: A message indicating the status of the copy operation.
        """
        result = "file_adls_copy failed"
        running_local = config['running_local']
        client_id = config['client_id']
        client_secret = config['client_secret']

        if client_secret is None:
            azure_client_secret_key = str(config["azure_client_secret_key"])
            client_secret = f"Environment variable: {azure_client_secret_key} not found"

        os.environ['AZCOPY_SPA_CLIENT_SECRET'] = client_secret
        tenant_id = config['tenant']

        print(f"running_local:{running_local}")
        print(f"from_to:{from_to}")
        print(f"source_path:{source_path}")
        print(f"destination_path:{destination_path}")

        if (running_local is True and (from_to == 'BlobFSLocal' or from_to == 'LocalBlobFS')):

            p_1 = f"--application-id={client_id}"
            p_2 = f"--tenant-id={tenant_id}"
            arr_azcopy_command = ["azcopy", "login",
                                  "--service-principal", p_1, p_2]
            arr_azcopy_command_string = ' '.join(arr_azcopy_command)
            print(arr_azcopy_command_string)

            try:
                check_output(arr_azcopy_command)
                result_1 = f"login --service-principal {p_1} to {p_2} succeeded"
            except subprocess.CalledProcessError as ex_called_process:
                result_1 = str(ex_called_process.output)

            print(result_1)

            if from_to == 'BlobFSLocal':
                arr_azcopy_command = [
                    'azcopy', 'copy', f"{source_path}", f"{destination_path}",
                    f'--from-to={from_to}', '--recursive',
                    '--trusted-microsoft-suffixes=', '--log-level=INFO']
            elif from_to == 'LocalBlobFS':
                arr_azcopy_command = [
                    'azcopy', 'copy', f"{source_path}", f"{destination_path}",
                    '--log-level=DEBUG', f'--from-to={from_to}']
            else:
                arr_azcopy_command = [f"from to:{from_to} is not supported"]

            arr_azcopy_command_string = ' '.join(arr_azcopy_command)
            print(arr_azcopy_command_string)

            try:
                check_output(arr_azcopy_command)
                result_2 = f"copy from {source_path} to {destination_path} succeeded"
            except subprocess.CalledProcessError as ex_called_process:
                result_2 = str(ex_called_process.output)

            result = result_1 + result_2
        elif ((running_local is False) and from_to == 'BlobFSLocal'):
            credential = ClientSecretCredential(
                tenant_id, client_id, client_secret)
            storage_account_loc = urlparse(source_path).netloc
            storage_path = urlparse(source_path).path
            storage_path_list = storage_path.split("/")
            storage_container = storage_path_list[1]
            account_url = f"https://{storage_account_loc}"
            service_client = DataLakeServiceClient(
                account_url=account_url, credential=credential)
            file_system_client = service_client.get_file_system_client(
                storage_container)
            dir_path = storage_path.replace(f"{storage_container}" + "/", "")
            is_directory = None
            directory_client: DataLakeDirectoryClient
            try:
                directory_client = file_system_client.get_directory_client(
                    dir_path)
                if directory_client.exists():
                    is_directory = True
                else:
                    is_directory = True
            except Exception as ex:
                directory_client = DataLakeDirectoryClient(
                    "empty", "empty", "empty")
                print(ex)

            obj_repo = pade_repo.RepoCore()

            if is_directory is True:

                azure_files = []

                try:
                    azure_files = file_system_client.get_paths(path=dir_path)
                except Exception as ex:
                    print(ex)

                for file_path in azure_files:
                    print(str(f"file_path:{file_path}"))
                    file_path_name = file_path.name
                    file_name = os.path.basename(file_path_name)
                    file_client = directory_client.get_file_client(file_path)
                    file_data = file_client.download_file()
                    file_bytes = file_data.readall()
                    file_string = file_bytes.decode("utf-8")
                    first_200_chars_of_string = file_string[0:200]
                    destination_file_path = destination_path + "/" + file_path_name

                    if len(file_string) > 0:
                        try:
                            # os.remove(destination_file_path)
                            dbutils.fs.rm(destination_file_path)
                        except OSError as ex_os_error:
                            # if failed, report it back to the user
                            print(
                                f"Error: {ex_os_error.filename} - {ex_os_error.strerror}.")
                        try:
                            print(
                                f"dbutils.fs.put({destination_file_path}, {first_200_chars_of_string}, True)")
                            result = dbutils.fs.put(
                                destination_file_path, file_string, True)
                        except Exception as ex_os_error:
                            # if failed, report it back to the user
                            print(f"Error: {ex_os_error}.")

                        content_type = "bytes"
                        result = obj_repo.import_file(
                            config, file_bytes, content_type, destination_file_path)

                    else:
                        result = f"destination_file_path:{destination_file_path} is empty"
                    # file_to_copy = io.BytesIO(file_bytes)
                    # print(f"destination_file_path:{destination_file_path}")
            else:
                file_path = storage_path.replace(
                    f"{storage_container}" + "/", "")
                print(f"file_path:{file_path}")
                file_client = file_system_client.get_file_client(file_path)
                file_data = file_client.download_file()
                file_bytes = file_data.readall()
                file_string = file_bytes.decode("utf-8")
                file_name = os.path.basename(file_path)
                destination_file_path = destination_path + "/" + file_name
                first_200_chars_of_string = file_string[0:500]
                if len(file_string) > 0:

                    try:
                        # os.remove(destination_file_path)
                        dbutils.fs.rm(destination_file_path)
                    except OSError as ex_os_error:
                        # if failed, report it back to the user
                        print(
                            f"Error: {ex_os_error.filename}-{ex_os_error.strerror}.")

                    try:
                        print(
                            f"dbutils.fs.put({destination_file_path}, {first_200_chars_of_string}, True)")
                        result = dbutils.fs.put(
                            destination_file_path, file_string, True)
                    except Exception as ex_os_error:
                        # if failed, report it back to the user
                        print(f"Error: {ex_os_error}.")

                    content_type = "bytes"
                    result = obj_repo.import_file(
                        config, file_bytes, content_type, destination_file_path)
                else:
                    result = f"destination_file_path:{destination_file_path} is empty"
        elif ((running_local is False) and from_to == 'LocalBlobFS'):
            url = destination_path
            storage_account_loc = urlparse(url).netloc
            storage_path = urlparse(url).path
            storage_path_list = storage_path.split("/")
            storage_container = storage_path_list[1]
            file_name = os.path.basename(destination_path)
            dir_path = storage_path.replace(file_name, "")
            dir_path = dir_path.replace(storage_container + '/', "")
            account_url = f"https://{storage_account_loc}"
            print(f"account_url:{account_url}")
            print(f"url:{url}")
            print(f"storage_path:{storage_path}")
            print(f"storage_container:{storage_container}")
            print(f"dir_path:{dir_path}")
            print(f"file_name:{file_name}")

            credential = ClientSecretCredential(
                tenant_id, client_id, client_secret)
            service_client = DataLakeServiceClient(
                account_url=account_url, credential=credential)
            file_system_client = service_client.get_file_system_client(
                storage_container)
            directory_client = file_system_client.get_directory_client(
                dir_path)
            file_client = directory_client.create_file(file_name)
            local_file = open(source_path, "r", encoding="utf-8")
            file_contents = local_file.read()
            file_client.append_data(
                data=file_contents, offset=0, length=len(file_contents))
            result = file_client.flush_data(len(file_contents))

            # with open(source_path) as f_json:
            #     json_data = json.load(f_json)
            # result = file_client.upload_data(json_data, overwrite=True, max_concurrency=5)

            # file_client = file_system_client.get_file_client(file_path)
            # file_data = file_client.download_file(0)
            # result = file_data.readall()

            # print(f" dbutils.fs.cp({source_path}, {destination_path})")
            # result = dbutils.fs.cp(source_path, destination_path)
        else:
            result = "invalid config: must download/client config files from azure to local"
            result = result + " - functionality not available on databricks"
            print(result)

        result = str(result)

        return result

    @classmethod
    def get_file_size(cls, running_local: bool, path: str, dbutils, spark: SparkSession) -> int:
        """Takes in file path, dbutils object and spark obejct, returns file size of provided path

        Args:
            path (str): path to check file size
            dbutils (object): Databricks dbutils object
            spark (SparkSession): spark session object

        Returns:
            int:  file size
        """

        if dbutils is not None:

            file_exists = cls.file_exists(running_local, path, dbutils)

            if file_exists is True:
                ddl_schema_3 = StructType(
                    [
                        StructField("path", StringType()),
                        StructField("name", StringType()),
                        StructField("size", IntegerType())
                    ]
                )

                ddl_schema_4 = StructType(
                    [
                        StructField("path", StringType()),
                        StructField("name", StringType()),
                        StructField("size", IntegerType()),
                        StructField("modification_time", LongType()),
                    ]
                )

                print(f"command: dbutils.fs.ls({path})")
                sk_list = dbutils.fs.ls(path)
                print(f"num_elements:{len(sk_list)}")

                df_file_list = None

                if len(sk_list) > 0:
                    if len(sk_list[0]) == 3:
                        df_file_list = spark.createDataFrame(
                            sk_list, ddl_schema_3)
                    elif len(sk_list[0]) == 4:
                        df_file_list = spark.createDataFrame(
                            sk_list, ddl_schema_4)

                    if df_file_list is None:
                        file_size = 0
                    else:
                        first = df_file_list.first()
                        if first is not None:
                            file_size = first.size
                        else:
                            file_size = -1

                    # df_file_list = df_file_list.toPandas()
                    # file_size = df_file_list.iloc[0, df_file_list.columns.get_loc("size")]

                    file_size = int(str(file_size))
                else:
                    file_size = -1
            else:
                file_size = -1
        else:
            file_size = -1

        return file_size

    @staticmethod
    def file_exists(running_local: bool, path: str, dbutils) -> bool:
        """
        Checks whether a file exists at the provided path. 

        Args:
            running_local (bool): A flag indicating if the function is running locally or on Databricks.
            path (str): The path to the file that should be checked.
            dbutils (object): An instance of Databricks dbutils. Used for filesystem operations when not running locally.

        Returns:
            bool: Returns True if the file exists, and False otherwise.
        """

        if running_local is True:
            b_exists = os.path.exists(path)
        else:
            try:
                path = path.replace("/dbfs", "")
                if dbutils is not None:
                    dbutils.fs.ls(path)
                    b_exists = True
                else:
                    b_exists = False
            except Exception as exception_result:
                if "java.io.FileNotFoundException" in str(exception_result):
                    b_exists = False
                else:
                    b_exists = False
                    raise

        return b_exists

    @classmethod
    def copy_url_to_blob(cls, config: dict, src_url: str,
                         dest_path: str, file_name: str) -> str:
        """
        Downloads a file from the source URL and uploads it to the specified path in Azure Storage.

        Args:
            config (dict): The configuration dictionary containing the necessary Azure Storage parameters.
            src_url (str): The source URL from which to download the file.
            dest_path (str): The destination path in Azure Storage where the file will be uploaded.
            file_name (str): The name to be given to the file when it is uploaded to Azure Storage.

        Returns:
            str: A message indicating the status of the upload. 
        """

        info_message = f"copy_url_to_blob: src_url:{src_url}, dest_path:{dest_path}, file_name:{file_name}"
        print(info_message)

        client_id = config['client_id']
        client_secret = config['client_secret']
        tenant_id = config['tenant']
        if client_secret is None:
            azure_client_secret_key = str(config["azure_client_secret_key"])
            client_secret = f"Environment variable: {azure_client_secret_key}not found"
            print(client_secret)
        credential = ClientSecretCredential(tenant_id, client_id,
                                            client_secret)
        storage_account_loc = urlparse(dest_path).netloc
        storage_path = urlparse(dest_path).path
        storage_path_list = storage_path.split("/")
        storage_container = storage_path_list[1]
        account_url = f"https://{storage_account_loc}"
        service_client = DataLakeServiceClient(
            account_url=account_url, credential=credential)
        os.environ['AZCOPY_SPA_CLIENT_SECRET'] = client_secret
        dir_path = storage_path.replace(f"{storage_container}" + "/", "")
        print(f"dir_path:{dir_path}")
        file_system_client = service_client.get_file_system_client(
            storage_container)
        directory_client = file_system_client.get_directory_client(dir_path)
        file_response = requests.get(src_url)
        file_data = file_response.content
        try:
            file_client = directory_client.create_file(file_name)
            result = file_client.upload_data(
                file_data, overwrite=True, max_concurrency=5)
        except Exception as ex:
            print(ex)
            result = "upload failed"
        return result

    @staticmethod
    def get_latest_file(path, file_type=None):
        """
        Gets the most recently modified file in a given directory.

        Args:
            path (str): The path to the directory to search.

        Returns:
            str: The full path of the most recently modified file. If the directory is empty or does not exist, 
            returns an empty string.
        """
        files = glob.glob(os.path.join(path, "*"))
        if "." not in file_type:
            file_type = "." + file_type

        if file_type:
            files = [file for file in files if file.endswith(f"{file_type}")]
        if not files:  # If no files found, return None
            return None
        latest_file = max(files, key=os.path.getctime)
        return latest_file

    @staticmethod
    def create_tar_gz_for_folder(folder_name, output_file_name_no_extension):
        """
        Archives the specified folder into a tar.gz file. 

        Args:
            folder_name (str): The name of the folder to archive. This should be the full path to the folder.
            output_file_name_no_extension (str): The desired name of the output file without the extension. 

        Returns:
            str: The full path to the created archive file.
        """
        try:
            subprocess.run(
                ["tar", "-zcf", f"{output_file_name_no_extension}.tar.gz", "-C", folder_name, "."], check=True)
            return f"Tar file: {output_file_name_no_extension} created successfully."
        except subprocess.CalledProcessError as ex:
            return f"An error occurred while creating tar file: {str(ex)}"

    @staticmethod
    def is_valid_json(file_path):
        """
        Check if a file contains valid JSON.

        This function attempts to load the contents of a file as JSON. 
        If the loading process fails due to a `json.JSONDecodeError`, 
        it's assumed that the file does not contain valid JSON and the function returns False. 
        If the loading process succeeds, the function returns True.

        Args:
            file_path (str): The path to the file to be checked.

        Returns:
            bool: True if the file contains valid JSON, False otherwise.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True
        except json.JSONDecodeError:
            return False
