# Discord Music Bot

A Discord bot built using `discord.py` and `yt-dlp` to play music from YouTube in voice channels. This bot supports basic music playback features, including play, skip, queue management, and more. It also includes utility commands like message purging and command syncing.

---

## Features

- **Music Playback**:
  - Play songs from YouTube using a URL.
  - Queue multiple songs for continuous playback.
  - Skip the currently playing song.
  - Display the current music queue.
  - Automatically disconnect and clear the queue when leaving the voice channel.

- **Utility Commands**:
  - `hello`: A simple command to test bot responsiveness.
  - `purge`: Delete a specified number of messages in the channel.
  - `sync`: Sync bot commands with Discord (useful for development).

- **Event Handlers**:
  - Logs the bot's username when it connects to Discord.

---

## Prerequisites

Before running the bot, ensure you have the following:

1. **Python 3.8 or higher** installed.
2. A **Discord Bot Token** from the [Discord Developer Portal](https://discord.com/developers/applications).
3. A `.env` file to store your bot token securely.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/discord-music-bot.git
   cd discord-music-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the `.env` file**:
   Create a `.env` file in the root directory and add your Discord bot token:
   ```
   DISCORD_TOKEN=your-discord-bot-token-here
   ```

4. **Run the bot**:
   ```bash
   python bot.py
   ```

---

## Usage

### Commands

- **Music Commands**:
  - `/play <url>`: Play a song from a YouTube URL.
  - `/skip`: Skip the currently playing song.
  - `/queue`: Display the current music queue.
  - `/leave`: Disconnect the bot from the voice channel and clear the queue.

- **Utility Commands**:
  - `/hello`: Say hello to the bot.
  - `/purge <amount>`: Delete a specified number of messages in the channel.
  - `!sync`: Sync bot commands with Discord (use in development).

### Example Workflow

1. Invite the bot to your server and ensure it has the necessary permissions.
2. Join a voice channel.
3. Use `/play <url>` to start playing music.
4. Use `/skip` to skip songs or `/queue` to view the current queue.
5. Use `/leave` to disconnect the bot and clear the queue.

---

## Configuration

- **Command Prefix**: The bot uses `!` as the default command prefix. This can be changed in the `bot.py` file.
- **FFmpeg Options**: The bot uses FFmpeg for audio playback. Ensure FFmpeg is installed on your system or update the `ffmpeg_options` in the code if needed.

---

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to your branch.
4. Submit a pull request with a detailed description of your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [discord.py](https://discordpy.readthedocs.io/) for the Discord API wrapper.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube audio extraction.
- [FFmpeg](https://ffmpeg.org/) for audio processing.

---

## Support

If you encounter any issues or have questions, feel free to open an issue on GitHub or reach out to the maintainers.

Enjoy your music! 🎶