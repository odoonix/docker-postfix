#!/bin/bash
set -e

postfix_gen_mysql_config(){
	local content="
mysql_virtual_alias_maps.cf:
user = postfix
password = password
hosts = localhost
dbname = postfix
query = SELECT goto FROM alias WHERE address='%s' AND active = '1'
#expansion_limit = 100

mysql_virtual_alias_domain_maps.cf:
user = postfix
password = password
hosts = localhost
dbname = postfix
query = SELECT goto FROM alias,alias_domain WHERE alias_domain.alias_domain = '%d' and alias.address = CONCAT('%u', '@', alias_domain.target_domain) AND alias.active='1' AND alias_domain.active='1'

mysql_virtual_alias_domain_catchall_maps.cf:
# handles catch-all settings of target-domain
user = postfix
password = password
hosts = localhost
dbname = postfix
query  = SELECT goto FROM alias,alias_domain WHERE alias_domain.alias_domain = '%d' and alias.address = CONCAT('@', alias_domain.target_domain) AND alias.active='1' AND alias_domain.active='1'

mysql_virtual_domains_maps.cf:
user = postfix
password = password
hosts = localhost
dbname = postfix
query          = SELECT domain FROM domain WHERE domain='%s' AND active = '1'
#query          = SELECT domain FROM domain WHERE domain='%s'
#optional query to use when relaying for backup MX
#query           = SELECT domain FROM domain WHERE domain='%s' AND backupmx = '0' AND active = '1'
#optional query to use for transport map support
#query           = SELECT domain FROM domain WHERE domain='%s' AND active = '1' AND NOT (transport LIKE 'smtp%%' OR transport LIKE 'relay%%')
#expansion_limit = 100

mysql_virtual_mailbox_maps.cf:
user = postfix
password = password
hosts = localhost
dbname = postfix
query           = SELECT maildir FROM mailbox WHERE username='%s' AND active = '1'
#expansion_limit = 100

mysql_virtual_alias_domain_mailbox_maps.cf:
user = postfix
password = password
hosts = localhost
dbname = postfix
query = SELECT maildir FROM mailbox,alias_domain WHERE alias_domain.alias_domain = '%d' and mailbox.username = CONCAT('%u', '@', alias_domain.target_domain) AND mailbox.active='1' AND alias_domain.active='1'

mysql_relay_domains.cf:
user = postfix
password = password
hosts = localhost
dbname = postfix
query = SELECT domain FROM domain WHERE domain='%s' AND active = '1' AND (transport LIKE 'smtp%%' OR transport LIKE 'relay%%')

mysql_transport_maps.cf:
user = postfix
password = password
hosts = localhost
dbname = postfix
query = SELECT transport FROM domain WHERE domain='%s' AND active = '1'

mysql_virtual_mailbox_limit_maps.cf:
user = postfix
password = password
hosts = localhost
dbname = postfix
query = SELECT quota FROM mailbox WHERE username='%s' AND active = '1'
"
	local map_files=$(echo "$content" | sed -n '/^mysql.*cf:/ s/://p')
	for file in $map_files ; do
		debug "Writing MySQL config: $file"
		(echo "$content" | sed -n "/$file:/,/^$/ p" | sed "
				1d ; # filename
				s/^user =.*/user = $POSTFIX_DB_USER/ ;
				s/^password =.*/password = $POSTFIX_DB_PASSWORD/ ;
				s/^hosts =.*/hosts = $POSTFIX_DB_HOST/ ;
				s/^dbname =.*/dbname = $POSTFIX_DB_NAME/ ;
			"
		) > "/etc/postfix/sql/$file"
	done

	debug "MySQL config files have been written to $tmpdir."
	debug "Please check their content."
}



