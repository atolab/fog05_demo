#!/bin/bash

apt update
apt upgrade -y
apt install openjdk-9-jre-headless gnupg wget apt-transport-https -y
wget -qO - 'https://bintray.com/user/downloadSubjectPublicKey?username=openhab' | sudo apt-key add -
echo 'deb https://dl.bintray.com/openhab/apt-repo2 stable main' | sudo tee /etc/apt/sources.list.d/openhab2.list 
sudo apt-get update
sudo apt-get install openhab2 -y 
sudo systemctl daemon-reload
sudo /bin/systemctl enable openhab2.service


#copy demo.sitemap in /etc/openhab2/sitemaps
#copy *.items in /etc/openhab2/items
#copy mqtt.cfg in //etc/openhab2/services
# set ip address to 10.170.163.136
# basic ui and mqtt binding installed in openhab

reboot