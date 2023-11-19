import asyncio
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo
from shared.model import Post, parse_main_link
from shared.secrets import secrets
from poster.github import GithubTarget


def to_datetime(timestring: str) -> datetime:
    """
    Parses a string into a timezone-aware datetime, according to the
    current timezone
    """
    dt = datetime.strptime(timestring, "%Y-%m-%d").astimezone(
        ZoneInfo(secrets["timezone"]))
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
            main_link=parse_main_link(self.body),
            title=self.title,
            body=self.body,
            published=to_datetime(self.timestring),
        )


posts = list(map(lambda t: IncompletePost(*t).to_post(), [
    ("2020-99-99", "post title", """Post Body"""),
]))


async def main():
    gh = GithubTarget(secrets)
    for post in posts:
        print(f"Posting {post.published.strftime("%Y-%m-%d")} {post.title}...")
        await gh.post(post)
    print("Complete!")


if __name__ == "__main__":
    asyncio.run(main())
