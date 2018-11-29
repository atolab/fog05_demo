#!/bin/bash


apk update
apk upgrade

#copy interfaces in /etc/network
#copy hostap.conf in /etc/hostapd/hostapd.conf

apk add hostapd dnsmasq bridge
rc-update add hostapd
rc-update add dnsmasq