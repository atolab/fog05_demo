import paho.mqtt.client as mqtt
import random
import time
import grovepi
import threading
SERVER = "139.162.144.10"
SENSOR = 2
LIGHT = 6
L_SENSOR = 2


def sensor_read(client):
    while True:
        grovepi.dht(2, 0)
        [t, h] = grovepi.dht(2, 1)
        #l = random.randint(1, 100)
        l = grovepi.analogRead(L_SENSOR)
        # 10000.0/pow(((1023.0-a)*10.0/a)*15.0,4.0/3.0)
        #t = random.randint(1,300)/10
        #h = random.randint(1,100)
        print('Read Light {} Temperature {} Humidity {}'.format(l, t, h))
        client.publish("booth/demo/tmp", t)
        client.publish("booth/demo/lsensor", l)
        client.publish("booth/demo/hum", h)
        time.sleep(1)


def on_connect(client, userdata, flags, rc):
    print("Connected to server!\n")
    client.subscribe("booth/demo/light")


def on_message(client, userdata, msg):
    print("{}".format(int(msg.payload)))
    data = int(msg.payload)
    if data == 1:
        grovepi.digitalWrite(LIGHT, 1)
    if data == 0:
        grovepi.digitalWrite(LIGHT, 0)


def main():
    client = mqtt.Client()
    flag = False
    while not flag:
        try:
            client.connect(SERVER, 1883, 60)
            flag = True
        except OSError as e:
            print('Server not yet available sleeping before retring\n')
            flag = False
            time.sleep(2)

    read_th = threading.Thread(target=sensor_read, args=(client,))
    read_th.setDaemon(True)
    read_th.start()
    client.on_connect = on_connect
    client.on_message = on_message
    # client.message_callback_add("#",on_message)
    client.loop_forever()
    # while True:
    #t = random.randint(0,400)/10
    #h = random.randint(0,100)

    #    grovepi.dht(2,0)
    #    [t,h]=grovepi.dht(2,1)
    #    client.publish("booth/demo/tmp",t)
    #    client.publish("booth/demo/hum",h)
    #    time.sleep(1)
    #    client.loop_misc()


if __name__ == '__main__':
    main()
