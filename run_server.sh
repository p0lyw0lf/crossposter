#!/usr/bin/env bash

# Enter the venv
NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
source .venv/bin/activate

# Rebuild static files
cd server
pnpm i
pnpm build

# Run the server
cd ..
sanic server
