import os
from dotenv import load_dotenv

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
import asyncio 

from daily_verse import send_daily_verse 
from constants import discord_client

# Load environment variables
load_dotenv()
ENVIRONMENT = os.getenv('ENV')

# Initialize the scheduler
scheduler = AsyncIOScheduler()

# Hardcoded timezone for Nigeria
nigeria_tz = pytz.timezone('Africa/Lagos')


@discord_client.event
async def on_ready():
  print(f'Logged in as {discord_client.user}')

  # Get the channel using the channel ID
  channel_id = ''
  if ENVIRONMENT == 'development':
    channel_id = int(os.getenv('DEV_RHEMA_CHANNEL_ID')) 
  else:
    channel_id = int(os.getenv('DISCORD_CHANNEL_ID')) 
    
  channel = discord_client.get_channel(channel_id) 

  if channel is None:
    print("Error: Channel not found. Please check the channel ID.")
    return

  # Check if in development mode
  if ENVIRONMENT == 'development':
    await asyncio.sleep(5)  # Wait for 5 seconds before sending the verse
    await send_daily_verse(channel)  # Send the verse immediately for development
  else:
    # Schedule the daily verse job for production
    scheduler.add_job(send_daily_verse, 'cron', hour=5, minute=0, args=[channel])  # Pass the channel object
    print("Scheduled job to send the verse of the day at 5:00 AM Nigerian time.")  # Log when the job is scheduled

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