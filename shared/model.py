from dataclasses import dataclass
from typing import TypeAlias
from datetime import datetime
import re
from typing import Optional

Url: TypeAlias = str


@dataclass
class Post:
    """
    Class describing all the information about a post
    """

    title: str
    description: Optional[str]
    tags: list[str]
    published: datetime  # absolute time, tz-aware
    repost_link: Optional[Url]
    body: str


# Very not secure. Fortunately I think only I'll be using it?
URL_REGEX = re.compile(r"\bhttps?://[^\s]+")


def parse_repost_link(body: str) -> Url:
    """
    Parses out the first url in a block of text. Used for extracting the
    `repost_link` from a given `body`. Throws an error if no url is found.
    """
    match = URL_REGEX.search(body)
    if match is None:
        raise ValueError("URL not found in body!")
    return match.group(0)


# Regex of all non-url-safe characters to be replaced with "-"
UNSAFE_REGEX = re.compile(r"[^a-zA-Z0-9]+")


def to_slug(post: Post) -> str:
    """
    Given a post, generates a title slug for it

    Resulting slugs will look like "2023-01-02-some-title"
    """
    safe_title = UNSAFE_REGEX.subn("-", post.title)[0]
    return f"{post.published.strftime('%Y-%m-%d')}-{safe_title}"
