#!/bin/bash
set -e

postfix_gen_pgsql_config(){
	local content="
pgsql_virtual_alias_maps.cf:
user     = postfix
password = password
hosts    = localhost
dbname   = postfix
query    = SELECT goto FROM alias WHERE address='%s' AND active = 't'

pgsql_virtual_alias_domain_maps.cf:
user     = postfix
password = password
hosts    = localhost
dbname   = postfix
query    = SELECT goto FROM alias,alias_domain WHERE alias_domain.alias_domain = '%d' and alias.address = '%u' || '@' || alias_domain.target_domain AND alias.active='t' AND alias_domain.active='t'

pgsql_virtual_alias_domain_catchall_maps.cf:
user     = postfix
password = password
hosts    = localhost
dbname   = postfix
query    = SELECT goto FROM alias,alias_domain WHERE alias_domain.alias_domain = '%d' and alias.address = '@' || alias_domain.target_domain AND alias.active='t' AND alias_domain.active='t'

pgsql_virtual_domains_maps.cf:
user     = postfix
password = password
hosts    = localhost
dbname   = postfix
query    = SELECT domain FROM domain WHERE domain='%s' AND active = 't'

pgsql_virtual_mailbox_maps.cf:
user     = postfix
password = password
hosts    = localhost
dbname   = postfix
query    = SELECT maildir FROM mailbox WHERE username='%s' AND active = 't'

pgsql_virtual_alias_domain_mailbox_maps.cf:
user     = postfix
password = password
hosts    = localhost
dbname   = postfix
query    = SELECT maildir FROM mailbox,alias_domain WHERE alias_domain.alias_domain = '%d' and mailbox.username = '%u'|| '@' || alias_domain.target_domain AND mailbox.active='t' AND alias_domain.active='t'

pgsql_relay_domains.cf:
user     = postfix
password = password
hosts    = localhost
dbname   = postfix
query    = SELECT domain FROM domain WHERE domain='%s' AND active = 't' AND (transport LIKE 'smtp%%' OR transport LIKE 'relay%%')

pgsql_transport_maps.cf:
user     = postfix
password = password
hosts    = localhost
dbname   = postfix
query    = SELECT transport FROM domain WHERE domain='%s' AND active = 't'


pgsql_virtual_mailbox_limit_maps.cf:
user     = postfix
password = password
hosts    = localhost
dbname   = postfix
query    = SELECT quota FROM mailbox WHERE username='%s' AND active = 't'


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

postfix_set_db_pgsql_config() {
	# We are using proxy map
	# see https://www.postfix.org/proxymap.8.html

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

	local tmpdir="/etc/postfix/sql"
	mkdir --parents "$tmpdir"
	chown root: "$tmpdir"
	if [[ ! -d "$tmpdir" ]]; then
		error "Impossible to create folder $tmpdir."
		exit 123
	fi

	info "Generating PgSQL DB configuration"
	postfix_gen_pgsql_config
	info "Setting Postfix Virtual configuration for PgSQL DB"
	postfix_set_db_pgsql_config
}

   
