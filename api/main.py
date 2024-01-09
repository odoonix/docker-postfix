#!/usr/bin/env python3

import uvicorn

from typing import Union
from fastapi import FastAPI

import config
import allowed_senders

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
