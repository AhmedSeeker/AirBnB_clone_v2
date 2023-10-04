#!/usr/bin/env bash
# Bash script that sets up a web servers for the deployment of web_static
if [ "$(dpkg -l | grep -c 'ii  nginx  ')" -eq 0 ]; then
	sudo apt-get update
	sudo apt-get install nginx -y
fi
mkdir -p /data/web_static/releases/test/

echo "\
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > index.html

mv index.html /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
ln -sf /data/web_static/releases/test /data/web_static/current
chown -R ubuntu:ubuntu /data/

link="/etc/nginx/sites-available/default"
sed -i "\%^\tlocation / %i\\\tlocation /hbnb_static/ { alias /data/web_static/current/; }\n" $link

service nginx restart
