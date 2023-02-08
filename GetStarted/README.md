# Getting started!
This section is aimed for beginners that want to use some basic code in order to start making API calls to their Cisco DNA Center through a Python script. 

## Requirements to get started
To be able to run the code in this section, you will need the following:
* Create a virtual environment with python
```bash
For mac
$ python3 -m venv venv

For windows 
$ TODO
```
Activate your virtual environment
```bash
For mac
$ source venv/bin/activate
(venv) $

For windows 
$ TODO
```
You know that your virtual environment is activated when you see (venv). Make sure you always have it activated.

* The next step is to install the libraries that are required in order to run the script. 
```bash
(venv) $ pip install requests

```
* Pull this repository to your local environment. OBS If you have already done this, skip this step!
```bash
(venv) $ git pull [CORRECT PATH]

```

## Get started with the python code!
The script you will be working with is called 'main.py' and you are able to see it in this directory. Let's break down the different sections of the script together. 

* Import the libraries we need in the script. 
```python
'''We start by importing all necessary python libraries'''
import requests 
import urllib3
```
We use the library 'urllib3' in order to disable warnings regarding unverified HTTPS calls. OBS! This is not recommended to do in a production environment. 
```python
# Disable warnings - not to be used in production
urllib3.disable_warnings()
```

* Insert all your credentials in following variables.
```python
USERNAME = "YOUR USERNAME HERE" # Add your DNAC username here, inside the " "
PASSWORD = "YOUR PASSWORD HERE" # Add your DNAC password here, inside the " "
URL_DNAC = "HOST URL HERE" # Add your DNA Center url here, inside the " "
```

* This function uses your credentials to authenticate to DNA Center and retrieves your DNAC authentication token.
```python
def generate_token():
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
```

* This function uses the physical-topology API to get information about the different nodes in the network topology.
```python
def get_physical_topology_nodes():

    url = URL_DNAC + "/dna/intent/api/v1/topology/physical-topology"
    headers = {"Content": "application/json", "X-Auth-Token": generate_token()}
    request = requests.get(url=url, headers=headers, verify=False, timeout=30)
    topology = request.json()
    topology_nodes = topology["response"]["nodes"]
    return topology_nodes
```

* This function uses the data from the get_physical_topology_nodes() function in order to loop through the dataset and identifies all access nodes, and prints them out
```python
def print_out_access_nodes():
    data = get_physical_topology_nodes()

    for item in data:
        if 'ACCESS' in item["role"]:
            print(item['label'])
        else:
            continue
    return "All acces devices are now printed"
```
* Call the function to print out all devices
```python
print_out_access_nodes()

```
* Now it is time to execute the script!
```bash
(venv) $ python main.py 
```

## Authors & Maintainers
People responsible for the creation and maintenance of this project:
* Christina Skoglund cskoglun@cisco.com
* Juulia Santala jusantal@cisco.com

## License
This project is licensed to you under the terms of the [Cisco Sample Code License](LICENSE).
