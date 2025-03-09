def on_message(client, userdata, message): # Функция, вызываемая во время получения сообщения
    global led
    global devicesPWM
    global devices
    global auto
    global isAuto
    print(message.payload.decode())
    # Настройка светодиодной ленты
    if message.topic == topics["get"]["ledSetting"]:
        print("Смена настроек светодиодной ленты")
        led = json.loads(message.payload.decode())
        with open("led.json", "w") as file:
            json.dump(json.loads(message.payload.decode()), file)
    # настройка PWM
    elif message.topic == topics["get"]["DevicesPWM"]:
        print("Смена настроек устройств")
        devicesPWM = json.loads(message.payload.decode())
        with open("devicesPWM.json", "w") as file:
            json.dump(devicesPWM, file)
    # Настройка состояния устройств
    elif message.topic == topics["get"]["DevicesOnOff"]:
        print("Смена состояния устройств")
        if isAuto == False:
            devoces = json.loads(message.payload.decode())
            with open("devicesonoff.json", "w") as file:
                json.dump(devoces, file)
    # Настройка автоуправления
    elif message.topic == topics["get"]["autoSettings"]:
        print("Смена настроек автоуправления")
        auto = json.loads(message.payload.decode())
        with open("auto.json", "w") as file:
            json.dump(auto, file)
    # Включение/выключение автоуправления
    elif message.topic == topics["get"]["isauto"]:
        isAuto = json.loads(message.payload.decode())["isauto"]
        with open("isAuto.json", "w") as file:
            json.dump({"isauto":isAuto}, file)
    # Иначе
    else:
        print(message.topic)

def on_connect(client, userdata, flags, rc): # Функция, вызываемая во время успешного подключения
    global flag_connected
    for topic in topics["get"].values():
        client.subscribe(topic)
        print(topic)
    flag_connected = 1

def on_disconnect(client, userdata, rc):
    global flag_connected
    flag_connected = 0

def sendData():
    while True:
        if flag_connected == 1:
            data = greenHouse.getData()
            client.publish(topics["send"]["sendData"], json.dumps(data))
        time.sleep(settings["sendPer"])

def sendDev():
    while True:
        greenHouse.setDev()
        time.sleep(settings["devPer"])

import paho.mqtt.client as mqtt
import json
import time
import threading
import hard
from flask import Flask, request, render_template

with open("topics.json") as json_file:
    topics = json.load(json_file)
with open("led.json") as json_file:
    led = json.load(json_file)
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
app = Flask(__name__)
@app.route("/")
def rootW():
    return "Это главная страница"

@app.route("/settings")
def settingsW():
    return render_template("test.html", name = "test")
    # return "Это страница настроек"


client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect
# client.user_data_set("sadfuhoiuhdfgiudpsifg/testdev", "2578fb4240bfebcfbcdb")
client.username_pw_set(username="GreenHouse/greenhouse", password="79f117d5ec61a7d431aa")
client.connect("tdolimpiada.hub.greenpl.ru", 1888)

devThread = threading.Thread(target=sendDev)
mqttThread = threading.Thread(target=sendData)
webThread = threading.Thread(target=app.run, args=("0.0.0.0",))

devThread.start()
mqttThread.start()
webThread.start()

client.loop_forever()