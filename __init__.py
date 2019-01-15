import sqlite3 as sql
import json
from flask import Flask, render_template, request,jsonify
import serial
app = Flask(__name__)
ser = ""
try:
    ser = serial.Serial('/dev/ttyACM0',timeout=1)
except:
    ser = serial.Serial('/dev/ttyACM1',timeout=1)
@app.route('/',methods = ['GET'])
def helloRover():
    return 'Welcome to rover'

@app.route('/getData', methods = ['GET'])
def getData():
    con = sql.connect("/var/www/rover/sensordata.db")
    cur = con.cursor()
    newData = {}
    data = cur.execute("select * from readings where ind = 1")
    for row in data:
        newData = {'temperature' : row[1], 'humidity' : row[2],'danger' : str(ser.readlines())}
    #newData = str(ser.readlines())
    return jsonify(newData)

@app.route('/putData',methods = ['GET'])
def putData():
    direction = request.args.get('direction')
    if direction == 'forward':
        ser.write(b'1')
    if direction == 'backward':
        ser.write(b'2')
    if direction == 'right':
        ser.write(b'5')
    if direction == 'straight':
        ser.write(b'4')
    if direction == 'left':
        ser.write(b'3')
    return direction

    