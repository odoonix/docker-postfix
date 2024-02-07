import uvicorn

from typing import Union
from fastapi import FastAPI, Response

import allowed_senders
import virtual_mailbox_domains
import virtual_alias_maps
import virtual_mailbox_maps
import opendkim

import prometheus_client
import time

app = FastAPI(
    # debug=False,
    # title="GPost API",
    # description="Mail API",
    # version="0.1.0",
    # root_path="",
)

start_time = time.time()

##########################################################################
# definding prometheus metrics
##########################################################################
get_counter= prometheus_client.Counter("get_counter","number of times get request was sent")
post_counter = prometheus_client.Counter("post_counter","number of times post request was sent")
delete_counter = prometheus_client.Counter("delete_counter","number of times delete request was sent")
new_allowed_senders = prometheus_client.Gauge("new_allowed_senders","numbr of new allowed senders")
new_virtual_alias_maps = prometheus_client.Gauge("new_virtual_alias_maps","numbr of new virtual alias maps")
new_virtual_mailbox_maps = prometheus_client.Gauge("new_virtual_mailbox_maps","numbr of new virtual mailbox maps")
new_dkim = prometheus_client.Gauge("new_dkim","numbr of new dkim")
proccess_time = prometheus_client.Summary("time_of_proccessing_eveything","the whole time of proccessing")


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
def read_allowed_senders():
    get_counter.inc()
    return allowed_senders.get_domains()

@app.post("/allowed_senders")
def write_allowed_senders(domain: allowed_senders.AllowdDomain):
    post_counter.inc()
    new_allowed_senders.inc()
    return allowed_senders.add_domain(domain)

@app.delete("/allowed_senders")
def write_allowed_senders(domain: allowed_senders.AllowdDomain):
    delete_counter.inc()
    new_allowed_senders.dec()
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
def read_virtual_alias_maps():
    get_counter.inc()
    return virtual_alias_maps.get_virtual_alias_maps()

@app.post("/virtual_alias_maps")
def write_virtual_alias_maps(virtual_alias_map: virtual_alias_maps.VirtualAliasMaps):
    post_counter.inc()
    new_virtual_alias_maps.inc()
    return virtual_alias_maps.add_virtual_alias_map(virtual_alias_map)

@app.delete("/virtual_alias_maps")
def write_virtual_alias_maps(virtual_alias_map: virtual_alias_maps.VirtualAliasMaps):
    delete_counter.inc()
    new_virtual_alias_maps.dec()
    return virtual_alias_maps.remove_virtual_alias_map(virtual_alias_map)

##########################################################################
# virtual_mailbox_maps
##########################################################################
@app.get("/virtual_mailbox_maps")
def read_virtual_mailbox_maps():
    get_counter.inc()
    return virtual_mailbox_maps.get_virtual_mailbox_maps()

@app.post("/virtual_mailbox_maps")
def write_virtual_mailbox_maps(virtual_mailbox_map: virtual_mailbox_maps.VirtualMailboxMaps):
    post_counter.inc()
    new_virtual_mailbox_maps.inc()
    return virtual_mailbox_maps.add_virtual_mailbox_map(virtual_mailbox_map)

@app.delete("/virtual_mailbox_maps")
def write_virtual_mailbox_maps(virtual_mailbox_map: virtual_mailbox_maps.VirtualMailboxMaps):
    delete_counter.inc()
    new_virtual_mailbox_maps.inc()
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
def read_dkim(name:str):
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
    get_counter.inc()
    
    return opendkim.get_dkim(name)

@app.post("/dkim/{name}")
def generate_dkim(name):
    post_counter.inc()
    new_dkim.inc()
    return read_dkim(name)

@app.delete("/opendkim/{name}")
def delete_dkim(name):
    """
    Remove the DKIM both public and private key.

    Parameters
    -------------------
    name: str
        The domain, which must be one othe allowed one.
    """
    # TODO: maso, 2024: check if the domain is allowed to send
    delete_counter.inc()
    new_dkim.dec()
    return opendkim.remove_dkim(name)


##########################################################################
# prometheus metrics
##########################################################################
@app.get('/metrics')
def get_metrics():
    proccess_time.observe(time.time() - start_time)
    return Response(
        media_type = "text/plain",
        content = prometheus_client.generate_latest(),
    )
