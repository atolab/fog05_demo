#!/bin/bash


lxc launch images:alpine/3.6 webui

lxc exec webui -- apk update
lxc exec webui -- apk add nodejs-npm nginx nodejs
lxc exec webui -- npm install mqtt
lxc exec webui -- cp -r node_modules/ /var/www/localhost/htdocs/

lxc file push ./templates/interfaces webui/etc/network/interfaces
lxc file push ./templates/backend webui/etc/init.d/backend
lxc file push ./templates/backend.js webui/var/www/localhost/htdocs/backend.js
lxc file push -r ./templates/webui webui/var/www/localhost/htdocs/
lxc file push -r ./templates/default.conf webui/etc/nginx/conf.d/default.conf


lxc exec webui -- chmod +x /etc/init.d/backend
lxc exec webui -- rc-update add backend
lxc exec webui -- rc-update add nginx

lxc stop webui
lxc publish webui --alias webuiimg
lxc image export webuiimg webui
lxc image delete webuiimg
lxc delete webui