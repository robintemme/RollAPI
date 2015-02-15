#!/usr/bin/env python

from flask import Flask
app = Flask(__name__)

from serial import Serial
port = Serial("/dev/ttyAMA0", baudrate = 57600) # timeout?

from Adafruit_DHT import DHT11, read_retry
sensor = DHT11
pin = 24

@app.route("/")
def hello():
    return "It works!"

@app.route("/dht")
def dht():
    humidity, temperature = read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        return "Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity)
    else:
        return "Failed to get reading. Try again!"


@app.route("/stop", methods = ['GET', 'POST', 'PUT', 'DELETE'])
def stop():
    # send "0"
    # NOTHALT (all methods allowed)
    port.write("0")
    return "True"


@app.route("/all/up", methods = ['POST'])
def all_up():
    # send "1"
    port.write("1")
    return "True"

@app.route("/all/down", methods = ['POST'])
def all_down():
    # send "2"
    port.write("2")
    return "True"


@app.route("/door/up", methods = ['POST'])
def door_up():
    # send "3"
    port.write("3")
    return "True"

@app.route("/door/down", methods = ['POST'])
def door_down():
    # send "4"
    port.write("4")
    return "True"


@app.route("/window/up", methods = ['POST'])
def window_up():
    # send "5"
    port.write("5")
    return "True"

@app.route("/window/down", methods = ['POST'])
def window_down():
    # send "6"
    port.write("6")
    return "True"

@app.route("/window/bit", methods = ['POST'])
def window_bit():
    # send "7"
    port.write("7")
    # just a bit up
    return "True"


if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True, port = 54321)