import json

class GreenHouse:
    def __init__(self, configPath):
        with open(configPath, 'r') as f:
            self.jsonConfig = json.loads(f.read())

        self.dhtInP = self.jsonConfig['dhtInP']
        self.dhtOutP = self.jsonConfig['dhtOutP']
        # self.lightInP = self.jsonConfig['lightInP']
        # self.lightOutP = self.jsonConfig['lightOutP']

        self.pump1P = self.jsonConfig['pump1P']
        self.pump2P = self.jsonConfig['pump2P']
        self.pump3P = self.jsonConfig['pump3P']

        self.lightP = self.jsonConfig['lightP']
        self.wentP = self.jsonConfig['wentP']
        self.hotP = self.jsonConfig['hotP']

        self.inTemp = None
        self.outTemp = None
        self.inHum = None
        self.outHum = None

        self.inLight = None
        self.outLight = None


    def getData(self):
        # Получить данные
        return {
            "intemp": self.inTemp,
            "outtemp": self.outTemp,
            "inhum": self.inHum,
            "outhum": self.outHum,
            "inlight": self.inLight,
            "outlight": self.outLight,
        }

    def setDev(self):
        # Установить устройства
        pass