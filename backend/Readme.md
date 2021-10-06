1. Bootstrap database

# Create user
...

# Create database, grant access to user
createdb btcexplore
GRANT ALL PRIVILEGES ON DATABASE btcexplore TO btcexplore;

# Grant create database so we can run tests

ALTER USER btcexplore CREATEDB;
