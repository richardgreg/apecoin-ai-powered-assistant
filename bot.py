import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import llm
import asyncio
import os
import logging


load_dotenv(find_dotenv())

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


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
logging.info('Bot is up and running.')

@bot.event
async def on_ready():
    logger.info("Bot is up and ready")
    try:
        synced = await bot.tree.sync()
        logger.info(f'Synced {len(synced)} command(s)')
    except Exception as e:
        logger.error(f'Syncing commands failed: {e}')


@bot.tree.command(name="apegpt", description="ask anything about apecoin or something else")
async def apegpt(ctx: discord.Interaction, prompt:str):
    try:
        await ctx.response.defer()
        await asyncio.sleep(3)
        content = llm.evaluate_prompt(prompt=prompt)
        
        # Split the content into chunks if it's too long
        if len(content) > 2000:
            for i in range(0, len(content), 2000):
                await ctx.followup.send(content[i:i+2000])
        else:
            await ctx.followup.send(content)

        command_logger.info(f"Apegpt command executed by {ctx.user} with prompt: {prompt}")

    except Exception as e:
        command_logger.info(f"Error occurred: {e}")
        await ctx.response.send_message("Sorry, I was unable to process your question.")


def run_bot():
    try:
        bot.run(os.environ.get("DISCORD_TOKEN"))
    except Exception as e:
        logger.info("Bot failed to start. Check your configuration.")
        logger.error(f"Error: {e}")
