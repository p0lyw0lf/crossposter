#!/usr/bin/env bash
cd bot
exec $HOME/.local/bin/hatch run -- python -m src.bot
