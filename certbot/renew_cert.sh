docker container stop traefik
docker run --rm -it \
  -v "/opt/docker-volumes/certbot/certs/:/etc/letsencrypt/" \
  -v "/opt/docker-volumes/certbot/logs/:/var/log/letsencrypt/" \
  -p 80:80 \
  certbot/certbot renew
docker container start traefik
