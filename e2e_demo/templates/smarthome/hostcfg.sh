#!/bin/bash


sudo iptables -t nat -A PREROUTING -i ens2 -p tcp --dport 8080 -j DNAT --to  10.170.163.136:8080
