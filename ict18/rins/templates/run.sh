#!/bin/sh
DIR=$(dirname $(realpath $0))
cd $DIR

IFACE="wlxe84e0624c0d1"
PLATFOMR="10.100.1.215"
MEPLATFORM_ID="1"
APP="rins.py"

ip link set $IFACE down
iw dev $IFACE set monitor otherbss
ip link set $IFACE up

FIELDS="-e wlan.sa -e wlan_radio.channel -e wlan_radio.signal_dbm -e wlan_radio.
tshark -l -i $IFACE -E separator=, -T fields $FIELDS | python3 $APP