#!/bin/sh
/usr/sbin/postfix -c /etc/postfix start-fg | \
fgrep -v 'connect from localhost[127.0.0.1]'
fgrep -v 'lost connection after EHLO from localhost[127.0.0.1]' | \
fgrep -v 'disconnect from localhost[127.0.0.1] ehlo=1 commands=1'
