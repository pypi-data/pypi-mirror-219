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


class Manifest:
    def __init__(self, schema_file_path):
        """
        Initializes a Manifest object with the provided schema_file_path.

        Args:
            schema_file_path (str): The path to the schema JSON file.

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
                self.title = ''
                self.alationDatasourceID = ''
                self.alationSchemaID = ''
                self.submitting_user = ''
                self.description = ''
                # self.releasedate = ''
                self.homepageUrl = ''
                self.identifier = ''
                self.dataformat = ''
                self.language = ''
                self.size = ''
                self.updateFrequency = ''
                self.temporalResolution = ''
                self.license = ''
                self.tags = []
                self.geographicCoverage = ''
                self.referencedBy = ''
                self.references = ''
                self.citation = ''
                self.reference = ''
                self.temporalApplicability = {}
                self.tables = {}
                self.pii = {}
                self.manifest_template_properties = {}
                self.extra_description_fields = {}

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    def set_alation_data(self, manifest_json):
        """
        Set Alation data using the provided manifest and schema_file_path.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("set_alation_data"):

            try:
                logger.info("Start Field by field:")
                schema_file = open(self.schema_file_path, encoding='utf-8')
                schemaContents = json.load(schema_file)
                self.manifest_template_properties = schemaContents['properties'].keys(
                )
                self.manifest_template_table_properties = schemaContents['$defs']['table']['properties'].keys(
                )
                self.manifest_template_column_properties = schemaContents['$defs']['column']['properties'].keys(
                )
                # extraDescriptionFields is an optional field
                self.extra_description_fields = {}
                if "extraDescriptionFields" in manifest_json:
                    optional_description_fields = manifest_json['extraDescriptionFields']
                    print("Extra description fields: ",
                          optional_description_fields)
                    for key in optional_description_fields:
                        self.extra_description_fields[key] = optional_description_fields[key]
                self.title = manifest_json['title']
                self.alationDatasourceID = manifest_json['alationDatasourceID']
                self.alationSchemaID = manifest_json['alationSchemaID']
                self.submitting_user = manifest_json['submitting_user']
                self.description = manifest_json['description']
                self.releasedate = manifest_json['releaseDate']
                self.homepageUrl = manifest_json['homepageUrl']
                self.identifier = manifest_json['identifier']
                # self.dataformat  = manifest['format']
                # self.language    = manifest['language']
                # self.size        = manifest['size']
                # self.temporalResolution = manifest['temporalResolution']
                # self.updateFrequency    = manifest['updateFrequency']
                # self.conformToStandard  = manifest['conformToStandard']
                self.license = manifest_json['license']
                self.tags = manifest_json['tags']
                self.referencedBy = manifest_json['referencedBy']
                self.citation = manifest_json['citation']
                self.reference = manifest_json['reference']
                self.geographicCoverage = manifest_json['geographicCoverage']
                # self.tables = list(map(lambda t: Table(t), manifest['tables']))
                from data_ecosystem_services.alation_service.table import Table
                self.tables = {table.name: table for table in map(
                    lambda t: Table(t, self.schema_file_path), manifest_json['tables'])}
                self.pii = manifest_json['pii']
                self.temporalApplicability = manifest_json['temporalApplicability']

                return 200, "Success"
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    def get_tables_data(self):
        """
        Retrieves the tables data from the current instance.

        Returns:
            dict: A dictionary containing the tables data.

        Example:
            >>> instance = MyClass()
            >>> tables_data = instance.get_tables_data()
            >>> print(tables_data)
            {'table1': [...], 'table2': [...], ...}
        """

        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_tables_data"):

            return self.tables

    def get_columns_data(self):
        """
        Retrieves the columns data for each table in the current instance.

        Returns:
            dict: A dictionary mapping table names to their respective column data.

        Example:
            >>> instance = MyClass()
            >>> columns_data = instance.get_columns_data()
            >>> print(columns_data)
            {'table1': ['column1', 'column2', ...], 'table2': ['column3', 'column4', ...], ...}
        """

        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_columns_data"):

            columndata = {}
            for t in self.tables:
                columndata[t] = t.columns
            return columndata

    def format_description(self):
        description = self.description
        if self.extra_description_fields:
            description += '<br><table><tr><th>Field</th><th>Value</th></tr>'
            for key in self.extra_description_fields:
                description += '<tr><td>' + key + '</td><td>' + \
                    self.extra_description_fields[key] + '</td></tr>'
            description += '</table>'
        return description

    def get_alation_data(self):
        """
        Retrieves Alation data from the Manifest object.

        Returns:
            dict: A dictionary containing Alation data extracted from the Manifest.

        Raises:
            Exception: If an error occurs while retrieving the Alation data.

        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_alation_data"):
            try:
                data = {}
                data['title'] = self.title
                data['description'] = self.format_description()
                # data['description']     = self.description
                # data['Release Date']    = self.releasedate
                data['Homepage URL'] = self.homepageUrl
                data['Identifier'] = self.identifier
                # data['Format']          = self.dataformat
                data['License'] = self.license

                # arrays
                # data['tags']            = self.tags
                # data['Language']        = self.language
                data['Is Referenced By'] = self.referencedBy
                data['Geographic Coverage'] = self.geographicCoverage
                data['Temporal Applicability'] = self.temporalApplicability
                data['References'] = self.references
                # self.alationdata = json.dumps(data)
                return data
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    def validate_json(self, jsonData, schema):
        """
        Validates JSON data against a given schema.

        Args:
            jsonData (dict): The JSON data to be validated.
            schema (dict): The JSON schema to validate against.

        Returns:
            bool: True if the JSON data is valid according to the schema.

        Raises:
            jsonschema.exceptions.ValidationError: If the JSON data fails validation against the schema.
            Exception: If an error occurs during validation.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("validate_json"):

            try:
                validate(instance=jsonData, schema=schema)
            except jsonschema.exceptions.ValidationError as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
            return True

    @staticmethod
    def print_manifest(manifest_object):
        for k, v, in manifest_object.items():
            print("{0}: {1}".format(k, v))

    def get_submitting_user_from_manifest_file(self, manifest_file):
        """
        Retrieves the submitting user from a manifest JSON file.

        Args:
            manifest_file (str): The path to the manifest JSON file.

        Returns:
            str: The submitting user extracted from the manifest.

        Raises:
            Exception: If an error occurs while retrieving the submitting user.

        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_submitting_user_from_manifest_file"):

            try:
                schema_file_path = open(self.schema_file_path)
                schema = json.load(schema_file_path)
                f = open(manifest_file, encoding='utf-8')
                manifest = json.load(f)
                return manifest['submitting_user']
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    def validate_manifest(self, manifest_file):
        """
        Validates a manifest JSON file against a schema.

        Args:
            manifest_file (str): The path to the manifest JSON file.

        Returns:
            tuple: A tuple containing an HTTP status code (200 if successful) and the manifest dictionary.

        Raises:
            ValueError: If the manifest schema is invalid.
            FileNotFoundError: If the specified schema file does not exist.
            JSONDecodeError: If the schema file or manifest file is not a valid JSON.

        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("validate_manifest"):

            try:
                schema_file_path = open(
                    self.schema_file_path, 'r', encoding='utf-8')
                schema_file_path = json.load(
                    schema_file_path)
                f = open(manifest_file, 'r', encoding='utf-8')
                manifest_json = json.load(f)

                self.validate_json(manifest_json, schema_file_path)
                logger.info("Manifest schema is valid")
                error_code, message = self.set_alation_data(manifest_json)
                return error_code, manifest_json
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    def get_manifest_expected_fields(self):
        """
        Reads the manifest JSON file and extracts expected fields for schema, table, and column objects.

        Returns:
            tuple: A tuple containing dictionaries of expected fields for schema, table, and column objects.

        Raises:
            FileNotFoundError: If the specified schema file does not exist.
            JSONDecodeError: If the schema file is not a valid JSON.

        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_manifest_expected_fields"):

            try:

                schema_file_path = open(
                    self.schema_file_path, encoding="utf-8")
                schema = json.load(schema_file_path)
                schema_fields = {}
                table_fields = {}
                column_fields = {}
                for p in schema['properties']:
                    # do not add properties blank_field_examples for tables, columns, this info will be extracted from alation obj strucutre
                    if p not in ["tables", "columns"]:
                        schema_fields[p] = schema['properties'][p].get(
                            'blank_field_examples')
                for p in schema['$defs']['table']['properties']:
                    # do not add properties blank_field_examples for tables, columns, this info will be extracted from alation obj strucutre
                    if p not in ["columns"]:
                        table_fields[p] = schema['$defs']['table']['properties'][p]['blank_field_examples']
                for p in schema['$defs']['column']['properties']:
                    column_fields[p] = schema['$defs']['column']['properties'][p]['blank_field_examples']
                return schema_fields, table_fields, column_fields

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise
