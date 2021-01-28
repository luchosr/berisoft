#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@name: config.py - Configuration File
@disclaimer: Copyright 2020, VASS GROUP - Delivery Cross - Tech Brewery
@lastrelease:  26/01/2021 00:00
"""

# Parameter : Device Name
# The Device name is the concatenation of the result : cat /proc/cpuinfo
# Hardware-Serial-Revision

device_id = 'BCM2835-00000000ec2a41ff-9000c1'

# Parameters : Sensors
# Select sensors to use 1 = use | 0 = skip
# DTH11 : Temperature,Humidity
# BMP180 : Temperature,Pressure,Altitude
# MQ135 : Air quality sensor based on SnO2 conductivity measurement
# TODO : include in the documentation the unit of measure for each indicator
dth11 = 0
bmp180 = 1
mq135 = 0

# TODO: next sensors to integrate
gyroscope = 0
accelerometer = 0
magnetometer = 0

# Parameters : Relay
# Select relay interval in miliseconds
relay = 180

# Parameter : endpoint
# Define endpoint for the Rust Stream Gateway
endpoint = 'http://127.0.0.1:8080/sensor_data'
