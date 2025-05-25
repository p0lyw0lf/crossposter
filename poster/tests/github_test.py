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

async def test_updating():
    gh = GithubTarget("github_blog", config, secrets)
    post = posts[0]
    print(f"Posting initial {post.title}")
    sha_0 = await gh.post(post, {})
    print(f"First post: {sha_0}")
    await asyncio.sleep(5) # So as to not spam endpoint
    print(f"Posting updated {post.title}")
    sha_1 = await gh.post(post, {"github_blog": sha_0, "bluesky_blog": "bluesky", "mastodon_blog": "mastodon"})
    print(f"Second post: {sha_1}")

async def test_reading():
    gh = GithubTarget("github_blog", config, secrets)
    slug = "2024-09-28-Write-Your-Own-Tools"
    post = await gh.from_slug(slug)
    print(post)


async def main():
    await test_reading()
    # await test_posting()
    await test_updating()

if __name__ == "__main__":
    asyncio.run(main())
