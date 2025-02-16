import discord
from discord.ext import commands
import yt_dlp
from typing import Literal, Optional
import asyncio
from dotenv import load_dotenv
import os

# Set up bot intents and command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# Global variables for music queue and voice client
music_queue = []
music_queue_names = []
voice_client = None
ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'opus',
            'preferredquality': '192',
        }],
    }

# Cache for song information
song_info_cache = {}

# Helper function to play the next song in the queue
async def play_next(interaction: discord.Interaction):
    global music_queue
    global voice_client
    global music_queue_names

    if not music_queue:
        return

    url = music_queue[0]
    try:
        if url in song_info_cache:
            info = song_info_cache[url]
        else:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                song_info_cache[url] = info

        title = info['title']
        music_queue_names.append(title)
        print(music_queue_names)
        url2 = info['url']  # Use the direct URL extracted by yt-dlp
        print(f"Extracted URL: {url2}")  # Debugging: Log the extracted URL

        # Use FFmpegOpusAudio for better compatibility with Discord
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        voice_client.play(discord.FFmpegOpusAudio(url2, **ffmpeg_options), after=lambda e: asyncio.run_coroutine_threadsafe(handle_after(e, interaction), bot.loop).result())
        await interaction.followup.send(content=f"Now playing: {info['title']}")
    except Exception as e:
        await interaction.followup.send(content=f"An error occurred: {e}")
        music_queue.pop(0)
        await play_next(interaction)

# Helper function to handle actions after a song finishes playing
async def handle_after(error, interaction: discord.Interaction):
    global music_queue
    if error:
        print(f"Error: {error}")
    music_queue.pop(0)
    await play_next(interaction)

# Command to say hello
@bot.tree.command(name="hello", description="Say hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(content="Hello, world!")

# Command to play a song from a YouTube URL
@bot.tree.command(name="play", description="Play a song")
async def play(interaction: discord.Interaction, url: str):
    global music_queue
    global voice_client

    # Validate the URL
    if "youtube.com" not in url and "youtu.be" not in url:
        await interaction.response.send_message(content="Please provide a valid YouTube URL.")
        return

    await interaction.response.defer()

    # Connect to the voice channel if not already connected
    if voice_client is None or not voice_client.is_connected():
        if interaction.user.voice:
            voice_client = await interaction.user.voice.channel.connect()
        else:
            await interaction.followup.send(content="You need to be in a voice channel to use this command.")
            return

    # Add the URL to the queue
    music_queue.append(url)
    if not voice_client.is_playing():
        await play_next(interaction)
    else:
        if url in song_info_cache:
            info = song_info_cache[url]
        else:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                song_info_cache[url] = info

        title = info['title']
        music_queue_names.append(title)
        print(music_queue_names)
        await interaction.followup.send(content="Added to queue.")

# Command to delete a specified number of messages in the channel
@bot.tree.command(name="purge", description="Deletes input amount of messages in the channel")
async def purge(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)

# Command to leave the voice channel and clear the queue
@bot.tree.command(name="leave", description="Leave the voice channel")
async def leave(interaction: discord.Interaction):
    global voice_client
    global music_queue
    global music_queue_names

    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        voice_client = None
        music_queue = []
        music_queue_names = []
        await interaction.response.send_message(content="Left the voice channel and cleared the queue.")
    else:
        await interaction.response.send_message(content="I'm not in a voice channel.")

# Command to skip the current song
@bot.tree.command(name="skip", description="Skip the current song")
async def skip(interaction: discord.Interaction):
    global voice_client

    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await interaction.response.send_message(content="Skipped the current song.")
    else:
        await interaction.response.send_message(content="No song is currently playing.")

# Command to show the current music queue
@bot.tree.command(name="queue", description="Show the current queue")
async def queue(interaction: discord.Interaction):
    global music_queue
    global music_queue_names

    if music_queue:
        embed = discord.Embed(title="Music Queue", color=discord.Color.blue())
        for index, (title, url) in enumerate(zip(music_queue_names, music_queue), start=1):
            embed.add_field(name=f"{index}.", value=f"[{title}]({url})\n\u200b", inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(content="The queue is empty.")

# Command to sync bot commands with Discord
@bot.command()
@commands.guild_only()
async def sync(
    ctx: commands.Context,
    guilds: commands.Greedy[discord.Object],
    spec: Optional[Literal["~", "*", "^"]] = None
) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

# Run the bot with the specified token
bot.run(DISCORD_TOKEN)