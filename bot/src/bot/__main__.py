import discord
import asyncio
from discord import TextChannel, app_commands
from zoneinfo import ZoneInfo

from poster.secrets import secrets
from poster.config import config
from poster.model import Post, parse_repost_link
from poster.dispatch import posting_target

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
poster = posting_target(config["outputs"]["bot"], config, secrets)


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

    response = await interaction.response.send_message("はい、ご主人さま～")
    if response.message_id is None:
        raise Exception("huh?")

    try:
        await poster.post(post, dict())
    except Exception as e:
        await interaction.followup.edit_message(response.message_id,
            content=f"Error making post: {e}")
        return

    await interaction.followup.edit_message(response.message_id, content=f"Successfully posted {title} to all platforms!")


@client.tree.command(
    name="awoo",
    description="awoo",
    guild=GUILD,
)
async def awoo(interaction: discord.Interaction):
    response = await interaction.response.send_message("awoo-ing begins in 10 seconds")
    if response.message_id is None:
        raise Exception("huh?")
    await asyncio.sleep(9)
    prefix = "awoooo"
    suffix = "!"
    for i in range(5):
        await asyncio.sleep(1)
        await interaction.followup.edit_message(response.message_id, content=prefix+"o"*i+suffix)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")


async def main():
    async with client:
        await client.start(secrets["DISCORD_TOKEN"], reconnect=True)

if __name__ == "__main__":
    asyncio.run(main())
