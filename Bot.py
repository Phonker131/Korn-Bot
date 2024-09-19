"""Music Bot for Discord with the ability to change roles using emoji's under the selected message
   Shapoval Tymur, I. year
   Winter semester 2022/23
   Programování I. NPRG030
"""
# imports for bot
import discord
from discord.ext import commands
from discord import utils
from youtube_dl import YoutubeDL
from functools import partial
import datetime
import Config
from discord.ext.tasks import loop

# YouTube DL and Ffmpeg options
YDL_OPTIONS = {
    "format": "worstaudio/best",
    "noplaylist": "False",
    "simulate": "True",
    "key": "FFmpegExtractAudio",
}
FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

# Bot permissions
intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True
intents.message_content = True
intents.emojis_and_stickers = True

client = commands.Bot(command_prefix="h!", intents=intents)   # Setting command prefix and permissions

current_song = None  # Setting variable for current song
queue = []  # Setting variable for queue
vc = None   # Setting variable for voice channel connection

last_activity = None  # Setting variable for last activity of bot


# Checking inactivity and if bot isn't used more than 3 mins disconnecting from voice channel
@loop(seconds=1)  # Setting loop that will check connection every second
async def check_inactivity():
    """
    param last_activity: gets current time
    param vc: gets method disconnect() and sets to None
    param queue: Sets to empty list
    return: removing role from member after removing emoji from selected message
    """
    global last_activity, vc, queue  # last_activity: datetime.datetime, vc: discord.voice_client.VoiceClient, queue: list
    if vc and vc.is_connected() and not vc.is_playing():  # Checking bot connection
        if last_activity and (datetime.datetime.now() - last_activity).seconds > 180:  # Checking that bot not used for more than 3 mins
            print("leave channel due to inactivity")
            await vc.disconnect()
            await vc.channel.send(f"left channel due to inactivity")
            last_activity = datetime.datetime.now()  # Updating last_activity time
            vc = None   # Setting voice channel status to unconnected
            queue = []  # Clearing queue
    else:
        last_activity = datetime.datetime.now()  # if bot is used setting last active to recent time


@client.command()
async def play(ctx: discord.ext.commands.context.Context, arg: str):
    """
    - connects to your voice chat and starts to play the song(only from youtube).
    """
    global current_song, queue, vc  # current_song: str, queue: list, vc: discord.voice_client.VoiceClient
    if vc is None:  # Checking if bot is already connected to voice channel
        try:
            vc = await ctx.message.author.voice.channel.connect()   # Connecting to voice channel
        except discord.errors.ClientException:
            pass
    if current_song:    # If something is playing right now appending song in queue
        queue.append(arg)
        await ctx.channel.send(f"{arg} added to queue, songs in queue: {len(queue)}")
    else:
        current_song = arg  # Searching song corresponding on name or link from YouTube
        with YoutubeDL(YDL_OPTIONS) as ydl:
            if "https://" in arg:
                await ctx.channel.send(f"playing: {arg}, songs in queue: {len(queue)}")
                info = ydl.extract_info(arg, download=False)  # Extracting song info
            else:
                await ctx.channel.send(f"playing: {arg}, Songs in queue: {len(queue)}")
                info = ydl.extract_info(f"ytsearch:{arg}", download=False)["entries"][0]  # Extracting song info and searching it by 0 position

        if info.get("_type") == "playlist":  # Checking if link is playlist or not
            play_now = info["entries"].pop(0)
            queue.extend([entry["webpage_url"] for entry in info["entries"]])
        else:
            play_now = info

        url = play_now["formats"][0]["url"]

        source = discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=url, **FFMPEG_OPTIONS)
        vc.play(source, after=partial(after, ctx))  # playing song

        source.on_completion = play_next_song_callback


def after(ctx: discord.ext.commands.context.Context, error):  # Creating a task for bot if song ends
    client.loop.create_task(play_next_song_callback(ctx))


async def play_next_song_callback(ctx: discord.ext.commands.context.Context):  # Calling play_next_song function
    global current_song, queue, vc
    current_song = None
    if queue:   # Checking if queue exist
        await play_next_song(ctx)


