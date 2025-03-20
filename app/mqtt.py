import asyncio

import paho.mqtt.client as mqtt
import json
import time
import threading
import hard
from flask import Flask, request, render_template
import neopixel

async def pump1(time):
    greenHouse.pump1State = 1
    print(f"Помпа 1 заработала {greenHouse.pump1State}")
    await asyncio.sleep(time)
    greenHouse.pump1State = 0
    print(f"Помпа 1 остановилась {greenHouse.pump1State}")

async def pump2(time):
    greenHouse.pump2State = 1
    print(f"Помпа 2 заработала {greenHouse.pump2State}")
    await asyncio.sleep(time)
    greenHouse.pump2State = 0
    print(f"Помпа 2 остановилась {greenHouse.pump2State}")

async def pump3(time):
    greenHouse.pump3State = 1
    print(f"Помпа 3 заработала {greenHouse.pump3State}")
    await asyncio.sleep(time)
    greenHouse.pump3State = 0
    print(f"Помпа 3 остановилась {greenHouse.pump3State}")

async def pumpMain(p1, p2, p3):
    task1 = asyncio.create_task(pump1(p1))
    task2 = asyncio.create_task(pump2(p2))
    task3 = asyncio.create_task(pump3(p3))

    await task1
    await task2
    await task3




def on_message(client, userdata, message): # Функция, вызываемая во время получения сообщения
    global led
    global devicesPWM
    global devices
    global auto
    global isAuto
    print(message.payload.decode())
    # Настройка светодиодной ленты
    if message.topic == "devices/greenhouse/cmds/ledsetting":
        print("Смена настроек светодиодной ленты")
        led = json.loads(message.payload.decode())
        with open("led.json", "w") as file:
            json.dump(json.loads(message.payload.decode()), file)
    # настройка PWM
    elif message.topic == "devices/greenhouse/cmds/devicespwm":
        print("Смена настроек устройств")
        devicesPWM = json.loads(message.payload.decode())
        with open("devicesPWM.json", "w") as file:
            json.dump(devicesPWM, file)
    # Настройка состояния устройств
    elif message.topic == "devices/greenhouse/cmds/devicesonoff":
        print("Смена состояния устройств")
        devoces = json.loads(message.payload.decode())
        greenHouse.lightState = devoces["light"]
        greenHouse.wentState = devoces["went"]
        with open("devicesonoff.json", "w") as file:
            json.dump(devoces, file)
    #Полив
    elif message.topic == "devices/greenhouse/cmds/pump":
        data = json.loads(message.payload.decode())
        print(data)
        asyncio.run(pumpMain(data["pump1"], data["pump2"], data["pump3"]))
    # Иначе
    else:
        print(message.topic)

def on_connect(client, userdata, flags, rc): # Функция, вызываемая во время успешного подключения
    global flag_connected
    for topic in topics["get"].values():
        client.subscribe(topic)
        print(topic)
    print("Произведено подключение")
    flag_connected = 1

def on_disconnect(client, userdata, rc):
    global flag_connected
    print("Произведено отключение")
    flag_connected = 0
# @timeOut.timeout(4)
def sendDataF():
    data = greenHouse.getData()
    client.publish(topics["send"]["sendData"], json.dumps(data))
def sendDataL():
    while True:
        print(flag_connected)
        if flag_connected == 1:
            try:
                sendDataF()
                # print("Данные отправлены")
            except Exception as e:
                print(e)
        time.sleep(settings["sendPer"])

def sendDev():
    while True:
        greenHouse.setDev()
        # print(12312)
        time.sleep(settings["devPer"])
        # print(type(flag_connected))


with open("topics.json") as json_file:
    topics = json.load(json_file)
with open("auto.json") as json_file:
    auto = json.load(json_file)
with open("devicesPWM.json") as json_file:
    devicesPWM = json.load(json_file)
with open("devicesonoff.json") as json_file:
    devices = json.load(json_file)
with open("isAuto.json") as json_file:
    isAuto = json.load(json_file)

with open("settings.json") as json_file:
    settings = json.load(json_file)

flag_connected = 0

client = mqtt.Client()
greenHouse = hard.GreenHouse("pins.json")
greenHouse.getData()
app = Flask(__name__)
@app.route("/")
def rootW():

    args = request.args.to_dict()
    if len(args) == 3 and "P1" in args:
        args["P1"] = 0 if not args["P1"].isdigit() else int(args["P1"])
        args["P2"] = 0 if not args["P2"].isdigit() else int(args["P2"])
        args["P3"] = 0 if not args["P3"].isdigit() else int(args["P3"])

        asyncio.run(pumpMain(args["P1"], args["P2"], args["P3"]))

    elif len(args) == 3 and "red" in args:
        args["red"] = int(args["red"])
        args["green"] = int(args["green"])
        args["blue"] = int(args["blue"])
        print(args)
        with open("led.json", "w") as file:
            file.write(json.dumps(args))

    print(request.url)



    data = greenHouse.getData()
    return render_template("main.html",
        inTemp = data["intemp"] if data["intemp"] != -17 else "Not connected",
        outTemp = data["outtemp"] if data["outtemp"] != -17 else "Not connected",
        inHum = data["inhum"] if data["inhum"] != -17 else "Not connected",
        outHum = data["outhum"] if data["outhum"] != -17 else "Not connected",
        light = data["outlight"] if data["outlight"] != -17 else "Not connected",
        shTemp = data["stemp"] if data["stemp"] != -17 else "Not connected",
        SH1 = data["soilhum1"] if data["soilhum1"] != -17 else "Not connected",
        SH2 = data["soilhum2"] if data["soilhum2"] != -17 else "Not connected",
        SH3 = data["soilhum3"] if data["soilhum3"] != -17 else "Not connected",)




client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect
# client.user_data_set("sadfuhoiuhdfgiudpsifg/testdev", "2578fb4240bfebcfbcdb")
client.username_pw_set(username="GreenHouse/greenhouse", password="79f117d5ec61a7d431aa")
client.connect("tdolimpiada.hub.greenpl.ru", 1888)
print("ыфавыав")

devThread = threading.Thread(target=sendDev)
mqttThread = threading.Thread(target=sendDataL)
webThread = threading.Thread(target=app.run, args=("0.0.0.0",))

devThread.start()
mqttThread.start()
webThread.start()

client.loop_forever()