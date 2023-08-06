import discord
from discord.ext import commands

from GustavSelfBot import log

from GustavSelfBot.Events import func_on_message, func_on_ready

# from GustavSelfBot.Events import func_on_voice_state_update

bot = commands.Bot(command_prefix=">", self_bot=True)


@log.catch
@bot.event
async def on_ready():
    await func_on_ready(bot)


@log.catch
@bot.event
async def on_message(message: discord.Message):
    await func_on_message(bot, message)

# @log.catch
# @bot.event
# async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
#     await func_on_voice_state_update(bot, member, before, after)
