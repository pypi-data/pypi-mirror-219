import discord

from GustavSelfBot import log, Config, bot

if __name__ == "__main__":
    try:
        bot.run(token=Config["token"], log_handler=None)
    except discord.errors.LoginFailure as e:
        log.error(e)
        raise Exception(e)
