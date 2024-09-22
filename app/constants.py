import discord

# Create intents
intents = discord.Intents.default()
intents.messages = True  # Enable the message intent
intents.message_content = True 

# Initialize the Discord client with intents
discord_client = discord.Client(intents=intents)