#!/bin/bash

# Stop and remove existing containers
docker compose down -v

# Start fresh containers and run tests
docker compose up --build --force-recreate test
