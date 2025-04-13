from dataclasses import asdict
import json
import os
import asyncio

from shared.model import Post
from .template import Renderable


class ScriptTarget(Renderable):
    """
    Runs a script with the given post in context.
    """

    def __init__(self, target: str, config: dict, secrets: dict):
        self.target = target
        config = config[target]
        secrets = secrets[target]

        self.script = config["path"]
        self.env = secrets["env"]

    async def post(self, post: Post, ctx: dict[str, str], **kwargs) -> str | None:
        env = os.environ.copy()
        for key, value in self.env.items():
            env[key] = value

        data = asdict(post)
        data["published"] = data["published"].timestamp() # Make serializable
        env["POST"] = json.dumps(data)

        p = await asyncio.create_subprocess_exec(self.script, env=env)
        await p.wait()
