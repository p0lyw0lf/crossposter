import discord
import asyncio
from discord import TextChannel, app_commands
from zoneinfo import ZoneInfo

from shared.secrets import secrets
from shared.config import config
from shared.model import Post, parse_repost_link
from poster import posting_target

GUILD = discord.Object(id=secrets["DISCORD_GUILD_ID"])
OWNER_ID = secrets["DISCORD_OWNER_ID"]


class Bot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)


intents = discord.Intents.default()
client = Bot(intents=intents)

posters = {
    target: posting_target(target, config, secrets)
    for target in config["outputs"]["bot"]
}


@client.tree.command(
    name="repost",
    description="Repost a given message!",
    guild=GUILD,
)
async def repost(
    interaction: discord.Interaction,
    # Can't be an integer, since they're too large for Discord lol
    message_id: str,
    title: str,
):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("""\
THAT'S MY PURSE! I DON'T KNOW YOU!!\
""")
        return

    if interaction.channel is None or not isinstance(interaction.channel, TextChannel):
        await interaction.response.send_message(f"""\
Must only be called from a text channel.
""")
        return

    try:
        message = await interaction.channel.fetch_message(int(message_id))
    except Exception:
        await interaction.response.send_message(f"""\
Could not get message with id {message_id}. Am I in the same channel?\
""")
        return
    try:
        repost_link = parse_repost_link(message.content)
    except Exception:
        await interaction.response.send_message("""\
Could not parse the url out of that message. Please edit and try again.\
""")
        return

    post = Post(
        title=title,
        description=None,
        tags=[],
        published=message.created_at.astimezone(
            ZoneInfo(config["timezone"])),
        repost_link=repost_link,
        body=message.content,
    )

    post_ctx = dict()
    for platform, poster in posters.items():
        try:
            # See comment in server/__init__.py
            post_ctx[platform] = await poster.post(post, post_ctx)
        except Exception as e:
            await interaction.response.send_message(
                f"Could not post to {platform}: {e}")

    await interaction.response.send_message(
        f"Successfully posted {title} to all platforms!")


@client.tree.command(
    name="awoo",
    description="awoo",
    guild=GUILD,
)
async def awoo(interaction: discord.Interaction):
    await interaction.response.send_message("awoooo!")


@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")


async def main():
    async with client:
        await client.start(secrets["DISCORD_TOKEN"], reconnect=True)

if __name__ == "__main__":
    asyncio.run(main())
