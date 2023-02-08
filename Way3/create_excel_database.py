"""
This script creates an Excel database that maps the APs to the interfaces on the switches
that they are connected to.
"""
import os
import requests
import urllib3
from requests.auth import HTTPBasicAuth
import pandas as pd
from pprint import pprint
from colorama import Fore, Back, Style


# Disable warnings -- OBS not recommended in production!
urllib3.disable_warnings()

# Cisco DNA Center credential paramenters
DNAC_PARAMS = {
    "username": os.environ.get("USERNAME"),
    "password": os.environ.get("PASSWORD"),
    "base_url": "https://dnac-sda.ciscolab.dk",
}


def generate_token() -> str:
    """
    Day 0-N
    This function generates an authentication token to Cisco DNA Center and which is valid for 1h
    """
    headers = {"Content": "application/json"}
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
        print(":: ERROR in generate_token(): No new token generated::")
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


def create_data_mapping(token: str) -> list:

    """
    This function returns a list of dictionaries with interfaceUuid, AP_Uuid and SW_Uuid data.
    The data is retrieved by the Topology API of DNAC.
    It is used at day 0 to help create your database.

    It will return a list of dictionaries is successfu, otherwise it returns an empty list.
    """
    print("\nNo I am creating the data mapping!\n")
    topology_data = get_physical_topology_nodes_links(token)
    topology_nodes = topology_data[0]
    topology__links = topology_data[1]

    mapping_list = []
    for node in topology_nodes:
        if "Unified AP" in node["family"]:
            ap_device_uuid = node["id"]
            ap_device_label = node["label"]
            ap_platform_id = node["platformId"]

            for link in topology__links:
                if link["source"] == ap_device_uuid:
                    interface_uuid = link["endPortID"]
                    switch_device_uuid = link["target"]
                    interface_name = link["endPortName"]
                    device = {
                        "interface_label": ap_device_label,
                        "ap_platform_id": ap_platform_id,
                        "interfaceUuid": interface_uuid,
                        "interface_name": interface_name,
                        "switch_deviceUuid": switch_device_uuid,
                        "AP_Uuid": ap_device_uuid,
                    }

                elif link["target"] == ap_device_uuid:
                    interface_uuid = link["startPortID"]
                    switch_device_uuid = link["source"]
                    interface_name = link["startPortName"]
                    device = {
                        "interface_label": ap_device_label,
                        "ap_platform_id": ap_platform_id,
                        "interfaceUuid": interface_uuid,
                        "interface_name": interface_name,
                        "switch_deviceUuid": switch_device_uuid,
                        "AP_Uuid": ap_device_uuid,
                    }
                else:
                    # TODO: Add other devices apart from accesspoints to the mapping list.
                    device = {}
                mapping_list.append(device)
        else:
            pass

    mapping_list = list(filter(None, mapping_list))
    return mapping_list


def create_database(token: str, dbname: str):
    
    print("\nNow I am creating the database!\n")
    columns = [
        "ap_uuid",
        "ap_label",
        "ap_platform_id",
        "interface_name_on_switch",
        "interface_uuid",
        "switch_uuid",
    ]
    mapping_list = create_data_mapping(token)
    ap_uuid_list = []
    ap_label_list = []
    ap_platform_id_list = []
    interface_name_list = []
    interface_uuid_list = []
    switch_uuid_list = []

    for i, mapping in enumerate(mapping_list):
        ap_uuid_list.append(mapping["AP_Uuid"])
        ap_platform_id_list.append(mapping["ap_platform_id"])
        interface_name_list.append(mapping["interface_name"])
        interface_uuid_list.append(mapping["interfaceUuid"])
        ap_label_list.append(mapping["interface_label"])
        switch_uuid_list.append(mapping["switch_deviceUuid"])

    #hardcoding another AP that is not provisioned in DNA Center for demo........
    ap_uuid_list.append("AP500F.8045.D35C")
    ap_platform_id_list.append("AP500F.8045.D35C")
    interface_name_list.append("GigabitEthernet1/0/24")
    interface_uuid_list.append("93439256-1177-4623-bc58-20e7455a9ccd")
    ap_label_list.append("AP500F.8045.D35C")
    switch_uuid_list.append("05fae396-14c1-493e-9539-31ccc172c7e4")

    df = pd.DataFrame(
        list(
            zip(
                ap_uuid_list,
                ap_label_list,
                ap_platform_id_list,
                interface_name_list,
                interface_uuid_list,
                switch_uuid_list,
            )
        ),
        columns=columns,
    )
    df.to_excel(f"{dbname}.xlsx")
    print(Fore.LIGHTGREEN_EX + f"Your database {dbname} has been created!")

if __name__ == "__main__":
    token = generate_token()
    #dbname = str(input("Name of database [test_database]: ") or "test_database")
    #create_database(token, dbname)
    pprint(get_physical_topology_nodes_links(token))
