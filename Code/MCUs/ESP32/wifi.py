import network


def connect_to_wifi_router():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Niloofar Khanoom 2G', "I'mAnAsshole!")
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
