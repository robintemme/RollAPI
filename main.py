#!/usr/bin/env python

from flask import Flask, render_template, redirect, request, current_app
app = Flask(__name__)

from functools import wraps
import json

from serial import Serial
port = Serial("/dev/ttyAMA0", baudrate = 57600) # timeout?

from Adafruit_DHT import DHT11, read_retry
sensor = DHT11
pin = 24

def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get("callback", False)
        if callback:
            content = str(callback) + "(" + str(f(*args,**kwargs)) + ")"
            return current_app.response_class(content, mimetype="application/javascript")
        else:
            return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def hello():
    hum, temp = raw_dht()
    return render_template("index.html", humidity = hum, temperature = temp)

@app.route("/dht")
@support_jsonp
def api_dht():
    humidity, temperature = raw_dht()
    if humidity is not None and temperature is not None:
        return '{"temperature":' + "{0:0.0f}".format(temperature) + ',"humidity":' + "{0:0.0f}".format(humidity) + '}'
    else:
        return '{"status":"Could not get reading from sensor!"}'


def raw_dht():
    return read_retry(sensor, pin)

@app.route("/stop", methods = ["POST"])
def stop():
    # send "0"
    port.write("0")
    return current_app.response_class('{ "status": "done" }', mimetype="application/json")


@app.route("/all/up", methods = ["POST"])
def all_up():
    # send "1"
    port.write("1")
    return current_app.response_class('{ "status": "done" }', mimetype="application/json")

@app.route("/all/down", methods = ["POST"])
def all_down():
    # send "2"
    port.write("2")
    return current_app.response_class('{ "status": "done" }', mimetype="application/json")


@app.route("/door/up", methods = ["POST"])
def door_up():
    # send "3"
    port.write("3")
    return current_app.response_class('{ "status": "done" }', mimetype="application/json")

@app.route("/door/down", methods = ["POST"])
def door_down():
    # send "4"
    port.write("4")
    return current_app.response_class('{ "status": "done" }', mimetype="application/json")


@app.route("/window/up", methods = ["POST"])
def window_up():
    # send "5"
    port.write("5")
    return current_app.response_class('{ "status": "done" }', mimetype="application/json")

@app.route("/window/down", methods = ["POST"])
def window_down():
    # send "6"
    port.write("6")
    return current_app.response_class('{ "status": "done" }', mimetype="application/json")

# @app.route("/window/bit", methods = ["POST"])
# def window_bit():
#     # send "7"
#     port.write("7")
#     # just a bit up
#     return


if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True, port = 54321)
