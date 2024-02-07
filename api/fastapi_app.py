import uvicorn

from typing import Union
from fastapi import FastAPI, Response

import allowed_senders
import virtual_mailbox_domains
import virtual_alias_maps
import virtual_mailbox_maps
import opendkim

import metrics


app = FastAPI(
    # debug=False,
    # title="GPost API",
    # description="Mail API",
    # version="0.1.0",
    # root_path="",
)


##########################################################################
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

##########################################################################
# Allowed domains
##########################################################################


@app.get("/allowed_senders")
@metrics.inc('get')
def read_allowed_senders():
    return allowed_senders.get_domains()


@app.post("/allowed_senders")
@metrics.inc('post', 'new_allowed_senders')
def write_allowed_senders(domain: allowed_senders.AllowdDomain):
    return allowed_senders.add_domain(domain)


@app.delete("/allowed_senders")
@metrics.inc('delete')
@metrics.dec('new_allowed_senders')
def write_allowed_senders(domain: allowed_senders.AllowdDomain):
    return allowed_senders.remove_domain(domain)


'''
##########################################################################
# virtual_mailbox_domains
##########################################################################
@app.get("/virtual_mailbox_domains")
def read_virtual_mailbox_domains():
    return virtual_mailbox_domains.get_domains()

@app.post("/virtual_mailbox_domains")
def write_virtual_mailbox_domains(domain: allowed_senders.AllowdDomain):
    return virtual_mailbox_domains.add_domain(domain)

@app.delete("/virtual_mailbox_domains")
def write_virtual_mailbox_domains(domain: allowed_senders.AllowdDomain):
    return virtual_mailbox_domains.remove_domain(domain)
'''
##########################################################################
# virtual_alias_maps
##########################################################################


@app.get("/virtual_alias_maps")
@metrics.inc('get')
def read_virtual_alias_maps():
    return virtual_alias_maps.get_virtual_alias_maps()


@app.post("/virtual_alias_maps")
@metrics.inc('post', 'virtual_alias_maps')
def write_virtual_alias_maps(virtual_alias_map: virtual_alias_maps.VirtualAliasMaps):
    return virtual_alias_maps.add_virtual_alias_map(virtual_alias_map)


@app.delete("/virtual_alias_maps")
@metrics.inc('delete')
@metrics.dec('virtual_alias_maps')
def write_virtual_alias_maps(virtual_alias_map: virtual_alias_maps.VirtualAliasMaps):
    return virtual_alias_maps.remove_virtual_alias_map(virtual_alias_map)

##########################################################################
# virtual_mailbox_maps
##########################################################################


@app.get("/virtual_mailbox_maps")
@metrics.inc('get')
def read_virtual_mailbox_maps():
    return virtual_mailbox_maps.get_virtual_mailbox_maps()


@app.post("/virtual_mailbox_maps")
@metrics.inc('post', 'virtual_mailbox_maps')
def write_virtual_mailbox_maps(virtual_mailbox_map: virtual_mailbox_maps.VirtualMailboxMaps):
    return virtual_mailbox_maps.add_virtual_mailbox_map(virtual_mailbox_map)


@app.delete("/virtual_mailbox_maps")
@metrics.inc('delete')
@metrics.dec('virtual_mailbox_maps')
def write_virtual_mailbox_maps(virtual_mailbox_map: virtual_mailbox_maps.VirtualMailboxMaps):
    return virtual_mailbox_maps.remove_virtual_mailbox_map(virtual_mailbox_map)


##########################################################################
# OpenDKIM
#
# OpenDKIM is a community effort to develop and maintain a C library for
# producing DKIM-aware applications and an open source milter for
# providing DKIM service.
#
# SEE: http://www.opendkim.org/
##########################################################################
@app.get("/dkim/{name}")
@metrics.inc('get')
def read_dkim(name: str):
    """
    Load the DKIM (Public key or DNS value) from the domain.

    If the DKIM does not created, then create a new one and return it as 
    the resut.

    NOTE: the private key is a secure data and must keep at the server 
          storage for ever.

    Parameters
    -------------------
    domain: str
        The domain, which must be one othe allowed one.
    """
    # TODO: maso, 2024: check if the domain is allowed to send
    return opendkim.get_dkim(name)


@app.post("/dkim/{name}")
@metrics.inc('post', 'dkim')
def generate_dkim(name):
    return read_dkim(name)


@app.delete("/opendkim/{name}")
@metrics.inc('delete')
@metrics.dec('dkim')
def delete_dkim(name):
    """
    Remove the DKIM both public and private key.

    Parameters
    -------------------
    name: str
        The domain, which must be one othe allowed one.
    """
    # TODO: maso, 2024: check if the domain is allowed to send
    return opendkim.remove_dkim(name)


##########################################################################
# prometheus metrics
##########################################################################
@app.get('/metrics')
@metrics.time('uptime', 'x')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=metrics.generate_latest(),
    )
