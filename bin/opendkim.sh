#!/bin/sh

noop() {
    echo "Fail to start opendkim, starting a noop loop"
    while true; do
        sleep infinity || sleep 2147483647
    done
}

mkdir -p /etc/opendkim
touch /etc/opendkim/TrustedHosts
touch /etc/opendkim/KeyTable
touch /etc/opendkim/SigningTable

if [ ! -d /etc/opendkim/keys ]; then
    noop
elif [ -z "$(find /etc/opendkim/keys -type f ! -name .)" ]; then
    noop
else
    /usr/sbin/opendkim -D -f -x /etc/opendkim/opendkim.conf
fi


