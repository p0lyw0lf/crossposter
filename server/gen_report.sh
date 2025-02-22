#!/usr/bin/env bash

# Must already have things downloaded into AWS_BUCKET_NAME. See ./gen_report.py

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

zcat $output_folder/**/*.gz | docker run --rm -i -v ./$output_file:/report.html -e LANG=$LANG allinurl/goaccess -a -o report.html --log-format CLOUDFRONT - 1>&2

echo $output_file
