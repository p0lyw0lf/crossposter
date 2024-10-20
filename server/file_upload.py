import asyncio
import tempfile
import traceback

import boto3
from sanic.response import text
from sanic import Blueprint, Request

from shared.secrets import secrets
from .auth import login_required

bp = Blueprint("file_upload", url_prefix="/upload")
s3 = None
bucket_name = None
try:
    s3 = boto3.client(
        service_name="s3",
        region_name=secrets["AWS_REGION_NAME"],
        aws_access_key_id=secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=secrets["AWS_SECRET_ACCESS_KEY"],
    )
    bucket_name = secrets["AWS_BUCKET_NAME"]
except Exception:
    print(traceback.format_exc())


@bp.post("/", stream=True)
@login_required
async def upload(request: Request, username: str):
    if s3 is None or bucket_name is None:
        return text("not implemented", status=501)

    file_name = request.args.get("f", None)
    if not file_name:
        return text("file name not provided", status=400)
    file_name = f"{username}/{file_name}"

    with tempfile.NamedTemporaryFile("wb+") as f:
        # Step 1: read streamed data into file
        while True:
            body = await request.stream.read()
            if body is None:
                break
            await asyncio.to_thread(f.write, body)

        # Step 2: upload file to S3
        f.seek(0)
        await asyncio.to_thread(
            s3.upload_fileobj,
            f, bucket_name, file_name,
        )

    return text(f"https://{bucket_name}/{file_name}")
