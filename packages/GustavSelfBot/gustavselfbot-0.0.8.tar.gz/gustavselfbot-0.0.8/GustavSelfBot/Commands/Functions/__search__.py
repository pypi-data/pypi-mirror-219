import os
import discord
import json
from discord.ext import commands

from GustavSelfBot import log
from GustavSelfBot.Commands.Functions.helpers import embed


@log.catch
async def func_search(bot: commands.Bot, ctx: commands.Context, message: discord.Message):
    search_query = message.content.split(" ", 1)[1]
    logs = f"Searching logs with: {search_query} ..."
    author = bot.user.display_name

    test = await embed(
        title="Search!",
        description=logs,
        author=author,
        color="241f31",
        redirect="https://clashy-besi.ddns.net/api/stats",
    )

    await message.add_reaction("👍")
    await message.reply(content=test)

    logs_directory = "_chatlogs"
    search_results = []

    for root, dirs, files in os.walk(logs_directory):
        for file in files:
            if file.endswith(".log"):
                log_file = os.path.join(root, file)

                with open(log_file, "r") as f:
                    lines = f.readlines()

                for line in lines:
                    if search_query in line:
                        # Get the channel and guild information
                        parts = log_file.split("/")
                        guild_info = parts[-3]
                        channel_info = parts[-2]

                        entry = {
                            "guild": guild_info,
                            "channel": channel_info,
                            "message": line.strip()
                        }

                        search_results.append(entry)

    if len(search_results) > 0:
        msg = await embed(
            title="Success!",
            description="Successfully found entries.",
            author=author,
            color="241f31",
            redirect="https://clashy-besi.ddns.net/api/stats",
        )
        json_file = f"search_results_{search_query}.json"
        with open(json_file, "w") as f:
            json.dump(search_results, f, indent=4)

        await message.reply(content=msg, file=discord.File(json_file))

        os.remove(json_file)
    else:
        err = await embed(
            title="Error!",
            description=f"No matching logs found for `{search_query}`.",
            author=author,
            color="a51d2d",
            redirect="https://clashy-besi.ddns.net/api/stats",
        )
        await message.reply(content=err)
        log.error("An error has occurred while handling the logs.")
        raise Warning("An error has occurred while handling the logs.")
