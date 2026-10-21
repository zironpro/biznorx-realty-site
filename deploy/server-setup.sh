#!/bin/sh
# One-time setup of a fresh Ubuntu VPS for biznorxrealty.com. Run as root on the server.
set -e
export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get install -y -q nginx certbot python3-certbot-nginx ufw rsync
mkdir -p /var/www/biznorxrealty.com
cp /tmp/nginx-host.conf /etc/nginx/sites-available/biznorxrealty.com
ln -sf /etc/nginx/sites-available/biznorxrealty.com /etc/nginx/sites-enabled/biznorxrealty.com
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl enable --now nginx
systemctl reload nginx
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable
echo "Server ready."
