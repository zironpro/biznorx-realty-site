# Dokploy builds this from the repo: no build step on the server, just Nginx serving site/ on port 80.
# (The pages in site/ are generated locally with `python3 build.py` and committed.)
FROM nginx:1.27-alpine
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY site /usr/share/nginx/html
EXPOSE 80
