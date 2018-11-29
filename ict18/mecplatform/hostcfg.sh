#!/bin/bash


sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 1883 -j DNAT --to 10.76.20.241:1883