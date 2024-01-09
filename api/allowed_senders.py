from pydantic import BaseModel
import config
import postfix

#########################################################################################
# Models
#########################################################################################
class AllowdDomain(BaseModel):
    domain: str
    allowed: bool

    def to_string(self):
        return "{domain} {state}".format(
            domain = self.domain, 
            state = "ok" if self.allowed else "cancel"
        )


#########################################################################################
# Utilities
#########################################################################################
def _store_domains(domains):
    """
    Write domains in map, then regenerate the hash map and reload teh
    postfix.
    """
    with open(config.get_allowed_senders_path(), 'w') as allowed_senders_file:
        for domain in domains:
            allowed_senders_file.write(domain.to_string())
            allowed_senders_file.write('\n')
    postfix.postmap(config.get_allowed_senders_path())
    postfix.restart()
    return True

def _load_domains():
    """
    Loads list of domains from the file
    """
    result = []
    with open(config.get_allowed_senders_path()) as allowed_senders_file:
        for line in allowed_senders_file:
            if len(line):
                items = line.split()
                result.append(AllowdDomain(
                    domain = items[0],
                    allowed = True if items[1] == 'ok' else False
                    ))
    return result


#########################################################################################
# API
#########################################################################################
def get_domains():
    return _load_domains()

def add_domain(domain):
    domains = _load_domains()
    domains.append(domain)
    _store_domains(domains)
    return True

def remove_domain(domain):
    domains = get_domains()
    domains.remove(domain)
    _store_domains(domains)