from mastodon import Mastodon
import asyncio

from poster.model import Post
from .template import Renderable


class MastodonTarget(Renderable):
    def __init__(self, target: str, config: dict, secrets: dict):
        super().__init__(target, config, secrets)

        config = config[target]
        secrets = secrets[target]
        self.m = Mastodon(
            api_base_url=secrets["MASTODON_BASE_URL"],
            access_token=secrets["MASTODON_TOKEN"],
        )
        self.add_tags = bool(config.get("add_tags", False))

    async def post(self, post: Post, ctx: dict[str, str]) -> str:
        post_text = await self.render(post, ctx)
        if self.add_tags and post.tags:
            # Add all tags to the rendered post, like #tag1 #tag2
            post_text += "\n\n"
            for i in range(len(post.tags)):
                if i > 0:
                    post_text += " "
                tag = post.tags[i]
                post_text += f"#{tag}"
        toot = await asyncio.to_thread(
            self.m.toot,
            post_text,
        )
        return toot["url"]
