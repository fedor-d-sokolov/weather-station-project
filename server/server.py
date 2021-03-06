# -*- coding: utf-8 -*-

import flask
import config
import math


app = flask.Flask(__name__)
last_received_data = "No data is gained yet :("

def get_dew_point_c(t_air_c, rel_humidity):
    A = 17.27
    B = 237.7
    alpha = ((A * t_air_c) / (B + t_air_c)) + math.log(rel_humidity / 100.0)
    return (B * alpha) / (A - alpha)


@app.route('/webhook', methods=['GET'])
def webhook():
    global last_received_data
    dht_22_temperature = flask.request.args.get('dht_22_temperature')
    dht_22_humidity = flask.request.args.get('dht_22_humidity')
    bmp_280_temperature = flask.request.args.get('bmp_280_temperature')
    bmp_280_pressure = flask.request.args.get('bmp_280_pressure')

    last_received_data = ""
    last_received_data += f"*Current wether in {config.settings['LOCATION']}:*\n"
    last_received_data += f"β’ Temperatureπ‘: {dht_22_temperature} β\n"
    last_received_data += f"β’ Humidity π§: {dht_22_humidity}%\n"

    pressure = float(bmp_280_pressure) * 0.00750062
    dew_point = get_dew_point_c(float(dht_22_temperature), float(dht_22_humidity))

    last_received_data += f"β’ Pressure β: {pressure} MMHG\n"

    if pressure <= 710:
        last_received_data += f"β’ Current weather β: storm\n"
    elif pressure <= 740:
        last_received_data += f"β’ Current weather π¨: rain\n"
    elif pressure <= 760:
        last_received_data += f"β’ Current weather β: alternating weather\n"
    elif pressure <= 775:
        last_received_data += f"β’ Current weather π: clear\n"
    else:
        last_received_data += f"β’ Current weather π: dry\n"

    if dew_point > 25:
        last_received_data += f"β’ Dew point: {dew_point} β (potential danger)\n"
    elif dew_point > 20:
        last_received_data += f"β’ Dew point: {dew_point} β (may be feeling sick)\n"
    else:
        last_received_data += f"β’ Dew point: {dew_point} β\n"


    return {200:"success"}

def start():
    print("Starting 'Flask' server at port 1337...")

    app.run(host="0.0.0.0", port=1337, debug=False)