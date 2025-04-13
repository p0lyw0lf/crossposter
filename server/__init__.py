from datetime import datetime
import asyncio
import json
import os

from sanic import Request, Sanic
from sanic.response import text, file
from zoneinfo import ZoneInfo
import aiofiles

from poster.dispatch import posting_target
from shared.config import config
from shared.model import Post
from shared.secrets import secrets

from .auth import login_required, bp as auth_bp
from .file_upload import bp as file_upload_bp
from .post_webhook import bp as post_webhook_bp
from .sync_logs import sync_logs, write_parquet

app = Sanic("crossposter")
app.config.TEMPLATING_PATH_TO_TEMPLATES = "./server/templates"
app.config.SECRET = secrets["SERVER_SECRET"]

app.static("/assets", "./server/dist/assets", name="assets")
app.static("/log_files", "./server/log_files", name="log_files")
app.blueprint(auth_bp)
app.blueprint(file_upload_bp)
app.blueprint(post_webhook_bp)

poster = posting_target(config["outputs"]["server"], config, secrets)


async def get_manifest():
    async with aiofiles.open("./server/dist/.vite/manifest.json", "rb") as f:
        return json.loads(await f.read())


@app.get("/")
@app.ext.template("index.html.j2")
@login_required
async def index_get(request: Request, username):
    sites = secrets["logs"].get(username, [])
    return {
        "index": (await get_manifest())["src/Composer/index.tsx"],
        "username": username,
        "sites": sites,
    }


@app.post("/")
@app.ext.template("index.html.j2")
@login_required
async def index_post(request: Request, username):
    sites = secrets["logs"].get(username, [])
    context = {
        "index": (await get_manifest())["src/Composer/index.tsx"],
        "username": username,
        "sites": sites,
    }

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
