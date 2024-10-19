from .bluesky import BlueskyTarget
from .github import GithubTarget
from .mastodon import MastodonTarget
from .template import Renderable


def posting_target(target: str, config: dict, secrets: dict) -> Renderable:
    if target.startswith("github"):
        return GithubTarget(target, config, secrets)
    elif target.startswith("mastodon"):
        return MastodonTarget(target, config, secrets)
    elif target.startswith("bluesky"):
        return BlueskyTarget(target, config, secrets)
    else:
        raise ValueError(f"invalid {target=}")
