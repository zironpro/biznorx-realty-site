#!/bin/sh
# Rebuild the pages and upload them to the live server:  ./deploy.sh
# Server IP lives in deploy/server-ip (one line). SSH key: ~/.ssh/biznorx_realty_vps
set -e
cd "$(dirname "$0")"
IP=$(cat deploy/server-ip)
python3 build.py
rsync -az --delete -e "ssh -i $HOME/.ssh/biznorx_realty_vps -o IdentitiesOnly=yes" site/ "root@$IP:/var/www/biznorxrealty.com/"
echo "Live: https://biznorxrealty.com"
