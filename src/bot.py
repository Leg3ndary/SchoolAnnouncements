"""
The discord bot file, this is how we connect to discord
"""

import asyncio
import datetime
import json
from typing import List

import aiohttp
import discord
from client import Wrapper
from aphs_client import APHSClient
from colorama import Fore, Style
from discord.ext import commands, tasks

with open("credentials/config.json", "r", encoding="utf8") as credentials:
    config = json.loads(credentials.read())

bot = APHSClient()
announcements = Wrapper()

announcements_group: discord.app_commands.Group = discord.app_commands.Group(
    name="announcements", description="Announcements related commands"
)


@announcements_group.command(name="latest", description="Get the latest announcements")
async def announcements_today_cmd(interaction: discord.Interaction) -> None:
    """
    Show the latest announcements
    """
    latest = await announcements.get_latest()

    announcement_date = datetime.datetime.fromtimestamp(latest.get("timestamp"))

    embed = discord.Embed(
        title=f"{announcement_date.strftime('%A %B %d')}",
        timestamp=discord.utils.utcnow(),
        color=discord.Color.blue(),
    )
    for name, announcement in latest.items():
        if name != "timestamp":
            embed.add_field(name=name, value=announcement, inline=False)
    await interaction.response.send_message(embed=embed)


async def on_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[discord.app_commands.Choice[str]]:
    """
    The autocomplete function for specific days
    """
    return [
        discord.app_commands.Choice(name=choice, value=choice)
        for choice in announcements.choices
        if current.lower() in choice.lower()
    ][:25]


@announcements_group.command(name="on", description="Announcements on a specific day")
@discord.app_commands.autocomplete(day=on_autocomplete)
async def announcements_on_cmd(interaction: discord.Interaction, day: str) -> None:
    """
    Show a certain days announcements
    """
    days_announcements = announcements.latest.get(
        day, {"No Announcements": "No Announcements"}
    )

    embed = discord.Embed(
        title=f"{day} Announcements",
        timestamp=discord.utils.utcnow(),
        color=discord.Color.blue(),
    )
    for name, announcement in days_announcements.items():
        if name != "timestamp":
            embed.add_field(name=name, value=announcement, inline=False)
    await interaction.response.send_message(embed=embed)


@tasks.loop(
    time=datetime.time(hour=13, minute=55, second=0)
)  # This is the equivalent of 8:55am EST
async def update_announcements() -> None:
    """
    Update our announcements documents every day at 8:55am EST
    """
    if datetime.datetime.now().weekday() in (5, 6):
        return
    await announcements.save_doc()
    await announcements.update_latest()
    print(f"{Fore.CYAN}Updated latest announcements{Style.RESET_ALL}")

    webhook = discord.Webhook.from_url(
        url=bot.config.get("Bot").get("AnnouncementsWebhook"), session=bot.session
    )

    latest = await announcements.get_latest()

    announcement_date = datetime.datetime.fromtimestamp(latest.get("timestamp"))

    embed = discord.Embed(
        title=f"{announcement_date.strftime('%A %B %d')}",
        timestamp=discord.utils.utcnow(),
        color=discord.Color.blue(),
    )
    for name, announcement in latest.items():
        if name != "timestamp":
            embed.add_field(name=name, value=announcement, inline=False)

    await webhook.send(embed=embed)


bot.tree.add_command(announcements_group)


@bot.event
async def on_ready() -> None:
    """
    On ready tell us and set everything up, then start an update loop to update data and run through it!
    """
    await bot.wait_until_ready()
    print(f"{Fore.CYAN}Bot {bot.user} has logged on.{Style.RESET_ALL}")

    await announcements.save_doc()
    # Sometimes it doesn't finish updating and displays old stuff so I we add a short delay even though it's awaited before
    await asyncio.sleep(5)
    await announcements.update_latest()
    print(f"{Fore.GREEN}Finished Saving and Updating Data.{Style.RESET_ALL}")
    update_announcements.start()


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
    """
    On command error print it so I can actually see what's happening
    """
    print(error)


async def start_bot() -> None:
    """
    Start the bot with everything it needs
    """
    async with bot:
        bot.config = config
        bot.session = aiohttp.ClientSession()

        await bot.start(config.get("Bot").get("Token"))


asyncio.run(start_bot())
