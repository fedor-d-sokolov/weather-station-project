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
    last_received_data += f"• Temperature🌡: {dht_22_temperature} ℃\n"
    last_received_data += f"• Humidity 💧: {dht_22_humidity}%\n"

    pressure = float(bmp_280_pressure) * 0.00750062
    dew_point = get_dew_point_c(float(dht_22_temperature), float(dht_22_humidity))

    last_received_data += f"• Pressure ⚓: {pressure} MMHG\n"

    if pressure <= 710:
        last_received_data += f"• Current weather ⛈: storm\n"
    elif pressure <= 740:
        last_received_data += f"• Current weather 🌨: rain\n"
    elif pressure <= 760:
        last_received_data += f"• Current weather ⛅: alternating weather\n"
    elif pressure <= 775:
        last_received_data += f"• Current weather 🌞: clear\n"
    else:
        last_received_data += f"• Current weather 🏜: dry\n"

    if dew_point > 25:
        last_received_data += f"• Dew point: {dew_point} ℃ (potential danger)\n"
    elif dew_point > 20:
        last_received_data += f"• Dew point: {dew_point} ℃ (may be feeling sick)\n"
    else:
        last_received_data += f"• Dew point: {dew_point} ℃\n"


    return {200:"success"}

def start():
    print("Starting 'Flask' server at port 1337...")

    app.run(host="0.0.0.0", port=1337, debug=False)