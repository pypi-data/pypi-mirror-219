import os
import sys
import requests
import json
import csv

from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)

from data_ecosystem_services.cdc_tech_environment_service import (
    environment_file as pade_env_file,
    environment_http as pade_env_http
)


# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)
REQUEST_TIMEOUT = 45
TIMEOUT_ONE_MIN = 60


class Query:

    @staticmethod
    def get_query(alation_headers, edc_alation_base_url, datasource_id, config):

        headers = alation_headers
        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        # Set the headers for the request
        headers = {"accept": "application/json",
                   'Token': edc_alation_api_token}

        logger.info("##### Get all queries #####")
        api_url = "/integration/v1/query/"
        edc_alation_base_url = config.get("edc_alation_base_url")
        query_list_url = edc_alation_base_url + api_url
        logger.info(f"query_list_url: {query_list_url}")
        response = requests.get(query_list_url,
                                headers=headers,
                                timeout=TIMEOUT_ONE_MIN)
        queries = json.loads(response.text)
        for query in queries:
            id = str(query["id"])
            logger.info(
                f"##### Get details for a single query {id} #####")
            query_detail_url = edc_alation_base_url + api_url + id
            response_detail = requests.get(query_detail_url,
                                           headers=headers,
                                           timeout=TIMEOUT_ONE_MIN)
            query_detail = json.loads(response_detail.text)
            detail = query_detail.get("detail")
            logger.info(f"query_detail: {query_detail}")
            if detail == "You do not have permission to perform this action.":
                query_title = "No Permission"
                logger.info(f"id: {id}, title: {query_title}")
            else:
                query_id = query_detail["id"]
                logger.info(f"id: {id}, title: {query_title}")

        # Get query text
        api_url = f"/integration/v1/query/{query_id}/sql/"
        query_text_url = edc_alation_base_url + api_url
        logger.info(f"query_text_url:{query_text_url}")
        response_query_text = requests.get(
            query_text_url, headers=headers, timeout=TIMEOUT_ONE_MIN
        )
        response_content_text = "not_set"
        # Check the response status code to determine if the request was
        # successful
        if response_query_text.status_code in (200, 201):
            # Extract the API token from the response
            response_content_text = response_query_text.content.decode(
                "utf-8")
            # logger.info(f"SQL Query Text response: {query_text}")
        else:
            logger.info(
                "Failed to get SQL Query Text :" +
                str(response_content_text)
            )

        query_text = response_content_text
        query_text = query_text.replace("\n", " ").replace("'", "'")

        # Get latest result id
        api_url = f"/integration/v1/query/{query_id}/result/latest/"
        query_url = edc_alation_base_url + api_url
        logger.info(f"query_url: {query_url}")
        logger.info(f"headers: {headers}")
        # Send the request to the Alation API endpoint.
        # The endpoint for executing queries is `/integration/v1/query`.
        response_query = requests.get(query_url,
                                      headers=headers,
                                      timeout=TIMEOUT_ONE_MIN)
        logger.info(
            "response_query.content:" +
            response_query.content.decode("utf-8")
        )

        # execution_result_id = json_response['id']
        execution_result_id = "570"

        # Get lastest results and place in dataframe
        api_url = f"/integration/v1/result/{execution_result_id}/csv/"
        result_url = edc_alation_base_url + api_url

        # download and parse response as csv
        with requests.Session() as s:
            response_results = requests.get(
                result_url, headers=headers, timeout=TIMEOUT_ONE_MIN
            )
            decoded_content = response_results.content.decode("utf-8")
            logger.info("response_results.content:" + decoded_content)
            csv_reader = csv.reader(
                decoded_content.splitlines(), delimiter=","
            )
            logger.info.logger.info(list(csv_reader))
