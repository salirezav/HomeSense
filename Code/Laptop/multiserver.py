import urllib.request
import socket
import os
import datetime
import threading
from _thread import *
from time import sleep

host = ''
port = 12345
ThreadCount = 0
threadList = []
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IPs = ["192.168.0.100", "192.168.0.196", "192.168.0.192"]

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def write_to_file(file, data):
    ct = datetime.datetime.now()

    with open(file+".txt", 'a') as file:
        print("writing data on file")
        file.writelines(str(ct) + "\t" + data + "\n")
        print("going to close file")
        file.close()


def NewClientThread(connection):
    connection.send(str.encode('Welcome to the Servern'))
    while True:
        device = ""
        event = ""
        try:
            data = connection.recv(2048).decode()
            data = data.split("=")
            if len(data) > 1:
                print(data)
                # if device == "DEVICE A - Bed Room A"
                write_to_file(data[0], str(data[0]) +
                              " " + str(data[1]))
            connection.close()
        except Exception as e:
            # print(str(e))
            connection.close()
            break
        finally:
            connection.close()
        if not data:
            print("connection terminated")
            break

            # connection.sendall(str.encode(reply))


# DeviceName: Living Room;Light:120;temp:25;ppm:3000;
def read_values():
    while True:
        print("getting")
        for ip in IPs:
            try:
                fp = urllib.request.urlopen("http://"+ip)
                html = fp.read().decode("utf-8")
                html = html.split(";")
                deviceName = html[0].split(":")[1]
                print(deviceName)
                lightIntensity = html[1].split(":")[1]
                temperature = html[2].split(":")[1]
                humidity = html[3].split(":")[1]
                ppm = html[4].split(":")[1]
                c_ppm = html[5].split(":")[1]

                thing_to_write = f"{html[1]}\t{html[2]}\t{html[3]}\t{html[4]}\t{html[5]}"
                write_to_file(deviceName, thing_to_write)
            except Exception as e:
                pass
        sleep(60)
        


valthread = threading.Thread(target=read_values)
threadList.append(valthread)
valthread.start()


while True:
    ClientSocket, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    thread = threading.Thread(target=NewClientThread, args=(ClientSocket,))
    threadList.append(thread)
    thread.start()
    # start_new_thread(NewClientThread, (ClientSocket, ))
    # ThreadCount += 1
    # print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()
