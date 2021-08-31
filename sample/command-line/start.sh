#!/bin/sh
cd $(dirname $0)/../../
docker build . -t boky/postfix && \
docker run -it --rm --name postfix -p 1587:587 $* boky/postfix
