import discord
from discord.ext import commands

from GustavSelfBot import log
from GustavSelfBot.Commands.Functions.helpers import embed


@log.catch
async def func_ping(bot: commands.Bot, ctx: commands.Context, message: discord.Message):
    ping = f"PONG: ({bot.latency} ms)"
    author = bot.user.display_name

    test = await embed(
        title="Ping!",
        description=ping,
        author=author,
        color="241f31",
        redirect="https://clashy-besi.ddns.net/api/stats",
    )

    await message.add_reaction("👍")
    await message.reply(content=test)
