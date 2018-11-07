#!/bin/bash

apt update
apt upgrade
apt install gnupg wget  -y
wget -qO - 'https://bintray.com/user/downloadSubjectPublicKey?username=openhab' | sudo apt-key add -
sudo apt-get install apt-transport-https -y
echo 'deb https://dl.bintray.com/openhab/apt-repo2 stable main' | sudo tee /etc/apt/sources.list.d/openhab2.list 
sudo apt-get update
sudo apt-get install openhab2 -y 
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable openhab2.service


#copy demo.sitemap in /etc/openhab2/sitemaps
#copy *.items in /etc/openhab2/items
#copu mqtt.cfg in //etc/openhab2/services

# basic ui and mqtt binding installed in openhab

reboot