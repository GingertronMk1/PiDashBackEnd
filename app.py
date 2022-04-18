import json
import re
import os

import psutil
import requests
# install python-dotenv
from dotenv import load_dotenv
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, jsonify, request

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)


load_dotenv()

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/cpu')
def get_cpu():
    cpu_percents = psutil.cpu_percent(percpu=True)
    return jsonify(cpu_percents)

@app.route('/memory')
def get_memory():
    # Calculate memory information
    memory = psutil.virtual_memory()
    return jsonify(memory)

@app.route('/disk')
def get_disk():
    partitions=psutil.disk_partitions()
    disks = {
        path.mountpoint:psutil.disk_usage(path.mountpoint)
        for path
        in partitions
    }
    return jsonify(disks)

@app.route('/temperatures')
def get_temperatures():
    return jsonify(psutil.sensors_temperatures())

@app.route('/transmission')
def get_transmission():
    url = "http://"
    url += os.getenv("RPC_USERNAME")
    url += ":"
    url += os.getenv("RPC_PASSWORD")
    url += "@localhost:9091/transmission/rpc"
    init_req = requests.get(url)
    pattern = re.compile(r"X-Transmission-Session-Id: (.*?)<\/")
    match = pattern.search(init_req.text)
    headers = { "X-Transmission-Session-Id": match.group(1) }
    arguments = json.loads(request.args.get("arguments"))
    torrents_req = requests.post(
      url,
      json={
        "method": "torrent-get",
        "arguments": arguments
      },
      headers=headers
    )
    return torrents_req.text

@app.after_request
def set_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response




# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
