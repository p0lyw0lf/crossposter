from mastodon import Mastodon
from shared.model import Post
import asyncio
from .template import Renderable


class MastodonTarget(Renderable):
    def __init__(self, prefix: str, secrets: dict):
        secrets = secrets[prefix]
        self.m = Mastodon(
            api_base_url=secrets["MASTODON_BASE_URL"],
            access_token=secrets["MASTODON_TOKEN"],
        )

    async def post(self, post: Post):
        await asyncio.to_thread(
            self.m.toot,
            self.render(post),
        )
