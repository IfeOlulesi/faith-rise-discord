import discord
import os
from dotenv import load_dotenv

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz

from daily_verse import send_daily_verse 

# Load environment variables
load_dotenv()

# Create intents
intents = discord.Intents.default()
intents.messages = True  # Enable the message intent
intents.message_content = True 

# Initialize the Discord client with intents
discord_client = discord.Client(intents=intents)

# Initialize the scheduler
scheduler = AsyncIOScheduler()

# Hardcoded timezone for Nigeria
nigeria_tz = pytz.timezone('Africa/Lagos')


@discord_client.event
async def on_ready():
  print(f'Logged in as {discord_client.user}')

  # Get the channel using the channel ID
  channel_id = int(os.getenv('DISCORD_CHANNEL_ID'))  # Convert to integer
  channel = discord_client.get_channel(channel_id)  # Replace YOUR_CHANNEL_ID with the actual channel ID

  if channel is None:
    print("Error: Channel not found. Please check the channel ID.")  # Log if the channel is not found
    return

  # Schedule the job to run daily at 3:42 PM Nigerian time
  scheduler.add_job(send_daily_verse, 'cron', hour=5, minute=00, args=[channel])  # Pass the channel object
  print("Scheduled job to send the verse of the day at 5:00 PM Nigerian time.")  # Log when the job is scheduled
  scheduler.start()

@discord_client.event
async def on_message(message):
  if message.author == discord_client.user:
    return

  if message.content.startswith('!verse'):
    print(f"Received command from {message.author}: {message.content}")  # Log the command received
    await send_daily_verse(message.channel, discord_client)  # Send the verse immediately when the command is received

# Run the Discord bot
discord_client.run(os.getenv('DISCORD_TEST_BOT_TOKEN'))