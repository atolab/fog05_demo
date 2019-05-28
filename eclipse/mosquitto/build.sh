#!/bin/bash

lxc launch images:alpine/3.6 mosquitto

lxc exec mosquitto -- apk update
lxc exec mosquitto -- apk add mosquitto


lxc file push ./templates/interfaces mosquitto/etc/network/interfaces

lxc exec mosquitto -- rc-update add mosquitto

lxc stop mosquitto
lxc publish mosquitto --alias mosquittoimg
lxc image export mosquittoimg mosquitto
lxc image delete mosquittomg
lxc delete mosquitto
