""" Core module with cli """
import click
import json
import os
import requests
import cipromote.constants as constants
import cipromote.instances as instances
import cipromote.queries as queries
import cipromote.loginInput as loginInput
import cipromote.login as login
import cipromote.labels as labels
import cipromote.label_versions as label_versions
import cipromote.projects as projects
from termcolor import cprint
from pprint import pprint
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
session = Session()
session.verify = False
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
session = Session()
session.verify = False
project_name = 'Admin'

@click.group()
def main():
    """
    This is a cli for promoting motioci labels

    Example:

    "$> cipromote get-instances 'https://cr16gwmciapp01'"


    Example:

    "$> cipromote get-instances-token "New Dev" "New QA" "BillingCenter""

    """


@main.command("check-env", short_help="Check required environment variables")
def check_env():
    """Prints out the current necessary environment variables"""
    motioci_username = os.getenv("MOTIOCI_USERNAME")
    motioci_password = os.getenv("MOTIOCI_PASSWORD")
    motioci_server = os.getenv("MOTIOCI_SERVERURL")
    motioci_token = os.getenv("MOTIOCI_TOKEN")
    print(f"Your environment has {motioci_username} for the variable MOTIOCI_USERNAME")
    print(f"Your environment has {motioci_password} for the variable MOTIOCI_PASSWORD")
    print(f"Your environment has {motioci_server} for the variable MOTIOCI_SERVERURL")
    print(f"Your environment has {motioci_token} for the variable MOTIOCI_TOKEN")


@main.command("get-instances", short_help="Get a list of instances")
def get_instances():
    """Gets a list of instances"""
    server_url = os.getenv("MOTIOCI_SERVERURL")
    constants.CI_URL = server_url
    constants.GRAPH_URL = constants.CI_URL + constants.GRAPH_URL
    print('Sending query to the following url')
    print(constants.GRAPH_URL)
    instance_object = instances.get_instances_default()
    pprint(instance_object)
    print(f"Instance 0 has these namespaces {instance_object[0]['node']['namespaces']}")
    return instance_object

@main.command("get-instance", short_help="Get an instance by name")
@click.argument("instance-name")
def get_instance(instance_name):
    """ Get a particular instance by name """
    server_url = os.getenv("MOTIOCI_SERVERURL")
    constants.CI_URL = server_url
    constants.GRAPH_URL = constants.CI_URL + constants.GRAPH_URL
    print('Sending query to the following url')
    print(constants.GRAPH_URL)
    instance_object = instances.get_instances_default()
    for instance in instance_object:
        if instance['node']['name'].lower() == instance_name.lower():
            target_instance = instance
            print(f"The target instance is {target_instance['node']['name']}")
            pprint(target_instance)
    return target_instance

@main.command("get-labels", short_help="Get a list of available labels")
def get_labels():
    """Gets a lit of available labels"""
    server_url = os.getenv("MOTIOCI_SERVERURL")
    constants.CI_URL = server_url
    constants.GRAPH_URL = constants.CI_URL + constants.GRAPH_URL
    existing_token = os.getenv("MOTIOCI_TOKEN", '""')
    if (os.getenv("MOTIOCI_TOKEN") == "") or (os.getenv("MOTIOCI_TOKEN") == None):
        print(f"You need a valid token defined in your environment"
                f"You should try check-env to check your environment."
                )
        raise SystemExit(1)
    else:
        constants.X_AUTH_TOKEN = os.getenv("MOTIOCI_TOKEN")
    labels_object = labels.get_labels_default()
    if labels_object == 'None':
        print(f"No labels found, maybe your token is expired?")
        raise SystemExit(1)
    return labels_object


