from shared.secrets import secrets
from poster.mastodon import MastodonTarget
import asyncio
from .posts import posts


async def main():
    m = MastodonTarget(secrets)
    for post in posts:
        print(f"Posting {post.published.strftime("%Y-%m-%d")} {post.title}...")
        await m.post(post)
    print("Complete!")

if __name__ == "__main__":
    asyncio.run(main())
