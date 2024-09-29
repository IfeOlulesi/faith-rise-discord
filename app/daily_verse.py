import os
from dotenv import load_dotenv 

from .rhema_exchange import start_conversation
from .constants import discord_client
from utils.logger import emit_log
import pandas as pd 

load_dotenv() 

async def send_daily_verse(channel): 
  DB_PATH = os.getenv("DB_LOCAL_PATH")
  emit_log('info', "Sending daily verse...")

  try:
    
    # Load the daily verses from the CSV file
    daily_verses_df = pd.read_csv(DB_PATH+'daily_verses_from_books_estimate.csv')
    emit_log('info', 'Fetched daily verses lookup csv...')
    
    random_row = daily_verses_df.sample(n=1).iloc[0]
    emit_log('info', f'random row gotten: {random_row}')
    
    book_name = random_row[0]  # First column value
    emit_log('info', f'book name: {book_name}')
    
    row_index = int(random_row.name) + 1
    filename = f"{DB_PATH}/books/{row_index}_{book_name}_Daily_Verses.csv"
    emit_log('info', f'Generated csv file path: {filename}')

    # Load the selected daily verses CSV file
    verses_df = pd.read_csv(filename, header=None)
    random_verse_row = verses_df.sample(n=1).iloc[0]
    verse_text, verse_chapter, verse_number = random_verse_row[2], random_verse_row[0], random_verse_row[1]

    verse = f"""{verse_text} - {book_name} {verse_chapter}:{verse_number}"""
  
    emit_log('good', f'Verse generated: {verse}')

    bot_response = f"""
      📖 **Verse of the Day** \n\n{verse}
    """
    
    await channel.send(bot_response)    
    await channel.send("What are your thoughts on today's verse? @everyone")
    
    emit_log('good', 'Daily verse sent')
    
    if discord_client is not False:
      await start_conversation(channel, discord_client, verse)
  except Exception as e:
    print(f"Error fetching verse: {e}")
