import discord
import os
from discord.ext import commands
from dotenv import load_dotenv # allows us to load the token without displaying it within the code
# this allows opern-source code to be secure because you cannot access my bot's token

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # load in the token from the .env file in the same folder
client = commands.Bot(command_prefix = 'q!') # COMMENT HERE

@client.command()
async def load(ctx, extension):
    '''Allows us to load in a cog from within the Discord guild. This makes it easier to add new features to the bot'''
    client.load_extension(f'cogs.{extension}')
    # all cogs are located within the cogs folder

@client.command()
async def unload(ctx, extension):
    '''Allows us to unlaod a cog from within the Discord guild. This will disable any features that the bot may have been
       using from this cog'''
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    '''Unloads and the loads a cog. Useful when the code of a cog is updated'''
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

# the os module will allow us to load in all the cogs we have when our bot goes online
for filename in os.listdir('./cogs'): # lists all the files in cogs
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}') # strips the last three characters to get rid of the .py

client.run(TOKEN) # run the client, bringing the bot online
