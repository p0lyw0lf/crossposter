from jinja2 import Environment, PackageLoader, select_autoescape
from shared.model import Post
from dataclasses import asdict

env = Environment(
    loader=PackageLoader(__name__),
    autoescape=select_autoescape(),
)

template = env.get_template("post.markdown.j2")


def render_post(post: Post) -> str:
    """
    Renders a post to a template
    """
    return template.render(**asdict(post))
