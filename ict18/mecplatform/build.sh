#!/bin/bash



lxc launch images:alpine/edge mecplatform
lxc exec mecplatform -- apk update
lxc exec mecplatform -- apk upgrade
lxc exec mecplatform -- apk add mosquitto
lxc exec mecplatform -- rc-update add mosquitto
lxc exec mecplatform -- halt
sleep 10
lxc publish mecplatform --alias platform
lxc image export platform ./platform
lxc image delete platform
lxc delete mecplatform