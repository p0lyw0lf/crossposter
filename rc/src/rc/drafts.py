from datetime import datetime
from pathlib import Path
import asyncio
import os
import subprocess
import urllib.parse

from aiofiles.tempfile import NamedTemporaryFile
from sanic import Blueprint, Request
from sanic.response import HTTPResponse, html, text, file, redirect
from sanic_ext import render
from zoneinfo import ZoneInfo
import aiofiles
import mistletoe

from poster.config import config
from poster.dispatch import posting_target
from poster.model import Post
from poster.secrets import secrets
from poster.template import Renderable

from .auth import check_token, login_required
from .markdown import DescriptionRenderer
from .web import get_manifest

bp = Blueprint("drafts", url_prefix="/drafts")

data_dir = Path(os.environ.get("RC_DRAFTS_DIR", os.path.dirname(os.path.realpath(__file__))))
drafts_dir = (data_dir / "drafts").resolve()

poster = posting_target(config["outputs"]["server"], config, secrets)
renderer = posting_target(config["outputs"]["drafts"], config, secrets)

driver_bin = Path(os.environ.get("RC_DRIVER_BIN", "/usr/bin/false"))
website_dir = Path(os.environ.get("RC_WEBSITE_DIR", os.path.join(os.path.dirname(os.path.realpath(__file__)), "website")))
website_drafts_dir = (website_dir / "drafts").resolve()
website_dist_dir = website_drafts_dir / "dist"

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
            return await render_file(request, path, request.args.get("full") is not None)
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

async def render_file(request: Request, path: Path, is_full: bool):
    """
    Given a markdown file at `path`, renders it as HTML.
    REQUIRES: path.exists() and path.is_file()
    """

    username = check_token(request)
    post = await post_from_file(path)
    if is_full:
        return await render_post(post)
    else:
        return await preview_post(post, username)

async def render_post(post: Post):
    """
    Given a parsed post object, renders it using the corresponding jinja template.
    """

    # 1: fully render post to text
    if not isinstance(renderer, Renderable):
        return text("cannot render post", status=500)
    content = await renderer.render(post, dict())

    # 2: copy post into website source directory
    # (this does require that directory to be mutable, but that's OK)
    async with NamedTemporaryFile(dir=(website_drafts_dir / "src")) as f:
        await f.write(content.encode("utf-8"))
        await f.flush()

        # 3: Run the renderer with that file
        filename = os.path.basename(str(f.name))
        await asyncio.to_thread(run_driver, filename)

        # 4: Collect the outputs
        async with aiofiles.open(website_dist_dir / f"{filename}.html") as body_file:
            body = await body_file.read()

    return html(body)

def run_driver(filename: str):
    """
    REQUIRES: website_dir / "drafts" / "src" / filename exists and contains a valid post
    ENSURES: website_dir / "drafts" / "dist" / f"{filename}.html" exists. 
    """

    p = subprocess.run(
        [
            str(driver_bin),
            "--dist", str(website_dist_dir),
            "--cache", str(website_drafts_dir / ".driver"),
            "run", "--no-delete-missing", str(website_dir / "DRAFT.js"),
            "--",
            filename,
        ],
        cwd=website_dir,
    )
    p.check_returncode()

async def preview_post(post: Post, username=None, messages=[], errors=[]):
    return await render(
        "drafts/file.html.j2",
        context={
            "index": await get_manifest("Render"),
            "title": post.title,
            "description": post.description,
            "tags": post.tags,
            "username": username,
            "messages": messages,
            "errors": errors,
        },
    )

@bp.post("/<subdir:path>")
@login_required
async def post_draft(_: Request, username, subdir=None):
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
    if not post.title or post.title == UNTITLED:
        errors.append("Must include title property!")
    if not post.tags or len(post.tags) == 0:
        errors.append("Must include tags!")

    if len(errors) > 0:
        return await preview_post(post, messages, errors)

    description = post.description
    if not description:
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

    return await preview_post(post, username, messages, errors)
