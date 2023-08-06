import requests
from .endpoint import Endpoint
import sys
import os

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
REQUEST_TIMEOUT = 45
LIMIT = 1000   # Limit the number of records returned by the API

# This isn't a true endpoint as it actually points to multiple URLS


class IdFinderEndpoint(Endpoint):
    """
    A class for interacting with the Alation V2 API to find the IDs of objects by type and name.

    This is a subclass of Endpoint, so users should instantiate the class by providing an API token
    and the base URL of the Alation server to work with.

    Note that this functionality may require a user with admin priviledges.
    """

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

    def find(self, object_type, key):
        """
        Finds the identifier for an object in Alation given a name and object type.

        Parameters
        ----------
        object_type : str
            The Alation object type: "schema", "table" or "attribute". Note that columns are called attributes in Alation.
        name : str
            The name of the object in Alation.

        Returns
        -------
        int or None
            If the call finds a single object, it will return the ID for the object. If it can't find anything or if it finds more than one object, it will return None.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("find"):

            api_url = ""
            try:
                # Create headers
                headers = {'Token': self.token,
                           'Accept': 'application/json'}
                params = self.parse_key(key)
                metadata_endpoint = '/integration/v2'
                base_url = self.base_url
                api_url = f"{base_url}{metadata_endpoint}/{object_type}"
                obj_http = pade_env_http.EnvironmentHttp()
                response = obj_http.get(
                    api_url, headers=headers, timeout=REQUEST_TIMEOUT, params=params)
                response.raise_for_status()
                response_json = response.json()
                if len(response_json) == 1:
                    return response_json[0]['id']
                else:
                    raise ValueError(
                        f"Found  {len(response_json)} ids for:" + str(key))

            except Exception as ex:
                error_msg = f"Error: {str(ex)} : token_length {str(len( self.token))}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                # raise
                return {"status": "error", "message": error_msg}
