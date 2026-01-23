from dataclasses import asdict
from datetime import datetime
from pathlib import Path
import os
import urllib.parse

import aiofiles
from sanic import Blueprint, Request
from sanic.response import text, file, redirect
from sanic_ext import render
import mistletoe

from poster.model import Post

from .web import get_manifest

data_dir = Path(os.environ.get("RC_DRAFTS_DIR", os.path.dirname(os.path.realpath(__file__))))
drafts_dir = (data_dir / "drafts").resolve(strict=True)

bp = Blueprint("drafts", url_prefix="/drafts")


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
            title="<Untitled>",
            description=None,
            tags=[],
            published=datetime.now(),
            repost_link=None,
            body=content,
        )

    return post

@bp.get("/<subdir:path>")
@bp.get("/", name="get_drafts_index")
async def get_drafts(request: Request, subdir=None):
    """
    This endpoint shows a simple file explorer for the drafts directory, rendering any ".md" files into HTML.
    No login is required because these links are meant to be shared.
    """
    path = drafts_dir
    if subdir:
        subdir = urllib.parse.unquote(subdir)
        path = path / subdir

    try:
        print(path)
        path = path.resolve(strict=True)
        if not path.is_relative_to(drafts_dir):
            return text("hahaha no", status=400)
    except:
        return text("Could not resolve path", status=404)

    if not path.exists():
        return text("Path doesn't exist", status=404)
    elif path.is_dir():
        if subdir is not None and not subdir.endswith("/"):
            return redirect(f"/drafts/{subdir}/")
        return await list_dir(path)
    elif path.is_file():
        if path.suffix == ".md":
            return await render_file(path)
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
    print(path, entries)
    return await render(
        "drafts/dir.html.j2",
        context={

            "index": await get_manifest("Render"),
            "entries": entries,
        },
    )

async def render_file(path: Path):
    """
    Given a markdown file at `path`, renders it as HTML.
    REQUIRES: path.exists() and path.is_file()
    """
    post = await post_from_file(path)
    body = mistletoe.markdown(post.body)
    return await render(
        "drafts/file.html.j2",
        context={
            "index": await get_manifest("Render"),
            "body": body,
            "title": post.title,
            "tags": post.tags,
        },
    )
