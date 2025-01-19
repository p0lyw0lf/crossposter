import asyncio

from sanic.response import text, file
from sanic import Blueprint, Request

from .auth import login_required

bp = Blueprint("report", url_prefix="/report")


@bp.get("/")
@login_required
async def report(request: Request, username: str):
    proc = await asyncio.create_subprocess_exec(
        "./server/gen_report.sh",
        ["gen_report.sh"],
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        return text(stderr.decode(), 500)

    filename = stdout.decode().strip()
    return await file(filename)
