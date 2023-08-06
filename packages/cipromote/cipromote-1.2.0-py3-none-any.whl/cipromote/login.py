import os
import requests
import cipromote.constants as constants


def login_init(login_instance_info):
    server_url = os.getenv("MOTIOCI_SERVERURL")
    constants.CI_URL = server_url
    print(f"Logging in at {constants.LOGIN_URL}.")
    response = requests.post(constants.LOGIN_URL, data=login_instance_info, verify=False)
    return response.headers.get("x-auth-token")
