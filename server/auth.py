from datetime import datetime, timezone, timedelta
from functools import wraps

import jwt
from sanic import Blueprint, Request
from sanic.response import redirect, empty, text
from sanic_ext import render

from shared.secrets import secrets

bp = Blueprint("auth", url_prefix="/")


def check_token(request: Request):
    """
    Checks token authentication for a given request. Returns the authenticated username, if any.
    """

    token = request.cookies.get("token")
    if not token:
        return None

    try:
        data = jwt.decode(
            token,
            request.app.config.SECRET,
            algorithms=["HS256"],
        )
        return data.get("sub", None)
    except jwt.exceptions.InvalidTokenError:
        return None


def check_basic_auth(request: Request):
    """
    Checks "basic authentication", that is, username and password provided as form parameters. Returns the authenticated username, if applicable.

    SHOULD be used on post request only.
    """
    if request.form is None:
        # Must provide a form
        return None

    username = request.form.get("username")
    password = request.form.get("password")

    # TODO: fix insecure password check
    if password is None or secrets["server"]["users"].get(username, None) != password:
        return None

    return username


def login_required(wrapped):

    @wraps(wrapped)
    async def decorated_function(request: Request, *args, **kwargs):
        username = check_token(request)
        if username is None:
            return redirect(f"/login?next={request.path}")

        kwargs["username"] = username
        return await wrapped(request, *args, **kwargs)

    return decorated_function


def basic_logic_required(wrapped):
    @wraps(wrapped)
    async def decorated_function(request: Request, *args, **kwargs):
        username = check_basic_auth(request)
        if username is None:
            # basic auth is never interactive, fail immediately
            return text("Bad password", status=401)

        kwargs["username"] = username
        return await wrapped(request, *args, **kwargs)

    return decorated_function


@bp.get("/login")
async def login_get(request: Request):
    return await render("login.html.j2")


@bp.post("/login")
async def login_post(request: Request):
    username = check_basic_auth(request)
    if username is None:
        return await render("login.html.j2", context={"error": "Invalid username/password"}, status=401)

    token = jwt.encode(
        {
            "sub": username,
            "exp": datetime.now(tz=timezone.utc) + timedelta(days=30),
        },
        request.app.config.SECRET,
        algorithm="HS256",
    )
    to = request.args.get("next", "/")
    return redirect(to, {"Set-Cookie": f"token={token}"})


@bp.route("/auth")
async def auth_route(request: Request):
    username = check_token(request)
    if username:
        return empty(status=200)
    else:
        return empty(status=401)
