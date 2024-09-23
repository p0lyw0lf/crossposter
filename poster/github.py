from dataclasses import asdict
from githubkit import GitHub, TokenAuthStrategy
from shared.model import Post
from pathlib import PurePosixPath
import re
from base64 import b64encode
from .template import Renderable

# Regex of all non-url-safe characters to be replaced with "-"
UNSAFE_REGEX = re.compile(r"[^a-zA-Z0-9]+")


def to_slug(post: Post) -> str:
    """
    Given a post, generates a title slug for it

    Resulting slugs will look like "2023-01-02-some-title"
    """
    safe_title = UNSAFE_REGEX.subn("-", post.title)[0]
    return f"{post.published.strftime('%Y-%m-%d')}-{safe_title}"


class GithubTarget(Renderable):

    def __init__(self, prefix: str, config: dict, secrets: dict):
        config = config[prefix]
        secrets = secrets[prefix]
        self.gh = GitHub(TokenAuthStrategy(secrets["GITHUB_TOKEN"]))
        self.owner = config["GITHUB_USERNAME"]
        self.repo = config["GITHUB_REPO"]
        self.branch = config["GITHUB_BRANCH"]
        self.output_dir = PurePosixPath(config["GITHUB_OUTPUT_DIR"])

    async def post(self, post: Post):
        filename = self.output_dir / f"{to_slug(post)}.md"
        # Make copy so this modification doesn't destroy anything
        post = Post(**asdict(post))
        post.body = post.body.replace(post.main_link, "").strip()
        content = self.render(post)

        response = await self.gh.rest.repos.\
            async_create_or_update_file_contents(
                self.owner,
                self.repo,
                filename,
                message=post.title,
                content=b64encode(content.encode('utf-8')).decode('utf-8'),
                branch=self.branch,
            )

        if response.status_code not in {200, 201}:
            raise ValueError(f"error posting to github: {response.text}")
