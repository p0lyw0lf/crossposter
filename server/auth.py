from functools import wraps

import jwt
from sanic import Blueprint, Request
from sanic.response import redirect, empty
from sanic_ext import render

from shared.secrets import secrets

bp = Blueprint("auth", url_prefix="/")


def check_token(request: Request):
    token = request.cookies.get("token")
    if not token:
        return None

    try:
        data = jwt.decode(
            token,
            request.app.config.SECRET,
            algorithms=["HS256"],
        )
        return data["username"]
    except jwt.exceptions.InvalidTokenError:
        return None


def login_required(wrapped):
    @wraps(wrapped)
    async def decorated_function(request: Request, *args, **kwargs):
        username = check_token(request)

        if username is not None:
            kwargs["username"] = username
            return await wrapped(request, *args, **kwargs)
        else:
            return redirect(f"/login?next={request.path}")

    return decorated_function


@bp.get("/login")
async def login_get(request: Request):
    return render("login.html.j2")


@bp.post("/login")
async def login_post(request: Request):
    to = request.args.get("next", "/")
    username = request.form.get("username")
    password = request.form.get("password")

    if password is not None and \
            secrets["server"]["users"].get(username, None) == password:
        token = jwt.encode(
            {"username": username},
            request.app.config.SECRET,
            algorithm="HS256",
        )
        return redirect(to, {"Set-Cookie": f"token={token}"})
    else:
        return render("login.html.j2", context={"error": "Invalid username/password"}, status=401)


@bp.route("/auth")
async def check_auth(request: Request):
    username = check_token(request)
    if username:
        return empty(status=200)
    else:
        return empty(status=401)
