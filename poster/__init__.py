from .bluesky import BlueskyTarget
from .github import GithubTarget
from .mastodon import MastodonTarget
from .template import Renderable


def mk_stub_post(self: Renderable, target: str):
    """
    For testing, we won't want to have the posts be live. However, we still
    want to be able to make sure the input mechanism works, so we'll just
    stub the output mechanism.

    There's probably a way to make this stub more lower-level, but there's
    the tradeoff of "it's useful to have just all the logic in one `post()`
    function", where making more complicated abstractions is overkill, so I'm
    going to keep it that way for now.
    """
    async def stub_post(post, ctx: dict[str, str]) -> str:
        post_text = await self.render(post, ctx)
        print(target, post_text)
        return target
    return stub_post


def posting_target(target: str, config: dict, secrets: dict) -> Renderable:
    out = None
    if target.startswith("github"):
        out = GithubTarget(target, config, secrets)
    elif target.startswith("mastodon"):
        out = MastodonTarget(target, config, secrets)
    elif target.startswith("bluesky"):
        out = BlueskyTarget(target, config, secrets)

    if out is None:
        raise ValueError(f"invalid {target=}")

    if config.get("TESTING", False):
        out.post = mk_stub_post(out, target)

    return out
