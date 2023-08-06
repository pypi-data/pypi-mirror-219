
import json
import jsonschema
from jsonschema import validate
import sys
import os

from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)

from data_ecosystem_services.alation_service.manifest import (
    Manifest
)
# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class Column:
    """Represents a column in a database table.

    Args:
        name (str): The name of the column.
        data_type (str): The data type of the column.
        nullable (bool, optional): Indicates if the column is nullable. Defaults to True.
        primary_key (bool, optional): Indicates if the column is a primary key. Defaults to False.
        default (Any, optional): The default value of the column. Defaults to None.

    Attributes:
        name (str): The name of the column.
        data_type (str): The data type of the column.
        nullable (bool): Indicates if the column is nullable.
        primary_key (bool): Indicates if the column is a primary key.
        default (Any): The default value of the column.

    """

    def __init__(self, column_json, schema_file_path):
        """
        Initialize a Column instance.

        Args:
            column_json (dict): The JSON object containing column details. The JSON object should contain
                - 'name': The name of the column.
                - 'title': The title of the column.
                - 'tags' (optional): A list of tags associated with the column.

        The function also calls get_column_extra_description_fields() and format_description() methods to further process
        the column data. Tags are an optional field and if not present in the column_json, an empty list is assigned.
        """

        self.schema_file_path = schema_file_path
        self.name = column_json['name']
        self.title = column_json['title']
        self.extra_description_fields = self.get_column_extra_description_fields(
            column_json)
        self.description = self.format_description(column_json)
        tags = column_json.get('tags')
        if tags is not None:
            self.tags = tags
        else:
            self.tags = []

    def format_description(self, column_json):
        """_summary_

        Args:
            column_json (_type_): _description_

        Returns:
            _type_: _description_
        """
        description = column_json['description']
        if self.extra_description_fields:
            description += '<br><table><tr><th>Field</th><th>Value</th></tr>'
            for key in self.extra_description_fields:
                description += '<tr><td>' + key + '</td><td>' + \
                    self.extra_description_fields[key] + '</td></tr>'
            description += '</table>'
        return description

    def get_column_extra_description_fields(self, column_json):
        """
        Extracts the extra description fields from the provided column JSON data.

        This function checks if the 'extraDescriptionFields' key exists in the 'column_json'. If present, 
        the key-value pairs from 'extraDescriptionFields' are extracted and returned as a new dictionary. 
        If 'extraDescriptionFields' does not exist, an empty dictionary is returned.

        Args:
            column_json (dict): The JSON data for a column, potentially containing 'extraDescriptionFields'
                                as a key with another dictionary as its value.

        Returns:
            dict: A dictionary containing the extra description fields from 'column_json'.
                Returns an empty dictionary if 'extraDescriptionFields' is not present in 'column_json'.
        """
        extra_description_fields = {}
        if "extraDescriptionFields" in column_json:
            optional_description_fields = column_json['extraDescriptionFields']
            print("Extra description fields: ", optional_description_fields)
            for key in optional_description_fields:
                extra_description_fields[key] = optional_description_fields[key]
        return extra_description_fields


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
