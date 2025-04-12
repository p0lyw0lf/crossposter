#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Assumes that the wolfgirl.dev repo is in the same folder as the crossposter repo
# I should really merge these into a monorepo at some point, but oh well
cd "${SCRIPT_DIR}/../../wolfgirl.dev"

# I used to have all these separate steps in GitHub actions, but now I have
# them all on the same machine, which honestly is probably better overall lol
# No need to restore caches & install tools every time, it's already all there!
pnpm install
pnpm build

# Uses the strategy at https://rclone.org/s3/#avoiding-get-requests-to-read-directory-listings
rclone --config "${SCRIPT_DIR}/rclone_blog.conf" sync --fast-list --checksum ./dist/ "s3:${AWS_BUCKET_NAME}"

# TODO: I probably want to be smarter about the files I invalidate, but for now
# this is fine; the majority of the cost is uploading so many files (which
# rclone should help with)
# aws cloudfront create-invalidation --distribution-id "${AWS_CLOUDFRONT_DISTRIBUTION}" --paths "/*"
