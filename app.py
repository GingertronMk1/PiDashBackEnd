"""
This is a module that creates a basic Flask application.
This application is an API that feeds a generic frontend, giving
information about the device that it is on (designed for a Raspberry Pi)
"""
import json
import re
import os

from flask import Flask, jsonify, request
import psutil
import requests
# install python-dotenv
from dotenv import load_dotenv

# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.

# Construct a new Flask object.
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)


load_dotenv()


@app.route('/cpu')
def get_cpu():
    """
    get_cpu is called when the user sends a GET request to the /cpu endpoint.

    Returns:
    string:the cpu percentages
    """
    cpu_percents = psutil.cpu_percent(percpu=True)
    return jsonify(cpu_percents)


@app.route('/memory')
def get_memory():
    """
    get_memory is called when the user sends a GET request to the /memory endpoint.

    Returns:
    string:the various memory statistics as recorded by psutil
    """
    return jsonify(psutil.virtual_memory())


@app.route('/disk')
def get_disk():
    """
    Called when the user GETs /disk

    Returns a list of disk usage statistics per mountpoint
    """
    partitions = psutil.disk_partitions()
    disks = {
        path.mountpoint: psutil.disk_usage(path.mountpoint)
        for path
        in partitions
    }
    return jsonify(disks)


@app.route('/temperatures')
def get_temperatures():
    """
    Called when the user GETs /temperatures

    Returns:
    string:the various temperature statistics as recorded by psutil
    """
    return jsonify(psutil.sensors_temperatures())


@app.route('/transmission')
def get_transmission():
    """
    Returns a list of torrents being handled by transmission.
    This is called when the user GETs /transmission
    The function first creates a request to transmission.
    This is a GET request, and is only used to get the transmission session ID
    header that will be used in the next request.
    Once we have that header we POST to transmission to get the list of torrents.
    We pass the list of arguments we get as a GET param through, for maximum
    flexibility.
    Returns:
    string:a JSON-encoded array of torrent details
    """
    url = "http://"
    url += os.getenv("RPC_USERNAME")
    url += ":"
    url += os.getenv("RPC_PASSWORD")
    url += "@localhost:9091/transmission/rpc"

    init_req = requests.get(url)
    pattern = re.compile(r"X-Transmission-Session-Id: (.*?)<\/")
    match = pattern.search(init_req.text)

    headers = {"X-Transmission-Session-Id": match.group(1)}
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
    """
    This is maybe not the nicest way to do this, but it works.
    Set the access-control header to allow cross-origin requests.
    """
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
