from .manifest import Manifest
from .column import Column

import json
import jsonschema
from jsonschema import validate
import sys
import os

from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class Table:
    """
    Represents a table object.

    """

    def __init__(self, table_json, schema_file_path):
        """
        Initializes a Table object using the provided table JSON.

        Args:
            table_json (dict): The JSON data representing the table.

        Raises:
            Exception: If an error occurs during initialization.

        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("__init__"):

            try:

                self.schema_file_path = schema_file_path
                manifest = Manifest(schema_file_path)

                # get the expected fields from the manifest
                schema_fields, expected_table_fields, expected_column_fields = manifest.get_manifest_expected_fields()

                msg = "Schema fields length: " + str(len(schema_fields))
                logger.info(msg)
                msg = "Expected table fields length: " + \
                    str(len(expected_column_fields))
                logger.info(msg)

                # add specified tables fields to the table object and update if necessary
                for key in expected_table_fields:
                    if key in table_json:
                        setattr(self, key, table_json[key])

                missing_keys = [
                    key for key in expected_table_fields if not hasattr(self, key)]

                if missing_keys:
                    logger.error(f"Missing keys: {missing_keys}")

                # get the extra description fields from the table JSON
                self.extra_description_fields = self.get_table_extra_description_fields(
                    table_json)

                self.name = table_json['name']
                self.title = table_json['title']
                self.description = self.format_description(table_json)

                tags = table_json.get('tags')
                if tags is not None:
                    self.tags = tags
                else:
                    self.tags = []
                columns_json = table_json.get('columns')

                if columns_json is not None:
                    # self.columns = list(
                    #     map(lambda c: Column(c, schema_file_path), columns_json))
                    self.columns = {column.name: column for column in map(
                        lambda c: Column(c, self.schema_file_path), columns_json)}

                else:
                    self.columns = None
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    def get_alation_data(self):
        """
        Retrieves the title and description from the instance.

        This function checks the 'title' and 'description' attributes of the instance and returns a dictionary that includes 
        'title' and 'description' keys, each with their respective values, only if the values are not None. 
        It includes keys whose values are empty strings.

        Returns:
            dict: A dictionary with 'title' and 'description' keys. The dictionary will not include keys whose values are None.
            If both 'title' and 'description' are None, an empty dictionary is returned.
        """
        return {k: v for k, v in {
            'title': self.title,
            'description': self.description
        }.items() if v is not None}

    def get_table_extra_description_fields(self, table_json):
        """
            Retrieves extra description fields from the table JSON.

            Args:
                table_json (dict): The JSON data representing the table.

            Returns:
                dict: A dictionary containing the extra description fields.

            Raises:
                Exception: If an error occurs while retrieving the extra description fields.

        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_table_extra_description_fields"):

            try:

                extra_description_fields = {}
                if "extraDescriptionFields" in table_json:
                    optional_description_fields = table_json['extraDescriptionFields']
                    msg = "Extra description fields: %s", optional_description_fields
                    logger.info(msg)
                    for key in optional_description_fields:
                        extra_description_fields[key] = optional_description_fields[key]
                return extra_description_fields
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    def format_description(self, table_json):
        """
        Formats the description for the table.

        Args:
            table_json (dict): The JSON data representing the table.

        Returns:
            str: The formatted description string.

        Raises:
            Exception: If an error occurs while formatting the description.

        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("format_description"):

            try:

                description = table_json['description']
                if self.extra_description_fields:
                    description += '<br><table><tr><th>Field</th><th>Value</th></tr>'
                    for key in self.extra_description_fields:
                        description += '<tr><td>' + key + '</td><td>' + \
                            self.extra_description_fields[key] + '</td></tr>'
                    description += '</table>'
                return description
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
