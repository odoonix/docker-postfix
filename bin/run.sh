#!/usr/bin/env bash
set -e



rsyslog_log_format() {
	local log_format="${LOG_FORMAT}"
	if [[ -z "${log_format}" ]]; then
		log_format="plain"
	fi
	sed -i -E "s/<log-format>/${log_format}/" /etc/rsyslog.conf
}


setup_timezone() {
	if [ ! -z "$TZ" ]; then
		TZ_FILE="/usr/share/zoneinfo/$TZ"
		if [ -f "$TZ_FILE" ]; then
			ln -snf "$TZ_FILE" /etc/localtime
			echo "$TZ" > /etc/timezone
		fi
	fi
}

# TODO: must update map files
postmap lmdb:/etc/postfix/aliases
postmap lmdb:/etc/postfix/allowed_senders
postmap lmdb:/etc/postfix/smtpd_milter_map
postmap lmdb:/etc/postfix/virtual_alias_maps
postmap lmdb:/etc/postfix/virtual_mailbox_domains
postmap lmdb:/etc/postfix/virtual_mailbox_maps

# TODO: maso, 2024: check if file exist and dns lookup work
# SEE
# https://serverfault.com/questions/1003885/postfix-in-docker-host-or-domain-name-not-found-dns-and-docker
cp /etc/resolv.conf /var/spool/postfix/etc/

setup_timezone
rsyslog_log_format
exec supervisord \
  -c /etc/supervisord.conf
