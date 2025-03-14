from datetime import datetime
import json
import os

import aiofiles
import aiohttp
import jwt
from sanic import Request, Sanic
from sanic.response import redirect
from zoneinfo import ZoneInfo

from shared.config import config
from shared.model import Post
from shared.secrets import secrets
from poster import posting_target

from .auth import login_required
from .file_upload import bp as file_upload_bp
from .report import bp as report_bp

app = Sanic("crossposter")
app.config.TEMPLATING_PATH_TO_TEMPLATES = "./server/templates"
app.config.SECRET = os.environ["SERVER_SECRET"]

app.static("/assets", "./server/dist/assets", name="assets")
app.blueprint(file_upload_bp)
app.blueprint(report_bp)


posters = {
    target: posting_target(target, config, secrets)
    for target in config["outputs"]["server"]
}


@app.before_server_start
def setup(app, loop):
    app.ctx.remote = "http://localhost:5601"
    app.ctx.client = aiohttp.ClientSession()


async def get_manifest():
    async with aiofiles.open("./server/dist/.vite/manifest.json", "rb") as f:
        return json.loads(await f.read())


@app.get("/")
@app.ext.template("index.html.j2")
@login_required
async def index_get(request, username):
    sites = secrets["logs"].get(username, [])
    return {
        "index": (await get_manifest())["src/index.tsx"],
        "username": username,
        "sites": sites,
    }


@app.post("/")
@app.ext.template("index.html.j2")
@login_required
async def index_post(request, username):
    sites = secrets["logs"].get(username, [])
    context = {
        "index": (await get_manifest())["src/index.tsx"],
        "username": username,
        "sites": sites,
    }

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

    post_ctx = dict()
    for platform, poster in posters.items():
        try:
            # NOTE: We don't track dependencies automatically; if a certain
            # poster depends on a previous poster, it must be manually
            # ordered after in the list. This works because Python dicts
            # have a stable iteration order based on insertion order.
            post_ctx[platform] = await poster.post(post, post_ctx)
        except Exception as e:
            context["error"] = f"Error posting to {platform}: {e}"
            return context

    context["message"] = "Posted successfully!"
    return context


@app.get("/login")
@app.ext.template("login.html.j2")
async def login_get(request):
    return {}


@app.post("/login")
@app.ext.template("login.html.j2")
async def login_post(request):
    username = request.form.get("username")
    password = request.form.get("password")

    if password is not None and \
            secrets["server"]["users"].get(username, None) == password:
        token = jwt.encode(
            {"username": username},
            request.app.config.SECRET,
            algorithm="HS256",
        )
        return redirect("/", {"Set-Cookie": f"token={token}"})
    else:
        return {"error": "Invalid username/password"}


@app.route("/opensearch/<path>")
@login_required
async def opensearch_proxy(request: Request, path: str):
    """
    y'know, I really should build this in something that actually support
    proxying. But! I like the simple authentication too much, so it goes here.
    """

    ctx = request.app.ctx
    local_resp = await ctx.client.request(request.method, f"{ctx.remote}/{path}", data=request.body, params=request.parsed_args, headers=request.headers, cookies=request.cookies)
    async with local_resp:
        remote_resp = await request.respond(status=local_resp.status, headers=local_resp.headers)
        if remote_resp is None:
            return
        async for data in local_resp.content.iter_any():
            await remote_resp.send(data)
