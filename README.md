# Korn Bot

A Python Discord bot for music playback and emoji-based role assignment.

## Features
- Play a song or playlist from a YouTube URL or a search term.
- Pause, resume, skip, and leave voice channels.
- Assign roles using reactions on a configured message.

## Commands
| Command | Purpose |
| --- | --- |
| `h!play <URL or search term>` | Start playback |
| `h!pause` | Pause playback |
| `h!resume` | Resume playback |
| `h!skip` | Skip the current track |
| `h!leave` | Leave the voice channel |
| `h!help` | Display command help |

The original documentation describes a maximum of 25 songs per playlist.

## Project structure
- [Bot.py](Bot.py): bot implementation.
- [Config.py](Config.py): bot configuration.
- [Documentation/](Documentation/): accompanying project documentation.

## Development status
This is a legacy project whose previous README dates the implementation to February 2023. Compatibility with current Discord and music-service APIs has not been verified.

## Local setup
1. Install Python and create a virtual environment.
2. Run `python -m pip install -r requirements.txt` from the repository root. This forwards to the original dependency snapshot in `Documentation/requirements.txt`.
3. Set `DISCORD_BOT_TOKEN` in your shell to a token for your own bot. For PowerShell: `$env:DISCORD_BOT_TOKEN = "your-token"`.
4. Configure the message and role IDs in `Config.py` for your Discord server.
5. The current implementation expects the Windows FFmpeg executable at `ffmpeg/ffmpeg.exe`, relative to the repository root.
6. Run `python Bot.py`.

The dependency snapshot is from the original implementation and has not been validated against current Discord/YouTube services. Review the accompanying [documentation](Documentation/) for the original design. Tokens belong in environment variables and must never be committed.

## Author
Tymur Shapoval

## License
See [LICENSE](LICENSE).
