import os
import shutil

import discord
from discord.ext import commands

from GustavSelfBot import log
from GustavSelfBot.Commands.Functions.helpers import embed


@log.catch
async def func_logs(bot: commands.Bot, ctx: commands.Context, message: discord.Message):
    logs = f"Getting logs ready... ({os.stat('_chatlogs/').st_size} bytes)"
    author = bot.user.display_name

    test = await embed(
        title="Logs!",
        description=logs,
        author=author,
        color="241f31",
        redirect="https://clashy-besi.ddns.net/api/stats",
    )

    await message.add_reaction("👍")
    await message.reply(content=test)

    msg = None
    file = None
    try:
        shutil.make_archive("_chatlogs", "zip", "_chatlogs")
        file = "_chatlogs.zip"

        msg = await embed(
            title="Success!",
            description="Successfully handled the logs.",
            author=author,
            color="241f31",
            redirect="https://clashy-besi.ddns.net/api/stats",
        )
    except (FileNotFoundError, PermissionError, TypeError) as e:
        msg = await embed(
            title="Error!",
            description="An error has occurred while handling the logs.",
            author=author,
            color="a51d2d",
            redirect="https://clashy-besi.ddns.net/api/stats",
        )
        log.error(e)
        raise Warning(e)
    finally:
        if msg is not None:
            if file is not None:
                await message.reply(content=msg, file=discord.File(file))
            else:
                await message.reply(content=msg)
        else:
            err = await embed(
                title="Error!",
                description="An error has occurred while handling the logs.",
                author=author,
                color="a51d2d",
                redirect="https://clashy-besi.ddns.net/api/stats",
            )
            await message.reply(content=err)
            log.error("An error has occurred while handling the logs.")
            raise Warning("An error has occurred while handling the logs.")
        os.remove("_chatlogs.zip")
