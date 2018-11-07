#!/bin/bash

#sudo killall wpa_supplicant
#sudo killall wpa_cli

sudo wpa_supplicant -B -i wlan1 -c /home/pi/fos/cyclone/tests/5gcity/wpa_supplicant.conf -dd
sudo dhclient -v wlan1

python3 /home/pi/fos/cyclone/tests/5gcity/sensor.py
