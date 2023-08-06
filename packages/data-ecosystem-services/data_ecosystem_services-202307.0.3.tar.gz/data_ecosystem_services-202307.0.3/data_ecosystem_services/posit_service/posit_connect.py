import os
from azure.storage.queue import QueueServiceClient
from azure.identity import ClientSecretCredential
import requests
from typing import List
import json

from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)

from data_ecosystem_services.cdc_tech_environment_service import (
    environment_file as pade_env_file
)

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class PositConnect:

    @staticmethod
    def verify_api_key(api_key, posit_connect_base_url):
        """
        Verifies the validity of an API key by making a request to a specified URL.

        Args:
            api_key (str): The API key to be verified.
            posit_connect_base_url (str): The URL of the API endpoint to which the request will be sent.

        Examples:
            url: 'https://dev.rconnect.edav.cdc.gov:8080"'  # replace with the actual API endpoint

        Returns:
            tuple: A tuple containing the status code and response_content from the server.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        pade_env_tracing.TracerSingleton.log_to_console = False
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("verify_api_key"):

            headers = {"Authorization": f"Key {api_key}"}

            api_url = f"{posit_connect_base_url}/__api__/v1/server_settings/r"
            response = requests.get(api_url, headers=headers)

            # If the request was successful, status_code will be 200
            status_code = response.status_code

            # If the request was successful, status_code will be 200
            logger.info(f"response.status_code: {response.status_code}")

            # Try to get the content of the response in JSON format, if not possible return it as text
            try:
                response_content = response.json()
            except ValueError:
                response_content = response.text
                status_code = 500

            logger.info(f"response_content: {response_content}")

            return status_code, response_content, api_url

    @staticmethod
    def get_python_information(api_key, posit_connect_base_url):
        """
        Gets POSIT Python configuration information by making a request to a specified URL.

        Args:
            api_key (str): The API key to be verified.

        Examples:
            url: 'https://dev.rconnect.edav.cdc.gov:8080"'  # replace with the actual API endpoint

        Returns:
            tuple: A tuple containing the status code and response_content from the server.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        pade_env_tracing.TracerSingleton.log_to_console = False
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("verify_api_key"):

            headers = {"Authorization": f"Key {api_key}"}

            api_url = f"{posit_connect_base_url}/__api__/v1/server_settings/python"
            response = requests.get(api_url, headers=headers)

            # If the request was successful, status_code will be 200
            status_code = response.status_code

            # If the request was successful, status_code will be 200
            logger.info(f"response.status_code: {response.status_code}")

            # Try to get the content of the response in JSON format, if not possible return it as text
            try:
                response_content = response.json()
            except ValueError:
                response_content = response.text
                status_code = 500

            logger.info(f"response_content: {response_content}")

            return status_code, response_content, api_url

    @staticmethod
    def publish_manifest(api_key, posit_connect_base_url, app_manifest_file):
        """
        Publishes an application on a given platform by sending its manifest file. 

        Args:
            api_key (str): The API key provided by the platform for authentication.
            posit_connect_base_url (str): The base URL of the platform where the application will be published.
            app_manifest_file (str): The path to the application's manifest file. This file contains metadata about the application such as its name, version, and the resources it needs.

        Returns:
            dict: A dictionary containing the response from the platform. This typically includes the status of the publication and any errors encountered during the process.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        pade_env_tracing.TracerSingleton.log_to_console = False
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("publish_app"):

            if posit_connect_base_url.endswith('/'):
                posit_connect_base_url = posit_connect_base_url[:-1]

            api_url = f"{posit_connect_base_url}/__api__/v1/content"
            headers = {"Authorization": f"Key {api_key}"}
            data = open(app_manifest_file, "rb", encoding="utf-8").read()
            response = requests.post(api_url, headers=headers, data=data)

            # If the request was successful, status_code will be 200
            status_code = response.status_code

            # If the request was successful, status_code will be 200
            logger.info(f"response.status_code: {response.status_code}")

            if response.status_code == 201:
                logger.info("App published successfully.")
            else:
                logger.info(response.content)

            # Try to get the content of the response in JSON format, if not possible return it as text
            try:
                response_content = response.json()
            except ValueError:
                response_content = response.text
                status_code = 500

            logger.info(f"response_content: {response_content}")

            return status_code, response_content, api_url

    @staticmethod
    def generate_manifest(swagger_file, requirements_file):
        """
        Generate the manifest.json file based on the current swagger and requirements.txt.

        Args:
            swagger_file (str): The path to the Swagger specification file. This file describes the structure of the API that the application will provide.
            requirements_file (str): The path to the requirements.txt file. This file lists the Python packages that the application requires to run.

        Returns:
            str: The path to the generated manifest.json file. This file includes a summary of the application's structure and dependencies.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        pade_env_tracing.TracerSingleton.log_to_console = False
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("generate_manifest"):

            # Load the Swagger JSON file
            with open(swagger_file, "rb", encoding="utf-8") as f:
                swagger = json.load(f)

            # Load the requirements file
            with open(requirements_file, "r", encoding="utf-8") as f:
                requirements = [r.strip() for r in f.readlines()]

            # Extract version information from the Swagger data
            swagger_version = swagger['info']['version']

            # Extract basePath from the Swagger data
            swagger_basePath = swagger.get('basePath', '')

            endpoints = []
            for path, methods in swagger['paths'].items():
                for method, info in methods.items():
                    # Check if the method is a HTTP verb
                    if method in ['get', 'post', 'put', 'delete', 'patch']:
                        endpoints.append({
                            "path": swagger_basePath + path,  # Include basePath in the path
                            "method": method.upper(),  # Convert to uppercase
                            # Use 'summary' for description
                            "description": info.get('summary', '')
                        })

            manifest = {
                "name": swagger['info']['title'],
                "description": swagger['info']['description'],
                "entrypoint": "app:app",
                "dependencies": requirements,
                "environment": {
                    "PORT": "5000"
                },
                "endpoints": endpoints
            }

            return json.dumps(manifest)

    @staticmethod
    def list_content(api_key, posit_connect_base_url):
        """
        List all content items visible to the requesting user.

        Args:
            api_key (str): The API key provided by the platform for authentication.
            posit_connect_base_url (str): The base URL of the platform where the application will be published.

        Returns:
            dict: A dictionary containing the response from the platform. This typically includes the status of the publication and any errors encountered during the process.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        pade_env_tracing.TracerSingleton.log_to_console = False
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("list_content"):

            if posit_connect_base_url.endswith('/'):
                posit_connect_base_url = posit_connect_base_url[:-1]

            api_url = f"{posit_connect_base_url}/__api__/v1/content"
            headers = {"Authorization": f"Key {api_key}"}

            response = requests.get(api_url, headers=headers)

            # If the request was successful, status_code will be 200
            status_code = response.status_code

            # If the request was successful, status_code will be 200
            logger.info(f"response.status_code: {response.status_code}")

            if response.status_code == 201:
                logger.info("App published successfully.")
            else:
                logger.info(response.content)

            # Try to get the content of the response in JSON format, if not possible return it as text
            try:
                response_content = response.json()
            except ValueError:
                response_content = response.text
                status_code = 500

            logger.info(f"response_content: {response_content}")

            return status_code, response_content, api_url

    @staticmethod
    def list_deployment_bundles(api_key, posit_connect_base_url, content_id):
        """
        List all bundles items visible to the requesting user.

        Args:
            api_key (str): The API key provided by the platform for authentication.
            posit_connect_base_url (str): The base URL of the platform where the application will be published.

        Returns:
            dict: A dictionary containing the response from the platform. This typically includes the status of the publication and any errors encountered during the process.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        pade_env_tracing.TracerSingleton.log_to_console = False
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("list_deployment_bundles"):

            if posit_connect_base_url.endswith('/'):
                posit_connect_base_url = posit_connect_base_url[:-1]

            api_url = f"{posit_connect_base_url}/__api__/v1/content/{content_id}/bundles"
            headers = {"Authorization": f"Key {api_key}"}

            response = requests.get(api_url, headers=headers)

            # If the request was successful, status_code will be 200
            status_code = response.status_code

            # If the request was successful, status_code will be 200
            logger.info(f"response.status_code: {response.status_code}")

            if response.status_code == 201:
                logger.info("App published successfully.")
            else:
                logger.info(response.content)

            # Try to get the content of the response in JSON format, if not possible return it as text
            try:
                response_content = response.json()
            except ValueError:
                response_content = response.text
                status_code = 500

            logger.info(f"response_content: {response_content}")

            return status_code, response_content, api_url

    @staticmethod
    def get_task_details(api_key, posit_connect_base_url, task_id):
        """
        Get task details

        Args:
            api_key (str): The API key provided by the platform for authentication.
            posit_connect_base_url (str): The base URL of the platform where the application will be published.
            task_id(str):

        Returns:
            dict: A dictionary containing the response from the platform. This typically includes the status of the publication and any errors encountered during the process.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        pade_env_tracing.TracerSingleton.log_to_console = False
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_task_details"):

            if posit_connect_base_url.endswith('/'):
                posit_connect_base_url = posit_connect_base_url[:-1]

            api_url = f"{posit_connect_base_url}/__api__/v1/tasks/{task_id}"
            headers = {"Authorization": f"Key {api_key}"}

            response = requests.get(api_url, headers=headers)

            # If the request was successful, status_code will be 200
            status_code = response.status_code

            # If the request was successful, status_code will be 200
            logger.info(f"response.status_code: {response.status_code}")

            if response.status_code == 201:
                logger.info("App published successfully.")
            else:
                logger.info(response.content)

            # Try to get the content of the response in JSON format, if not possible return it as text
            try:
                response_content = response.json()
            except ValueError:
                response_content = response.text
                status_code = 500

            logger.info(f"response_content: {response_content}")

            return status_code, response_content, api_url

    @staticmethod
    def upload_deployment_bundle(api_key, posit_connect_base_url, app_path):
        """
        Uploads a deployment bundle to the platform.

        Args:
            api_key (str): The API key provided by the platform for authentication.
            posit_connect_base_url (str): The base URL of the platform where the application will be published.
            app_path (str): The path of the application that will be uploaded to the platform.

        Returns:
            dict: A dictionary containing the response from the platform. This typically includes the status of the upload and any errors encountered during the process.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        pade_env_tracing.TracerSingleton.log_to_console = False
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()
        env_file = pade_env_file.EnvironmentFile()

        with tracer.start_as_current_span("generate_manifest"):

            if posit_connect_base_url.endswith('/'):
                posit_connect_base_url = posit_connect_base_url[:-1]

            api_url = f"{posit_connect_base_url}/__api__/v1/content"
            headers = {"Authorization": f"Key {api_key}"}

            response = requests.get(api_url, headers=headers)

            # If the request was successful, status_code will be 200
            status_code = response.status_code

            # If the request was successful, status_code will be 200
            logger.info(f"response.status_code: {response.status_code}")

            if response.status_code == 201:
                logger.info("App published successfully.")
            else:
                logger.info(response.content)

            # Try to get the content of the response in JSON format, if not possible return it as text
            try:
                response_content = response.json()
            except ValueError:
                response_content = response.text
                status_code = 500

            logger.info(f"response_content: {response_content}")

            return status_code, response_content, api_url

    @staticmethod
    def build_deployment_bundle(api_key, posit_connect_base_url, content_id, bundle_id):
        """
        Builds a deployment bundle to the platform.

        Args:
            api_key (str): The API key provided by the platform for authentication.
            posit_connect_base_url (str): The base URL of the platform where the application will be published.
            bundle_id (str): 

        Returns:
            dict: A dictionary containing the response from the platform. This typically includes the status of the upload and any errors encountered during the process.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        pade_env_tracing.TracerSingleton.log_to_console = False
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()
        env_file = pade_env_file.EnvironmentFile()

        with tracer.start_as_current_span("build_deployment_bundle"):

            if posit_connect_base_url.endswith('/'):
                posit_connect_base_url = posit_connect_base_url[:-1]

            data = {'bundle_id': f'{bundle_id}'}

            api_url = f"{posit_connect_base_url}/__api__/v1/content/{content_id}/deploy"
            headers = {"Authorization": f"Key {api_key}"}

            response = requests.post(api_url, headers=headers, json=data)

            # If the request was successful, status_code will be 200
            status_code = response.status_code

            # If the request was successful, status_code will be 200
            logger.info(f"response.status_code: {response.status_code}")

            if response.status_code == 201:
                logger.info("App published successfully.")
            else:
                logger.info(response.content)

            # Try to get the content of the response in JSON format, if not possible return it as text
            try:
                response_content = response.json()
            except ValueError:
                response_content = response.text
                status_code = 500

            logger.info(f"response_content: {response_content}")

            return status_code, response_content, api_url
