# Crossposter

This is a project I've made to crosspost things between Discord, Mastodon, and
my own blog! Very custom-made, just like
[p2_tagging](https://github.com/p0lyw0lf/p2_tagging) I don't really recommend
using it unless ur me :)

## Usage

1. Send a message in Discord in a channel where the bot has read permissions
2. Copy the message ID and use the `/repost` slash command to post it to all
   configured platforms.

## Platforms

### Mastodon

TODO: what API keys are needed and what does the setup process look like?

### GitHub

TODO: what API keys are needed and what does the setup process look like?

## Running

After configuring the platforms above into the `secrets.toml` file, also put in
the Discord bot keys into the file. Then, run:

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m bot
```

and that's it! enjoy :)))

## Code Structure

* `bot/`: Code for the Discord bot
* `poster/`: Code for all the crossposting targets
    * `mastodon/`: The mastodon target
    * `github/`: The github target
    * `target.py`: Class definition for a valid target
    * `model.py`: Data model
* `shared/`: Shared utility code
    * `secrets.py`: Utilities for reading secrets
* `scripts/`: Scripts to test things out

Because of the module structure, everything needs to be run with `python -m` to
work correctly. Bit weird but u get used to it!
