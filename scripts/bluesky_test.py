from shared.config import config
from shared.secrets import secrets
from poster.bluesky import BlueskyTarget
import asyncio
from .posts import posts


async def main():
    m = BlueskyTarget("bluesky_blog", config, secrets)
    for post in posts:
        print(f"Posting {post.published.strftime("%Y-%m-%d")} {post.title}...")
        await m.post(post)
    print("Complete!")

if __name__ == "__main__":
    asyncio.run(main())
