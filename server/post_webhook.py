from sanic import Blueprint, Request
from sanic.response import empty, text

from poster.github import GithubTarget
from server.auth import basic_logic_required
from shared.config import config
from shared.secrets import secrets
from poster import posting_target

bp = Blueprint(name="post_webhook", url_prefix="/post")

webhooks = filter(lambda output: output.startswith(
    "webhook_"), config["outputs"].keys())
targets = {
    webhook: {
        target: posting_target(target, config, secrets)
        for target in config["outputs"][webhook]
    }
    for webhook in webhooks
}


@bp.post("/github/update")
@basic_logic_required
async def github_webhook(request: Request, username: str):
    if request.form is None:
        return text("Form must be provided", status=400)

    # The site without the "webhook_" prefix
    site = request.form.get("site", None)
    if site is None or site not in config:
        return text("Invalid site", status=400)

    webhook = f"webhook_{site}"
    if webhook not in targets:
        return text("Invalid site", status=400)

    # The slug of the post to update
    slug = request.form.get("slug", None)
    if slug is None:
        return text("Missing slug", status=400)

    gh = GithubTarget(site, config, secrets)
    post = await gh.from_slug(slug)
    if post is None:
        return text("Bad slug", status=400)

    post_ctx = dict()
    for platform, poster in targets[webhook].items():
        try:
            # See comment in server/__init__.py
            post_ctx[platform] = await poster.post(post, post_ctx, trigger_webhook=False)
        except Exception as e:
            return text(f"Error posting to {platform}: {e}", status=500)

    return empty(status=200)
