#!/bin/bash
HOME_PATH=$(dirname $0)
cd $HOME_PATH/../../../
docker build . -t viraweb123/gpost

docker run -it --rm \
  --name postfix \
  -p 1587:587 \
  -p 8000:8000 \
  -v $OME_PATH/spool:/var/spool/postfix \
	-v $OME_PATH/postfix:/etc/postfix \
	-v $OME_PATH/opendkim:/etc/opendkim/keys \
  -e TZ="Europe/Amsterdam" \
  -e LOG_FORMAT=plain \
  -e ALLOWED_SENDER_DOMAINS=example.org \
  -e INBOUND_DEBUGGING=yes \
  -e POSTFIX_myhostname=localhost \
  -e POSTFIX_message_size_limit=26214400 \
  -e POSTFIX_inet_interfaces=all \
  -e POSTFIX_mynetworks_style=subnet \
  -e POSTFIX_mynetworks=10.1.2.0/24,192.168.88.0/24,172.17.0.0/24 \
  viraweb123/gpost
