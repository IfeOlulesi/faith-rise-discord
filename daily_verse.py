import os
from dotenv import load_dotenv
from groq import Groq  # Import the Groq client
from apscheduler.schedulers.asyncio import AsyncIOScheduler


load_dotenv()

# Initialize the Groq client
groq_api_key = os.getenv('GROQ_API_KEY')
groq_client = Groq(api_key=groq_api_key)

async def send_daily_verse(channel):
  """Generate and send the verse of the day using Groq."""  
  print("Triggering Groq API to fetch the verse of the day...")  # Log to terminal

  try:
    chat_completion = groq_client.chat.completions.create(
      messages=[
        {
          "role": "system",
          "content": "You are a helpful assistant that provides a daily verse from the bible in KJV."
        },
        {
          "role": "user",
          "content": "Give me the verse of the day. Only the verse and nothing else."
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
    bot_response = f"""
    📖 **Verse of the Day** \n\n{verse}
    """
    await channel.send(bot_response)
  except Exception as e:
    print(f"Error fetching verse: {e}")  # Log any errors that occur