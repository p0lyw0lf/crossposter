from .template import Renderable
from .github import GithubTarget
from .mastodon import MastodonTarget


def posting_target(target: str, config: dict, secrets: dict) -> Renderable:
    if target.startswith("github"):
        return GithubTarget(target, config, secrets)
    elif target.startswith("mastodon"):
        return MastodonTarget(target, secrets)
    else:
        raise ValueError(f"invalid {target=}")
