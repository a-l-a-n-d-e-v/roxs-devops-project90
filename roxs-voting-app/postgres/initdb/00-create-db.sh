#!/bin/bash
set -e

# This script will be executed when the PostgreSQL container starts
# It will be run by the postgres user with superuser privileges

# Create the votes database if it doesn't exist
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE votes;
    GRANT ALL PRIVILEGES ON DATABASE votes TO $POSTGRES_USER;
EOSQL
