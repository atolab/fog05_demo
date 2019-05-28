#!/bin/bash

PROF=$1
lxc launch images:alpine/3.6 rnis -p $PROF
sleep 1;
lxc exec rnis -- apk update
lxc exec rnis -- apk add tshark iw python3
lxc exec rnis -- pip3 install paho-mqtt

lxc file push ./templates/rnis webui/etc/init.d/rnis
lxc file push ./templates/rnis.py webui/root/rnis.py
lxc file push ./templates/run.sh webui/root/run.sh

lxc exec rnis -- chmod +x /etc/init.d/rnis
lxc exec rnis -- rc-update add rnis

lxc stop rnis
lxc publish rnis --alias rnisimg
lxc image export rnisimg rnis
lxc image delete rnisimg
lxc delete rnis