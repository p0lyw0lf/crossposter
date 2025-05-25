from base64 import b64encode
from dataclasses import asdict
from datetime import datetime
from pathlib import PurePosixPath
from typing import Any

from githubkit import GitHub, TokenAuthStrategy
from zoneinfo import ZoneInfo
import frontmatter

from poster.model import Post, to_slug
from .template import Renderable


class GithubTarget(Renderable):

    def __init__(self, target: str, config: dict, secrets: dict):
        super().__init__(target, config, secrets)

        self.tz = ZoneInfo(config["timezone"])
        config = config[target]
        secrets = secrets[target]
        self.gh = GitHub(TokenAuthStrategy(secrets["GITHUB_TOKEN"]))
        self.owner = config["GITHUB_USERNAME"]
        self.repo = config["GITHUB_REPO"]
        self.branch = config["GITHUB_BRANCH"]
        self.output_dir = PurePosixPath(config["GITHUB_OUTPUT_DIR"])

    async def post(self, post: Post, ctx: dict[str, str]) -> str | None:
        slug = to_slug(post)
        filename = self.output_dir / f"{slug}.md"

        # Make copy so this modification doesn't destroy anything
        post = Post(**asdict(post))
        if post.repost_link:
            post.body = post.body.replace(post.repost_link, "")
        post.body = post.body.replace("\r", "").strip()
        content = await self.render(post, ctx)

        response = await self.gh.rest.repos.\
            async_create_or_update_file_contents(
                self.owner,
                self.repo,
                str(filename),
                message=post.title,
                content=b64encode(content.encode('utf-8')).decode('utf-8'),
                sha=ctx.get(self.target, None),
                branch=self.branch,
            )

        if response.status_code not in {200, 201}:
            raise ValueError(f"GitHub API response: {response.text}")

        # We return the blob's sha so that later passes' API calls to update
        # will be correctly-formed
        if (content := response.parsed_data.content) and (sha := content.sha):
            return sha

    async def from_slug(self, slug: str) -> Post | None:
        """
        Given a slug, read the post contents. Assumes all relevant metadata is present in the frontmatter.
        """
        filename = self.output_dir / f"{slug}.md"

        response = await self.gh.rest.repos.\
            async_get_content(
                self.owner,
                self.repo,
                str(filename),
                ref=self.branch,
                headers={
                    "Accept": "application/vnd.github.raw+json",
                },
            )

        if response.status_code not in {200, 201}:
            raise ValueError(f"GitHub API response: {response.text}")

        meta, body = frontmatter.parse(response.content.decode("utf-8"))
        meta: dict[str, Any] = meta

        if timestamp := meta.get("published", None) is not None:
            published = datetime.fromtimestamp(timestamp)
        else:
            published = datetime.now(tz=self.tz)

        return Post(
            title=meta["title"],
            description=meta.get("description", None),
            tags=meta.get("tags", []),
            published=published,
            repost_link=meta.get("repost_link", None),
            body=body,
        )
