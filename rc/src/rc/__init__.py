from datetime import datetime
from pathlib import Path
import asyncio
import importlib.resources as impresources
import os

from mistletoe import block_token, span_token
from mistletoe.base_renderer import BaseRenderer
from sanic import Request, Sanic
from sanic.response import redirect, text
from zoneinfo import ZoneInfo
import mistletoe

from poster.script import ScriptTarget
from poster.config import config
from poster.model import Post
from poster.secrets import secrets

from .auth import login_required, bp as auth_bp
from .drafts import bp as drafts_bp
from .file_upload import bp as file_upload_bp
from .sync_logs import sync_logs, write_parquet
from .web import WEB_FILES, get_manifest

app = Sanic("crossposter2")
app.config.TEMPLATING_PATH_TO_TEMPLATES = impresources.files(__name__) / "templates"
app.config.SECRET = secrets["SERVER_SECRET"]

LOG_FILES = Path(os.environ.get("RC_DATA_DIR", "./src/rc")) / "log_files"

app.static("/assets", f"{WEB_FILES}/assets", name="assets")
app.static("/log_files", str(LOG_FILES), name="log_files")
app.blueprint(auth_bp)
app.blueprint(drafts_bp)
app.blueprint(file_upload_bp)


async def index_context(username: str):
    sites = secrets["logs"].get(username, [])
    scripts = secrets["scripts"].get(username, [])
    return {
        "index": await get_manifest("Composer"),
        "username": username,
        "sites": sites,
        "scripts": scripts,
    }


@app.get("/")
@app.ext.template("index.html.j2")
@login_required
async def index_get(request: Request, username):
    return await index_context(username)


@app.get("/dashboard")
@app.ext.template("dashboard.html.j2")
@login_required
async def dashboard(request: Request, username):
    sites = secrets["logs"].get(username, [])
    site = request.get_args().get("site")

    ctx = {
        "index": await get_manifest("Dashboard"),
        "username": username,
    }

    if len(sites) == 0:
        ctx["error"] = "Not allowed to access any sites"
        return ctx
    elif site is None:
        ctx["error"] = "Must specify a \"site\" argument"
        return ctx
    elif site not in sites:
        ctx["error"] = "Not allowed to access that site"
        return ctx
    else:
        ctx["site"] = site

    await asyncio.to_thread(sync_logs, site)
    await asyncio.to_thread(write_parquet, site)

    return ctx


@app.post("/webhook/post")
@app.ext.template("login.html.j2")
@login_required
async def webhook_post(request: Request, username):
    if request.form is None:
        return text("Form must be provided", status=400)

    site = request.form.get("site", None)
    scripts = secrets["scripts"].get(username, [])
    if site is None or site not in config or site not in scripts:
        return text("Invalid site", status=400)

    if not site.startswith("script"):
        return text("Error: can only run scripts from this endpoint", status=400)

    poster = ScriptTarget(site, config, secrets)
    try:
        await poster.run_script()
    except Exception as e:
        return text(f"Error running script: {e}")

    return redirect(app.url_for('index_get'), status=303)
