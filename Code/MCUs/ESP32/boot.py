try:
    import gc
    import usocket as socket
except:
    import socket

from machine import Pin
import network
import esp
esp.osdebug(None)
gc.collect()
