from githubkit import GitHub, TokenAuthStrategy
from shared.model import Post
from pathlib import PurePosixPath
import re
from base64 import b64encode

from .template import render_post


# Regex of all non-url-safe characters to be replaced with "-"
UNSAFE_REGEX = re.compile(r"[^a-zA-Z0-9]+")


def to_slug(post: Post) -> str:
    """
    Given a post, generates a title slug for it

    Resulting slugs will look like "2023-01-02-some-title"
    """
    safe_title = UNSAFE_REGEX.subn("-", post.title)[0]
    return f"{post.published.strftime("%Y-%m-%d")}-{safe_title}"


class GithubTarget:

    def __init__(self, secrets: dict):
        self.gh = GitHub(TokenAuthStrategy(secrets["GITHUB_TOKEN"]))
        self.owner = secrets["GITHUB_USERNAME"]
        self.repo = secrets["GITHUB_REPO"]
        self.branch = secrets["GITHUB_BRANCH"]
        self.output_dir = PurePosixPath(secrets["GITHUB_OUTPUT_DIR"])

    async def post(self, post: Post):
        filename = self.output_dir / f"{to_slug(post)}.mdx"
        post.body = post.body.replace(post.main_link, "").strip()
        content = render_post(post)

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
