import os
import sys
import pandas as pd
import numpy as np
import xlsxwriter
from openpyxl.utils import get_column_letter

from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)

from .tokenendpoint import TokenEndpoint
from .customfieldsendpoint import CustomFieldsEndpoint
from .tagsendpoint import TagsEndpoint
from .idfinderendpoint import IdFinderEndpoint
from .datasource import DataSource
from .manifest import Manifest

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)
TIMEOUT_ONE_MIN = 60  # or set to whatever value you want


class ExcelMetadata:

    @staticmethod
    def convert_dict_to_csv(dictionary):

        return 'UNSUPPORTED LIST'

        if isinstance(dictionary, dict):
            csv_rows = []
            for key, value in dictionary.items():
                csv_row = f"{key}:{value}"
                csv_rows.append(csv_row)
            csv_data = ','.join(csv_rows)
            return csv_data
        else:
            return None

    @classmethod
    def generate_excel_file_data(cls, alation_schema_id, config):
        """
        Generate Excel file data for the given Alation schema ID and configuration.

        Args:
            alation_schema_id (int): The ID of the Alation schema.
            config (dict): A dictionary containing the configuration settings.

        Returns:
            tuple: A tuple containing the following elements:
                - df_schema (pandas.DataFrame): The DataFrame containing the schema data.
                - df_table_list (pandas.DataFrame): The DataFrame containing the table data.
                - manifest_excel_file (str): The file name of the generated Excel file.

        Raises:
            Exception: If there is an error during the generation process.

        This method generates Excel file data for the specified Alation schema ID and configuration settings.
        It retrieves the necessary data from Alation using the provided credentials and builds DataFrames
        to represent the schema and table data.

        The method returns a tuple containing the following elements:
        - df_schema: The DataFrame containing the schema data with columns 'type', 'field_name', and 'value'.
        - df_table_list: The DataFrame containing the table data with columns based on the dictionary keys.
        - manifest_excel_file: The file name of the generated Excel file.

        Note:
        - This method assumes the existence of an `alation_schema` module with a `Schema` class.
        - The method relies on external logging and tracing modules (`logger_singleton` and `tracer_singleton`) that are not provided here.
        - The configuration dictionary (`config`) is expected to contain specific keys such as 'repository_path', 'environment', 'edc_alation_user_id', 'edc_alation_base_url', etc.
        - The method makes use of the `pd.DataFrame` function from the `pandas` library to create DataFrames.
        """

        from data_ecosystem_services.alation_service import (
            schema as alation_schema
        )
        schema = alation_schema.Schema()

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        schema_id = alation_schema_id
        schema_name = None

        with tracer.start_as_current_span("generate_excel_file_data"):
            try:

                # Get Parameters
                repository_path = config.get("repository_path")
                environment = config.get("environment")
                alation_user_id = config.get("edc_alation_user_id")
                edc_alation_base_url = config.get("edc_alation_base_url")
                token_endpoint = TokenEndpoint(
                    edc_alation_base_url)
                status_code, edc_alation_api_token, api_refresh_token = token_endpoint.get_api_token_from_config(
                    config)

                print(
                    f"edc_alation_api_token_length: {str(len(edc_alation_api_token))}")
                print(
                    f"api_refresh_token_length: {str(len(api_refresh_token))}")
                assert status_code == 200

                # Get Datasource and Schema Results
                schema_result, datasource_result = schema.get_schema(
                    edc_alation_api_token, edc_alation_base_url, schema_id)

                alation_data_source_id = schema_result.get("ds_id")

            except Exception as ex:
                error_msg = "Error: {str(ex)}",
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

            # Pandas Dataframe
            try:
                # Get Table Results
                table_result = schema.get_schema_tables(
                    edc_alation_api_token, edc_alation_base_url, alation_data_source_id, alation_schema_id)

                # log results
                logger.info(f"schema_result length: {len(schema_result)}")
                logger.info(
                    f"datasource_result length: {len(datasource_result)}")

                schema_name = schema_result.get("name")
                datasource_title = datasource_result.get("title")

                # Create dictionaries
                simple_dict = {i: (k, v) for i, (k, v) in enumerate(
                    schema_result.items()) if not isinstance(v, list) and not isinstance(v, dict)}
                custom_dict = schema_result['custom_fields']

                # Get Excel File Name
                manifest_excel_file = schema.get_manifest_excel_file_name(
                    "download", repository_path, datasource_title, schema_name, environment, alation_user_id)

                # Convert simple_dict to DataFrame
                df_schema_standard = pd.DataFrame.from_dict(simple_dict, orient='index', columns=[
                    'field_name', 'value'])

                df_schema_standard = df_schema_standard.assign(type='standard')

                df_schema_custom = pd.DataFrame(
                    custom_dict)

                df_schema_custom = df_schema_custom.assign(type='custom')

                # Select columns 'type', 'field_name', and 'value' from each DataFrame
                df_custom_selected = df_schema_custom[[
                    'type', 'field_name', 'value']]
                df_standard_selected = df_schema_standard[[
                    'type', 'field_name', 'value']]

                # Concatenate the two selected DataFrames
                concatenated_df = pd.concat(
                    [df_custom_selected, df_standard_selected])

                # Sort the concatenated DataFrame based on 'type' and 'field_name'
                df_schema = concatenated_df.sort_values(
                    ['type', 'field_name'], ascending=[False, True])

                # Loop through each column and
                for column in df_schema.columns:
                    # convert numeric values to 0
                    if np.issubdtype(df_schema[column].dtype, np.number):
                        df_schema[column].fillna(0, inplace=True)
                    # convert dictionary objects to string
                    if df_schema[column].dtype == 'object':
                        df_schema[column] = df_schema[column].apply(
                            lambda x: cls.convert_dict_to_csv(x) if isinstance(x, dict) else x)
                        df_schema[column] = df_schema[column].astype(
                            str)

                df_table_raw = pd.DataFrame(
                    table_result)

                # Transpose the DataFrame
                df_table_transposed = df_table_raw.T

                # Reset index to make 'name' values become column headers
                df_table_transposed.reset_index(drop=False, inplace=True)

                # Loop through each column and
                for column in df_table_transposed.columns:
                    # convert numeric values to 0
                    if np.issubdtype(df_table_transposed[column].dtype, np.number):
                        df_table_transposed[column].fillna(0, inplace=True)
                    # convert dictionary objects to string
                    if df_table_transposed[column].dtype == 'object':
                        df_table_transposed[column] = df_table_transposed[column].apply(
                            lambda x: cls.convert_dict_to_csv(x) if isinstance(x, dict) else x)
                        df_table_transposed[column] = df_table_transposed[column].astype(
                            str)

                # Get the column names from the dictionary keys
                column_names = list(table_result.keys())

                df_table_list = pd.DataFrame.from_dict(
                    table_result, orient='index', columns=column_names)

                return df_schema, df_table_list, df_table_raw, df_table_transposed, manifest_excel_file

            except Exception as ex:
                error_msg = "Error: {str(ex)}",
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def generate_excel_file_from_data(cls, df_schema, df_table_transposed, manifest_excel_file):
        """
        Generate an Excel file using the given DataFrame objects and save it.

        Args:
            df_schema (pandas.DataFrame): The DataFrame containing schema data.
            df_table_transposed (pandas.DataFrame): The DataFrame containing table data.
            manifest_excel_file (str): The file path to save the generated Excel file.

        Returns:
            str: The file path of the generated Excel file.

        Raises:
            None

        This method takes two DataFrame objects, `df_schema` and `df_table_list`, and a file path `manifest_excel_file`.
        It generates an Excel file using the data from the DataFrames and saves it to the specified file path.

        The schema data is written to the "Instructions" sheet, and the table data is written to the "Tables" sheet.
        The columns in both sheets are auto-fitted to accommodate the data.

        The method returns the file path of the generated Excel file once it is saved.

        Note:
        - This method uses the xlsxwriter library to create and manipulate the Excel file.
        - The get_column_letter function is assumed to be imported from the openpyxl.utils module.
        """

        # Create a new xlsxwriter Workbook object
        workbook = xlsxwriter.Workbook(
            manifest_excel_file, {'nan_inf_to_errors': True})

        # Create a sheet in the workbook
        ws_schema = workbook.add_worksheet('Instructions')
        ws_table_list = workbook.add_worksheet('Tables')

        # Write df_schema to the "Instructions" sheet
        for row_num, row in enumerate(df_schema.values.tolist(), start=0):
            for col_num, value in enumerate(row):
                if isinstance(value, dict):
                    value = cls.convert_dict_to_csv(value)

                ws_schema.write(row_num, col_num, value)

        # Write df_table_list to the "Tables" sheet
        for row_num, row in enumerate(df_table_transposed.values.tolist(), start=0):
            for col_num, value in enumerate(row):
                if isinstance(value, dict):
                    value = cls.convert_dict_to_csv(value)
                ws_table_list.write(row_num, col_num, value)

        # Close the workbook
        workbook.close()

        return manifest_excel_file
