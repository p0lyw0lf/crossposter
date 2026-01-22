from pathlib import Path
import os

from sanic import Blueprint, Request
from sanic.response import text

from .auth import login_required

data_dir = Path(os.environ.get("RC_DATA_DIR", os.path.dirname(os.path.realpath(__file__))))
drafts_dir = data_dir / "drafts"

bp = Blueprint("drafts", url_prefix="/drafts")


@bp.get("list")
@login_required
async def list_drafts(request: Request):
    return text("Not Implemented", status=500)

@bp.get("by_id/:id")
@login_required
async def get_draft(request: Request):
    """
    This endpoint fetches the draft from disk, and returns it as a json object.
    `/drafts/render/:id` should be used to show the final product of a draft.
    """
    return text("Not Implemented", status=500)

@bp.put("by_id/:id")
@login_required
async def upsert_draft(request: Request):
    return text("Not Implemented", status=500)

@bp.delete("by_id/:id")
@login_required
async def delete_draft(request: Request):
    return text("Not Implemented", status=500)

@bp.get("render/:id")
async def render_draft(request: Request):
    """
    This endpoint takes the draft markdown identified by the id and renders it as HTML. No login is
    required, because these links are meant to be shared with other people for pre-post review.
    """
    return text("Not Implemented", status=500)
