#!/bin/sh
AP=ap.pid
function stop() {
    # kill -9 $(cat $AP)
    echo "Killing..."
}

trap stop SIGINT

DIR=$(dirname $(realpath $0))
cd $DIR
#kill -9 $(cat $AP)
IFACE="wlx74da381ab4d4"
MEPLATFORM_ID="1"
PLATFORM="172.16.123.10"
APP="rnis.py"

export MEPLATFORM_ID
export PLATFORM

ip link set $IFACE down
iw dev $IFACE set monitor otherbss
ip link set $IFACE up

#hostapd -B -P ap.pid /etc/hostapd/hostapd.conf

FIELDS="-e wlan.sa -e wlan_radio.channel -e wlan_radio.signal_dbm -e wlan_radio"
tshark -l -i $IFACE -E separator=, -T fields $FIELDS | python3 $APP