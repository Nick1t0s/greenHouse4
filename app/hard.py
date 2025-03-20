import json
import sensors
import board
import RPi.GPIO as GPIO
import neopixel

class GreenHouse:
    def __init__(self, configPath):
        with open(configPath, 'r') as f:
            self.jsonConfig = json.loads(f.read())

        with open("devicesonoff.json", 'r') as f:
            self.devicesOnOff = json.loads(f.read())

        GPIO.setmode(GPIO.BCM)

        self.dhtInP = board.D13
        self.dhtOutP = board.D12
        # self.lightInP = self.jsonConfig['lightInP']
        # self.lightOutP = self.jsonConfig['lightOutP']

        self.pump1P = self.jsonConfig['pump1P']
        self.pump2P = self.jsonConfig['pump2P']
        self.pump3P = self.jsonConfig['pump3P']

        self.wentP = self.jsonConfig['wentP']
        # self.hotP = self.jsonConfig['hotP']

        self.pump1State = 0;
        self.pump2State = 0;
        self.pump3State = 0;

        self.lightState = self.devicesOnOff['light']
        self.wentState = self.devicesOnOff['went']

        self.DSaddr = self.jsonConfig['DSaddr']

        try:
            self.dhtIn = sensors.DHT(self.dhtInP)
        except:
            self.dhtIn = None
        try:
            self.dhtOut = sensors.DHT(self.dhtOutP)
        except:
            self.dhtOut = None

        self.DS = sensors.DS(self.DSaddr)

        self.ADS = sensors.ADS()

        self.inTemp = None
        self.outTemp = None
        self.inHum = None
        self.outHum = None

        self.inLight = None
        self.outLight = None

        self.shTemp = None

        self.sh1 = None
        self.sh2 = None
        self.sh3 = None

        self.lent = neopixel.NeoPixel(board.D18, 30)

        GPIO.setup(self.pump1P, GPIO.OUT)
        GPIO.setup(self.pump2P, GPIO.OUT)
        GPIO.setup(self.pump3P, GPIO.OUT)

        GPIO.setup(self.wentP, GPIO.OUT)



    def getData(self):

        # Для работы с DHT
        if not (self.dhtIn is None):
            inData = self.dhtIn.read()
            self.inTemp = inData["temp"]
            self.inHum = inData["hum"]
        else:
            self.inTemp = -17
            self.inHum = -17

        if not (self.dhtOut is None):
            outData = self.dhtOut.read()
            self.outTemp = outData["temp"]
            self.outHum = outData["hum"]
        else:
            self.outTemp = -17
            self.outHum = -17


        #Для работы с DS
        self.shTemp = self.DS.read()

        #Для работы с ADS
        adsDT = self.ADS.read()
        self.sh1 = adsDT[1]["value"]
        self.sh2 = adsDT[2]["value"]
        self.sh3 = adsDT[3]["value"]
        self.outLight = adsDT[0]["value"]

        # print("Были получены данные из класса")

        return {
            "intemp": self.inTemp,
            "outtemp": self.outTemp,
            "inhum": self.inHum,
            "outhum": self.outHum,
            "outlight": self.outLight,
            "stemp": self.shTemp["temp"],
            "soilhum1": self.sh1,
            "soilhum2": self.sh2,
            "soilhum3": self.sh3,
        }

    def setDev(self):
        # Установить устройства
        GPIO.output(self.pump1P, [GPIO.LOW,GPIO.HIGH][self.pump1State])
        # print(self.pump1State)
        GPIO.output(self.pump2P, [GPIO.LOW,GPIO.HIGH][self.pump2State])
        # print(self.pump2State)
        GPIO.output(self.pump3P, [GPIO.LOW,GPIO.HIGH][self.pump3State])
        # print(self.pump3State)
        GPIO.output(self.wentP, [GPIO.LOW,GPIO.HIGH][self.wentState])

        with open("led.json") as f:
            colors = json.load(f)
            if self.lightState:
                self.lent.fill((colors["red"], colors["green"], colors["blue"]))
            else:
                self.lent.fill((0, 0, 0))
        # print(self.wentState)
        # print("Были установлены устройства")



# greenHouse = GreenHouse("pins.json")
# greenHouse.getData()