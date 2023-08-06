# import os
# import asyncio
import discord
from discord.ext import commands

# from datetime import datetime
from GustavSelfBot import log


# @log.catch
# async def save_recording(audio_source):
#     # Save the recorded audio to an MP3 file with a unique filename
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     folder = "_recordings"
#     if not os.path.exists(folder):
#         os.makedirs(folder)
#
#     filename = f"{folder}/recording_{timestamp}.mp3"
#
#     ffmpeg_options = {
#         "options": "-vn -ar 44100 -ac 2 -b:a 192k",
#         "executable": "ffmpeg",
#         "pipe": True,
#     }
#
#     try:
#         await asyncio.create_subprocess_shell(
#             f'ffmpeg -i "{audio_source}" {ffmpeg_options["options"]} "{filename}"',
#             stdout=asyncio.subprocess.PIPE,
#             stderr=asyncio.subprocess.PIPE,
#             executable=ffmpeg_options["executable"],
#         )
#         log.info("Recording saved.")
#     except Exception as e:
#         log.error(f"Error converting recording to MP3: {str(e)}")


@log.catch
async def func_on_voice_state_update(bot: commands.Bot, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    # if member.id == bot.user.id:
    #     if after.channel is not None:
    #         log.info(
    #             f"{member.display_name} (ID: {member.id}) Joined VC: {after.channel.name} {after.channel.guild.name} (ID: {after.channel.guild.id})"
    #         )
    #         channel: discord.VoiceChannel = bot.get_channel(after.channel.id)
    #
    #         await asyncio.sleep(5)
    #
    #         if before.channel == after.channel:
    #             log.warning(
    #                 f"{member.display_name} (ID: {member.id}) Already in VC: {after.channel.name} {after.channel.guild.name} (ID: {after.channel.guild.id})"
    #             )
    #             return
    #
    #         voice_client = discord.utils.get(bot.voice_clients, guild=channel.guild)
    #         if voice_client and voice_client.is_connected():
    #             await voice_client.disconnect(force=True)
    #
    #         if not voice_client or not voice_client.is_connected():
    #             connect: discord.VoiceClient = await channel.connect(self_mute=True)
    #             log.info(
    #                 f"{member.display_name} (ID: {member.id}) Reconnected to VC: {after.channel.name} {after.channel.guild.name} (ID: {after.channel.guild.id})"
    #             )
    #
    #         await asyncio.sleep(1)
    #
    #         voice_client = discord.utils.get(bot.voice_clients, guild=channel.guild)
    #
    #         if not voice_client.is_connected():
    #             log.error(
    #                 f"{member.display_name} (ID: {member.id}) Failed to reconnect to VC: {after.channel.name} {after.channel.guild.name} (ID: {after.channel.guild.id})"
    #             )
    #             return
    #
    #         audio_source = discord.FFmpegOpusAudio(source=connect.source.read(), bitrate=192)  # Set the audio source to the voice client
    #         recording_started = True
    #         recording_duration = 0
    #
    #         while True:
    #             # Check if there are any other users in the voice channel
    #             users_in_vc = len(channel.members) - 1  # Exclude bot user
    #
    #             if users_in_vc == 0:
    #                 await voice_client.disconnect(force=True)
    #                 await save_recording(audio_source)
    #                 log.info("Recording finished and saved.")
    #                 break
    #
    #             if recording_started and recording_duration >= 300:  # 5 minutes
    #                 await save_recording(audio_source)
    #                 log.info("Partial recording saved.")
    #
    #                 # Reset the audio source for the next 5-minute interval
    #                 audio_source = discord.FFmpegOpusAudio(source=voice_client.source, bitrate=192)  # Set the audio source to the voice client
    #                 recording_duration = 0
    #
    #             # Increase the recording duration
    #             recording_duration += 1
    #
    #             await asyncio.sleep(1)  # Check every 1 second

    pass
