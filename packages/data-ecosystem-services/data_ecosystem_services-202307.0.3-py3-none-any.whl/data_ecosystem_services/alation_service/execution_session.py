# TODO WIRE UP CLASS

logger.info("##### Get all execution sessions #####")
api_url = "/integration/v1/query/execution_session/"
session_list_url = edc_alation_base_url + api_url
response = requests.get(session_list_url,
                        headers=headers,
                        timeout=TIMEOUT_ONE_MIN)
sessions = json.loads(response.text)
for session in sessions:
    session_id = session["id"]
    client_session_id = session["client_session_id"]
    msg = f"ID: {session_id}, Client-session-ID: {client_session_id}"
    logger.info(msg)

query_id = "249"
