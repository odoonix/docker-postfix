#!/usr/bin/env python3

import uvicorn

from typing import Union
from fastapi import FastAPI

import config
import allowed_senders
import virtual_mailbox_domains
import virtual_alias_maps
import virtual_mailbox_maps

app = FastAPI(
    # debug=False,
    # title="GPost API",
    # description="Mail API",
    # version="0.1.0",
    # root_path="",
)


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
    return allowed_senders.get_domains()

@app.post("/allowed_senders")
def write_allowed_senders(domain: allowed_senders.AllowdDomain):
    return allowed_senders.add_domain(domain)

@app.delete("/allowed_senders")
def write_allowed_senders(domain: allowed_senders.AllowdDomain):
    return allowed_senders.remove_domain(domain)


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

##########################################################################
# virtual_alias_maps
##########################################################################
@app.get("/virtual_alias_maps")
def read_virtual_alias_maps():
    return virtual_alias_maps.get_domains()

@app.post("/virtual_alias_maps")
def write_virtual_alias_maps(domain: allowed_senders.AllowdDomain):
    return virtual_alias_maps.add_domain(domain)

@app.delete("/virtual_alias_maps")
def write_virtual_alias_maps(domain: allowed_senders.AllowdDomain):
    return virtual_alias_maps.remove_domain(domain)

##########################################################################
# virtual_mailbox_maps
##########################################################################
@app.get("/virtual_mailbox_maps")
def read_virtual_mailbox_maps():
    return virtual_mailbox_maps.get_domains()

@app.post("/virtual_mailbox_maps")
def write_virtual_mailbox_maps(domain: allowed_senders.AllowdDomain):
    return virtual_mailbox_maps.add_domain(domain)

@app.delete("/virtual_mailbox_maps")
def write_virtual_mailbox_maps(domain: allowed_senders.AllowdDomain):
    return virtual_mailbox_maps.remove_domain(domain)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
