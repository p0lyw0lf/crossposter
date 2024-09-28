import json

import aiofiles
import jwt
from sanic import Sanic
from sanic.response import redirect

from shared.config import config
from shared.secrets import secrets
from poster import posting_target

from .auth import login_required

DEV = True
VITE_MANIFEST = None

app = Sanic("crossposter")
app.config.TEMPLATING_PATH_TO_TEMPLATES = "./server/templates"
app.config.SECRET = secrets["SERVER_SECRET"]

app.static("/assets", "./server/dist/assets", name="assets")


async def get_manifest():
    global VITE_MANIFEST
    if VITE_MANIFEST is None or DEV:
        async with aiofiles.open("./server/dist/.vite/manifest.json", "rb") \
                as f:
            VITE_MANIFEST = json.loads(await f.read())
    return VITE_MANIFEST


posters = {
    target: posting_target(target, config, secrets)
    for target in config["outputs"]["server"]
}


@app.route("/")
@app.ext.template("index.html.j2")
@login_required
async def index(request, username):
    return {
        "index": (await get_manifest())["src/index.tsx"],
        "username": username
    }


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
