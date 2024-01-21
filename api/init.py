
import utils.linux as linux
import utils.rsyslog as rsyslog

import postfix

def announce_startup():
    print(
        """
===========================================
  __________________               __   
 /  _____/\______   \____  _______/  |_ 
/   \  ___ |     ___/  _ \/  ___/\   __\\
\    \_\  \|    |  (  <_> )___ \  |  |  
 \______  /|____|   \____/____  > |__|  
        \/                    \/        

===========================================
"""
    )




def load_configs():
    # Print startup banner
    announce_startup()

    linux.setup_timezone()

    
    rsyslog.log_format()

    postfix.setup_conf()
    postfix.check_utf8_support()
    postfix.check_aliases()


    # Setup a relay host, if defined
    # postfix_setup_relayhost

    # (Post) Setup XOAUTH2 autentication
    # postfix_setup_xoauth2_post_setup

    # Set MYNETWORKS
    # postfix_setup_networks

    # Enable debugging, if defined
    # postfix_setup_debugging

    # Configure allowed sender domains
    # postfix_setup_sender_domains

    # Load virtual
    # postfix_setup_virtual_mailbox_domains
    # postfix_setup_virtual_alias_maps
    # postfix_setup_virtual_mailbox_maps
    # postfix_setup_aliases_maps

    # Setup masquaraded domains
    # postfix_setup_masquarading

    # Enable SMTP header checks, if defined
    # postfix_setup_header_checks

    # Configure DKIM, if enabled
    # postfix_setup_dkim

    # Apply custom postfix settings
    # postfix_custom_commands

    # Apply custom OpenDKIM settings
    # opendkim_custom_commands

    # Enable the submission port
    # postfix_open_submission_port

    # Execute any scripts found in /docker-init.db/
    # execute_post_init_scripts

    # Remove environment variables that contains sensible values (secrets) that are read from conf files
    # unset_sensible_variables

    pass


if __name__ == "__main__":
    load_configs()
