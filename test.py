import discord
import os
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz  # Timezone support

load_dotenv()  # Load environment variables from .env

client = discord.Client(intents=discord.Intents.default())
scheduler = AsyncIOScheduler()

# Your local timezone, replace 'America/New_York' with your actual timezone
local_tz = pytz.timezone('America/New_York')

def get_verse_of_the_day():
    # Simulate a call to LLM (like Grok) to generate the verse
    verse = "Hebrews 3:13 AMP"
    message = (
        "[13] But continually encourage one another every day, "
        "as long as it is called 'Today' [and there is an opportunity], "
        "so that none of you will be hardened [into settled rebellion] by "
        "the deceitfulness of sin [its cleverness, delusive glamour, and sophistication]."
    )
    return verse, message

async def send_daily_verse():
    channel_id = int(os.getenv('DISCORD_CHANNEL_ID'))  # Replace with your actual channel ID
    channel = client.get_channel(channel_id)
    
    if channel:
        verse, message = get_verse_of_the_day()
        await channel.send(f"📖 **Verse of the Day:** {verse}\n{message}")
    else:
        print("Channel not found!")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    
    # Send the daily verse immediately when the bot is ready
    await send_daily_verse()  # Call the function to send the verse

client.run(os.getenv('DISCORD_TOKEN'))