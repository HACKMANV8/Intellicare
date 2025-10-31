from flask import Flask, render_template, request, jsonify, session
import serial
import serial.tools.list_ports
import time
import json
import urllib.request
import requests
import threading
import json
import random
from googletrans import Translator
translator = Translator()


def LangTranslator(to_lang, get_sentence):
    from_lang = 'en'
    text_to_translate = translator.translate(get_sentence,src= from_lang,dest= to_lang)
    text = text_to_translate.text
    print(text)
    return text

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def GetData():
    from serial_test import ReadData
    ReadData()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan_qr')
def scan_qr():
    from reader import QRReader
    d = QRReader()
    if d == 'IntelliCare':
        return render_template('dashboard.html')
    else:
        return render_template('index.html', msg = 'Invalide QR code')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/Language/<lng>')
def Language(lng):
    f = open('language.txt', 'w')
    f.write(lng)
    f.close()
    if lng == 'kn':
        return render_template('dashboard.html', msg="Language set to Kannada")
    else:
        return render_template('dashboard.html', msg="Language set to English")

@app.route('/get_sensor_data')
def get_sensor_data():
    f = open('data.txt', 'r')
    data = f.read()
    f.close()
    data = data.split(',')
    print(data)
    f = open('language.txt', 'r')
    lang = f.read()
    f.close()

    Text = LangTranslator(lang, data[7])
    Motion = LangTranslator(lang, data[8])
    sensor_data = {
        'oxygen': int(float(data[5])),
        'blood_pressure': {
            'systolic': int(float(data[4])),
            'diastolic': int(float(data[4]))/2 + int(int(float(data[4])/2) / 2)
        },
        'flex': [int(float(data[0])), int(float(data[1])), int(float(data[2])), int(float(data[3]))],
        'temperature': int(float(data[6])),
        'notification': Text,
        'Motion': Motion
    }
    print(sensor_data)
    if data[7] != 'No commands':
        print('send notification')
    if data[8] == "Motion: Detected":
        print('send notification')
    return jsonify(sensor_data)

if __name__ == '__main__':
    t1 = threading.Thread(target = GetData)
    t1.start()
    app.run(debug=True,host="0.0.0.0")