#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@name: dht11.py - DTH11
@disclaimer: Copyright 2020, VASS GROUP - Delivery Cross - Tech Brewery
@lastrelease:  26/01/2021 00:00
"""

"""

Class for DTH11 , based on the module of adaFruit
This Sensor provides : Temperature and humidity

"""

import Adafruit_DHT
import time
import math

class DTH11(object):
    def __init__(self):
        self.sensor = Adafruit_DHT.DHT11
        self.pin = 21
        self.temperature = None
        self.humidity = None

    # This method return a JSON with all the indicators
    def get_read(self):
        iso = time.ctime()
        self.__get_data__()
        json_body = [{
            "measurement": "Enviroment",
            "tags": {
                "host": "Rasp_ZERO_0",
                "region": "es-ES",
                "sensor": "DTH11"},
            "time": iso,
            "fields": {
                "temperature": self.temperature,
                "humidity": self.humidity
            }}]
        return json_body

    # Getter for Temperature
    def get_temperature(self):
        self.__get_data__()
        return self.temperature

    # Getter for Humidity
    def get_humidity(self):
        self.__get_data__()
        return self.humidity

    # Read the values from the sensor
    def __get_data__(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if humidity is None or humidity == 144.0:
            print('Humidity read failed! %s' % humidity)
        else:
            self.humidity = humidity

        if temperature is None or \
                (self.temperature is not None and math.fabs(self.temperature-temperature)) > 10:
            print('Temperature read failed! %s => %s !!!' % (self.temperature, temperature))
        else:
            self.temperature = temperature
        return self.humidity, self.temperature
