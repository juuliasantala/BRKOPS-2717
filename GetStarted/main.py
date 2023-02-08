'''
This is a beginner python script with the goal of listing all
the access devices in the network
'''

'''We start by importing all necessary python libraries'''
import requests 
import urllib3

# Disable warnings - not to be used in production
urllib3.disable_warnings()

'''Insert all your credentials in following variables'''
USERNAME = "YOUR USERNAME HERE" # Add your DNAC username here, inside the " "
PASSWORD = "YOUR PASSWORD HERE" # Add your DNAC password here, inside the " "
URL_DNAC = "HOST URL HERE" # Add your DNA Center url here, inside the " "

def generate_token():
    '''
    This function uses your credentials to authenticate to DNA Center
    and retrieves your DNAC authentication token
    '''
    headers = {"Content": "application/json"}
    api_url = URL_DNAC + "/dna/system/api/v1/auth/token"

    request = requests.post(
        url=api_url,
        auth=(USERNAME, PASSWORD),
        headers=headers,
        verify=False,
        timeout=30,
    )
    token = request.json()['Token']
    return token

def get_physical_topology_nodes():
    '''
    This function uses the physical-topology API to get 
    information about the different nodes in the network topology
    '''
    url = URL_DNAC + "/dna/intent/api/v1/topology/physical-topology"
    headers = {"Content": "application/json", "X-Auth-Token": generate_token()}
    request = requests.get(url=url, headers=headers, verify=False, timeout=30)
    topology = request.json()
    topology_nodes = topology["response"]["nodes"]
    return topology_nodes

def print_out_access_nodes():
    '''
    This function uses the data from the get_physical_topology_nodes()
    function in order to loop through the dataset and identifies all
    access nodes, and prints them out
    '''
    data = get_physical_topology_nodes()

    for item in data:
        if 'ACCESS' in item["role"]:
            print(item['label'])
        else:
            continue
    return "All acces devices are now printed"

''' Call the function to print out all devices '''
print_out_access_nodes()