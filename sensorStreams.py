#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@name: config.py - Configuration File
@disclaimer: Copyright 2020, VASS GROUP - Delivery Cross - Tech Brewery
@lastrelease:  26/01/2021 00:00
"""

import time
import config
import requests
import json

# Import the libraries for each sensor
from sensors.bmp180 import BMP180
from sensors.dth11 import DTH11
from sensors.mq135 import MQ135

# Use read_retry method. This will retry up to 15 times to
# get a sensor reading (waiting 2 seconds between each retry).
while True:

    # Get Unix timestamp
    timestamp = int(time.time())

    # Json open
    build_json = {
        "iot2tangle": [],
        "device": str(config.device_id),
        "timestamp": str(timestamp)
    }

    # If DHT11
    if config.dth11:
        sensor = DTH11()
        build_json['iot2tangle'].append({
            "sensor": "DHT11 - Environmental",
            "data": [{
                "Temp": str(sensor.get_temperature())
            }, {
                "Humidity": str(sensor.get_humidity())
            }]
        })

    # If MQ135
    if config.mq135:
        sensor = MQ135()
        build_json['iot2tangle'].append({
            "sensor": "MQ135 - Enviromental",
            "data": [{
                "PPM": str(sensor.get_ppm())
            }]
        })

    # If BMP180
    if config.bmp180:
        sensor = BMP180()
        build_json['iot2tangle'].append({
            "sensor": "BMP180-Enviromental",
            "data": [{
                "Pressure": str(sensor.get_pressure()),
                "Temp": str(sensor.get_temperature())
            },{
                "Altitude": str(sensor.get_altitude())
            }]
        })

    # Set Json headers
    headers = {"Content-Type": "application/json"}

    # Send Data to Json server
    try:
        build_json = json.dumps(build_json)
        r = requests.post(config.endpoint, data=build_json, headers=headers)
        r.raise_for_status()
        print(":: Sending datasets ::")
        print("--------------------------------------------------------")
        print(build_json)

    except:

        print("No server listening at " + str(config.endpoint))

        # Interval
        time.sleep(config.relay)
