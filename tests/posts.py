from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo
from shared.model import Post, parse_repost_link
from shared.config import config


def to_datetime(timestring: str) -> datetime:
    """
    Parses a string into a timezone-aware datetime, according to the
    current timezone
    """
    dt = datetime.strptime(timestring, "%Y-%m-%d").astimezone(
        ZoneInfo(config["timezone"]))
    dt.replace(hour=12, minute=0, second=0)
    return dt


@dataclass
class IncompletePost:
    timestring: str
    title: str
    body: str

    def to_post(self) -> Post:
        """
        Creates a full `Post` out of the `IncompletePost`
        """
        return Post(
            title=self.title,
            description=None,
            tags=[],
            published=to_datetime(self.timestring),
            repost_link=parse_repost_link(self.body),
            body=self.body,
        )


posts = list(map(lambda t: IncompletePost(*t).to_post(), [
    # ("2020-99-99", "post title", """Post Body"""),
    ("2023-11-18", "testing post title",
     """random post body https://wolfgirl.dev/cybersec/""")
]))
