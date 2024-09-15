import asyncio
from groq import Groq  # Import the Groq client


async def start_conversation(channel, discord_client, groq_client):
    # Create a dictionary to track user responses
    user_responses = {}
    # end_time = datetime.now(nigeria_tz).replace(hour=22, minute=0, second=0, microsecond=0)

    def check_response(message):
        return message.channel == channel and message.author != discord_client.user

    # Wait for user responses for 8 hours
    for _ in range(8):
        try:
            message = await discord_client.wait_for(
                "message", timeout=3600, check=check_response
            )
            user_responses[message.author] = message.content
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that facilitates edifying gospel conversations between peer believers.",
                    },
                    {
                        "role": "user",
                        "content": f"""Here's the conversation history between the peer Christians about the verse of the day.
                          {user_responses}.
                          Respond to the messages in an edifying and godly manner. Steer the conversation from theory to 
                          practical application.
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
            # await channel.send(f"Thank you, {message.author}! That's a great insight.")
            await channel.send(feedback)
        except asyncio.TimeoutError:
            # Gentle reminder to users who haven't responded
            await channel.send(
                "Hey everyone, feel free to share your thoughts on today's verse!"
            )

    # After 8 hours, summarize the conversation
    await summarize_conversation(channel, user_responses)


async def summarize_conversation(channel, user_responses):
    summary = "Here's a summary of our discussion:\n"
    for user, response in user_responses.items():
        summary += f"{user}: {response}\n"
    await channel.send(summary)

    # If no responses, drop an edifying text about the key verse
    if not user_responses:
        await channel.send("Remember, the verse teaches us to... [insert lesson here]")
