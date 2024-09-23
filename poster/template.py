from jinja2 import Environment, PackageLoader, select_autoescape
from shared.model import Post
from shared.config import config
from dataclasses import asdict

env = Environment(
    loader=PackageLoader(__name__),
    autoescape=select_autoescape(),
    enable_async=True,
)


templates = {
    t: env.get_template(t)
    for t in [
        "cybersec_post.md.j2",
        "blog_post.md.j2",
        "post.txt.j2",
    ]
}


class Renderable:
    target: str

    async def render(self, post: Post) -> str:
        """
        Renders a post to a template, based on the inheriting class
        """
        template = config[self.target].template
        return await templates[template].render_async(**asdict(post))
