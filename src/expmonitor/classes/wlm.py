#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thur Jun 13 17:29:00 2024

@author: tc
"""

# Local imports:
from expmonitor.classes.sensor import Sensor
from expmonitor.classes.network_com.network_com import NetworkCom

class WLM(Sensor):

    def __init__(self, descr, port):
        # General sensor setup:
        self.type = 'Wavelength Meter'
        self.descr = descr.replace(' ', '_').lower() # Multi-word
        self.unit = 'THz'
        self.conversion_fctn = lambda t: t # no conversion
        self.port = port
        super().__init__(
            self.type, self.descr, self.unit, self.conversion_fctn, num_prec=6
            )
        # wavelength logger specifi:
        self.network_com = NetworkCom(self.port)

    def connect(self):
        """Open the connection to the wavemeter server."""
        self.network_com.connect()

    def disconnect(self):
        """Close the connection to the wavemeter server."""
        self.network_com.disconnect()

    def rcv_vals(self):
        """Receive and return measurement values from wavemeter server."""
        return self.network_com.measure()


# Execution:
if __name__ == '__main__':

    from expmonitor.config import *
    WLM.test_execution()
