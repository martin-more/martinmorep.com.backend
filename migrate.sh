#!/usr/bin/env bash

# Run migrate
echo "Running migrate..."
yoyo apply --database="${DATABASE_URL}" ./migrations
