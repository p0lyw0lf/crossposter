from sanic import Sanic

from shared.secrets import secrets
from shared.config import config
from poster import posting_target

app = Sanic("crossposter")

app.static("/", "./server/dist/index.html", name="index")
app.static("/assets", "./server/dist/assets", name="assets")

posters = {
    target: posting_target(target, config, secrets)
    for target in config["outputs"]["server"]
}
