import requests
import os
import cipromote.constants as constants
import cipromote.queries as queries

# Available options:
valid_instance_names = {}
valid_namespace_names = {}

# String literals
login_str = "{{"'"namespaceId"'":"'"{namespaceIn}"'","'"username"'":"'"{usernameIn}"'","'"password"'":"'"{passwordIn}"'","'"instanceId"'":"'"{instanceIn}"'"}}"""
comma_str = ", "
starting_str = "["
ending_str = "]"


# Set the instances and namespaces that the user can log in to based on their server link.
def get_instance_info_from_server():
    response = requests.post(constants.GRAPH_URL, headers={'x-auth-token': constants.X_AUTH_TOKEN},
                             json={'query': queries.GET_INSTANCES}, verify=False)
    instance_array = response.json()["data"]["instances"]["edges"]
    for instance in instance_array:
        valid_instance_names.update({instance["node"]["name"]: instance["node"]["id"]})
        for namespace in instance["node"]["namespaces"]:
            valid_namespace_names.update({namespace["name"]: namespace["id"]})
    return


# Ask the user to input necessary info for logging in. Returns credential string to ci-cli.
def get_login_from_user(source_instance_name, target_instance_name, namespace_name):
    get_instance_info_from_server()
    #print("Enter credentials below. Press q to stop.")
    credentials = ""
    firstCred = True
    # Allow user to input credentials only two times.
    for i in range(2):
        if firstCred:
            instanceInput = source_instance_name #instanceInput = input("Enter instanceName: ")
        else:
            instanceInput = target_instance_name
        while instanceInput not in valid_instance_names and instanceInput != "q":
            print("Invalid instance. Available instances: ",
                  ', '.join(str(key) for key, _ in valid_instance_names.items()))
            print("Please try with valid instance names")
            raise SystemExit(1)
        namespaceNameInput = namespace_name #input("Enter namespaceName: ")
        while namespaceNameInput not in valid_namespace_names and namespaceNameInput != "q":
            print("Invalid namespace. Available namespaces: ",
                  ', '.join(str(key) for key, _ in valid_namespace_names.items()))
            print("Please try with valid instance names")
            raise SystemExit(1)
        usernameInput = os.getenv('MOTIOCI_USERNAME') #input("Enter username: ")
        passwordInput = os.getenv('MOTIOCI_PASSWORD') #getpass()
        if firstCred:
            credentials = starting_str + login_str.format(namespaceIn=valid_namespace_names.get(namespaceNameInput),
                                                          usernameIn=usernameInput,
                                                          passwordIn=passwordInput,
                                                          instanceIn=valid_instance_names.get(instanceInput))
            firstCred = False
        else:
            credentials = credentials + comma_str + login_str.format(
                namespaceIn=valid_namespace_names.get(namespaceNameInput),
                usernameIn=usernameInput,
                passwordIn=passwordInput,
                instanceIn=valid_instance_names.get(instanceInput))
        print("Login instance saved!")

    if credentials != "":
        print("Logging in...")
        credentials = credentials + ending_str
        return credentials
    return
