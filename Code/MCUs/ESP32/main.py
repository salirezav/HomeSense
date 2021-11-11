from wifi import connect_to_wifi_router
import socket
from machine import Pin, ADC
from time import sleep
import mysocket
from dht import DHT11
from MQ135 import *

# Defining pin numbers
PIR_PIN = 34
LIGHT_SENSOR_PIN = 35
DHT_PIN = 25
BUILT_IN_LED = 2
AIR_QUALITY_SENSOR_PIN = 39
# AIR_QUALITY_SENSOR_PIN = 32

# Laptop IP and Port
DEVICENAME = "DEVICE C - Living Room"
# DEVICENAME = "DEVICE A - Bedroom A"
# DEVICENAME = "DEVICE B - Bedroom B"
PORT = 12345
LAPTOPIP = "192.168.0.193"

# Setting up pins
led = Pin(BUILT_IN_LED, Pin.OUT)
pir = Pin(PIR_PIN, Pin.IN)
lightSensor = Pin(LIGHT_SENSOR_PIN, Pin.IN)
lightADC = ADC(lightSensor)
aqSensorPin = Pin(AIR_QUALITY_SENSOR_PIN, Pin.IN)


# Initializing objects from classes
dht11 = DHT11(Pin(DHT_PIN))
mq135 = MQ135(aqSensorPin)

# Initial values
temperature = 0.0
humidity = 0.0
motion = False
connected = False
latestError = ""

try:
    dht11.measure()
    temperature = dht11.temperature()
    humidity = dht11.humidity()
except:
    pass


connect_to_wifi_router()


# Socket connection to laptop
s = mysocket.sock(LAPTOPIP, PORT, DEVICENAME)


# Web server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('', 80))
server_socket.listen(5)

# Constructs and returns a web page


def web_page(lightValue="None", dhtValue="None", aqsensor=[]):
    global DEVICENAME
    global latestError

    html = """<html><head><title>""" + DEVICENAME+"""</title><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}</style></head><body> <h1>""" + \
        DEVICENAME+"""</h1> <p>Light: <strong>""" + lightValue + """</strong></p><p>DHT: <strong>""" + \
        dhtValue + """</strong></p><p>PPM: """ + \
        aqsensor[0]+"""</p><p>Corrected PPM:""" + \
        aqsensor[1]+"""</p></body></html>"""

    return html


# Interrupt handle for PIR motion sensor
def handle_interrupt(pin):

    # print("MOTION!!")
    s.establish()

    global motion
    motion = True
    global PIR_PIN
    global connected
    PIR_PIN = pin
    led.value(pir.value())
    value = f"{DEVICENAME}="
    value += "motion detected" if pir.value() == 1 else "motion stopped"
    try:
        # send_to_server(value)
        s.send(value)
    except Exception as e:
        print(str(e))
        print("error here")
        connected = False


# Registering interrupt for motion sensor
pir.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=handle_interrupt)


# The rest
while True:
    conn, addr = server_socket.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print("data received")
    request = str(request)
    try:
        light = 4095 - lightADC.read()
        dht11.measure()
        temperature = dht11.temperature()
        humidity = dht11.humidity()
        try:
            rzero = mq135.get_rzero()
            corrected_rzero = mq135.get_corrected_rzero(temperature, humidity)
            resistance = mq135.get_resistance()
            ppm = mq135.get_ppm()
            corrected_ppm = mq135.get_corrected_ppm(temperature, humidity)
            print("here we go")
        except Exception as e:
            print(str(e))

        # response = web_page(str(light), str(
            # str(temperature) + " ; " + str(humidity)), [str(ppm), str(corrected_ppm)])
        response = f"Device:{DEVICENAME};Light intensity:{light};Temperature:{temperature};Humidity:{humidity};PPM:{str(ppm)};Corrected PPM:{str(corrected_ppm)}"
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except Exception as e:
        print(str(e))
    finally:
        conn.close()
