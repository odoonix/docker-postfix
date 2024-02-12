import os

import utils.storage as storage
import utils.linux as linux



# Return a DKIM selector from DKIM_SELECTOR environment variable.
# See README.md for detais.
def _get_dkim_selector(domain):
    """
    DKIM selector is an string used with in DNS to find out currect
    private key.

    You may set different selector fo a domain with:

    DKIM_SELECTOR: mail=example.com default=example.org _mail=myname.com

    This function check if you define a selector for a domain
    """
    # No settings for selectors
    if not 'DKIM_SELECTOR' in os.environ:
        return "mail"
	
    # check if there is a setting for selector
    no_domain_selector="mail"
    selector_value = os.environ['DKIM_SELECTOR']
    selectors = selector_value.split(',')
    for part in selectors:
        if '=' in part:
            items = part.split('=')
            if items[0] == domain:
                return items[1]
        else:
            no_domain_selector=part
    return no_domain_selector


def _load_public_key(domain):
    public_path = _get_public_key_path(domain)
    with open(public_path) as file:
        dkim = file.read()
    return dkim


def _get_public_key_path(domain):
    return '{}/{}.txt'.format(storage.get_dkim_path(), 
                              domain)


def _get_private_key_path(domain):
    return '{}/{}.private'.format(storage.get_dkim_path(), 
                                  domain)


def generate_dkim(domain,
                  append_domain = False,
                  bits=2048,
                  note=None,
                  selector = None,
                  hash_algorithms = 'rsa-sha256',
                  subdomains = True,
                  restrict=True,
                  testmode=False,
                  directory='/tmp'):

    if not selector:
        selector = _get_dkim_selector(domain)
    cmd = ['opendkim-genkey',
        '--bits', str(bits), 
        '--hash-algorithms', hash_algorithms,  
        '--selector', selector, 
        '--directory', directory,
        '--domain', domain]
    if note:
        cmd.append('--note')
        cmd.append(note)

    if subdomains:
        cmd.append('--subdomains')
    
    if restrict:
        cmd.append('--restrict')
    
    if testmode:
        cmd.append('--testmode')
    
    if append_domain:
        cmd.append('--append-domain')
    linux.run(cmd, cwd='/tmp')
    # Fixes https://github.com/linode/docs/pull/620
    linux.file_mv('{}/{}.private'.format(directory, selector), 
               _get_private_key_path(domain))
    linux.file_mv('{}/{}.txt'.format(directory, selector), 
               _get_public_key_path(domain))
    return _load_public_key(domain)


def get_dkim(domain):
    public_path = _get_public_key_path(domain)
    if not os.path.exists(public_path):
        return generate_dkim(domain)
    return _load_public_key(domain)


def remove_dkim(domain):
    os.remove(_get_public_key_path(domain))
    os.remove(_get_private_key_path(domain))