@main.command("get-instances-token", short_help="Authenticate to two instances")
@click.argument("source-instance-name")
@click.argument("target-instance-name")
@click.argument("namespace-name")
def get_instances_token(source_instance_name, target_instance_name, namespace_name):
    """Authenticate against two instances and generates a token"""
    server_url = os.getenv("MOTIOCI_SERVERURL")
    constants.CI_URL = server_url
    constants.LOGIN_URL = constants.CI_URL + constants.LOGIN_URL
    constants.LOGOUT_URL = constants.CI_URL + constants.LOGOUT_URL
    constants.GRAPH_URL = constants.CI_URL + constants.GRAPH_URL
    motioci_username = os.getenv("MOTIOCI_USERNAME")
    motioci_password = os.getenv("MOTIOCI_PASSWORD")
    motioci_server = os.getenv("MOTIOCI_SERVERURL")
    print(
        f'The source instance is "{source_instance_name}". The target instance'
        f' is "{target_instance_name}". The namespace is "{namespace_name}".'
    )
    existing_token = os.getenv("MOTIOCI_TOKEN", '""')
    if (os.getenv("MOTIOCI_TOKEN") == "") or (os.getenv("MOTIOCI_TOKEN") == None):
        credentials = loginInput.get_login_from_user(
            source_instance_name, target_instance_name, namespace_name
        )
        #print(credentials)
        auth_token = login.login_init(credentials)
        if auth_token is None:
            print("Invalid parameters. Login cancelled!")
        else:
            #print("Credentials: ", credentials)
            print("Login successful!")
            print("x-auth_token: ", auth_token)
            #os.environ.setdefault('MOTIOCI_TOKEN', auth_token)
            #os.environ['MOTIOCI_TOKEN'] = auth_token
            #print(os.getenv('MOTIOCI_TOKEN'))
            constants.X_AUTH_TOKEN = os.getenv("MOTIOCI_TOKEN")
    else:
        print(
            f"Found a token in environment variable MOTIOCI_TOKEN. {os.getenv('MOTIOCI_TOKEN')}\n"
            f"If you want to get a new token, clear your environment variable."
        )
        constants.X_AUTH_TOKEN = os.getenv("MOTIOCI_TOKEN")


@main.command("promote-label", short_help="Promote a label to a new instance")
@click.argument("source-instance-name")
@click.argument("target-instance-name")
@click.argument("namespace-name")
@click.argument("label-name")
def promote_label(source_instance_name, target_instance_name, namespace_name, label_name):
    """Promote a label from one instance to another"""
    global project_name
    server_url = os.getenv("MOTIOCI_SERVERURL")
    constants.CI_URL = server_url
    constants.LOGIN_URL = constants.CI_URL + constants.LOGIN_URL
    constants.LOGOUT_URL = constants.CI_URL + constants.LOGOUT_URL
    constants.GRAPH_URL = constants.CI_URL + constants.GRAPH_URL
    existing_token = os.getenv("MOTIOCI_TOKEN", '""')
    if (os.getenv("MOTIOCI_TOKEN") == "") or (os.getenv("MOTIOCI_TOKEN") == None):
        print(f"You need a valid token defined in your environment"
                f"You should try check-env to check your environment."
                )
        raise SystemExit(1)
    else:
        print(
            f"Found a token in environment variable MOTIOCI_TOKEN. {os.getenv('MOTIOCI_TOKEN')}\n"
            f"If you want to get a new token, clear your environment variable and run get-instances-token command."
        )
        constants.X_AUTH_TOKEN = os.getenv("MOTIOCI_TOKEN")
    # Minimum required arguments for deploy label: target_instance_id and label_version_id.
    source_instance_id = instances.get_instance_id(source_instance_name)
    print(f"Instance {source_instance_name} has an ID of {source_instance_id}.")
    target_instance_id = instances.get_instance_id(target_instance_name)
    print(f"Instance {target_instance_name} has an ID of {target_instance_id}.")
    project_id = projects.get_project_id(source_instance_id, project_name)
    print(f"The project {project_name} has an ID of {project_id}.")
    label_list = labels.get_label_id(project_id, label_name)
    label_id = label_list[0]['node']['id']
    print(f"The label {label_name} has an ID of {label_id}.")
    label_version_id = label_versions.get_version_id_default(label_id)
    print(f"The Label ID {label_id} has a version of {label_version_id}.")
    print(f"Making the label version promote call")
    label_versions.promote_label_version_call(target_instance_id, label_version_id)
    return
