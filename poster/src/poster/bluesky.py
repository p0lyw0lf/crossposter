import asyncio

from atproto import Client
from atproto import client_utils
import mistletoe
from mistletoe.base_renderer import BaseRenderer

from poster.model import Post
from .template import Renderable


class BlueskyTarget(Renderable):
    def __init__(self, target: str, config: dict, secrets: dict):
        super().__init__(target, config, secrets)

        config = config[target]
        secrets = secrets[target]
        self.client = Client(secrets["BLUESKY_HOMESERVER"])
        self.client.login(
            login=secrets["BLUESKY_USERNAME"],
            password=secrets["BLUESKY_PASSWORD"],
        )
        self.add_tags = bool(config.get("add_tags", False))

    async def post(self, post: Post, ctx: dict[str, str], **kwargs):
        post_text = await self.render(post, ctx)
        builder: client_utils.TextBuilder = mistletoe.markdown(
            post_text, BlueskyRenderer)
        if self.add_tags and post.tags:
            # Add all tags as a sequence of tagged strings like #tag1 #tag2
            builder.text("\n\n")
            for i in range(len(post.tags)):
                if i > 0:
                    builder.text(" ")
                tag = post.tags[i]
                builder.tag(f"#{tag}", tag)
        toot = await asyncio.to_thread(
            self.client.send_post,
            builder,
        )
        return toot["uri"]


class BlueskyRenderer(BaseRenderer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.builder = client_utils.TextBuilder()
        self.has_paragraph = False

    def render_inner(self, token):
        for token in token.children:
            self.render(token)
        return self.builder

    def render_raw_text(self, token):
        return self.builder.text(token.content)

    def render_line_break(self, token):
        return self.builder.text("\n")

    def render_paragraph(self, token):
        if self.has_paragraph:
            self.builder.text("\n\n")
        self.has_paragraph = True
        return self.render_inner(token)

    def render_link(self, token):
        return self.builder.link(token.title, token.target)

    def render_auto_link(self, token):
        return self.builder.link(token.target, token.target)
