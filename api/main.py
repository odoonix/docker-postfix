#!/usr/bin/env python3

import uvicorn
import fastapi_app


if __name__ == "__main__":
    uvicorn.run(
        fastapi_app.app,
        host="0.0.0.0",
        port=8000
    )
