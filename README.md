# Crossposter

This is a project I've made to crosspost things between Discord, Mastodon, and
my own blog! Very custom-made, so just like all my other projects, I don't
really recommend using it unless ur me :)

## Usage

1. Send a message in Discord in a channel where the bot has read permissions
2. Copy the message ID and use the `/repost` slash command to post it to all
   configured platforms.

## Platforms

### Mastodon

In the developer settings tab, create an application and give it the
`read:statuses` and `write:statuses` permissions. Then, read the "Your Access
Token" variable and put it into `MASTODON_TOKEN` variable in `secrets.toml`.

Also, provide the following environment variables:
* `MASTODON_BASE_URL`: the URL of the server the app is registered in

To edit the post layout, see `poster/templates/post.txt.j2`. This is laid out
using jinja2 templating from the model in `shared/model.py`.

### GitHub

[Create a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
and put in in the `GITHUB_TOKEN` variable in `secrets.toml`. If creating a
fine-grained token, make sure to give it access to the repository you want to
crosspost to. Specifically, give it read-write access in the following
categories:
* Contents

What this target will do is, for a given post, create a commit adding the post
file to the main branch. This assumes that the branch has a automatic deploy
action set on push already.

Additionally, configure the following variables in `secrets.toml`:
* `GITHUB_USERNAME`: the owner of the repository
* `GITHUB_REPO`: the repository name
* `GITHUB_BRANCH`: the branch to add posts to automatically
* `GITHUB_OUTPUT_DIR`: the directory to output posts to

And edit `post.mdx.j2` as desired. It uses jinja2 formatting. To
control what goes before the `.j2`, see `poster/template.py`. To control
what the final filename will look like, see `poster/github/__init__.py`.

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
* `shared/`: Shared utility code
    * `model.py`: Data model
    * `secrets.py`: Utilities for reading secrets
* `scripts/`: Scripts to test things out

Because of the module structure, everything needs to be run with `python -m` to
work correctly. Bit weird but u get used to it!
