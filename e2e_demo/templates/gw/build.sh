#!/bin/bash


apk update
apk upgrade
apk add awall
awall enable fos-gw
yes | awall activate
apk add dnsmasq

#copy interfaces in /etc/network
#copy fos-gw.conf in /etc/dnsmasq.d/
#copu fos-gw.json in /etc/awall/optional/

rc-update add iptables
rc-update add dnsmasq
reboot