#!/bin/sh
cd tests/unit
docker-compose up --build --abort-on-container-exit --exit-code-from tests
