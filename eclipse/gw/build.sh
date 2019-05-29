#!/bin/bash

lxc launch images:alpine/3.6 gw

lxc exec gw -- apk update
lxc exec gw -- apk add dnsmasq awall


lxc file push ./templates/interfaces gw/etc/network/interfaces
lxc file push ./templates/mec-gw.conf gw/etc/dnsmasq.d/
lxc file push ./templates/dnsmasq.hosts gw/etc/dnsmasq.hosts
lxc file push ./templates/mec-gw.json gw/etc/awall/optional/

lxc exec gw -- awall enable mec-gw
lxc exec gw -- sh -c "yes | awall activate"

lxc exec gw -- rc-update add iptables
lxc exec gw -- rc-update add dnsmasq

lxc stop gw
lxc publish gw --alias gwimg
lxc image export gwimg gw
lxc image delete gwimg
lxc delete gw
