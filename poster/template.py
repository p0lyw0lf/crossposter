from jinja2 import Environment, PackageLoader, select_autoescape
from shared.model import Post
from dataclasses import asdict

env = Environment(
    loader=PackageLoader(__name__),
    autoescape=select_autoescape(),
)

class_to_template = {
    "GithubTarget": "post.md.j2",
    "MastodonTarget": "post.txt.j2",
}

class_to_template = {
    c: env.get_template(t)
    for c, t in class_to_template.items()
}


class Renderable:

    def render(self, post: Post) -> str:
        """
        Renders a post to a template, based on the inheriting class
        """
        return class_to_template[type(self).__name__].render(**asdict(post))
