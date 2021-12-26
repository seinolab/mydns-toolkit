#!/bin/bash

URL="https://www.mydns.jp/directedit.html"
AUTH=`head -c -1 /root/.mydns | base64`

  env \
| grep ^CERTBOT \
| sed -e 's/$/"/' -e 's/^/-d "/' -e '$ a -d EDIT_CMD=DELETE' \
| xargs curl -X POST -d @- -H "Authorization: Basic ${AUTH}" -s -i ${URL} \
| head -1 \
| sed -e "s/^/DELETE ${CERTBOT_DOMAIN} - /" \
| logger -t MyDNS
