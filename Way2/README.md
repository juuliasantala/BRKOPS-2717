# Let's get ready to save some power!
This section is aimed for those who would like to try to automate the way you shut down access ports on switches through the Cisco DNA Center APIs. 

## Requirements
Make sure you have:
* A virtual environment installed and activated
* Installed the necessary requirements
```bash
(venv) $ pip install -r requirements.txt
```
Before you execure powersave.py, you will need to export your user credentials to your virtual environment by doing
```bash
(venv) $ export USERNAME=<username>
(venv) $ export PASSWORD=<password>
```

## Get started with the code
In the repository you will find two python scrips
- create_excel_database.py
- powersave.py

powersave.py uses script create_excel_database.py in order to create an Excel database, in order to map inventory information from Cisco DNA Center. The background to this is to be able to record which interfaces the access points are connected to, information that otherwise disappears when the ports are shut down. 
```bash
(venv) $ python powersave.py
```

To run the script, you run the following command (make sure you are in the correct directory):
```bash
(venv) $ python powersave.py
```

When you run the script, you should be greetet with the following message: 

```bash
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
*                                                                               *
*                          Welcome to the power saver script!                   *
*                                                                               *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
```
You will then be presented with input options, you will either be able to: 
* Create a new database
* Shut down the access points
* Turn the access points up again

Here is an example of how it can look like: 
```bash
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
*                                                                               *
*                          Welcome to the power saver script!                   *
*                                                                               *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

Do you want to shut down the access points and save some watts (y/n)[n]?:y

...double checking: You REALLY want to shut down the access points?(y/n)[n]y

Your action "shut APs down" is being pushed to Cisco DNA Center... 

Port GigabitEthernet1/0/23 with id 43f9297c-9de3-4527-b513-2beecc6432ef is updated to DOWN
Port GigabitEthernet1/0/23 with id e500025a-f9bc-45db-a527-de3eca59be1d is updated to DOWN
Port GigabitEthernet1/0/24 with id 93439256-1177-4623-bc58-20e7455a9ccd is updated to DOWN
```

Now your task is to take this code, and start adapting it so it better fits ***your use cases***.

## Authors & Maintainers
People responsible for the creation and maintenance of this project:
* Christina Skoglund cskoglun@cisco.com
* Juulia Santala jusantal@cisco.com

## License
This project is licensed to you under the terms of the [Cisco Sample Code License](LICENSE).
