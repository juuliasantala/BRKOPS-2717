'''
Simple example of a Ping testcase using pyATS.

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

from pyats import aetest, topology

__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"
__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"

class CommonSetup(aetest.CommonSetup):
    ''' Common setup tasks - this class is instantiated only once per testscript. '''

    @aetest.subsection
    def mark_tests_for_looping(self, testbed):
        '''
        Each iteration of the marked Testcase will be passed the parameter
        "device" with the current device from the testbed.
        '''
        aetest.loop.mark(PingTestcase, device=testbed)

class PingTestcase(aetest.Testcase):
    ''' Simple Testcase for checking connectivity from the network devices. '''

    @aetest.setup
    def connect(self, device):
        ''' Setup method to connect to the device. '''
        device.connect(log_stdout=False, learn_hostname=True)

    @aetest.test
    def ping(self, steps, device, destinations):
        '''
        Simple ping test: using pyats API "ping", try pinging each of the IP addresses
        in the destinations tuple. If the ping is successful, the test step is marked passed,
        but if the ping is unsuccesful, the step is marked as failed.
        '''
        for destination in destinations:
            with steps.start(
                f"Checking Ping from {device.hostname} to {destination}", continue_=True
                ) as step:
                try:
                    device.ping(destination)
                except:
                    step.failed(f'Ping {destination} from device {device.hostname} unsuccessful')
                else:
                    step.passed(f'Ping {destination} from device {device.hostname} successful')

    @aetest.cleanup
    def disconnect(self, device):
        ''' Cleanup method to disconnect from the device. '''
        device.disconnect()

if __name__ == "__main__":
    print(f"\n{'* '*11}*")
    print("* STARTING PING TEST  *")
    print(f"{'* '*11}*\n")

    my_destinations = (
        '10.105.22.34', #S1-AP4800
        '10.105.37.3', #S2-AP3800
        '10.105.0.10' #associated WLC
        )

    my_testbed = topology.loader.load("testbed.yaml")
    ping_test = aetest.main(testbed=my_testbed, destinations=my_destinations)
