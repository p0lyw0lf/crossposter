# rc.wolfgirl.dev

Source code for <https://rc.wolfgirl.dev/>.

## Setup

First, follow the instructions in `README.md` at the root of the repository.
Then, in `poster/src/poster/config/config.yaml`, add additional outputs (or
share them!) to `outputs.server`. Make sure to configure these outputs in
`poster/src/poster/secrets/secrets.yaml` the same way you did previously.

In addition to the secrets configured previously, also add a value for
`SERVER_SECRET` in `secrets.yaml`, as well as a mapping of usernames ->
passwords in the `server.users.<user>` dictionary.

If you want to support file uploads, you'll need to add the following to
`secrets.yaml` too:

- `AWS_ACCESS_KEY_ID`: from `~/.aws/credentials`
- `AWS_SECRET_ACCESS_KEY`: from `~/.aws/credentials`
- `AWS_REGION_NAME`: the region the bucket lives in
- `AWS_BUCKET_NAME`: the name of the bucket

Finally, from the root of the repository, run:

```bash
cd rc/web
pnpm install
```

## Running

All commands run from the root of the repository.

In development mode:

```bash
source .venv/bin/activate
cd server
pnpm dev &
cd ..
sanic server
```

In production mode:

```bash
source .venv/bin/activate
cd server
pnpm build
cd ..
sanic server
```
