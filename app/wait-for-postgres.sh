#!/bin/sh

set -e

host="$1"

shift

until pg_isready -h "$host" -p 5432; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - running DB init"
python scripts/init_db.py

>&2 echo "Starting app with: $@"
exec "$@"
