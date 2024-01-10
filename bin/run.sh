#!/usr/bin/env bash
set -e

. /usr/bin/common.sh
. /usr/bin/common-run.sh

# Print startup banner
announce_startup

# Check if we need to configure the container timezone
setup_timezone

# Setup rsyslog output format
rsyslog_log_format

# Copy over files from /etc/postfix.template to /etc/postfix, 
# if the user mounted the folder manually
setup_conf

# Make and reown /var/spool/postfix/ folders
reown_folders

# Upgrade old coniguration, replace "hash:" and "btree:" databases to "lmdb:"
postfix_upgrade_conf

# Disable SMTPUTF8, because libraries (ICU) are missing in alpine
postfix_disable_utf8

# Update aliases database. It's not used, but postfix complains if the .db file is missing
postfix_create_aliases

# Disable local mail delivery
postfix_disable_local_mail_delivery 

# Don't relay for any domains
postfix_disable_domain_relays

# Increase the allowed header size, the default (102400) is quite smallish
postfix_increase_header_size_limit

# Restrict the size of messages (or set them to unlimited)
postfix_restrict_message_size

# Reject invalid HELOs
postfix_reject_invalid_helos

# Set up host name
postfix_set_hostname

# Set TLS level security for relays
postfix_set_relay_tls_level

# (Pre) Setup XOAUTH2 authentication
postfix_setup_xoauth2_pre_setup

# Setup a relay host, if defined
postfix_setup_relayhost

# (Post) Setup XOAUTH2 autentication
postfix_setup_xoauth2_post_setup

# Set MYNETWORKS
postfix_setup_networks

# Enable debugging, if defined
postfix_setup_debugging

# Configure allowed sender domains
postfix_setup_sender_domains

# Load virtual
postfix_setup_virtual_mailbox_domains
postfix_setup_virtual_alias_maps
postfix_setup_virtual_mailbox_maps

# Setup masquaraded domains
postfix_setup_masquarading

# Enable SMTP header checks, if defined
postfix_setup_header_checks

# Configure DKIM, if enabled
postfix_setup_dkim

# Apply custom postfix settings
postfix_custom_commands

# Apply custom OpenDKIM settings
opendkim_custom_commands

# Enable the submission port
postfix_open_submission_port

# Execute any scripts found in /docker-init.db/
execute_post_init_scripts

# Remove environment variables that contains sensible values (secrets) that are read from conf files
unset_sensible_variables

notice "Starting: ${emphasis}rsyslog${reset}, ${emphasis}postfix${reset}$DKIM_ENABLED"
exec supervisord \
  -c /etc/supervisord.conf
