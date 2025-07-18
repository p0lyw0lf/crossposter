#!/usr/bin/env bash
set -euo pipefail
trap "echo; exit -1" INT

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

repo="${RC_DATA_DIR:-$HOME}/wolfgirl.dev"
if [ ! -d "$repo" ]; then
  git clone https://github.com/p0lyw0lf/website.git "$repo"
fi

cd "$repo"
git pull

# I used to have all these separate steps in GitHub actions, but now I have
# them all on the same machine, which honestly is probably better overall lol
# No need to restore caches & install tools every time, it's already all there!

# Use nvm, if installed
NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Build the site
pnpm install
pnpm build

# Uses the strategy at https://rclone.org/s3/#avoiding-get-requests-to-read-directory-listings
rclone --config "${SCRIPT_DIR}/rclone_blog.conf" sync --fast-list --checksum ./dist/ "s3:${AWS_BUCKET_NAME}"

# TODO: I probably want to be smarter about the files I invalidate, but for now
# this is fine; the majority of the cost is uploading so many files (which
# rclone should help with)
aws cloudfront create-invalidation --distribution-id "${AWS_CLOUDFRONT_DISTRIBUTION}" --paths "/*"
