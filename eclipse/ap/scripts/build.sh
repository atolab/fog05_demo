#!/bin/bash

PROF=$1

lxc launch images:alpine/3.6 ap -p $PROF

lxc exec ap -- apk update
lxc exec ap -- apk upgrade

lxc exec ap -- apk add hostapd bridge
# lxc exec ap -- rc-update add hostapd
# lxc exec ap -- rc-update add dnsmasq

lxc file push ../templates/interfaces ap/etc/network/interfaces
lxc file push ../templates/hostapd.conf ap/etc/hostapd/hostapd.conf
# lxc file push ../templates/mec-gw.conf ap/etc/dnsmasq.d/mec-gw.conf

lxc restart ap
