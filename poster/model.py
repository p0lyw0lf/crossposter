from dataclasses import dataclass
from typing import TypeAlias
from datetime import datetime
import re

Url: TypeAlias = str

@dataclass
class Post:
    """
    Class describing all the information about a post
    """

    main_link: Url
    title: str,
    body: str
    published: datetime # absolute time, tz-aware

# Very not secure. Fortunately I think only I'll be using it?
URL_REGEX = re.compile(r"\bhttps?://[^\s]+")

def parse_main_link(body: str) -> Url:
    """
    Parses out the first url in a block of text. Used for extracting the
    `main_link` from a given `body`. Throws an error if no url is found.
    """
    match = URL_REGEX.search(body)
    if match is None:
        raise ValueError("URL not found in body!")
    return match.group(0)

