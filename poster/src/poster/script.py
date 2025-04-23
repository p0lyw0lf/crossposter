from dataclasses import asdict
import json
import os
import asyncio

from poster.model import Post
from .template import Postable


class ScriptTarget(Postable):
    """
    Runs a script with the given post in context.
    """

    def __init__(self, target: str, config: dict, secrets: dict):
        super().__init__(target, config, secrets)

        config = config[target]
        secrets = secrets[target]

        self.script = config["path"]
        self.env = secrets["env"]

    async def post(self, post: Post, ctx: dict[str, str]) -> str | None:
        return await self.run_script(post)

    async def run_script(self, post: Post | None = None):
        env = os.environ.copy()
        for key, value in self.env.items():
            env[key] = value

        if post is not None:
            data = asdict(post)
            # Make serializable
            data["published"] = data["published"].timestamp()
            env["POST"] = json.dumps(data)

        p = await asyncio.create_subprocess_exec(self.script, env=env)
        await p.wait()
        if p.returncode != 0:
            raise Exception(f"process failed with exit code {p.returncode}")
