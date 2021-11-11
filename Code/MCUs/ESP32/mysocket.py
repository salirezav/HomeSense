import socket

class sock:
    isConnected = False
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, ip="192.168.0.109", port=12345, deviceName="NONAME"):
        print("inside init", ip, port, deviceName)
        self.ip = ip
        self.port = port
        self.deviceName = deviceName

    def establish(self):
        print("inside establish")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr_info = socket.getaddrinfo(self.ip,  self.port)
        self.addr = self.addr_info[0][-1]
        try:
            self.client_socket.connect(self.addr)
            myname = f"Device: {self.deviceName}"
            # self.send(myname)
            print("connected!")
            self.isConnected = True
            return True
        except Exception as e:
            print(str(e))
            self.isConnected = False
            return False

        
    def send(self, data):
        if not self.isConnected:
            self.establish()
        try:
            # print("data to be sent: ", data)
            self.client_socket.send(str(data).encode())
            self.terminate()
        except Exception as e:
            print(str(e))
        finally:
            # self.terminate()
            pass

    def terminate(self):
        self.client_socket.close()
