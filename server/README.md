# rc.wolfgirl.dev

Source code for <https://rc.wolfgirl.dev/>.

## Setup

First, follow the instructions in `README.md` at the root of the repository.
Then, in `shared/config/config.toml`, add additional outputs (or share them!)
to `outputs.server`. Make sure to configure these outputs in
`shared/secrets/secrets.toml` the same way you did previously.

In addition to the secrets configured previously, also add a value for
`SERVER_SECRET` in `secrets.toml`, as well as a mapping of usernames ->
passwords in the `server.users.<user>` dictionary.

Finally, from the root of the repository, run:

```bash
cd server
npm install
```

## Running

All commands run from the root of the repository.

In development mode:

```bash
source .venv/bin/activate
cd server
npm run dev &
cd ..
sanic server
```

In production mode:

```bash
source .venv/bin/activate
cd server
npm run build
cd ..
sanic server
```
