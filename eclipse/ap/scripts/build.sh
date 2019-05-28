#!/bin/bash

WFACE=$1

lxc profile copy default ap_p
lxc profile device add ap_p $WFACE nic nictype=physical parent=$WFACE

echo $WFACE | xargs -i sed -i -e "s/wlan/{}/g" ../templates/interfaces

lxc launch images:alpine/3.9 ap -p ap_p

lxc exec ap -- apk update
lxc exec ap -- apk upgrade

lxc exec ap -- apk add hostapd dnsmasq bridge
lxc exec ap -- rc-update add hostapd
lxc exec ap -- rc-update add dnsmasq

lxc file push ../templates/interfaces ap/etc/network/interfaces
lxc file push ../templates/hostapd.conf ap/etc/hostapd/hostapd.conf
lxc file push ../templates/mec-gw.conf ap/etc/dnsmasq.d/mec-gw.conf


