import asyncio
import os

from sanic.response import text, file
from sanic import Blueprint, Request

from server.sync_logs import sync_logs
from shared.secrets import secrets
from .auth import login_required

bp = Blueprint("report", url_prefix="/report")


@bp.get("/")
@login_required
async def report(request: Request, username: str):
    sites = secrets["logs"].get(username, [])
    if len(sites) == 0:
        return text("no sites for user", 400)

    site_name = request.args.get("site", sites[0])
    if site_name not in sites:
        return text(f"site {site_name} not found", 400)

    site = secrets.get(site_name, {}).get("logs", None)
    if site is None:
        return text(f"site {site} not defined", 500)

    env = os.environ.copy()
    for var in [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_REGION_NAME",
        "AWS_BUCKET_NAME",
    ]:
        env[var] = site[var]

    await asyncio.to_thread(sync_logs, site_name)

    proc = await asyncio.create_subprocess_exec(
        "bash",
        "./server/gen_report.sh",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
    )

    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        return text(stderr.decode(), 500)

    filename = stdout.decode().strip()
    return await file(filename)
