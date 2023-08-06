import aiohttp
import discord
from discord.ext import commands

from GustavSelfBot import log
from GustavSelfBot.Commands.Functions.helpers import embed


@log.catch
async def func_quote(bot: commands.Bot, ctx: commands.Context, message: discord.Message):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                    url="https://clashy-besi.ddns.net/api/quote",
                    headers={"Accept": "application/json"},
            ) as resp:
                if resp.status == 200:
                    res = await resp.json()
                    quote = res.get("text")
                    author = res.get("author")

                    if quote and author:
                        test = await embed(
                            title="Quote!",
                            description=quote,
                            author=author,
                            color="241f31",
                            redirect="https://clashy-besi.ddns.net/api/quote",
                        )
                    else:
                        author = bot.user.display_name
                        test = await embed(
                            title="Error!",
                            description="An error has occurred while processing the response.",
                            author=author,
                            color="a51d2d",
                            redirect="https://clashy-besi.ddns.net/api/quote",
                        )
                else:
                    author = bot.user.display_name
                    test = await embed(
                        title="Error!",
                        description="An error has occurred while handling the request.",
                        author=author,
                        color="a51d2d",
                        redirect="https://clashy-besi.ddns.net/api/quote",
                    )
        except aiohttp.ClientError:
            author = bot.user.display_name
            test = await embed(
                title="Error!",
                description="An error has occurred while processing the request.",
                author=author,
                color="a51d2d",
                redirect="https://clashy-besi.ddns.net/api/quote",
            )

        await message.add_reaction("👍")
        await message.reply(content=test)
