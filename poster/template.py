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

    async def render(self, post: Post) -> str:
        """
        Renders a post to a template, based on the inheriting class
        """
        template = config[self.target]["template"]
        return await templates[template].render_async(
            slug=to_slug(post),
            **asdict(post),
        )
