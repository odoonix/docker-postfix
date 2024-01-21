#!/usr/bin/env bash
set -e

if [ -f /path/to/file ]; then
  python3 /api/init.py
fi

exec supervisord \
  -c /etc/supervisord.conf
