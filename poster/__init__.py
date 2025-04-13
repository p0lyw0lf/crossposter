from typing import Callable

from .bluesky import BlueskyTarget
from .chain import ChainTarget
from .github import GithubTarget
from .mastodon import MastodonTarget
from .script import ScriptTarget
from .template import Postable, Renderable

targets: dict[str, Callable[[str, dict, dict], Postable]] = {
    "bluesky": BlueskyTarget,
    "chain": ChainTarget,
    "github": GithubTarget,
    "mastodon": MastodonTarget,
    "script": ScriptTarget,
}


def mk_stub_post(self: Postable, target: str):
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
        if isinstance(self, Renderable):
            post_text = await self.render(post, ctx)
            print(target, post_text)
        else:
            print(target)
        return target
    return stub_post


def posting_target(target: str, config: dict, secrets: dict) -> Postable:
    out = None
    for target_prefix, post_class in targets.items():
        if target.startswith(target_prefix):
            out = post_class(target, config, secrets)
            break

    if out is None:
        raise ValueError(f"invalid {target=}")

    if config.get("TESTING", False):
        out.post = mk_stub_post(out, target)

    return out
