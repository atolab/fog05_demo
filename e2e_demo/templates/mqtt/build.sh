#!/bin/bash


apk update
apk upgrade
apk add awall
apk add mosquitto
#copy interfaces in /etc/network
#copy fos-gw.conf in /etc/dnsmasq.d/
#copu fos-gw.json in /etc/awall/optional/

rc-update add mosquitto
reboot