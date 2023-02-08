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

import logging
import time
from pyats import aetest, topology


logger = logging.getLogger(__name__)

__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"
__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"

class CommonSetup(aetest.CommonSetup):
    '''
    Common setup tasks - this class is instantiated only once per testscript.
    '''
    @aetest.subsection
    def mark_tests_for_looping(self, testbed):
        '''
        Each iteration of the marked Testcase will be passed the parameter
        "device" with the current device from the testbed.
        '''
        aetest.loop.mark(PingTestcase, device=testbed)


class PingTestcase(aetest.Testcase):
    '''
    Simple Testcase for checking connectivity from the network devices.
    '''
    @aetest.setup
    def connect(self, device):
        '''
        Setup method to connect to the device.
        '''
        device.connect(log_stdout=False, learn_hostname=True)

    @aetest.test
    def ping(self, steps, device, destinations, wait=False):
        '''
        Simple ping test: using pyats API "ping", try pinging each of the IP addresses
        in the destinations tuple. If the ping is successful, the test step is marked passed,
        but if the ping is unsuccesful, the step is marked as failed.
        '''
        for destination in destinations:
            with steps.start(
                f"Checking Ping from {device.hostname} to {destination}", continue_=True
                ) as step:
                for i in range(1,8):
                    try:
                        ping = device.ping(destination)
                    except:
                        if wait==False or i==7:
                            step.failed(f'Ping {destination} from device {device.hostname} unsuccessful')
                        else:
                            logger.info(f'{i}/7 try failed.')
                            logger.info('Waiting 30 seconds.')
                            time.sleep(30)
                    else:
                        step.passed(f'Ping {destination} from device {device.hostname} successful')

    @aetest.cleanup
    def disconnect(self, device):
        device.disconnect()


if __name__ == "__main__":
    print(f"\n{'* '*11}*")
    print("* STARTING PING TEST  *")
    print(f"{'* '*11}*\n")

    my_testbed = "testbed.yaml"
    my_destinations = ('208.67.222.222', '173.30.1.1', '2001:4860:4860::8888')
    testbed = topology.loader.load(my_testbed)
    ping_test = aetest.main(
                            testable=__name__,
                            testbed=testbed,
                            destinations=my_destinations
                        )
