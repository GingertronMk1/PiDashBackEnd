"""
This is a module that creates a basic Flask application.
This application is an API that feeds a generic frontend, giving
information about the device that it is on (designed for a Raspberry Pi)
"""
import json
import re
import os

import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import psutil
import requests
# install python-dotenv
from dotenv import load_dotenv
from typing import List

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

argument_param = 'arguments'


def obj_to_dict(obj):
  return {
          item: str(getattr(obj, item))
                for item
                in dir(obj)
                if not item.startswith('__')
        }

@app.get('/cpu')
def get_cpu():
    """
    get_cpu is called when the user sends a GET request to the /cpu endpoint.

    Returns:
    string:the cpu percentages
    """
    cpu_percents = psutil.cpu_percent(percpu=True)
    return cpu_percents

@app.get('/processes')
def get_processes(arguments):
    args_decoded = json.loads(arguments)
    processes = psutil.process_iter(args_decoded)
    process_dict = [p.info for p in processes];
    return process_dict


@app.get('/memory')
def get_memory():
    """
    get_memory is called when the user sends a GET request to the /memory endpoint.

    Returns:
    string:the various memory statistics as recorded by psutil
    """
    return obj_to_dict(psutil.virtual_memory())


@app.get('/disk')
def get_disk():
    """
    Called when the user GETs /disk

    Returns a list of disk usage statistics per mountpoint
    """
    partitions = psutil.disk_partitions()
    disks = {
        path.mountpoint: obj_to_dict(psutil.disk_usage(path.mountpoint))
        for path
        in partitions
    }
    return disks

@app.get('/temperatures')
def get_temperatures():
    """
    Called when the user GETs /temperatures

    Returns:
    string:the various temperature statistics as recorded by psutil
    """
    # {'cpu_thermal': [shwtemp(label='', current=83.82, high=None, critical=None)]}

    return { k: obj_to_dict(v[0]) for (k, v) in psutil.sensors_temperatures().items() }


@app.get('/transmission')
def get_transmission(fields):
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
    fields_decoded = json.loads(fields)
    url = "http://"
    url += os.getenv("RPC_USERNAME")
    url += ":"
    url += os.getenv("RPC_PASSWORD")
    url += "@localhost:9091/transmission/rpc"

    init_req = requests.get(url)
    pattern = re.compile(r"X-Transmission-Session-Id: (.*?)<\/")
    match = pattern.search(init_req.text)

    headers = {"X-Transmission-Session-Id": match.group(1)}
    torrents_req = requests.post(
        url,
        json={
            "method": "torrent-get",
            "arguments": {
              "fields": fields_decoded
            }
        },
        headers=headers
    )
    return json.loads(torrents_req.text)

# main driver function
if __name__ == '__main__':
    uvicorn.run("main:app")
