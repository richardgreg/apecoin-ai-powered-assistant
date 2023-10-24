import discord
from dotenv import load_dotenv, find_dotenv, dotenv_values
import llm
import asyncio
import os
import logging


# Environment variables
load_dotenv(find_dotenv())
config = dotenv_values('.env')
CHANNELID = (config['CHANNELID'])

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the desired logging level
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

logger = logging.getLogger("BotLogger")
# Separate logger for command-specific logs
command_logger = logging.getLogger("CommandLogger")

# Configure discord client (bot)
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logger.info("Bot is up and ready")


@client.event
async def on_message(message):
    
    # Exit if not in designated channel
    if str(message.channel.id) not in CHANNELID:
        return
    
    # Prevent bot from responding to its own messages
    if message.author == client.user:
        return
    
    # Get message and channel id
    message_id = message.id
    channel_id = message.channel.id

    client_channel_getter = client.get_channel(channel_id)

    # Retrieve user message
    message = await client_channel_getter.fetch_message(message_id)
    human_message = message.content

    # Ignore messages that start with '!'
    if human_message.startswith('!'):
        return

    try:
        async with message.channel.typing():
            response = llm.evaluate_prompt(prompt=human_message)

            # Simulate delay
            await asyncio.sleep(2)

        # Split the content into chunks if it's too long
        if len(response) > 2000:
            for i in range(0, len(response), 2000):
                await message.channel.send(response[i:i+2000])
        else:
            await message.channel.send(response)

        command_logger.info(f"Apegpt command executed by {message.author} with prompt: {message.content}")

    except Exception as e:
        command_logger.info(f"Error occurred: {e}")
        await message.response.send_message("Sorry, I was unable to process your question.")


def run_bot():
    try:
        client.run(os.environ.get("DISCORD_TOKEN"))
    except Exception as e:
        logger.info("Bot failed to start. Check your configuration.")
        logger.error(f"Error: {e}")
