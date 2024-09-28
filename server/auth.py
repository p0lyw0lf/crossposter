from functools import wraps

import jwt
from sanic.response import redirect


def check_token(request):
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
    async def decorated_function(request, *args, **kwargs):
        username = check_token(request)

        if username is not None:
            kwargs["username"] = username
            return await wrapped(request, *args, **kwargs)
        else:
            return redirect("/login")

    return decorated_function
