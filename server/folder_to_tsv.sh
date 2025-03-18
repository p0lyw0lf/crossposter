#!/usr/bin/env bash

set -euo pipefail
shopt -s globstar

output_folder="$1"
mkdir -p $output_folder
output_file="$1.html"
touch $output_file

# Add the header, since the next line will strip all comments that would usually contain it
echo "date	time	x-edge-location	sc-bytes	c-ip	cs-method	cs(Host)	cs-uri-stem	sc-status	cs(Referer)	cs(User-Agent)	cs-uri-query	cs(Cookie)	x-edge-result-type	x-edge-request-id	x-host-header	cs-protocol	cs-bytes	time-taken	x-forwarded-for	ssl-protocol	ssl-cipher	x-edge-response-result-type	cs-protocol-version	fle-status	fle-encrypted-fields	c-port	time-to-first-byte	x-edge-detailed-result-type	sc-content-type	sc-content-len	sc-range-start	sc-range-end"
zcat $output_folder/**/*.gz | sed '/^#/d'
