import board
import busio

import adafruit_ads1x15.ads1115 as AD
from adafruit_ads1x15.analog_in import AnalogIn

import adafruit_dht

class ADS:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = AD.ADS1115(self.i2c)
        self.channel0 = AnalogIn(self.ads, AD.P0)
        self.channel1 = AnalogIn(self.ads, AD.P1)
        self.channel2 = AnalogIn(self.ads, AD.P2)
        self.channel3 = AnalogIn(self.ads, AD.P3)

    def read(self):
        try:
            return [{"value":self.channel0.value,
                     "voltage":self.channel0.voltage},
                    {"value":self.channel1.value,
                     "voltage":self.channel1.voltage},
                    {"value":self.channel2.value,
                     "voltage":self.channel2.voltage},
                    {"value":self.channel3.value,
                     "voltage":self.channel3.voltage},
                    False]
        except OSError:
            return [{"value": -17,
                     "voltage": -17},
                    {"value": -17,
                     "voltage": -17},
                    {"value": -17,
                     "voltage": -17},
                    {"value": -17,
                     "voltage": -17},
                    True]

class DHT:
    def __init__(self, pin):
        self.pin = pin
        self.dht = adafruit_dht.DHT22(self.pin)

    def read(self):
        try:
            return {"temp": self.dht.temperature, "hum": self.dht.humidity, "error": False}
        except RuntimeError:
            return {"temp": -17, "hum": -17, "error": True}

class DS:
    def __init__(self, address):
        self.address = address

    def read(self):
        try:
            with open(f"/sys/bus/w1/devices/{self.address}/temperature") as file:
                return {"temp": int(file.read().rstrip())/1000, "error": False}
        except:
            return {"temp": -17, "error": True}

