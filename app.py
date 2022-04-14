import psutil
import json
import requests
import re
import os
from dotenv import load_dotenv
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, jsonify
  
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
  

load_dotenv()

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/cpu')
def getCpu():
  cpuPercents = psutil.cpu_percent(percpu=True)
  return json.dumps(cpuPercents)

@app.route('/memory')
def getMemory():
# Calculate memory information
  memory = psutil.virtual_memory()
  return jsonify(memory)

@app.route('/disk')
def getDisk():
  disks = {path.mountpoint:psutil.disk_usage(path.mountpoint) for path in psutil.disk_partitions()}
  return jsonify(disks)

@app.route('/temperatures')
def getTemperatures():
  return psutil.sensors_temperatures()

@app.route('/transmission')
def getTransmission():
  url = f"http://{os.getenv('RPC_USERNAME')}:{os.getenv('RPC_PASSWORD')}@localhost:9091/transmission/rpc"
  initReq = requests.get(url)
  pattern = re.compile("X-Transmission-Session-Id: (.*?)<\/")
  match = pattern.search(initReq.text)
  headers = { "X-Transmission-Session-Id": match.group(1) }
  torrentsReq = requests.post(
      url,
      json = {
        "method": "torrent-get",
        "arguments": {
          "fields": [
            "addedDate",
            "id",
            "name",
            "eta",
            "leftUntilDone",
            "percentDone",
            "rateDownload"
          ]
        }
      },
      headers=headers
  )
  return torrentsReq.text

@app.after_request
def set_headers(response):
  response.headers.add("Access-Control-Allow-Origin", "*")
  return response



  
# main driver function
if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
