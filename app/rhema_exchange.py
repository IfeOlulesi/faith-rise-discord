import asyncio
from datetime import datetime 
import pytz
from .constants import groq_client


async def start_conversation(channel, discord_client, verse):
  # Create a dictionary to track user responses
  message_history = {}

  def check_response(message):
    return message.channel == channel and message.author != discord_client.user

  # Wait for user responses for 8 hours
  for _ in range(8):
    try:
      message = await discord_client.wait_for(
        "message", timeout=3600, check=check_response
      )
      message_key = f"{message.author.display_name} - {message.created_at}"
      message_history[message_key] = message.content
      chat_completion = groq_client.chat.completions.create(
        messages=[
          {
            "role": "system",
            "content": "You are a helpful assistant that facilitates edifying gospel conversations between peer believers.",
          },
          {
            "role": "user",
            "content": f"""Here's the conversation history between the peer Christians about the verse of the day.
              {message_history}.
              Here is the verse of the day in question: {verse}
              
              Respond to the most recent message sent by the user in an edifying and godly manner. 
              Keep your messages short and concise.
              Steer the conversation from theory to practical application. Once practical applications have been shared,
              close the conversation with an edifying ending.
              
              If the conversation has ended, don't give a reply.
              
              Use emoji's sparingly to spice up your responses.
            """,
          },
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
      )
      feedback = chat_completion.choices[0].message.content
      feedback_key = f"bot - {datetime.now(pytz.utc)}"  # Use UTC timezone
      message_history[feedback_key] = feedback
      
      await channel.send(feedback)
    except asyncio.TimeoutError:
      # Gentle reminder to users who haven't responded
      await channel.send("Hey @everyone, feel free to share your thoughts on today's verse!")

  # After 8 hours, summarize the conversation
  await summarize_conversation(channel, message_history)


async def summarize_conversation(channel, message_history):
  summary = "Here's a summary of our discussion:\n"
  for user, response in message_history.items():
    summary += f"{user}: {response}\n"
  await channel.send(summary)

  # If no responses, drop an edifying text about the key verse
  if not message_history:
    await channel.send("Remember, the verse teaches us to... [insert lesson here]")
