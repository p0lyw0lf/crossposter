#!/usr/bin/env python3

"""
Meant to be run periodically, to sync the files in `./log_files`
"""

from datetime import date, timedelta
from pathlib import Path
import glob
import importlib.resources as impresources
import io
import os
import subprocess

import pyarrow.csv as pv
import pyarrow.parquet as pq

from poster.secrets import secrets

data_dir = Path(os.environ.get("RC_DATA_DIR", os.path.dirname(os.path.realpath(__file__))))
log_files = data_dir / "log_files"
folder_to_tsv = impresources.files(__name__) / "folder_to_tsv.sh"


def sync_logs(site_name: str, days_delta: int = 28):
    """
    Syncs all logs corresponding to the given site into the cache
    """
    cfg = secrets[site_name]["logs"]
    bucket: str = cfg["AWS_BUCKET_NAME"]
    env = os.environ.copy()
    for var in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION_NAME"]:
        env[var] = cfg[var]

    output_folder = str(data_dir / "tmp" / bucket)

    # First, sync bucket. This is so we know everything that's inside.
    p = subprocess.run(
        ["aws", "s3", "sync", "--delete", f"s3://{bucket}", output_folder],
        stdout=subprocess.PIPE,
        env=env,
    )
    p.check_returncode()

    # Then, find all the folders that are before a certain cutoff
    now = date.today()
    cutoff = now - timedelta(days=days_delta)

    to_remove = []

    # {output_folder}/{yyyy}/{MM}/{dd}
    for folder in glob.iglob(f"{output_folder}/*/*/*/"):
        [year, month, day] = folder[len(output_folder)+1:-1].split("/")
        folder_date = date(int(year), int(month), int(day))
        if folder_date < cutoff:
            to_remove.append(f"{year}/{month}/{day}")

    # Then, remove all those folders
    for folder in to_remove:
        p = subprocess.run(
            ["aws", "s3", "rm", "--recursive", f"s3://{bucket}/{folder}"],
            stdout=subprocess.PIPE,
            env=env,
        )
        p.check_returncode()

        p = subprocess.run(
            ["rm", "-rf", f"{output_folder}/{folder}"],
            stdout=subprocess.PIPE,
        )
        p.check_returncode()


def write_parquet(site_name: str):
    """
    Writes the synced logs to a parquet file in `log_files`
    """
    cfg = secrets[site_name]["logs"]
    bucket: str = cfg["AWS_BUCKET_NAME"]
    output_folder = str(data_dir / "tmp" / bucket)

    # Generate the TSV from the given folder
    p = subprocess.run(
        ["bash", str(folder_to_tsv), str(output_folder)],
        stdout=subprocess.PIPE,
    )
    p.check_returncode()

    # Convert the TSV to an Apache Arrow table
    table = pv.read_csv(io.BytesIO(p.stdout), parse_options=pv.ParseOptions(
        delimiter="\t", quote_char=False, double_quote=False,
    ))
    os.makedirs(log_files, exist_ok=True)
    pq.write_table(table, str(log_files / f"{site_name}.parquet"))


if __name__ == "__main__":
    print("starting")
    for site_name, site in secrets.items():
        if isinstance(site, dict) and "logs" in site:
            print("syncing", site_name)
            sync_logs(site_name)
            write_parquet(site_name)
    print("done")
