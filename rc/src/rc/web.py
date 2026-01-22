import json
import os

import aiofiles

WEB_FILES = os.environ.get("RC_WEB_FILES", "./web/dist")


async def get_manifest(page: str):
    async with aiofiles.open(f"{WEB_FILES}/.vite/manifest.json", "rb") as f:
        manifest = json.loads(await f.read())
    return manifest[f"src/{page}/index.tsx"]
