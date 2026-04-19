#!/bin/bash
set -e

sleep 5

alembic upgrade head

exec python -m app.main
