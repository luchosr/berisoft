#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@name: mq135.py - MQ-135 GAS SENSOR WITH ADC MCP3008
@disclaimer: Copyright 2020, VASS GROUP - Delivery Cross - Tech Brewery
@lastrelease:  26/01/2021 00:00
"""

"""

Class for MQ135 gas sensor | MCP 3008 (Analog-to-Digital Converter for Raspberry Pi), based on the module of adaFruit

They are used in air quality control equipments for buildings/offices, are suitable for detecting of NH3, NOx, alcohol, Benzene, smoke, CO2, etc
In this first version only air quality measured in ppm , the normal range are between 35 - 60

"""

import time
import os
import RPi.GPIO as GPIO


class MQ135(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.DEBUG = 1

        # from the # SPI port on the ADC to the Cobbler
        self.SPICLK = 18
        self.SPIMISO = 23
        self.SPIMOSI = 24
        self.SPICS = 25
        # 10k trim pot connected to adc #0
        self.sensor_adc = 0
        # set up the SPI interface pins
        GPIO.setup(self.SPIMOSI, GPIO.OUT)
        GPIO.setup(self.SPIMISO, GPIO.IN)
        GPIO.setup(self.SPICLK, GPIO.OUT)
        GPIO.setup(self.SPICS, GPIO.OUT)

    def __readadc__(self):

        if ((self.sensor_adc > 7) or (self.sensor_adc < 0)):
            return -1

        GPIO.output(self.SPICS, True)
        GPIO.output(self.SPICLK, False)  # start clock low
        GPIO.output(self.SPICS, False)  # bring CS low

        commandout = self.sensor_adc
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3  # we only need to send 5 bits here

        for i in range(5):
            if (commandout & 0x80):
                GPIO.output(self.SPIMOSI, True)
            else:
                GPIO.output(self.SPIMOSI, False)

            commandout <<= 1

            GPIO.output(self.SPICLK, True)
            GPIO.output(self.SPICLK, False)

        adcout = 0

        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):

            GPIO.output(self.SPICLK, True)
            GPIO.output(self.SPICLK, False)

            adcout <<= 1

            if (GPIO.input(self.SPIMISO)):
                adcout |= 0x1

        GPIO.output(self.SPICS, True)

        adcout >>= 1  # first bit is 'null' so drop it

        return adcout

    # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    # This method return a JSON with all the indicators
    def get_read(self):
        read_pin = self.__readadc__()
        iso = time.ctime()
        json_body = [{
            "measurement": "Air_Quality",
            "tags": {
                "host": "Rasp_ZERO_0",
                "region": "es-ES",
                "sensor": "MQ135"},
            "time": iso,
            "fields": {
                "ppm": read_pin}}]
        return json_body

    # Getter for concentration
    def get_ppm(self):
        read_pin = self.__readadc__()
        return read_pin

