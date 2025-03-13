#!/usr/bin/env bash
# Rebuild static files
cd server
npm i
npm run build
cd ..
# Run the server
source .venv/bin/activate
../infrastructure/with_secret_env.sh ../infrastructure/secret.env -- sanic server
