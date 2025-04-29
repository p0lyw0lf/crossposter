from poster.config import config
from poster.secrets import secrets
from poster.mastodon import MastodonTarget
import asyncio
from .posts import posts


async def main():
    m = MastodonTarget("mastodon_blog", config, secrets)
    for post in posts:
        print(f"Posting {post.published.strftime('%Y-%m-%d')} {post.title}...")
        await m.post(post, {})
    print("Complete!")

if __name__ == "__main__":
    asyncio.run(main())
