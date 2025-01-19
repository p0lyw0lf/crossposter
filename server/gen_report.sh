#!/usr/bin/env bash

set -euo pipefail
shopt -s globstar

if [[ -z "${AWS_BUCKET_NAME+x}" ]]; then
  >&2 echo "Must get bucket passed as AWS_BUCKET_NAME"
  exit 1
fi

output_folder="tmp/${AWS_BUCKET_NAME}"
mkdir -p $output_folder
output_file="tmp/${AWS_BUCKET_NAME}.html"
touch $output_file

# Must also receive environment variables that allow this to work
aws s3 sync --delete "s3://${AWS_BUCKET_NAME}" "tmp/${AWS_BUCKET_NAME}" 1>&2

zcat $output_folder/**/*.gz | docker run --rm -i -v ./$output_file:/report.html -e LANG=$LANG allinurl/goaccess -a -o report.html --log-format CLOUDFRONT - 1>&2

echo $output_file
