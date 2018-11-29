#!/bin/bash


sudo iptables -t nat -A PREROUTING -i wlp58s0 -p tcp --dport 80 -j DNAT --to 10.67.94.233:80
sudo iptables -t nat -A PREROUTING -i wlp58s0 -p tcp --dport 8080 -j DNAT --to 10.67.94.233:8080

# sudo iptables -t nat -L --line-numbers
# sudo iptables -t nat -D PREROUTING {number-here}