import discord
import os
from dotenv import load_dotenv
from groq import Groq  # Import the Groq client
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
from datetime import datetime

# Load environment variables
load_dotenv()

# Create intents
intents = discord.Intents.default()
intents.messages = True  # Enable the message intent
intents.message_content = True 

# Initialize the Discord client with intents
discord_client = discord.Client(intents=intents)

# Initialize the Groq client
groq_client = Groq()

# Initialize the scheduler
scheduler = AsyncIOScheduler()

# Hardcoded timezone for Nigeria
nigeria_tz = pytz.timezone('Africa/Lagos')

async def send_daily_verse(channel):
    """Generate and send the verse of the day using Groq."""
    print("Triggering Groq API to fetch the verse of the day...")  # Log to terminal

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that provides a daily verse."
                },
                {
                    "role": "user",
                    "content": "Give me the verse of the day."
                }
            ],
            model="llama3-8b-8192",
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )

        # Log the entire response from Groq
        print("Response from Groq:", chat_completion)  # Log the full response object

        # Extract the generated verse from the response
        verse = chat_completion.choices[0].message.content
        # Send the verse to the specified channel immediately after receiving the response
        await channel.send(f"📖 **Verse of the Day:** {verse}")
    except Exception as e:
        print(f"Error fetching verse: {e}")  # Log any errors that occur

@discord_client.event
async def on_ready():
    print(f'Logged in as {discord_client.user}')

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    if message.content.startswith('!verse'):
        print(f"Received command from {message.author}: {message.content}")  # Log the command received
        await send_daily_verse(message.channel)  # Send the verse immediately when the command is received

# Run the Discord bot
discord_client.run(os.getenv('DISCORD_TOKEN'))