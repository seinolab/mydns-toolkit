#!/bin/bash

URL="https://ipv4.mydns.jp/login.html"
AUTH=`cat /root/.mydns`

RESULT=`curl -s -S -I -u ${AUTH} ${URL} 2>&1 | head -1`
logger -t MyDNS "${URL} - $RESULT"
