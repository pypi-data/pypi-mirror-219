""" Module for environment_metadata for the developer service with
metadata config file dependencies. """


# core
import sys  # don't remove required for error handling
import os
from pathlib import Path

# text
import json
from html.parser import HTMLParser  # web scraping html

import logging.config

# data
import logging
import uuid
from datetime import datetime

# pade
from data_ecosystem_services.cdc_security_service \
    import security_core as pade_sec_core
from data_ecosystem_services.cdc_tech_environment_service \
    import environment_file as pade_env_file
from data_ecosystem_services.cdc_self_service \
    import logging_metadata as pade_log_metadata

from dotenv import load_dotenv, find_dotenv, set_key

# spark
from pyspark.sql import (SparkSession, DataFrame)
from pyspark.sql.functions import (col, concat_ws, lit,
                                   udf, trim)
from pyspark.sql.types import (StringType, StructType)


# http
import requests

# Import from sibling directory ..\developer_service
OS_NAME = os.name


uuid_udf = udf(lambda: str(uuid.uuid4()), StringType())

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class EnvironmentMetaData:
    """This is a conceptual class representation of an Environment
    It is a static class libary
    Todo
    Note which variables require manual updates from the centers and which
    can be prepopulated
    Note which variables are EDAV or Peraton specific
    Separate out config.devops.dev, config.pade.dev and config.core.dev
    """

    @classmethod
    def check_configuration_files(cls, config: dict, dbutils: object) -> dict:
        """Takes in config dictionary and dbutils objects, returns populated
            check_files dictionary with check results

        Args:
            config (dict): global config dictionary
            dbutils (object): databricks dbutils object

        Returns:
            dict: check_files dictionary with results of file configuration
                    checks
        """

        running_local = config["running_local"]
        # confirm ingress_folder
        ingress_folder = config["ingress_folder"]
        ingress_folder_files_exists = str(cls.file_exists(
                                          running_local,
                                          ingress_folder, dbutils))

        # confirm config_folder
        config_folder = config["config_folder"]
        config_folder_files_exists = str(cls.file_exists(
                                         running_local, config_folder,
                                         dbutils))

        # confirm database path
        pade_database_folder = config.get("pade_database_folder")
        files_exists = cls.file_exists(running_local,
                                       pade_database_folder, dbutils)
        pade_database_folder_files_exists = str(files_exists)

        s_text = f"ingress_folder_files_exists exists test result:\
            {ingress_folder_files_exists}"
        s_text_1 = f"pade_database_folder_files_exists exists test result:\
            {pade_database_folder_files_exists}"
        s_text_2 = f"{config.get('pade_database_name')} at pade_database_folder:\
            {pade_database_folder}"
        ingress_folder_files_exists_test = s_text
        config_folder_files_exists_test = f"config_folder_files_exists exists\
            test result: {config_folder_files_exists}"
        check_files = {
            "ingress_folder": f"{ingress_folder}",
            "ingress_folder_files_exists_test":
            ingress_folder_files_exists_test,
            "config_folder": f"{config_folder}",
            "config_folder_files_exists_test": config_folder_files_exists_test,
            "pade_database_folder": f"{pade_database_folder}",
            "pade_database_folder_files_exists test": s_text_1,
            "creating new pade_database_name": s_text_2
        }

        return check_files

    @classmethod
    def get_job_list(cls, job_name: str, config: dict, spark: SparkSession) -> DataFrame:
        """Get list of jobs actions for a selected job

        Args:
            job_name (str): Selected Job name
            config (dict): Configuration dictionary
            spark (SparkSession): Spark object

        Returns:
            DataFrame: Dataframe with list of job actions
        """

        obj_env_log = pade_log_metadata.LoggingMetaData()

        ingress_folder_sps = config["ingress_folder_sps"]
        ingress_folder_sps = ingress_folder_sps.rstrip("/")
        config_jobs_path = f"{ingress_folder_sps}/bronze_sps_config_jobs.csv"

        project_id = config["project_id"]
        info_msg = f"config_jobs_path:{config_jobs_path}"
        obj_env_log.log_info(config, info_msg)

        first_row_is_header = "true"
        delimiter = ","
        df_jobs = (
            spark.read.format("csv")
            .option("header", first_row_is_header)
            .option("sep", delimiter)
            .option("multiline", True)
            .option("inferSchema", True)
            .load(
                config_jobs_path, forceLowercaseNames=True, inferLong=True
            )
        )
        df_jobs = df_jobs.withColumn('job_name', trim('job'))
        df_jobs = df_jobs.filter(df_jobs.job_name == job_name)
        df_jobs.show(truncate=False)

        return df_jobs

    @classmethod
    def get_column_list(cls, config: dict, spark: SparkSession,
                        dbutils: object) -> DataFrame:
        """Takes in dataset config dictionary, spark object, dbutils object\
        and returns dataframe
        with list of columns for dataset

        Args:
            config (dict): dataset config dictionary
            spark (SparkSession): spark session
            dbutils (object): databricks dbutils object

        Returns:
            DataFrame: dataframe popluated with list of columns for dataset
        """

        first_row_is_header = "true"
        delimiter = ","

        dataset_name = config["dataset_name"]
        running_local = config["running_local"]
        ingress_folder_sps = config["ingress_folder_sps"]
        project_id = config["project_id"]
        ingesttimestamp = datetime.now()

        file_path = f"{ingress_folder_sps}bronze_sps_config_columns.csv"
        # check if size of file is 0
        file_size = cls.get_file_size(running_local, file_path, dbutils, spark)

        print(f"file_size: {str(file_size)}")

        # default to empty DataFrame
        df_results = spark.createDataFrame([], StructType([]))

        if file_size > 0:
            df_results = (
                spark.read.format("csv")
                .option("header", first_row_is_header)
                .option("sep", delimiter)
                .option("inferSchema", True)
                .option("inferLong", True)
                .option("multiline", True)
                .option("inferDecimal", True)
                .option("inferInteger", True)
                .option("forceLowercaseNames", True)
                .load(file_path)
                .withColumn("meta_ingesttimestamp", lit(ingesttimestamp))
                .withColumn(
                    "row_id",
                    concat_ws(
                        "-", col("project_id"), col("dataset_name"),
                        col("column_name")
                    ),
                )
            )

            # bronze_sps_config_columns_df.select(col("column_batch_group").cast("int").as("column_batch_group"))
            if df_results.count() == 0:
                print("File hase 0 rows")
            else:
                if dataset_name == "sps":
                    project_filter = f"(project_id == '{project_id}')"
                    df_results = df_results.filter(project_filter)
        else:
            print("File is empty")

        return df_results

    @staticmethod
    def get_file_size(running_local: bool,
                      file_path: str,
                      dbutils, spark) -> int:
        """Gets file size as integer for file_path

        Args:
            running_local (bool): _description_
            file_path (str): _description_
            dbutils (_type_): _description_
            spark (_type_): _description_

        Returns:
            int: _description_
        """

        obj_env_file = pade_env_file.EnvironmentFile()
        file_size = obj_env_file.get_file_size(running_local,
                                               file_path, dbutils, spark)
        return file_size

    @staticmethod
    def file_exists(running_local: bool, path: str, dbutils) -> bool:
        """Takes in path, dbutils object, returns whether file exists at provided path

        Args:
            running_local: bool
            path (str): path to file
            dbutils (object): databricks dbutils

        Returns:
            bool: True/False indication if file exists
        """

        obj_env_file = pade_env_file.EnvironmentFile()
        file_exists = obj_env_file.file_exists(running_local, path, dbutils)
        return file_exists

    @staticmethod
    def convert_to_windows_dir(path: str) -> str:
        """Takes in path and returns path with backslashes converted to forward slashes

        Args:
            path (str): path to be converted

        Returns:
            str: converted path
        """
        obj_env_file = pade_env_file.EnvironmentFile()
        converted_path = obj_env_file.convert_to_windows_dir(path)
        return converted_path

    @staticmethod
    def convert_to_current_os_dir(path: str) -> str:
        """Takes in path and returns path with backslashes converted to forward slashes

        Args:
            path (str): path to be converted

        Returns:
            str: converted path
        """
        obj_env_file = pade_env_file.EnvironmentFile()
        converted_path = obj_env_file.convert_to_current_os_dir(path)
        return converted_path

    @staticmethod
    def load_environment(running_local: bool, sp_tenant_id: str,
                         subscription_id: str,
                         sp_client_id: str,
                         environment: str,
                         project_id: str,
                         dbutils,
                         applicaton_insights_connection_string: str,
                         az_sub_oauth_token_endpoint: str):
        """  
        Loads the environment file to configure the environment for the application.

        Args:
            running_local (bool): A flag indicating whether the application is running locally or deployed.
            sp_tenant_id (str): The Azure Active Directory tenant (directory) ID.
            subscription_id (str): The ID of the Azure subscription.
            sp_client_id (str): The Azure service principal's client (application) ID.
            environment (str): The deployment environment (e.g., 'dev', 'test', 'prod').
            project_id (str): The project ID to which the application belongs.
            dbutils: Databricks utilities object, which provides access to the Databricks filesystem and secrets, etc.
            applicaton_insights_connection_string (str): The connection string for Azure Application Insights for application monitoring.
        """

        path = sys.executable + "\\.."
        sys.path.append(os.path.dirname(os.path.abspath(path)))
        env_path = os.path.dirname(os.path.abspath(path))

        OS_NAME = os.name
        if dbutils is None:
            running_local = True
        if running_local is True:
            print(f"running_local: {running_local}")
            if OS_NAME.lower() == "nt":
                print("windows")
                env_share_path = env_path + "\\share"
                folder_exists = os.path.exists(env_share_path)
                if not folder_exists:
                    # Create a new directory because it does not exist
                    os.makedirs(env_share_path)
                env_share_path_2 = sys.executable + "\\..\\share"
                sys.path.append(os.path.dirname(
                    os.path.abspath(env_share_path_2)))
                env_file_path = env_share_path + "\\.env"
                print(f"env_file_path: {env_file_path}")
                # don't delete line below - it creates the file
            else:
                print("non windows")
                #env_share_path = env_path + "/share"
                env_share_path = os.path.expanduser("~") + '/share'
                folder_exists = os.path.exists(env_share_path)
                if not folder_exists:
                    # Create a new directory because it does not exist
                    os.makedirs(env_share_path)
                env_share_path_2 = sys.executable + "/../share"
                sys.path.append(os.path.dirname(
                    os.path.abspath(env_share_path_2)))
                env_file_path = env_share_path + "/.env"
                print(f"env_file_path: {env_file_path}")
                # don't delete line below - it creates the file

            env_file = open(env_file_path, "w+", encoding="utf-8")
            dotenv_file = find_dotenv(env_file_path)
            print(f"dotenv_file: {dotenv_file}")
            set_key(dotenv_file, "AZURE_TENANT_ID", sp_tenant_id)
            set_key(dotenv_file, "AZURE_SUBSCRIPTION_ID", subscription_id)
            set_key(dotenv_file, "AZURE_CLIENT_ID", sp_client_id)
        else:
            print(f"running_local: {running_local}")
            env_file_path = f"/mnt/{environment}/{project_id}"
            print(f"env_file_path: {env_file_path}")
            env_file_path = env_file_path + "/config/config_{environment}.txt"
            dbutils.fs.put(env_file_path, f"""AZURE_TENANT_ID {sp_tenant_id}
AZURE_SUBSCRIPTION_ID {subscription_id}
AZURE_CLIENT_ID {sp_client_id}
            """, True)

        set_key(dotenv_file, "APPLICATIONINSIGHTS_CONNECTION_STRING",
                applicaton_insights_connection_string)
        set_key(dotenv_file, "AZURE_AUTHORITY_HOST ",
                az_sub_oauth_token_endpoint)
        set_key(dotenv_file, "PYARROW_IGNORE_TIMEZONE", "1")
        dotenv_file = find_dotenv(env_file_path)
        load_dotenv(dotenv_file)

        return env_file_path

    @classmethod
    def get_configuration_common(cls, parameters: dict, dbutils) -> dict:
        """Takes in parameters dictionary and returns config dictionary

        Args:
            parameters (dict): global parameters dictionary

        Returns:
            dict: update global configuration dictionary
        """

        parameters.setdefault('running_local', False)
        parameters.setdefault('dataset_name', 'na')
        parameters.setdefault('cicd_action', 'na')

        if isinstance(parameters['running_local'], (bool)) is False:
            running_local = parameters['running_local'].lower() in [
                'true', '1', 't', 'y', 'yes']
        else:
            running_local = parameters['running_local']

        if dbutils is None:
            running_local = True

        project_id = parameters["project_id"]
        print(f"running_local: {running_local}")
        environment = parameters["environment"]
        project_id_root = parameters["project_id_root"]
        # Get the current year
        current_year = str(datetime.now().year)
        # Retrieve the parameter 'yyyy', and if it's not present, default to the current year
        yyyy_param = parameters.get("yyyy", current_year)
        # Get the current month
        current_month = datetime.now().strftime('%m')
        # Retrieve the parameter 'mm', and if it's not present, default to the current month
        mm_param = parameters.get("mm", current_month)
        # Get the current day
        current_day = datetime.now().strftime('%d')
        # Retrieve the parameter 'dd', and if it's not present, default to the current day
        dd_param = parameters.get("dd", current_day)

        dataset_name = parameters["dataset_name"]
        cicd_action = parameters["cicd_action"]
        repository_path = parameters["repository_path"]

        # create logger
        logger = logging.getLogger(project_id)
        logger.setLevel(logging.DEBUG)

        config_string = "config"
        cicd_action_string = "cicd"

        repository_path = cls.convert_to_current_os_dir(repository_path)
        env_folder_path = f"{repository_path.rstrip('/')}/{project_id_root}/{project_id}/"
        env_folder_path = cls.convert_to_current_os_dir(env_folder_path)
        config_folder_path = f"{env_folder_path}{config_string}/"
        config_folder_path = cls.convert_to_current_os_dir(
            config_folder_path)
        environment_json_path = f"{config_folder_path}{config_string}.{environment}.json"
        environment_json_path_default = f"{config_folder_path}{config_string}.{environment}.json"

        # Check if environment_json_path exists
        environment_json_path = cls.convert_to_current_os_dir(
            environment_json_path)
        logger.info(
            f"environment_json_path check 1: {environment_json_path}")
        if not cls.file_exists(running_local, environment_json_path, None):
            logger.info(f"config does not exist: {environment_json_path}")
            repository_path_temp = os.getcwd()
            repository_path_temp = str(Path(repository_path_temp))
            repository_path_temp = f"{repository_path_temp}{project_id_root}/{project_id}/{config_string}/"
            repository_path_temp = cls.convert_to_current_os_dir(
                repository_path_temp)
            environment_json_path = f"{repository_path_temp}{config_string}.{environment}.json"
            logger.info(
                f"environment_json_path check 2: {environment_json_path}")
            if not cls.file_exists(running_local, environment_json_path, None):
                logger.info(f"config does not exist: {environment_json_path}")
                repository_path_temp = os.getcwd()
                repository_path_temp = str(Path(repository_path_temp).parent)
                repository_path_temp = f"{repository_path_temp}{project_id_root}/{project_id}/{config_string}/"
                repository_path_temp = cls.convert_to_current_os_dir(
                    repository_path_temp)
                environment_json_path = f"{repository_path_temp}{config_string}.{environment}.json"
                logger.info(
                    f"environment_json_path check 3: {environment_json_path}")
                if not cls.file_exists(running_local, environment_json_path, None):
                    logger.info(
                        f"config does not exist: {environment_json_path}")
                    # Try two levels up from the current folder
                    repository_path_temp = os.getcwd()
                    repository_path_temp = str(
                        Path(repository_path_temp).parent.parent)
                    repository_path_temp = f"{repository_path_temp}{project_id_root}/{project_id}/{config_string}/"
                    repository_path_temp = cls.convert_to_current_os_dir(
                        repository_path_temp)
                    environment_json_path = f"{repository_path_temp}{config_string}.{environment}.json"
                    logger.info(
                        f"environment_json_path check 4: {environment_json_path}")
                    if not cls.file_exists(running_local, environment_json_path, None):
                        logger.info(
                            f"config does not exist: {environment_json_path}")
                        repository_path_temp = os.getcwd()
                        repository_path_temp = str(
                            Path(repository_path_temp).parent.parent.parent)
                        repository_path_temp = cls.convert_to_current_os_dir(
                            repository_path_temp)
                        repository_path_temp = f"{repository_path_temp}{project_id_root}/{project_id}/{config_string}/"
                        repository_path_temp = cls.convert_to_current_os_dir(
                            repository_path_temp)
                        environment_json_path = f"{repository_path_temp}{config_string}.{environment}.json"
                        logger.info(
                            f"environment_json_path check 5: {environment_json_path}")

                        if not cls.file_exists(running_local, environment_json_path, None):
                            logger.info(
                                f"config does not exist: {environment_json_path}")
                            environment_json_path = environment_json_path_default
                        else:
                            logger.info(
                                f"config exists: {environment_json_path}")
                    else:
                        logger.info(f"config exists: {environment_json_path}")
        else:
            logger.info(f"config exists: {environment_json_path}")

        cicd_folder = f"{repository_path}{project_id_root}/{project_id}/{cicd_action_string}/"
        cicd_folder = cls.convert_to_current_os_dir(cicd_folder)
        cicd_action_path = f"{cicd_folder}" + \
            f"{cicd_action}" + f".{environment}.json"

        print("---- WORKING REPOSITORY FILE REFERENCE -------")
        print(f"environment_json_path: {environment_json_path}")
        print(project_id, "----------------------------------------------")

        # Assuming `parameters` and `environment_json_path` are defined somewhere above this code.

        with open(environment_json_path, mode="r", encoding="utf-8") as json_file:
            config = json.load(json_file)

        # Try to fetch from parameters, fallback to config, use an empty string as last resort
        az_kv_az_sub_client_secret_key = parameters.get(
            'az_kv_az_sub_client_secret_key') or config.get('az_kv_az_sub_client_secret_key', '')
        azure_client_secret_key = parameters.get(
            'azure_client_secret_key') or config.get('azure_client_secret_key', '')

        # If the fetched values are empty, replace them with None
        az_kv_az_sub_client_secret_key = az_kv_az_sub_client_secret_key if az_kv_az_sub_client_secret_key else azure_client_secret_key
        azure_client_secret_key = azure_client_secret_key if azure_client_secret_key else az_kv_az_sub_client_secret_key

        config['running_local'] = running_local
        config["yyyy"] = yyyy_param
        config["mm"] = mm_param
        config["dd"] = dd_param
        config["dataset_name"] = dataset_name
        config["dataset_type"] = "TABLE"
        config["repository_path"] = repository_path
        config["environment_json_path"] = environment_json_path
        config["cicd_action_path"] = cicd_action_path
        config["azure_client_secret_key"] = azure_client_secret_key
        config["ingress_folder_sps"] = "".join(
            [config["config_folder"], "pade/"])
        config["project_id"] = config["cdc_project_id"]
        config["project_id_root"] = config["cdc_project_id_root"]
        config["project_id_individual"] = config["cdc_project_id_individual"]
        project_id_individual = config["project_id_individual"]
        config["databricks_instance_id"] = config.get(
            "pade_databricks_instance_id")
        config["environment"] = config["cdc_environment"]
        config["override_save_flag"] = "override_with_save"
        config["is_using_dataset_folder_path_override"] = False
        config["is_using_standard_column_names"] = "force_lowercase"
        config["is_export_schema_required_override"] = True
        config["ingress_mount"] = f"/mnt/{environment}/{project_id_individual}/ingress"
        if config["az_kv_az_sub_client_secret_key"] is None:
            config["az_kv_az_sub_client_secret_key"] = str(
                az_kv_az_sub_client_secret_key)
        project_id = config["project_id"]
        pade_database_folder = config.get("pade_database_folder")
        if not pade_database_folder:
            schema_dataset_file_path = ""
        else:
            schema_dataset_file_path = pade_database_folder.rstrip(
                "/") + "/bronze_clc_schema"
        config["schema_dataset_file_path"] = schema_dataset_file_path

        if config:
            print(
                f"Configuration found environment_json_path: {environment_json_path}")
        else:
            error_message = "Error: no configurations were found."
            error_message = error_message + \
                f"Check your settings file: {environment_json_path}."
            print(error_message)

        scope = config.get('pade_databricks_kv_scope')
        kv_client_id_key = config.get('pade_oauth_sp_kv_client_secret_key')
        kv_client_secret_key = config.get('pade_oauth_sp_kv_client_secret_key')
        if kv_client_id_key is not None:
            if kv_client_id_key.strip() == '':
                kv_client_id_key = None

        if kv_client_secret_key is not None:
            if kv_client_secret_key.strip() == '':
                kv_client_secret_key = None

        sp_redirect_url = config.get("pade_oauth_sp_redirect_url")
        az_sub_oauth_token_endpoint = config.get("az_sub_oauth_token_endpoint")
        sp_tenant_id = config["az_sub_tenant_id"]
        subscription_id = config["az_sub_subscription_id"]
        sp_client_id = config['az_sub_client_id']
        sp_azure_databricks_resource_id = config.get(
            'pade_oauth_databricks_resource_id')

        az_apin_ingestion_endpoint = config.get("az_apin_ingestion_endpoint")
        az_apin_instrumentation_key = config.get("az_apin_instrumentation_key")
        applicaton_insights_connection_string = f"InstrumentationKey={az_apin_instrumentation_key};IngestionEndpoint={az_apin_ingestion_endpoint}"
        az_sub_oauth_token_endpoint = config.get("az_sub_oauth_token_endpoint")

        # Write changes to .env file - create .env file if it does not exist
        env_file_path = cls.load_environment(running_local, sp_tenant_id,
                                             subscription_id,
                                             sp_client_id,
                                             environment,
                                             project_id,
                                             dbutils,
                                             applicaton_insights_connection_string,
                                             az_sub_oauth_token_endpoint)

        config["env_file_path"] = env_file_path
        if running_local is True:
            print(f"azure_client_secret_key:{azure_client_secret_key}")
            sp_client_secret = os.getenv(azure_client_secret_key)
        else:
            sp_client_secret = dbutils.secrets.get(scope=scope,
                                                   key=kv_client_secret_key)

        config["client_id"] = sp_client_id
        config["client_secret"] = sp_client_secret
        config["tenant_id"] = sp_tenant_id

        sp_authority_host_url = "https://management.azure.com/.default"

        if sp_client_secret is None:
            config["error_message"] = "azure_client_secret_value_not_set_error"
        else:
            obj_security_core = pade_sec_core.SecurityCore()

            config_user = \
                obj_security_core.acquire_access_token_with_client_credentials(sp_client_id,
                                                                               sp_client_secret,
                                                                               sp_tenant_id,
                                                                               sp_redirect_url,
                                                                               sp_authority_host_url,
                                                                               sp_azure_databricks_resource_id,
                                                                               project_id)
            config["redirect_uri"] = config_user["redirect_uri"]
            config["authority_host_url"] = config_user["authority_host_url"]
            config["azure_databricks_resource_id"] = config_user["azure_databricks_resource_id"]
            config["az_sub_oauth_token_endpoint"] = config_user["az_sub_oauth_token_endpoint"]
            config["access_token"] = config_user["access_token"]

        return config

    @staticmethod
    def get_dataset_list(config: dict, spark: SparkSession) -> DataFrame:
        """Takes in config dictioarny, spark object, returns list of datasets in project

        Args:
            config (dict): global config dictionary
            spark (SparkSession): spark session

        Returns:
            DataFrame: dataframe with list of datasets in project
        """

        obj_env_log = pade_log_metadata.LoggingMetaData()

        first_row_is_header = "true"
        delimiter = ","

        csv_file_path = config["ingress_folder_sps"]
        csv_file_path = csv_file_path + '\\'
        csv_file_path = csv_file_path + "bronze_sps_config_datasets.csv"
        project_id = config["project_id"]
        ingesttimestamp = datetime.now()

        df_results = (
            spark.read.format("csv")
            .option("header", first_row_is_header)
            .option("sep", delimiter)
            .option("multiline", True)
            .option("inferSchema", True)
            .load(
                csv_file_path, forceLowercaseNames=True,
                inferLong=True
            )
            .withColumn("meta_ingesttimestamp", lit(ingesttimestamp))
            .withColumn(
                "row_id", concat_ws("-", col("project_id"),
                                    col("dataset_name"))
            )
        )

        # sort
        if df_results.count() > 0:
            # df_results.show()
            df_results = df_results.sort("pipeline_batch_group")
        else:
            err_message = f"No datasets found for project_id:{project_id}"
            obj_env_log.log_error(project_id, err_message)
            print(err_message)

        return df_results

    @staticmethod
    def get_pipeline_list(config: dict, spark: SparkSession) -> DataFrame:
        """Takes in config dictionary, spark session object, returns dataframe with list of pipelines in project

        Args:
            config (dict): global config dictionary
            spark (SparkSession): spark session

        Returns:
            DataFrame: dataframe with list of pipelines in project
        """

        first_row_is_header = "true"
        delimiter = ","

        ingress_folder_sps = config["ingress_folder_sps"]
        ingesttimestamp = datetime.now()
        project_id = config["project_id"]

        bronze_sps_config_pipelines_df = (
            spark.read.format("csv")
            .option("header", first_row_is_header)
            .option("sep", delimiter)
            .option("multiline", True)
            .option("inferSchema", True)
            .load(
                f"{ingress_folder_sps}bronze_sps_config_pipelines.csv",
                forceLowercaseNames=True,
                inferLong=True,
            )
            .withColumn("meta_ingesttimestamp", lit(ingesttimestamp))
            .withColumn("row_id", concat_ws("-", col("project_id"), col("view_name")))
        )

        bronze_sps_config_pipelines_df = bronze_sps_config_pipelines_df.filter(
            "project_id == '" + project_id + "' "
        )

        # sort by load group to ensure dependencies are run in order
        bronze_sps_config_pipelines_df = bronze_sps_config_pipelines_df.sort(
            "pipeline_batch_group"
        )

        return bronze_sps_config_pipelines_df

    @classmethod
    def list_files(cls, config: dict, token: str, base_path: str) -> list:
        """Takes in a config dictionary, token and base_path, returns
        populated list of files

        Args:
            config (dict): global config dictionary
            token (str): token
            base_path (str): path to list files

        Returns:
            list: list of files at the path location
        """

        obj_env_log = pade_log_metadata.LoggingMetaData()

        databricks_instance_id = config["databricks_instance_id"]
        json_text = {"path": base_path}
        headers = {"Authentication": f"Bearer {token}"}
        url = f"https://{databricks_instance_id}/api/2.0/workspace/list"
        project_id = config["project_id"]
        obj_env_log.log_info(config, f"------- Fetch {base_path}  -------")
        obj_env_log.log_info(config, f"url:{str(url)}")
        headers_redacted = str(headers).replace(token, "[bearer REDACTED]")
        obj_env_log.log_info(config, f"headers:{headers_redacted}")

        response = requests.get(url=url, headers=headers, json=json_text,
                                timeout=120)
        data = None
        results = []

        try:
            response_text = str(response.text)
            data = json.loads(response_text)
            msg = f"Received list_files with length : {len(str(response_text))} when posting to : "
            msg = msg + f"{url} to list files for : {base_path}"
            response_text_fetch = msg
            print("- response : success  -")
            print(f"{response_text_fetch}")
            lst = data["objects"]

            for i in lst:
                if i["object_type"] == "DIRECTORY" or i["object_type"] == "REPO":
                    path = i["path"]
                    results.extend(cls.list_files(config, token, path))
                else:
                    path = i["path"]
                    results.append(path)
        except Exception as exception_object:
            f_filter = HTMLFilter()
            f_filter.feed(response.text)
            response_text = f_filter.text
            print(f"- response : error - {exception_object}")
            print(f"Error converting response text:{response_text} to json")

        return results

    @classmethod
    def setup_databricks_configuration(cls, config: dict, spark: SparkSession) -> str:
        """Takes in config dictionary, spark object, returns configured spark object

        Args:
            config (dict): global config dictionary
            spark (SparkSession): spark session

        Returns:
            str: folder_database_path
        """

        pade_database_name = config["pade_database_name"]
        pade_database_folder = config["pade_database_folder"]

        running_local = config["running_local"]

        if running_local is True:
            # use default location
            sql_statement = f"create database if not exists {pade_database_name};"
        else:
            sql_statement = f"create database if not exists {pade_database_name}  LOCATION '{pade_database_folder}';"

        print(sql_statement)
        spark.sql(sql_statement)

        # pade_databricks_owner_group = config["pade_databricks_owner_group"]
        # sql_statement = f"alter schema {pade_database_name} owner to `{pade_databricks_owner_group}`;"
        # print(sql_statement)
        # spark.sql(sql_statement)

        sql_statement = f"Describe database {pade_database_name}"
        df_db_schema = spark.sql(sql_statement)

        if running_local is True:
            df_db_schema.show(truncate=False)

        df_db_schema = df_db_schema.filter(
            df_db_schema.database_description_item == "Location")
        rdd_row = df_db_schema.first()

        if rdd_row is not None:
            folder_database_path = rdd_row["database_description_value"]
        else:
            folder_database_path = "missing dataframe value error"

        return folder_database_path

    @staticmethod
    def setup_spark_configuration(spark: SparkSession, config: dict) -> SparkSession:
        """Takes spark session, global config dictionary
        and return configured Spark session

        Args:
            spark (SparkSession): spark session
            config (dict): global config dictionary

        Returns:
            SparkSession: configured spark session
        """

        obj_env_log = pade_log_metadata.LoggingMetaData()

        c_ep = config["pade_oauth_sp_authority_host_url"]
        c_id = config["client_id"]
        c_secret = config["client_secret"]
        sp_tenant_id = config["az_sub_tenant_id"]
        running_local = config['running_local']
        project_id = config['project_id']

        client_secret_exists = True
        if c_id is None or c_secret is None:
            client_secret_exists = False
        storage_account = config["pade_azure_storage_account"]

        client_token_provider = "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider"
        provider_type = "OAuth"

        # stack overflow example
        fs_prefix_e1 = "fs.azure.account.auth."
        fso_prefix_e1 = "fs.azure.account.oauth"
        fso2_prefix_e1 = "fs.azure.account.oauth2"
        fso3_prefix_e1 = "fs.azure.account.oauth2.client.secret"  # spark.hadoop
        fs_suffix_e1 = f".{storage_account}.dfs.core.windows.net"
        fso3_prefix_e1 = fso3_prefix_e1 + fs_suffix_e1

        if client_secret_exists is None:
            client_secret_exists = False

        print(f"client_secret_exists:{str(client_secret_exists)}")
        print(f"endpoint:{str(c_ep)}")

        config["run_as"] = "service_principal"
        run_as = config["run_as"]
        print(f"running databricks access using run_as:{run_as}")

        if (client_secret_exists is True) and (run_as == "service_principal") and running_local is True:

            spark.conf.set(f"{fs_prefix_e1}type{fs_suffix_e1}", provider_type)
            spark.conf.set(
                f"{fso_prefix_e1}.provider.type{fs_suffix_e1}", client_token_provider)
            spark.conf.set(f"{fso2_prefix_e1}.client.id{fs_suffix_e1}", c_id)
            spark.conf.set(
                f"{fso2_prefix_e1}.client.secret{fs_suffix_e1}", c_secret)
            client_endpoint_e1 = f"https://login.microsoftonline.com/{sp_tenant_id}/oauth2/token"
            spark.conf.set(
                f"{fso2_prefix_e1}.client.endpoint{fs_suffix_e1}", client_endpoint_e1)

            obj_env_log.log_info(
                config, f'spark.conf.set "({fs_prefix_e1}type{fs_suffix_e1}", "{provider_type}")')
            obj_env_log.log_info(config, f'spark.conf.set "({fso_prefix_e1}.provider.type{fs_suffix_e1}", \
                "{client_token_provider}")')
            obj_env_log.log_info(
                config, f'spark.conf.set "({fso2_prefix_e1}.client.id{fs_suffix_e1}", "{c_id}")')
            obj_env_log.log_info(config, f'spark.conf.set "{fso2_prefix_e1}.client.endpoint{fs_suffix_e1}" \
                = "{client_endpoint_e1}"')

        spark.conf.set("spark.databricks.io.cache.enabled", "true")
        # Enable Arrow-based columnar data transfers
        spark.conf.set("spark.sql.execution.arrow.enabled", "true")
        # sometimes azure storage has a delta table not found bug - in that scenario try filemount above
        spark.conf.set("spark.sql.execution.arrow.fallback.enabled", "true")
        spark.conf.set("spark.databricks.pyspark.enablePy4JSecurity", "false")
        # Enable Delta Preview
        spark.conf.set("spark.databricks.delta.preview.enabled ", "true")

        if running_local is False:
            os.environ['PYARROW_IGNORE_TIMEZONE'] = '1'
            spark.sql(
                "SET spark.databricks.delta.schema.autoMerge.enabled = true")
            pade_checkpoint_folder = config["pade_checkpoint_folder"]
            print(f"pade_checkpoint_folder: {pade_checkpoint_folder}")
            spark.sparkContext.setCheckpointDir(pade_checkpoint_folder)

        # Checkpoint
        return spark


class HTMLFilter(HTMLParser):
    """Parses HTMLData

    Args:
        HTMLParser (_type_): _description_
    """

    text = ""

    def handle_data(self, data):
        """Parses HTMLData

        Args:
            data (_type_): _description_
        """
        self.text += data
