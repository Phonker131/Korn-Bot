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

The previous installation instructions referenced a requirements file, but none exists in the current repository root. A reproducible dependency list and configuration review are needed before a verified quick-start guide can be provided. Do not commit bot tokens.

## Author
Tymur Shapoval

## License
See [LICENSE](LICENSE).
