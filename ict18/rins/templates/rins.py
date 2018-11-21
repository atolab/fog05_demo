#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import random
import time
import json
import os
MEPLATFORM_ID = os.environ['MEPLATFORM_ID']
SERVER = os.environ['PLATFORM']


def on_connect(client, userdata, flags, rc):
    print("Connected to server!\n")


def on_message(client, userdata, msg):
    print("{}".format(int(msg.payload)))


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

    client.on_connect = on_connect
    client.on_message = on_message

    while True:
        line = input()
        info = line.split(',')
        if len(info) == 5:
            data = {
                'station': info[0],
                'channel': info[1],
                'dbm': info[2],
                'data-rate': info[3],
                'retries': info[4]
            }
            print('Read  {}'.format(data))
            topic = '//{}/rins'.format(MEPLATFORM_ID)
            client.publish(topic, json.dumps(data))

    '''
    tshark -l -i wlxe84e0624c0d1 -E separator=, -T fields -e wlan.sa -e wlan_rad io.channel -e wlan_radio.signal_dbm -e wlan_radio.data_rate -e wlan.fc.retry
    Capturing on 'wlxe84e0624c0d1'
    sid               ch db dr r
    e4:9e:12:12:76:50,1,-38,1,0
    '''
    client.loop_forever()


if __name__ == '__main__':
    main()
