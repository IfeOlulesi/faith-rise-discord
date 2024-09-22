import os
from dotenv import load_dotenv

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
import asyncio 

from app.daily_verse import send_daily_verse 
from app.constants import discord_client

from utils.logger import emit_log
 

load_dotenv()
ENVIRONMENT = os.getenv('ENV')

scheduler = AsyncIOScheduler() 
nigeria_tz = pytz.timezone('Africa/Lagos')


@discord_client.event
async def on_ready():
  emit_log('info', f'Logged in as {discord_client.user}')
  

  # Get the channel using the channel ID
  channel_id = ''
  if ENVIRONMENT == 'development':
    channel_id = int(os.getenv('DEV_RHEMA_CHANNEL_ID')) 
  else:
    channel_id = int(os.getenv('DISCORD_CHANNEL_ID')) 
    
  channel = discord_client.get_channel(channel_id) 

  if channel is None:
    emit_log('err', "ERROR: Channel not found. Please check the channel ID.")
    return

  # Check if in development mode
  if ENVIRONMENT == 'development':
    await asyncio.sleep(5)  # Wait for 5 seconds before sending the verse
    await send_daily_verse(channel)  # Send the verse immediately for development
  else:
    # Schedule the daily verse job for production
    scheduler.add_job(send_daily_verse, 'cron', hour=5, minute=0, args=[channel])
    emit_log('info', 'Scheduled job to send the verse of the day at 5:00 AM Nigerian time.' )

  scheduler.start()

@discord_client.event
async def on_message(message):
  if message.author == discord_client.user:
    return

  if message.content.startswith('!verse'):
    emit_log('info', f"Received command from {message.author}: {message.content}")
    await send_daily_verse(message.channel, discord_client)


discord_client.run(os.getenv('DISCORD_TEST_BOT_TOKEN'))