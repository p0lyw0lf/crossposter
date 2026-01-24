from dataclasses import asdict
from datetime import datetime
from pathlib import Path
import os
import urllib.parse

import aiofiles
from sanic import Blueprint, Request
from sanic.response import HTTPResponse, text, file, redirect
from sanic_ext import render
import mistletoe
from zoneinfo import ZoneInfo

from poster.dispatch import posting_target
from poster.config import config
from poster.model import Post
from poster.secrets import secrets

from .auth import check_token, login_required
from .markdown import DescriptionRenderer
from .web import get_manifest

bp = Blueprint("drafts", url_prefix="/drafts")

data_dir = Path(os.environ.get("RC_DRAFTS_DIR", os.path.dirname(os.path.realpath(__file__))))
drafts_dir = (data_dir / "drafts").resolve()

poster = posting_target(config["outputs"]["server"], config, secrets)


UNTITLED = "<Untitled>"


async def post_from_file(p: Path) -> Post:
    """
    Given a filename for a serialized post, returns that post as a Python object.
    """
    async with aiofiles.open(p, mode="r") as f:
        content = await f.read()

    try:
        # Try to parse out frontmatter
        post = Post.from_string(content)
    except:
        # In case there is no frontmatter, treat the entire thing as markdown
        post = Post(
            title=UNTITLED,
            description=None,
            tags=[],
            published=datetime.now(),
            repost_link=None,
            body=content,
        )

    return post

def validate_path(subdir: str | None) -> HTTPResponse | Path:
    """
    Given an (unsafe) subdirectory, validates there is no path traversal and returns the path it
    corresponds to. Otherwise, returns the HTTPResponse that should be sent to the client indicating
    this is an invalid path.

    ENSURES: isinstance(return, Path) implies return.exists() and return.is_relative_to(drafts_dir)
    """
    path = drafts_dir
    if subdir:
        subdir = urllib.parse.unquote(subdir)
        path = path / subdir

    try:
        path = path.resolve(strict=True)
        if not path.is_relative_to(drafts_dir):
            return text("hahaha no", status=400)
    except:
        return text("Could not resolve path", status=404)

    if not path.exists():
        return text("Path doesn't exist", status=404)

    return path


@bp.get("/<subdir:path>")
async def get_drafts(request: Request, subdir=None):
    """
    This endpoint shows a simple file explorer for the drafts directory, rendering any ".md" files into HTML.
    No login is required because these links are meant to be shared.
    """
    path = validate_path(subdir)
    if not isinstance(path, Path):
        return path

    elif path.is_dir():
        if subdir and not subdir.endswith("/"):
            return redirect(f"/drafts/{subdir}/")
        return await list_dir(path)
    elif path.is_file():
        if path.suffix == ".md":
            return await render_file(request, path)
        else:
            return await file(path)
    else:
        return text("Bad inode", status=400)


async def list_dir(path: Path):
    """
    Given a directory at `path`, returns an HTML page.
    REQUIRES: path.exists() and path.is_dir()
    """
    entries = []
    for f in path.iterdir():
        if f.is_dir():
            entries.append({
                "type": "dir",
                "name": f.name,
            })
        elif f.is_file():
            title = f.name
            if f.suffix == ".md":
                try:
                    post = await post_from_file(f)
                    title = post.title
                except:
                    pass
            title = title or "<Untitled>"
            entries.append({
                "type": "file",
                "title": title,
                "name": f.name,
            })

    entries.sort(key=lambda e: e["type"] + e["name"])
    return await render(
        "drafts/dir.html.j2",
        context={

            "index": await get_manifest("Render"),
            "entries": entries,
        },
    )

async def render_file(request: Request, path: Path):
    """
    Given a markdown file at `path`, renders it as HTML.
    REQUIRES: path.exists() and path.is_file()
    """

    username = check_token(request)
    post = await post_from_file(path)
    return await render_post(post, username)

async def render_post(post: Post, username=None, messages=[], errors=[]):
    """
    Given a parsed post object, renders it using the corresponding jinja template.
    """

    body = mistletoe.markdown(post.body)
    return await render(
        "drafts/file.html.j2",
        context={
            "index": await get_manifest("Render"),
            "body": body,
            "title": post.title,
            "tags": post.tags,
            "username": username,
            "messages": messages,
            "errors": errors,
        },
    )

@bp.post("/<subdir:path>")
@login_required
async def post_draft(request: Request, username, subdir=None):
    path = validate_path(subdir)
    if not isinstance(path, Path):
        return path

    if not path.is_file():
        return text("Not a file", status=400)
    if path.suffix != ".md":
        return text("Not a markdown file", status=400)

    try:
        post = await post_from_file(path)
    except:
        return text("Could not read file??", status=500)

    messages = []
    errors = []
    if post.title == UNTITLED:
        errors.append("Must include title property!")
    if len(post.tags) == 0:
        errors.append("Must include tags!")

    if len(errors) > 0:
        return await render_post(post, messages, errors)

    description = mistletoe.markdown(post.body, DescriptionRenderer)
    published = datetime.now(ZoneInfo(config["timezone"]))
    full_post = Post(
        title=post.title,
        description=description,
        tags=post.tags,
        published=published,
        repost_link=None,
        body=post.body,
    )

    try:
        await poster.post(full_post, dict())
    except Exception as e:
        errors.append(f"Error making post: {e}")

    if len(errors) == 0:
        messages.append("Posted successfully!")

    return await render_post(post, username, messages, errors)
