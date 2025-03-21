from jinja2 import Environment, PackageLoader, select_autoescape
from shared.model import Post, to_slug
from shared.config import config
from dataclasses import asdict

env = Environment(
    loader=PackageLoader(__name__),
    autoescape=select_autoescape(),
    enable_async=True,
)
env.filters["to_slug"] = to_slug


templates = {
    t: env.get_template(t)
    for t in [
        "github_cybersec.md.j2",
        "github_blog.md.j2",
        "mastodon_cybersec.txt.j2",
        "mastodon_blog.txt.j2",
        "bluesky_blog.md.j2",
    ]
}


class Renderable:
    target: str

    async def render(self, post: Post, ctx: dict[str, str]) -> str:
        """
        Renders a post to a template, based on the inheriting class.

        post: the post to render
        ctx:  the context of posts from all platforms that have been rendered
              previously. What's inside depends on the poster type, but so
              far it's used to pass completed social media URLs to the blog
              template.
        """
        template = config[self.target]["template"]
        return await templates[template].render_async(
            slug=to_slug(post),
            **asdict(post),
            **ctx,
        )

    async def post(self, post: Post, ctx: dict[str, str]) -> str | None:
        """
        Publishes a post, using `self.render` internally.

        Returns the link to the published post, if applicable.
        """
        raise NotImplementedError()
