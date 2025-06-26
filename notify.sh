#!/bin/bash

URL="https://ipv4.mydns.jp/login.html"
AUTH=$(tr -d '\n' < /root/.mydns | base64)

RESULT=`curl -s -S -I -H "Authorization: Basic ${AUTH}" ${URL} 2>&1 | head -1`
logger -t MyDNS "${URL} - $RESULT"
