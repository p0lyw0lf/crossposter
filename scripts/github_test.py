import asyncio
from poster.github import GithubTarget
from shared.secrets import secrets
from .posts import posts


async def main():
    gh = GithubTarget(secrets)
    for post in posts:
        print(f"Posting {post.published.strftime("%Y-%m-%d")} {post.title}...")
        await gh.post(post)
    print("Complete!")


if __name__ == "__main__":
    asyncio.run(main())
