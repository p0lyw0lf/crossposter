from sanic import Sanic
from sanic.response import text

app = Sanic("crossposter")


@app.get("/")
async def index(request):
    return text("index.html")
