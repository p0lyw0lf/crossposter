from dataclasses import asdict
from githubkit import GitHub, TokenAuthStrategy
from shared.model import Post, to_slug
from pathlib import PurePosixPath
from base64 import b64encode
from .template import Renderable


class GithubTarget(Renderable):

    def __init__(self, target: str, config: dict, secrets: dict):
        self.target = target
        config = config[target]
        secrets = secrets[target]
        self.gh = GitHub(TokenAuthStrategy(secrets["GITHUB_TOKEN"]))
        self.owner = config["GITHUB_USERNAME"]
        self.repo = config["GITHUB_REPO"]
        self.branch = config["GITHUB_BRANCH"]
        self.output_dir = PurePosixPath(config["GITHUB_OUTPUT_DIR"])

    async def post(self, post: Post, ctx: dict[str, str]):
        filename = self.output_dir / f"{to_slug(post)}.md"
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
                filename,
                message=post.title,
                content=b64encode(content.encode('utf-8')).decode('utf-8'),
                branch=self.branch,
            )

        if response.status_code not in {200, 201}:
            raise ValueError(f"error posting to github: {response.text}")
