from flask import Flask, render_template
import serial


arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
app = Flask(__name__)


@app.route('/cmd/<c>')
def cmd(c):
   arduino.write(c.encode())
   return "OK"


@app.route('/')
def home():
   return """
   <h1>Robot Controller</h1>
   <button onclick="fetch('/cmd/F')">Forward</button>
   <button onclick="fetch('/cmd/B')">Backward</button>
   <button onclick="fetch('/cmd/L')">Left</button>
   <button onclick="fetch('/cmd/R')">Right</button>
   <button onclick="fetch('/cmd/S')">Stop</button>
   """


app.run(host='0.0.0.0', port=5000)
