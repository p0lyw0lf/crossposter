from mastodon import Mastodon
import asyncio

from shared.model import Post
from .template import Renderable


class MastodonTarget(Renderable):
    def __init__(self, target: str, config: dict, secrets: dict):
        self.target = target
        config = config[target]
        secrets = secrets[target]
        self.m = Mastodon(
            api_base_url=secrets["MASTODON_BASE_URL"],
            access_token=secrets["MASTODON_TOKEN"],
        )

    async def post(self, post: Post):
        await asyncio.to_thread(
            self.m.toot,
            await self.render(post),
        )
