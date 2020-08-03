import discord
##import os
from discord.ext import commands
from bot_token import TOKEN # Allows us to load the token without displaying it within the code
# This allows opern-source code to be secure because you cannot access my bot's token

bot = commands.Bot(command_prefix = "q!") # Here we set the server prefix to q!, meaning that all commands
# are called using the format q!cmdname

##### in the functions below, we check to see if the user has administrative privileges in the guild so that random
##### server users cannot unload or load cogs and create chaos

# List of all the cogs that this bot will run by default. When new cogs are created, bots that ran the original code
# can either re-run this code (I will update this list) or they can use the load and reload functions
allcogs = ["defaults",
           "round_creator"]

@bot.event
async def on_ready():
    print("Bot successfully connected!")

@bot.command()
async def load(ctx, ext):
    '''Allows us to load in a cog from within the Discord guild. This makes it easier to add new features to the bot'''
    bot.load_extension("cogs.%s" % ext)
    # All cogs are located within the cogs folder

@bot.command()
async def unload(ctx, ext):
    '''Allows us to unlaod a cog from within the Discord guild. This will disable any features that the bot may have been
       using from this cog'''
    bot.unload_extension("cogs.%s" % ext)

@bot.command()
async def reload(ctx, ext):
    '''Unloads and the loads a cog. Useful when the code of a cog is updated'''
    bot.reload_extension("cogs.%s" % ext)

if __name__ == "__main__":
##    # The os module will allow us to load in all the cogs we have when our bot goes online
##    for file in os.listdir("./cogs"): # Lists all the files in cogs
##        if file.endswith(".py"):
##            bot.load_extension("cogs.%s" % file[:-3]) # Strips the last three characters to get rid of the .py

    for cog in allcogs:
        bot.load_extension("cogs.%s" % cog)

bot.run(TOKEN) # Bring the bot online
