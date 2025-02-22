import asyncio
import os

from sanic.response import text, file
from sanic import Blueprint, Request

from shared.secrets import secrets
from .auth import login_required

bp = Blueprint("report", url_prefix="/report")



@bp.get("/")
@login_required
async def report(request: Request, username: str):
    sites = secrets["logs"].get(username, [])
    if len(sites) == 0:
        return text("no sites for user", 400)

    site = request.args.get("site", sites[0])
    if site not in sites:
        return text(f"site {site} not found", 400)

    site = secrets.get(site, {}).get("logs", None)
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

    proc = await asyncio.create_subprocess_exec(
        "/usr/bin/env",
        "python3",
        "./server/gen_report.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
    )

    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        return text(stderr.decode(), 500)

    filename = stdout.decode().strip()
    return await file(filename)
