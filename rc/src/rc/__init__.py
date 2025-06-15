from datetime import datetime
import asyncio
import importlib.resources as impresources
import json
import os

import aiofiles
from sanic import Request, Sanic
from sanic.response import redirect, text
from zoneinfo import ZoneInfo

from poster.dispatch import posting_target
from poster.script import ScriptTarget
from poster.config import config
from poster.model import Post
from poster.secrets import secrets

from .auth import login_required, bp as auth_bp
from .file_upload import bp as file_upload_bp
from .sync_logs import sync_logs, write_parquet

app = Sanic("crossposter")
app.config.TEMPLATING_PATH_TO_TEMPLATES = impresources.files(__name__) / "templates"
app.config.SECRET = secrets["SERVER_SECRET"]

WEB_FILES = os.environ.get("RC_WEB_FILES", "./web/dist")
LOG_FILES = os.environ.get("RC_LOG_FILES", "./log_files")

app.static("/assets", f"{WEB_FILES}/assets", name="assets")
app.static("/log_files", LOG_FILES, name="log_files")
app.blueprint(auth_bp)
app.blueprint(file_upload_bp)

poster = posting_target(config["outputs"]["server"], config, secrets)


async def get_manifest():
    async with aiofiles.open(f"{WEB_FILES}/.vite/manifest.json", "rb") as f:
        return json.loads(await f.read())


async def index_context(username: str):
    sites = secrets["logs"].get(username, [])
    scripts = secrets["scripts"].get(username, [])
    return {
        "index": (await get_manifest())["src/Composer/index.tsx"],
        "username": username,
        "sites": sites,
        "scripts": scripts,
    }


@app.get("/")
@app.ext.template("index.html.j2")
@login_required
async def index_get(request: Request, username):
    return await index_context(username)


@app.post("/")
@app.ext.template("index.html.j2")
@login_required
async def index_post(request: Request, username):
    context = await index_context(username)

    if request.form is None:
        context["error"] = "No form passed!"
        return context

    title = request.form.get("title")
    body = request.form.get("body")
    tags = request.form.getlist("tags")

    if title is None or body is None:
        context["error"] = "Must include title and body!"
        return context

    post = Post(
        title=title,
        description=body[:137].replace(
            "\n", " ").strip() + ("..." if len(body) > 137 else ""),
        tags=tags,
        published=datetime.now(ZoneInfo(config["timezone"])),
        repost_link=None,
        body=body,
    )

    try:
        await poster.post(post, dict())
    except Exception as e:
        context["error"] = f"Error making post: {e}"
        return context

    context["message"] = "Posted successfully!"
    return context


@app.get("/dashboard")
@app.ext.template("dashboard.html.j2")
@login_required
async def dashboard(request: Request, username):
    sites = secrets["logs"].get(username, [])
    site = request.get_args().get("site")

    ctx = {
        "index": (await get_manifest())["src/Dashboard/index.tsx"],
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
