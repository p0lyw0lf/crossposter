#!/usr/bin/env python3

from datetime import date, timedelta
import glob
import os
import subprocess
import sys

bucket = os.environ["AWS_BUCKET_NAME"]
if not bucket:
    print("Must get passed bucket as AWS_BUCKET_NAME", file=sys.stderr)
    sys.exit(1)

output_folder = f"tmp/{bucket}"

# First, sync bucket. This is so we know everything that's inside.
# Must also receive environment variables that allow this to work
p = subprocess.run(["aws", "s3", "sync", "--delete", f"s3://{bucket}", output_folder], stdout=subprocess.PIPE)
p.check_returncode()

# Then, find all the folders that are before a certain cutoff
now = date.today()
cutoff = now - timedelta(days=14) # TODO: make delta configurable ?

to_remove = []

# {output_folder}/{yyyy}/{MM}/{dd}
for folder in glob.iglob(f"{output_folder}/*/*/*/"):
    [year, month, day] = folder[len(output_folder)+1:-1].split("/")
    folder_date = date(int(year), int(month), int(day))
    if folder_date < cutoff:
        to_remove.append(f"{year}/{month}/{day}")

# Then, remove all those folders
for folder in to_remove:
    p = subprocess.run(["aws", "s3", "rm", "--recursive", f"s3://{bucket}/{folder}"], stdout=subprocess.PIPE)
    p.check_returncode()

    p = subprocess.run(["rm", "-rf", f"{output_folder}/{folder}"], stdout=subprocess.PIPE)
    p.check_returncode()

# Finally, generate the report
p = subprocess.run(["bash", "./server/gen_report.sh"])
p.check_returncode()
