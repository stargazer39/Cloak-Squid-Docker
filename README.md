# Cloak-Squid-Docker

Deploy a quick squid proxy with cloak transport..
Primarily made to work with Heroku

```bash
docker run -d -v /home/stargazer/configs/docker/cloak:/config -p 443:443 <image_name>
```

To set parameters manually make a .env file with

```bash
CK_ADMINUID=<uid>
CK_BYPASSUID=<uid>
CK_PRIVATEKEY=<private_key>
PORT=<internal_listening_port>
```
