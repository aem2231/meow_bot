import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import re

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

TARGET_CHANNEL = 1471152428979195924
LETTERS = set("mrpeowuf")

MEOWS = [
    r"^m+e+o+w+$",
    r"^m+r+e+o+w+$",
    r"^m+r*p+$",
    r"^p+u+r+r*$",
    r"^w+o+f+$",
    r"^m+r+e+o+f+$",
    r"^p+r*p+$",
    r"^(m+e+o+w+|m+r+e+o+w+|m+r*p+|p+u+r+r*|w+o+f+|m+r+e+o+f+|p+r*p+)+$",
]


def is_cat_sound(text):
    text = text.lower().strip()
    for pattern in MEOWS:
        if re.match(pattern, text):
            return True
    return False

def is_valid_message(text):
    text = text.lower().strip()

    words = text.split()
    if not words:
        return False

    for word in words:
        if not is_cat_sound(word):
            return False

    return True

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check allowed letters
    message_letters = set(message.content.lower().replace(" ", ""))
    if not message_letters.issubset(LETTERS):
        return

    # Check valid cat sounds
    if is_valid_message(message.content):
        target = bot.get_channel(TARGET_CHANNEL)
        if target:
            await target.send(f"**{message.author}**: {message.content}")
        else:
            print(f"Target channel {TARGET_CHANNEL} not found")

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    bot.run(token)
