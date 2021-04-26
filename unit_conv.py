#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 08:58:50 2020

@author: jp

Unit conversion for experiment monitoring with Arduino.

Takes lab measurement data (analog voltages) in a list, converts each entry
to corresponding unit and returns them along with the raw data as a list of
dictionaries to be stored in a database.
"""


def unit_conv(analog_signals):
    """ Convert measurement data in list of floats from Arduino to
    corresponding units."""

    # Local imports:
    from filter_past_spikes import SpikeFilter

    """ ---------- USER INPUT: Measurements ---------- """

    # Create list to hold all measurements:
    conv_measurements = []

    # Lab temperature:
    lab_temp = {}
    conv_measurements.append(lab_temp)
    lab_temp['measurement'] = 'lab_temperature'
    lab_temp['unit'] = '°C'
    lab_temp['arduino_analog_in'] = 1
    lab_temp['function'] = lambda v: \
        (10.888 - (((-10.888)**2 + 4 * 0.00347 * (1777.3 - v * 1e3)) **
                   (1/2))) / (2 * (-0.00347)) + 30

    # Science Chamber Vacuum:
    sc_vac = {}
    conv_measurements.append(sc_vac)
    sc_vac['measurement'] = 'sc_vac'
    sc_vac['unit'] = 'mbar'
    sc_vac['arduino_analog_in'] = 2
    sc_vac['function'] = lambda v: 10**(v - 11.5)

    """ ---------- Conversion ---------- """

    for measurement in conv_measurements:
        measurement['raw'] = analog_signals[measurement['arduino_analog_in']]
        # Check for numerical errors in raw data:
        if SpikeFilter.is_inbounds(measurement['raw'], 0, 3.3):
            measurement['value'] = measurement['function'](measurement['raw'])
        else:
            measurement['value'] = None

    return conv_measurements


if __name__ == '__main__':

    from eth_com import rcv_meas
    analog_signals = rcv_meas()
    conv_measurements = unit_conv(analog_signals)
    print(conv_measurements)
