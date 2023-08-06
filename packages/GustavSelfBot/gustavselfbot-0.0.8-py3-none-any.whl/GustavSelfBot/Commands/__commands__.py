import aiohttp.client_exceptions
import discord
from discord.ext import commands

from GustavSelfBot import log

from GustavSelfBot.Commands.Functions import func_ping, func_quote, func_logs, func_search


@log.catch
async def _blacklist(ctx: commands.Context):
    pass


@log.catch
async def ping(bot: commands.Bot, ctx: commands.Context, message: discord.Message):
    log.info(f"Command {message.content.replace('>', '')} called by {ctx.author.display_name} (ID: {ctx.author.id})")
    try:
        await func_ping(bot, ctx, message)
    except (discord.errors.ClientException, aiohttp.client_exceptions.ClientOSError) as e:
        log.error(e)
        await ctx.send("Error")
        raise Exception(e)


@log.catch
async def quote(bot: commands.Bot, ctx: commands.Context, message: discord.Message):
    log.info(f"Command {message.content.replace('>', '')} called by {ctx.author.display_name} (ID: {ctx.author.id})")
    try:
        await func_quote(bot, ctx, message)
    except (discord.errors.ClientException, aiohttp.client_exceptions.ClientOSError) as e:
        log.error(e)
        await ctx.send("Error")
        raise Exception(e)


@log.catch
async def logs(bot: commands.Bot, ctx: commands.Context, message: discord.Message):
    log.info(f"Command {message.content.replace('>', '')} called by {ctx.author.display_name} (ID: {ctx.author.id})")
    try:
        await func_logs(bot, ctx, message)
    except (discord.errors.ClientException, aiohttp.client_exceptions.ClientOSError) as e:
        log.error(e)
        await ctx.send("Error")
        raise Exception(e)


@log.catch
async def search(bot: commands.Bot, ctx: commands.Context, message: discord.Message):
    log.info(f"Command {message.content.replace('>', '')} called by {ctx.author.display_name} (ID: {ctx.author.id})")
    try:
        await func_search(bot, ctx, message)
    except (discord.errors.ClientException, aiohttp.client_exceptions.ClientOSError) as e:
        log.error(e)
        await ctx.send("Error")
        raise Exception(e)
