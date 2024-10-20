from datetime import datetime
import json

import aiofiles
import jwt
from sanic import Sanic
from sanic.response import redirect
from zoneinfo import ZoneInfo

from shared.config import config
from shared.model import Post
from shared.secrets import secrets
from poster import posting_target

from .auth import login_required
from .file_upload import bp as file_upload_bp

app = Sanic("crossposter")
app.config.TEMPLATING_PATH_TO_TEMPLATES = "./server/templates"
app.config.SECRET = secrets["SERVER_SECRET"]

app.static("/assets", "./server/dist/assets", name="assets")
app.blueprint(file_upload_bp)

posters = {
    target: posting_target(target, config, secrets)
    for target in config["outputs"]["server"]
}


async def get_manifest():
    async with aiofiles.open("./server/dist/.vite/manifest.json", "rb") as f:
        return json.loads(await f.read())


@app.get("/")
@app.ext.template("index.html.j2")
@login_required
async def index_get(request, username):
    return {
        "index": (await get_manifest())["src/index.tsx"],
        "username": username
    }


@app.post("/")
@app.ext.template("index.html.j2")
@login_required
async def index_post(request, username):
    context = {
        "index": (await get_manifest())["src/index.tsx"],
        "username": username,
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
        published=datetime.now(ZoneInfo(secrets["timezone"])),
        repost_link=None,
        body=body,
    )

    for platform, poster in posters.items():
        try:
            await poster.post(post)
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
