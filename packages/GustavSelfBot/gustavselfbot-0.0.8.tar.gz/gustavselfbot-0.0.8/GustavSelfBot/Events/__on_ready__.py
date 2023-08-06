from discord.ext import commands

from GustavSelfBot import log


@log.catch
async def func_on_ready(bot: commands.Bot):
    log.info(f"Logged in as {bot.user.display_name} (ID: {bot.user.id})")
