#!/usr/bin/env python
'''
Job to run the tests.

Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''

__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"
__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"

import os
from pyats.easypy import run
from message import message # custom module for what we print
import powersave

DESTINATIONS = (
        '10.105.22.34', #S1-AP4800
        # '10.105.37.3', #S2-AP3800
        '10.105.0.10' #associated WLC
)

def full_path(script_name:str)->str:
    test_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(test_path, script_name)

def main():

    print(f"\n{'* '*22}*\n* {'  '*21}*")
    print("* Welcome to the Test-Driven port automator *")
    print(f"* {'  '*21}*\n{'* '*22}*\n")

    pre_test = run(
        testscript=full_path('ping_test.py'),
        taskid="PRE-TEST",
        destinations=DESTINATIONS
    )
    print(message("PRE-TEST", pre_test))

    selection = input("Would you like to run a Port change? (y/n) [n]") or "n"
    if selection.strip().lower() == "y":
        powersave.entrypoint()

        post_test = run(
            testscript=full_path('ping_test.py'),
            taskid="POST-TEST",
            destinations=DESTINATIONS,
            wait= True
        )
        print(message("POST-TEST", post_test))

    else:
        print("Thank you for using the app ☺️")
