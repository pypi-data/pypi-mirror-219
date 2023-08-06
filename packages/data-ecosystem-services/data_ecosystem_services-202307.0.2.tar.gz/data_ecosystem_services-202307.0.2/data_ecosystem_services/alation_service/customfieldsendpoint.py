
from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)

from data_ecosystem_services.cdc_tech_environment_service import (
    environment_http as pade_env_http
)

import requests
import json
from .column import Column
from .table import Table
import os
import sys
import re

# Default request time out
REQUEST_TIMEOUT = 180
# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)
# Default limit item number of items to retrieve
LIMIT = 500


class EdcAlationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class CustomFieldsEndpoint():
    """
    A class for interacting with the bulk metadata upload from the Alation API.
    """

    def __init__(self):
        """
        Create an endpoint object.

        Parameters
        ----------
        token: string
            The Alation API Access token to interact with the API. See
            https://developer.alation.com/dev/docs/authentication-into-alation-apis#create-api-access-token
            for details.
        base_url: string
            The root URL for the Alation server to use. It should not have a slash "/" at the end of the URL.
            Example: https://edc.cdc.gov
        """
        self.updates = []

    def format_fields(self, obj):
        """Format the fields of an object as name-value pairs.

        Args:
            obj: The object whose fields will be formatted.

        Returns:
            str: A formatted string containing the name, type, and value of each field.

        This function takes an object 'obj' and retrieves its fields using the 'vars' function.
        It then iterates over each field, extracting the field name, type, and value. The
        extracted information is formatted into a string of the form:
        "name (type): value", and all field strings are collected in a list.

        Finally, the function joins the field strings using newline characters and returns
        the resulting formatted string.

        If a TypeError occurs during the field retrieval process, the function returns
        a string indicating the type and value of the object itself.

        Note: This function assumes that the object 'obj' has public fields accessible
        using the 'vars' function and that the fields can be reliably converted to strings.
        """

        try:
            fields = vars(obj)
            field_strings = []

            for name, value in fields.items():
                field_type = type(value).__name__
                field_value = str(value)
                field_string = f"{name} ({field_type}): {field_value}"
                field_strings.append(field_string)

            return "\n".join(field_strings)

        except TypeError:
            return f"Variable of type {type(obj).__name__} with value: {obj}"

    def has_special_chars(self, string):
        """Check if a string contains any special characters.

        Args:
            string (str): The string to be checked.

        Returns:
            bool: True if the string contains at least one special character,
                False otherwise.

        The function uses a regular expression pattern to match any character that
        isn't alphanumeric, a dot, or an underscore. It then searches for a match
        of the pattern in the string using re.search. If a match is found, it
        indicates the presence of a special character, and the function returns
        True. Otherwise, it returns False.
        """
        pattern = r'[^a-zA-Z0-9._]'
        # re.search returns a match object if the pattern is found in the string, and None otherwise
        match = re.search(pattern, string)
        return match is not None

    def get_alation_data(self, fields):
        """
        Returns a dictionary with 'title' and 'description' fields of the provided object.

        Args:
            fields (Column, Table): An instance of either Column or Table class.

        Returns:
            dict: A dictionary with 'title' and 'description' of the provided fields object. 
            If 'title' or 'description' is None, it is not included in the dictionary. 
            If both are None, an empty dictionary is returned.
        """
        if isinstance(fields, (Column, Table)):
            return {k: v for k, v in {
                'title': fields.title,
                'description': fields.description
            }.items() if v is not None}
        elif isinstance(fields, dict):
            return fields
        else:
            msg = self.format_fields(fields)
            error_msg = f"fields {msg} should be an instance of Column or Table"
            raise EdcAlationError(error_msg)

    def parse_key(self, key):
        """
        Parse a key in the format 'ds_id.schema_name.table_name.column'
        and create a parameters dictionary for the non-null values.

        Args:
            key (str): The key to be parsed.

        Returns:
            dict: A dictionary containing the non-null values as key-value pairs.
                Possible keys: 'ds_id', 'schema_name', 'table_name', 'column'.
        """

        # Split the key into components using the dot (.) separator
        components = key.split('.')

        # Extract ds_id, schema_name, table_name, and column
        ds_id = components[0]
        schema_name = components[1] if len(components) >= 2 else None
        table_name = components[2] if len(components) >= 3 else None
        column = components[3] if len(components) >= 4 else None

        # Create a parameters dictionary for non-null values
        parameters = {}
        if ds_id:
            parameters['ds_id'] = ds_id
        if schema_name:
            parameters['schema_name'] = schema_name
        if table_name:
            parameters['table_name'] = table_name
        if column:
            parameters['name'] = column
        parameters['limit'] = LIMIT

        return parameters

    def get_object_by_key(self, edc_alation_api_token, edc_alation_base_url, object_type, alation_datasource_id, key):
        """
        Retrieves data from a specified API endpoint.

        Args:
            edc_alation_api_token (str): The API token for authentication.
            edc_alation_base_url (str): The base URL of the API.
            object_type (str): The type of object to retrieve.
            alation_datasource_id (int): The ID of the data source.
            key (str): The key used for retrieval.

        Returns:
            dict: A dictionary containing the retrieved data.

        Raises:
            EdcAlationError: If there is an error during the retrieval process.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_objet_by_key"):
            try:

                # Check if the alation_datasource_id is an integer
                if not isinstance(alation_datasource_id, int):
                    raise EdcAlationError(
                        "alation_datasource_id must be an integer.")

                # Remove the data source ID from the key if it exists to avoid duplicate data source ID
                key = key.replace(str(alation_datasource_id) + ".", "")

                # Add the data source ID to the key
                full_key = f"{alation_datasource_id}.{key}"

                # Check if the key contains special characters
                if self.has_special_chars(full_key):
                    logger.warning(
                        f"The following submitted key contains special characters: {str(full_key)}")

                # Create headers
                headers = {'Token': edc_alation_api_token,
                           'Content-Type': 'application/json',
                           'Accept': 'application/json',
                           'cache-control': "no-cache"
                           }

                params = self.parse_key(full_key)
                obj_http = pade_env_http.EnvironmentHttp()
                metadata_endpoint = '/integration/v2'
                api_url = f"{edc_alation_base_url}{metadata_endpoint}/{object_type}"
                response_custom = obj_http.get(
                    api_url, headers=headers, timeout=REQUEST_TIMEOUT, params=params)

                response_custom.raise_for_status()

                custom_result = response_custom.json()
                number_received = custom_result.get('number_received')
                logger.info(f"number_received: {number_received}")
                updated_objects = custom_result.get('updated_objects')
                new_objects = custom_result.get('new_objects')
                error_objects = custom_result.get('error_objects')
                if error_objects and len(error_objects) > 0:
                    error_message = ', '.join(str(e)
                                              for e in error_objects)
                    raise EdcAlationError(
                        f"Errors occurred: {error_message}: api_url {api_url} : params {params}")
                error = custom_result.get('error')
                if len(error) > 0:
                    raise EdcAlationError(
                        f"Errors occurred: {error}: api_url {api_url}  : params {params}")

                if updated_objects == 0 and new_objects == 0:
                    error_message = "No objects updated or created"
                    raise EdcAlationError(
                        f"Errors occurred: {error_message}: api_url {api_url} : params {params}")

                return custom_result

            except Exception as ex:
                error_msg = f"Error: {str(ex)} : {str(key)}: {str(object_type)}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    def get_custom_by_key(self, edc_alation_api_token, edc_alation_base_url, object_type, alation_datasource_id, key):
        """
        Retrieves data from a specified API endpoint.

        Args:
            edc_alation_api_token (str): The API token for authentication.
            edc_alation_base_url (str): The base URL of the API.
            object_type (str): The type of object to retrieve.
            alation_datasource_id (int): The ID of the data source.
            key (str): The key used for retrieval.

        Returns:
            dict: A dictionary containing the retrieved data.

        Raises:
            EdcAlationError: If there is an error during the retrieval process.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_custom_by_key"):
            try:

                # Check if the alation_datasource_id is an integer
                if not isinstance(alation_datasource_id, int):
                    raise EdcAlationError(
                        "alation_datasource_id must be an integer.")

                # Remove the data source ID from the key if it exists to avoid duplicate data source ID
                key = key.replace(str(alation_datasource_id) + ".", "")

                # Add the data source ID to the key
                full_key = f"{alation_datasource_id}.{key}"

                # Check if the key contains special characters
                if self.has_special_chars(full_key):
                    logger.warning(
                        f"The following submitted key contains special characters: {str(full_key)}")

                # Create headers
                headers = {'Token': edc_alation_api_token,
                           'Content-Type': 'application/json',
                           'Accept': 'application/json',
                           'cache-control': "no-cache"
                           }

                data = {"key": full_key}
                metadata_endpoint = '/api/v1/bulk_metadata/custom_fields/default'
                api_url = f"{edc_alation_base_url}{metadata_endpoint}/{object_type}"
                response_custom = requests.post(
                    api_url, headers=headers, timeout=REQUEST_TIMEOUT, json=data)

                response_custom.raise_for_status()
                custom_result = response_custom.json()
                number_received = custom_result.get('number_received')
                logger.info(f"number_received:{number_received}")
                updated_objects = custom_result.get('updated_objects')
                new_objects = custom_result.get('new_objects')
                error_objects = custom_result.get('error_objects')
                if error_objects and len(error_objects) > 0:
                    error_message = ', '.join(str(e)
                                              for e in error_objects)
                    raise EdcAlationError(
                        f"Errors occurred: {error_message}: api_url {api_url}")
                error = custom_result.get('error')
                if len(error) > 0:
                    raise EdcAlationError(
                        f"Errors occurred: {error}: api_url {api_url} ")

                return response_custom

            except Exception as ex:
                error_msg = f"Error: {str(ex)} : {str(key)}: {str(object_type)}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    def get_data(self, u):
        """Get data from an object or its 'get_alation_data' method.

        Args:
            u: The object from which to retrieve the data.

        Returns:
            str: JSON representation of the data.

        This function retrieves data from the provided object 'u' by either calling its
        'get_alation_data' method (if available) or directly using the object itself.
        The retrieved data is then returned as a JSON string.

        If an exception occurs during the retrieval process, an error message is logged
        using the logger instance and the exception is re-raised.

        Note: This function relies on the 'logger_singleton' and 'tracer_singleton'
        instances from the 'pade_env_logging' and 'pade_env_tracing' modules respectively.
        These instances are assumed to be properly initialized and available within the
        class where this method is defined.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_data"):
            try:

                # If the object has a get_alation_data method, use it to get the data
                if hasattr(u, 'get_alation_data'):
                    data = u.get_alation_data()
                # Otherwise, just use the object itself
                else:
                    data = u
                return json.dumps(data)
            except Exception as ex:
                error_msg = "Error: %s : %s", ex, str(u)
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise EdcAlationError(error_msg)

    def update(self, edc_alation_api_token, edc_alation_base_url, object_type, alation_datasource_id, key, fields, force_submit):
        """
        Update business metadata on an object in Alation.

        Parameters
        ----------
        edc_alation_api_token : str
            The API token for authenticating requests to the Alation API.

        edc_alation_base_url : str
            The base URL of the Alation instance.

        object_type : str
            The Alation object type which can be one of the following:
                - source
                - schema
                - table
                - attribute (aka database column)
                - attribute_value (Column values custom metadata, generally not used)

        alation_datasource_id : int
            The ID of the data source that this object belongs to.

        key : str
            The object key in Alation. See the Alation API documentation for details. The key format depends on the object type.

        fields : dict
            The fields to update. It should be a dictionary containing key-value pairs representing the field names and their corresponding values.

        force_submit : bool
            Specifies whether to force the submission of updates even if the batch size is not reached.

        Raises
        ------
        EdcAlationError
            If an error occurs during the update process.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("update"):
            array_of_json = None
            try:
                batch_size = 50

                processed_fields = {}
                fields = self.get_alation_data(fields)

                # Check if the alation_datasource_id is an integer
                if not isinstance(alation_datasource_id, int):
                    raise EdcAlationError(
                        "alation_datasource_id must be an integer.")

                # If the fields is a dictionary, then it is already processed
                if isinstance(fields, dict):
                    processed_fields = {k: v for k, v in fields.items()}
                else:
                    raise EdcAlationError(
                        f"Errors occurred and cannot process object because it is missing get_alation_data: {str(fields)}")

                # Remove the data source ID from the key if it exists to avoid duplicate data source ID
                key = key.replace(str(alation_datasource_id) + ".", "")

                # Add the data source ID to the key
                full_key = f"{alation_datasource_id}.{key}"

                # Check if the key contains special characters
                if self.has_special_chars(full_key):
                    logger.warning(
                        f"The following submitted key contains special characters: {str(full_key)}")

                # Remove the key from the fields if it exists to avoid duplicate key
                if 'key' in processed_fields:
                    processed_fields.pop('key')

                # Add the key to the fields
                single_update = {"key": full_key, **processed_fields}
                self.updates.append(single_update)

                # Submit the updates if the batch size is reached or if force_submit is True
                if len(self.updates) >= batch_size or force_submit:
                    # Create the request body with array if needed
                    array_of_json = [json.dumps(u) for u in self.updates]
                    if len(array_of_json) > 1:
                        request_body = "[" + ", ".join(array_of_json) + "]"
                        # request_body = ", ".join(array_of_json)
                    else:
                        request_body = array_of_json[0]

                    # Validate json
                    try:
                        # Parse the request_body to check for JSON parsing errors
                        data = json.loads(request_body)
                        logger.info(
                            f"Successfully parsed request_body: {len(data)}")
                    except json.JSONDecodeError as ex:
                        error_msg = f"Error parsing request_body: {ex} : {request_body}"
                        logger.error(error_msg)
                        raise EdcAlationError(error_msg)

                    # submit the batch
                    logger.info(
                        f"Submitting {object_type} batch")
                    metadata_endpoint = '/api/v1/bulk_metadata/custom_fields/default'
                    api_url = f"{edc_alation_base_url}{metadata_endpoint}/{object_type}?create_new=false"

                    # Create headers
                    headers = {'Token': edc_alation_api_token,
                               'Content-Type': 'application/json',
                               'Accept': 'application/json'}

                    # Submit the updates using the constructed URL and request_body
                    response = requests.post(
                        api_url, headers=headers, json=data, verify=True, timeout=REQUEST_TIMEOUT)
                    response_json = response.json()

                    # Clear updates after submission
                    self.updates = []
                    logger.info(
                        f"Response Status {object_type} batch of {request_body}")
                    response.raise_for_status()
                    result = response_json
                    number_received = result.get('number_received')
                    logger.info(f"number_received: {number_received}")
                    updated_objects = result.get('updated_objects')
                    new_objects = result.get('new_objects')
                    error_objects = result.get('error_objects')
                    if error_objects and len(error_objects) > 0:
                        error_message = ', '.join(str(e)
                                                  for e in error_objects)
                        raise EdcAlationError(
                            f"Errors occurred: {error_message}: api_url {api_url} : request_body {request_body}")
                    error = result.get('error')
                    if len(error) > 0:
                        raise EdcAlationError(
                            f"Errors occurred: {error}: api_url {api_url} : request_body {request_body}")

                    if updated_objects == 0 and new_objects == 0:
                        error_message = "No objects updated or created"
                        raise EdcAlationError(
                            f"Errors occurred: {error_message}: api_url {api_url} : request_body {request_body}")

                    return {"status": "success", "message": "Batch complete"}, response_json
                else:
                    return {"status": "success", "message": "Batch not submitted"}, {"number_of_updates", len(self.updates), "batch_size", batch_size, "force_submit", force_submit}

            except Exception as ex:
                error_msg = f"Error: {str(ex)} : {str(key)}: {str(fields)}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
