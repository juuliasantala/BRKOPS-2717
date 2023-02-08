import requests 
import os
import urllib3
from pprint import pprint

# Disable warnings - not to be used in production
urllib3.disable_warnings()

DNAC_PARAMS = {
    'username' : os.environ["USERNAME"],
    'password' : os.environ["PASSWORD"],
    "base_url": "https://dnac-sda.ciscolab.dk"
}

def generate_token():
    headers = {"Content": "application/json"}
    api_url = DNAC_PARAMS["base_url"] + "/dna/system/api/v1/auth/token"

    request = requests.post(
        url=api_url,
        auth=(DNAC_PARAMS["username"], DNAC_PARAMS["password"]),
        headers=headers,
        verify=False,
        timeout=30,
    )
    token = request.json()['Token']
    return token

def get_physical_topology_nodes():
    url = "https://dnac-sda.ciscolab.dk/dna/intent/api/v1/topology/physical-topology"
    headers = {"Content": "application/json", "X-Auth-Token": generate_token()}
    request = requests.get(url=url, headers=headers, verify=False, timeout=30)
    topology = request.json()
    topology_nodes = topology["response"]["nodes"]
    return topology_nodes

def print_out_access_nodes():
    data = get_physical_topology_nodes()

    for item in data:
        if 'ACCESS' in item["role"]:
            print(item['label'])
        else:
            continue

print_out_access_nodes()