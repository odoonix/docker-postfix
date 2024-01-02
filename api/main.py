#!/usr/bin/env python3
from typing import Union
from fastapi import FastAPI

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
