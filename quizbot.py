# The load, unload, and reload commands used below (along with the for loop) were all derived from a Lucas YouTube tutorial
# The idea for accessing the bot token through a .env file (and the implementation of this feature) were taken from a web tutorial
# Lucas YouTube channel: https://www.youtube.com/channel/UCR-zOCvDCayyYy1flR5qaAg/featured
# Web tutorial: https://realpython.com/how-to-make-a-discord-bot-python/#creating-a-bot

import discord
import os
from discord.ext import commands
from dotenv import load_dotenv # allows us to load the token without displaying it within the code
# this allows opern-source code to be secure because you cannot access my bot's token

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # load in the token from the .env file in the same folder
bot = commands.Bot(command_prefix = 'q!') # COMMENT HERE

@bot.command()
async def load(ctx, extension):
    '''Allows us to load in a cog from within the Discord guild. This makes it easier to add new features to the bot'''
    bot.load_extension(f'cogs.{extension}')
    # all cogs are located within the cogs folder

@bot.command()
async def unload(ctx, extension):
    '''Allows us to unlaod a cog from within the Discord guild. This will disable any features that the bot may have been
       using from this cog'''
    bot.unload_extension(f'cogs.{extension}')

@bot.command()
async def reload(ctx, extension):
    '''Unloads and the loads a cog. Useful when the code of a cog is updated'''
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

# the os module will allow us to load in all the cogs we have when our bot goes online
for filename in os.listdir('./cogs'): # lists all the files in cogs
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}') # strips the last three characters to get rid of the .py

client.run(TOKEN) # bring the bot online
