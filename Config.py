import os

# Set this in your shell; never commit a real bot token.
token = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
if not token:
    raise RuntimeError("Set DISCORD_BOT_TOKEN before starting Korn Bot")

POST_ID = 1070832535283699772  # Selected message ID for giving roles, type: int

ROLES = {  # Dictionary for emojis and their roles, type: dict[str, int]
    '👨‍🎓': 1070833161627517040,  # Student role
    '👨‍🏫': 1070833271455367189  # Professor role
}

EXCROLES = ()  # Exclude these roles from counting, Type: tuple

MAX_ROLES_PER_USER = 10  # Max roles number per user, type: int
