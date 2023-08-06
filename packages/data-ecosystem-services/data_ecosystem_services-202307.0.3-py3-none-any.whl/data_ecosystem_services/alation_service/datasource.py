import os
import sys
import json
import requests

from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)

from data_ecosystem_services.cdc_tech_environment_service import (
    environment_http as pade_env_http
)

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)
# Default request timout
REQUEST_TIMEOUT = 45


class DataSource:
    """
    A base class for interacting with Alation DataSource. 
    """

    @staticmethod
    def get_datasource(edc_alation_api_token, edc_alation_base_url, datasource_id):

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_datasource"):

            try:

                # Must use v1 of the API - v2 returns a 404
                api_url = f"{edc_alation_base_url}/integration/v1/datasource/{str(datasource_id)}/"

                # Set the headers for the API request
                headers = {"accept": "application/json",
                           "Token": edc_alation_api_token}
                # Intentionally not set
                response_datasource_text = "not_set"

                # Log Parameters
                logger.info(f"api_url: {api_url}")

                # Make the API request
                obj_http = pade_env_http.EnvironmentHttp()
                response_datasource = obj_http.get(
                    api_url, headers=headers, timeout=REQUEST_TIMEOUT, params=None)

                # Raise an exception if the response status code is not 200 or 201
                response_datasource.raise_for_status()

                # Check the response status code to determine if successful
                if response_datasource.status_code in (200, 201):
                    response_datasource_text = response_datasource.text
                    response_datasource_json = response_datasource.json()
                    datasource_title = response_datasource_json.get(
                        "title")
                    logger.info(f"datasource: {str(datasource_title)}")
                    return response_datasource
                else:
                    response_datasource_text = response_datasource.reason
                    raise ValueError(
                        "Failed to get Datasource :" + str(response_datasource_text))

            except requests.HTTPError as err:
                error_msg = f"HTTP Error occurred: {err}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
            except requests.ConnectionError as err:
                error_msg = f"Connection Error occurred: {err}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
            except requests.Timeout as err:
                error_msg = f"Timeout Error occurred: {err}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
            except requests.RequestException as err:
                error_msg = f"An error occurred: {err}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def check_datasource(cls, edc_alation_api_token, edc_alation_base_url, alation_datasource_id, alation_datasource_name):
        """
        Checks the given data source against the Alation API.

        Args:
            akatibn_datasource_name (str): The name of the data source to be checked.
            alation_datasource_id (int): The ID of the data source in Alation.
            alation_headers (dict): The headers to be used for Alation API requests. These should include authentication information.
            edc_alation_base_url (str): The base URL of the Alation instance.

        Returns:
            str: A status message indicating whether the data source was found or not. This could potentially be extended to return more detailed information.

        Raises:
            Exception: If there is an error in the API request, such as invalid authentication, an exception will be raised.

        Note:
            This function is designed to interact with the Alation API. Please ensure that all necessary access permissions and API credentials are correctly set up before using this function.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("check_datasource"):
            try:

                # Must use v1 of the API - v2 returns a 404
                api_url = f"{edc_alation_base_url}/integration/v1/datasource/{str(alation_datasource_id)}/"

                headers = {"accept": "application/json"}
                headers["Token"] = edc_alation_api_token

                # Set the headers for the API request
                headers = {"accept": "application/json"}
                # Intentionally not set
                # headers["Token"] = edc_alation_api_token

                alation_datasource_name = str(alation_datasource_name)
                alation_datasource_name = alation_datasource_name.lower()
                # service_account_authentication for this datasource
                logger.info("Checking data source %s", alation_datasource_name)
                logger.info("API URL: %s", api_url)
                response_datasource = cls.get_datasource(
                    edc_alation_api_token, edc_alation_base_url, alation_datasource_id)
                logger.info(f"Response: {str(response_datasource)}")
                print(f"Type of response: {type(response_datasource)}")
                response_datasource_json = response_datasource.json()
                ds_title = response_datasource_json.get("title", "")
                ds_title = ds_title.lower()
                message = f"Found correct data source {ds_title}"
                logger.info(message)

                if alation_datasource_name not in ds_title:
                    message = f"Data source {alation_datasource_name} not found in {ds_title} from {api_url}"
                    raise ValueError(message)

                return response_datasource
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def update_datasource(edc_alation_api_token, edc_alation_base_url, alation_datasource_id, datasource_title, datasource_description):

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("update_datasource"):

            try:

                # Must use v1 of the API - v2 returns a 404
                api_url = f"{edc_alation_base_url}/integration/v1/datasource/{str(alation_datasource_id)}/"

                # Set the headers for the API request
                headers = {"accept": "application/json",
                           "content-type": "application/json",
                           "Token": edc_alation_api_token}
                # Intentionally not set
                response_datasource_text = "not_set"

                payload = {"title": datasource_title,
                           "description": datasource_description}

                # Log Parameters
                logger.info(f"api_url: {api_url}")

                # Make the API request

                response_datasource = requests.put(
                    api_url, headers=headers, timeout=REQUEST_TIMEOUT, json=payload)

                # Raise an exception if the response status code is not 200 or 201
                response_datasource.raise_for_status()

                # Check the response status code to determine if successful
                if response_datasource.status_code in (200, 201):
                    response_datasource_text = response_datasource.text
                    response_datasource_json = response_datasource.json()
                    datasource_title = response_datasource_json.get(
                        "title")
                    logger.info(f"datasource: {str(datasource_title)}")
                    return response_datasource
                else:
                    response_datasource_text = response_datasource.reason
                    raise ValueError(
                        "Failed to get Datasource :" + str(response_datasource_text))

            except requests.HTTPError as err:
                error_msg = f"HTTP Error occurred: {err}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
            except requests.ConnectionError as err:
                error_msg = f"Connection Error occurred: {err}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
            except requests.Timeout as err:
                error_msg = f"Timeout Error occurred: {err}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
            except requests.RequestException as err:
                error_msg = f"An error occurred: {err}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def get_datasource_schemas(alation_headers, edc_alation_base_url, alation_datasource_id):
        """
        Retrieves the schemas for a given data source from the Alation API.

        Args:
            alation_headers (dict): The headers to be used for Alation API requests. These should include authentication information.
            edc_alation_base_url (str): The base URL of the Alation instance.
            alation_datasource_id (int): The ID of the data source in Alation for which the schemas are to be fetched.

        Returns:
            list: A list of schemas associated with the provided data source. Each schema is represented as a dictionary.

        Raises:
            Exception: If there is an error in the API request, such as invalid authentication, an exception will be raised.

        Note:
            This function is designed to interact with the Alation API. Please ensure that all necessary access permissions and API credentials are correctly set up before using this function.
            This function uses a limit of 100 and a skip of 0 for pagination with the Alation API.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_datasource_schemas"):
            try:
                ds_id = alation_datasource_id
                # Create a connection to Alation
                print(f"alation_headers:{alation_headers}")
                print(f"alation_datasource_id: {alation_datasource_id}")
                print(f"edc_alation_base_url: {edc_alation_base_url}")
                # Pl. Update DS Server ID with the DS Server Id you have created
                # Pl. Update limit and Skip
                limit = 100
                skip = 0
                params = {}
                params['ds_id'] = ds_id
                params['limit'] = limit
                params['skip'] = skip
                params_json = json.dumps(params)
                api_url = f"{edc_alation_base_url}/integration/v2/schema/"
                print(f"api_url:{api_url}")
                # Get the schemas for the datasource
                response = requests.get(
                    api_url, headers=alation_headers, params=params)
                schemas = json.loads(response.text)

                # Close the connection to Alation
                response.close()

                return schemas
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
