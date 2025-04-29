import asyncio
from poster.github import GithubTarget
from poster.config import config
from poster.secrets import secrets
from .posts import posts


async def test_posting():
    gh = GithubTarget("github_cybersec", config, secrets)
    for post in posts:
        print(f"Posting {post.published.strftime('%Y-%m-%d')} {post.title}...")
        await gh.post(post, {})
    print("Complete!")


async def test_reading():
    gh = GithubTarget("github_blog", config, secrets)
    slug = "2024-09-28-Write-Your-Own-Tools"
    post = await gh.from_slug(slug)
    print(post)


async def main():
    await test_reading()
    # test_posting()

if __name__ == "__main__":
    asyncio.run(main())
