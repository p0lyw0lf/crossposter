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