postfix_gen_pgsql_config(){
	local content="
pgsql_virtual_alias_maps.cf:
user = postfix
password = password
hosts = localhost
dbname = postfix
query = SELECT goto FROM alias WHERE address='%s' AND active = 't'
#expansion_limit = 100

pgsql_virtual_alias_domain_maps.cf:
user = postfix
password = password
hosts = localhost
dbname = postfix
query = SELECT goto FROM alias,alias_domain WHERE alias_domain.alias_domain = '%d' and alias.address = '%u' || '@' || alias_domain.target_domain AND alias.active='t' AND alias_domain.active='t'

pgsql_virtual_alias_domain_catchall_maps.cf:
# handles catch-all settings of target-domain
user = postfix
password = password
hosts = localhost
dbname = postfix
query  = SELECT goto FROM alias,alias_domain WHERE alias_domain.alias_domain = '%d' and alias.address = '@' || alias_domain.target_domain AND alias.active='t' AND alias_domain.active='t'

pgsql_virtual_domains_maps.cf:
user = postfix
password = password
hosts = localhost
dbname = postfix
query          = SELECT domain FROM domain WHERE domain='%s' AND active = 't'
#query          = SELECT domain FROM domain WHERE domain='%s'
#optional query to use when relaying for backup MX
#query           = SELECT domain FROM domain WHERE domain='%s' AND backupmx = 'f' AND active = 't'
#optional query to use for transport map support
#query           = SELECT domain FROM domain WHERE domain='%s' AND active = 't' AND NOT (transport LIKE 'smtp%%' OR transport LIKE 'relay%%')
#expansion_limit = 100

pgsql_virtual_mailbox_maps.cf:
user = postfix
password = password
hosts = localhost
dbname = postfix
query           = SELECT maildir FROM mailbox WHERE username='%s' AND active = 't'
#expansion_limit = 100

pgsql_virtual_alias_domain_mailbox_maps.cf:
user = postfix
password = password
hosts = localhost
dbname = postfix
query = SELECT maildir FROM mailbox,alias_domain WHERE alias_domain.alias_domain = '%d' and mailbox.username = '%u'|| '@' || alias_domain.target_domain AND mailbox.active='t' AND alias_domain.active='t'

pgsql_relay_domains.cf:
user = postfix
password = password
hosts = localhost
dbname = postfix
query = SELECT domain FROM domain WHERE domain='%s' AND active = 't' AND (transport LIKE 'smtp%%' OR transport LIKE 'relay%%')

pgsql_transport_maps.cf:
user = postfix
password = password
hosts = localhost
dbname = postfix
query = SELECT transport FROM domain WHERE domain='%s' AND active = 't'


pgsql_virtual_mailbox_limit_maps.cf:
user = postfix
password = password
hosts = localhost
dbname = postfix
query = SELECT quota FROM mailbox WHERE username='%s' AND active = 't'


"
	local map_files=$(echo "$content" | sed -n '/^pgsql.*cf:/ s/://p')
	for file in $map_files ; do
		debug "Writing PGSQL config: $file"
		(echo "$content" | sed -n "/$file:/,/^$/ p" | sed "
				1d ; # filename
				s/^user =.*/user = $POSTFIX_DB_USER/ ;
				s/^password =.*/password = $POSTFIX_DB_PASSWORD/ ;
				s/^hosts =.*/hosts = $POSTFIX_DB_HOST/ ;
				s/^dbname =.*/dbname = $POSTFIX_DB_NAME/ ;
			"
		) > "/etc/postfix/sql/$file"
	done
	debug "PostgreSQL config files have been written to $tmpdir."
	debug "Please check their content."
}


postfix_set_db_mysql_config() {
	do_postconf -e "virtual_mailbox_domains=\
	proxy:mysql:/etc/postfix/sql/mysql_virtual_domains_maps.cf"
	do_postconf -e "virtual_alias_maps =\
	proxy:mysql:/etc/postfix/sql/mysql_virtual_alias_maps.cf,\
	proxy:mysql:/etc/postfix/sql/mysql_virtual_alias_domain_maps.cf,\
	proxy:mysql:/etc/postfix/sql/mysql_virtual_alias_domain_catchall_maps.cf"
	do_postconf -e "virtual_mailbox_maps =\
	proxy:mysql:/etc/postfix/sql/mysql_virtual_mailbox_maps.cf,\
	proxy:mysql:/etc/postfix/sql/mysql_virtual_alias_domain_mailbox_maps.cf"
}

postfix_set_db_pgsql_config() {
	do_postconf -e "virtual_mailbox_domains=\
	proxy:pgsql:/etc/postfix/sql/pgsql_virtual_domains_maps.cf"
	do_postconf -e "virtual_alias_maps =\
	proxy:pgsql:/etc/postfix/sql/pgsql_virtual_alias_maps.cf,\
	proxy:pgsql:/etc/postfix/sql/pgsql_virtual_alias_domain_maps.cf,\
	proxy:pgsql:/etc/postfix/sql/pgsql_virtual_alias_domain_catchall_maps.cf"
	do_postconf -e "virtual_mailbox_maps =\
	proxy:pgsql:/etc/postfix/sql/pgsql_virtual_mailbox_maps.cf,\
	proxy:pgsql:/etc/postfix/sql/pgsql_virtual_alias_domain_mailbox_maps.cf"
}

postfix_set_proxy_config(){
	info "Generating DB queries"
	if [[ -z "$POSTFIX_DB_TYPE" ]]; then
		POSTFIX_DB_TYPE="pgsql"
	fi

	local tmpdir="/etc/postfix/sql"
	mkdir --parents "$tmpdir"
	chown root: "$tmpdir"
	if [[ ! -d "$tmpdir" ]]; then
		error "Impossible to create folder $tmpdir."
		exit 123
	fi

	case "$POSTFIX_DB_TYPE" in
		pgsql)
			info "Generating PgSQL DB configuration"
			postfix_gen_pgsql_config
			info "Setting Postfix Virtual configuration for PgSQL DB"
			postfix_set_db_pgsql_config
			;;
		mysql)
			info "Generating MySQL DB configuration"
			postfix_gen_mysql_config
			info "Setting Postfix Virtual configuration for PgSQL DB"
			postfix_set_db_mysql_config
			;;
		*)
			error "The DB type is not supported: $POSTFIX_DB_TYPE"
			exit 1
			;;
	esac

}

   