async def play_next_song(ctx: discord.ext.commands.context.Context):  # Function that plays next song in queue
    global current_song, queue, vc  # current_song: str, queue: list, vc: discord.voice_client.VoiceClient
    current_song = queue.pop(0)  # Putting next song from queue
    with YoutubeDL(YDL_OPTIONS) as ydl:  # Checking the type of request(link or song name)
        if "https://" in current_song:
            await ctx.channel.send(f"playing: {current_song}, songs in queue: {len(queue)}")
            info = ydl.extract_info(current_song, download=False)   # Extracting song info
        else:
            await ctx.channel.send(f"playing: {current_song}, songs in queue: {len(queue)}")
            info = ydl.extract_info(f"ytsearch:{current_song}", download=False)["entries"][0]   # Extracting song info and searching it by 0 position

    if info.get("_type") == "playlist":  # Checking if link is playlist or not
        play_now = info["entries"].pop(0)
        queue.extend([entry["webpage_url"] for entry in info["entries"]])
    else:
        play_now = info

    url = play_now["formats"][0]["url"]

    source = discord.FFmpegPCMAudio(
        executable="ffmpeg\\ffmpeg.exe", source=url, **FFMPEG_OPTIONS
    )
    vc.play(source, after=partial(after, ctx))

    source.on_completion = play_next_song_callback  # Calling this function again if queue exist


@client.command()
async def pause(ctx: discord.ext.commands.context.Context):
    """- pauses the song."""
    await ctx.channel.send(f"song is paused")
    vc = ctx.guild.voice_client  # Checking that bot is connected to voice channel
    vc.pause()


@client.command()
async def resume(ctx: discord.ext.commands.context.Context):
    """- if song is paused, starts playing again."""
    vc = ctx.guild.voice_client  # Checking that bot is connected to voice channel
    if vc.is_paused():  # Checking if song is paused
        await ctx.channel.send(f"resuming song...")
        vc.resume()
    else:
        await ctx.channel.send(f"The song is not paused.")


@client.command()
async def leave(ctx: discord.ext.commands.context.Context):
    """- leaves your voice channel"""
    global vc, queue
    vc = None   # Clearing voice channel info
    queue = []  # Clearing queue
    voice = ctx.guild.voice_client  # Checking that bot is connected to voice channel
    if voice and voice.is_connected():  # Checking connection
        await ctx.channel.send("Left your voice channel")
        await voice.disconnect()
    else:
        await ctx.channel.send("I'm not in a voice channel yet.")


@client.command()
async def skip(ctx: discord.ext.commands.context.Context):
    """- skips to the next song."""
    global vc
    await ctx.channel.send(f"skipping song..")
    vc.stop()


@client.event
async def on_ready():
    """
    return: Shows that bot is online and launches loop on check_inactivity function
    """
    # Check if bot is ready
    print("Bot online")
    await check_inactivity.start()   # Starting loop in check_inactivity function


@client.event
async def on_raw_reaction_add(payload: discord.raw_models.RawReactionActionEvent):
    """
    param channel: gets channel ID
    param message: gets message ID
    param member: gets member's ID
    return: adding role to member after putting emoji under selected message
    """
    if payload.message_id == Config.POST_ID:
        channel = client.get_channel(payload.channel_id)  # Get the channel object
        message = await channel.fetch_message(payload.message_id)  # Get the message object
        member = utils.get(message.guild.members, id=payload.user_id)  # Get the user object that added the reaction

        if not member:
            print(f"[ERROR] Member not found for ID {payload.user_id}")
            return
        try:
            emoji = str(payload.emoji)  # The emoji selected by the user
            role = utils.get(message.guild.roles, id=Config.ROLES[emoji])  # Get the selected role (if any)
            if (
                    role is not None
                    and len([i for i in member.roles if i.id not in Config.EXCROLES])
                    <= Config.MAX_ROLES_PER_USER
            ):
                await member.add_roles(role)
                print(f"[SUCCESS] User {member.display_name} has been granted with role {role.name}")
            else:
                await message.remove_reaction(payload.emoji, member)
                print(f"[ERROR] No role found for {emoji} or too many roles for user {member.display_name}")
        except KeyError as e:
            print(f"[ERROR] KeyError, no role found for {emoji}")
        except Exception as e:
            print(repr(e))


@client.event
async def on_raw_reaction_remove(payload: discord.raw_models.RawReactionActionEvent):
    """
    param channel: gets channel ID
    param message: gets message ID
    param member: gets member's ID
    return: removing role from member after removing emoji from selected message
    """
    channel = client.get_channel(payload.channel_id)  # Get the channel object
    message = await channel.fetch_message(payload.message_id)  # Get the message object
    member = utils.get(message.guild.members, id=payload.user_id)  # Get the user object that added the reaction

    if member:
        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=Config.ROLES[emoji])

            await member.remove_roles(role)
            print(f"[SUCCESS] Role {role.name} has been removed for user {member.display_name}")

        except KeyError:
            print(f"[ERROR] KeyError, no role found for {emoji}")
        except Exception as e:
            print(repr(e))
    else:
        print(f"[ERROR] Member not found with ID {payload.user_id}")


# Running bot
client.run(Config.token)
