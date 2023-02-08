"""
The purpose of this script is PoE port management through Cisco DNA Center.
"""
import os
import sys
from pprint import pprint
import json

import urllib3
import requests
from requests.auth import HTTPBasicAuth

import pandas as pd
# from colorama import Fore, Back, Style

from create_excel_database import create_database

import requests
import urllib3

# Disable warnings -- OBS not recommended in production!
urllib3.disable_warnings()

DNAC_PARAMS = {
    "username": os.environ.get("USERNAME"),
    "password": os.environ.get("PASSWORD"),
    "base_url": "https://dnac-sda.ciscolab.dk",
}

def generate_token() -> str:
    """
    This function generates an authentication token to Cisco DNA Center and which is valid for 1h
    """
    headers = {"Content-Type": "application/json"}
    auth_url = DNAC_PARAMS["base_url"] + "/dna/system/api/v1/auth/token"

    req = requests.post(
        url=auth_url,
        auth=HTTPBasicAuth(DNAC_PARAMS["username"], DNAC_PARAMS["password"]),
        headers=headers,
        verify=False,
        timeout=30,
    )
    if req.status_code in (200, 201):
        token_data = req.json()
        token = token_data["Token"]
    else:
        token = "No token generated"
        print(":: ERROR in generate_token() ::")
        print(f"The status code is {req.status_code}")

    return token

def get_physical_topology_nodes_links(token_arg) -> list:
    """
    This function shall give return all physical topology links.
    It is used at day 0 to help create your database.
    """
    print("\nNow I am retrieving the topology from Cisco DNA Center!\n")

    url = DNAC_PARAMS["base_url"] + "/dna/intent/api/v1/topology/physical-topology"
    headers = {"Content": "application/json", "X-Auth-Token": token_arg}
    req = requests.get(url=url, headers=headers, verify=False, timeout=30)

    if req.status_code == 200:
        topology = req.json()
        topology_dict = topology["response"]
        topology_links = topology_dict["links"]
        topology_nodes = topology_dict["nodes"]
    else:
        topology_dict = "No devices received"
        print(
            ":: ERROR in get_physical_topology_nodes_links() : No topology devices received::"
        )
        print(f"The status code is {req.status_code}")

    return topology_nodes, topology_links

def update_interface_status(action_arg, interface_uuid, interface_name, token_arg) -> bool:
    """
    Function updates switch interface Admin Status and changes its description
    """
    new_status = action_arg.upper() 
    url = (
        DNAC_PARAMS["base_url"]
        + f"/dna/intent/api/v1/interface/{interface_uuid}?deploymentMode=Deploy"
    )
    headers = {"content-type": "application/json", "X-Auth-Token": token_arg}
    payload = json.dumps(
        {
            "description": f"Interface status is configured to 'Admin {new_status} through API'",
            "adminStatus": f"{new_status}",
        }
    )

    req = requests.put(url=url, headers=headers, data=payload, verify=False, timeout=30)
    if req.status_code in (200, 202):
        print(f"Port {interface_name} with id {interface_uuid} is updated to {new_status}")
        updating_status = True
    elif req.status_code == 500:
        print(f"{req.json()['response']['detail']}, as the port is already {new_status}"
        )
        updating_status = False
    else:
        print("::ERROR update_interface_status() failed::")
        print(f"Status code is {req.status_code}")
        print(req.text)
        updating_status = False
    return updating_status

def main(args: list):
    """
    Main function to either create a database or update port status
    """
    token = generate_token()

    if len(args) == 2:
        if "create" in args[0].lower():
            db_name = args[1].lower()
            create_database(token, db_name)

    elif len(args) == 1:
        action = args[0].upper()

        if action in ("UP", "DOWN"):
            data = pd.read_excel("database.xlsx")
            interface_id = data["interface_uuid"].values.tolist()
            interface_names = data["interface_name_on_switch"].values.tolist()

            for i, value in enumerate(interface_id):
                interface_name = interface_names[i]
                interfaceuuid = value
                update_interface_status(action, interfaceuuid, interface_name, token)
        else:
            pprint(f"{action} is not a valid argument")
            pprint("Valid input arguments are UP or DOWN")

def entrypoint():
    arg = sys.argv[1:]

    if len(arg) >= 1:
        main(arg)

    else:
        print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        print("*                                                                               *")
        print("*                          Welcome to the power saver script!                   *")
        print("*                                                                               *")
        print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
        
        _PORTSTATUS = str(
            input(
                "\nDo you want to shut down the access points and save some watts (y/n)[n]?:"
            )
            or "n"
        )

        if _PORTSTATUS.lower() in ("n", "no"):
            _TURNON = str(
                input("\nDo you want to turn on the access points (y/n)[n]?:") or "n"
            )

            if _TURNON.lower() in ("n", "no"):
                print("No action will be taken")
            elif _TURNON.lower() in ("y", "yes"):
                _STATUS = "up"
                print('\nYour action "turn APs on" is being posted to Cisco DNA Center...\n ')
                arguments = [_STATUS]
                main(arguments)
            else:
                print("I did not understand that. No action taken.")

        elif _PORTSTATUS.lower() in ("y", "yes"):
            _CHECK = str(
                input(
                    "\n...double checking: You REALLY want to shut down the access points?(y/n)[n]"
                )
                or "n"
            )
            if _CHECK.lower() in ("y", "yes"):
                _STATUS = "down"
                print('\nYour action "shut APs down" is being pushed to Cisco DNA Center... ')
                arguments = [_STATUS]
                main(arguments)
            elif _CHECK.lower() in ("n", "no"):
                print("\nAborted!\n")
            else:
                print(
                    "\nI did not understand that. Please try to run the script again\n"
                )

if __name__ == "__main__":
    entrypoint()
