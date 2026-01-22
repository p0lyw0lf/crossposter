from dataclasses import asdict
from datetime import datetime
from os.path import basename
from pathlib import Path
import os
from typing import Tuple

import aiofiles
from sanic import Blueprint, Request
from sanic.request import RequestParameters
from sanic.response import json, text

from poster.model import Post, to_slug
from poster.template import templates

from .auth import login_required

data_dir = Path(os.environ.get("RC_DATA_DIR", os.path.dirname(os.path.realpath(__file__))))
drafts_dir = data_dir / "drafts"

bp = Blueprint("drafts", url_prefix="/drafts")


async def post_from_file(p: Path) -> Post:
    """
    Given a filename for a serialized post, returns that post as a Python object.
    """
    async with aiofiles.open(p, mode="r") as f:
        contents = await f.read()
    return Post.from_string(contents)


async def post_from_form(form: RequestParameters) -> Post | None:
    """
    Given a Sanic form object, parse the Post out of it.
    """
    title = form.get("title")
    body = form.get("body")
    tags = form.getlist("tags")

    if not (\
        isinstance(title, str) and \
        isinstance(body, str) and \
        isinstance(tags, list) and \
        all(isinstance(tag, str) for tag in tags) \
    ):
        return None

    return Post(
        title=title,
        description=None,
        tags=tags,
        published=datetime.now(),
        repost_link=None,
        body=body,
    )

async def serialize_post_to_file(path: Path, post: Post):
    """
    Given a filename for a post object, serializes the post to that file.
    """
    rendered = await serialize_post(post)
    async with aiofiles.open(path, mode="w") as f:
        await f.write(rendered)

async def serialize_post(post: Post) -> str:
    template = templates["github_blog.md.j2"]
    rendered = await template.render_async(
        slug=to_slug(post),
        **asdict(post),
    )
    return rendered

@bp.get("list")
@login_required
async def list_drafts(request: Request, username: str):
    dir = drafts_dir / username
    dir.mkdir(parents=True, exist_ok=True)

    drafts: list[Tuple[str, Post]] = []
    for f in dir.iterdir():
        drafts.append((f.stem, await post_from_file(f)))
    drafts.sort(key=lambda p: p[1].title)

    return json([
        {
            "draftId": id,
            "title": draft.title,
            "body": draft.body,
            "tags": draft.tags,
        }
        for id, draft in drafts
    ])

@bp.get("by_id/<id:slug>")
@login_required
async def get_draft(request: Request, username: str, id: str):
    """
    This endpoint fetches the draft from disk, and returns it as a json object.
    `/drafts/render/<id>` should be used to show the final product of a draft.
    """

    file = drafts_dir / username / f"{id}.md"
    draft = await post_from_file(file)

    return json(draft)

@bp.put("by_id/<id:slug>")
@login_required
async def upsert_draft(request: Request, username: str, id: str):
    print("handling upsert_draft")
    if request.form is None:
        return text("must provide form", status=400)

    draft = await post_from_form(request.form)
    if draft is None:
        return text("bad post", status=400)

    file = drafts_dir / username / f"{id}.md"
    await serialize_post_to_file(file, draft)

    return text("ok")

@bp.delete("by_id/<id:slug>")
@login_required
async def delete_draft(request: Request, username: str, id: str):

    file = drafts_dir / username / f"{id}.md"
    file.unlink()

    return text("ok")

@bp.get("render/<username:slug>/<id:slug>")
async def render_draft(request: Request, username: str, id: str):
    """
    This endpoint takes the draft markdown identified by the id and renders it as HTML. No login is
    required, because these links are meant to be shared with other people for pre-post review.
    """

    file = drafts_dir / username / f"{id}.md"
    post = await post_from_file(file)

    return text("Not Implemented", status=500)
