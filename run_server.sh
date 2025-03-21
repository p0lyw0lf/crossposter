#!/usr/bin/env bash
# Rebuild static files
cd server
pnpm i
pnpm build
cd ..
# Run the server
source .venv/bin/activate
sanic server
