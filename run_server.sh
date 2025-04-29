#!/usr/bin/env bash

# Enter the venv
NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Rebuild static files
cd rc/web
pnpm i
pnpm build

# Run the server
cd ..
hatch run -- sanic src.rc
