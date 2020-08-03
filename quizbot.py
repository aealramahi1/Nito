import discord
from discord.ext import commands # this is where our load and unload commands go
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

currentcogs = ["defaults",
               "round_creator"] # Contains all the loaded cogs (which will be all the cogs unless one is unloaded)

@bot.event
async def on_ready():
    print("Bot successfully connected!")

@bot.command(aliases = ["load", "loadcog"])
async def load_cog(ctx, ext):
    '''Allows us to load in a cog from within the Discord guild. This makes it easier to add new features to the bot'''
    try:
        if ext not in currentcogs: # Check to make sure we actually need to load this cog
            bot.load_extension("cogs.%s" % ext) # All cogs are located within the cogs folder
            currentcogs.append(ext) # Add it to the list of currently loaded cogs
            if ext not in allcogs:
                allcogs.append(ext) # If the code hasn't been updated with the new list of all the cogs, then this
                # line will add it to the list (this action will be undone if the program restarts so the user should
                # always make sure they have the most up-to-date version of this file)
            await ctx.send("Cog loaded successfully!")
        elif ext in currentcogs:
            await ctx.send("This cog is already loaded")
    except: # if the cog doesn't exist and throws an error, then we can deal with it accordingly here
        await ctx.send("This cog does not exist.")

@bot.command(aliases = ["unload", "unloadcog"])
async def unload_cog(ctx, ext):
    '''Allows us to unlaod a cog from within the Discord guild. This will disable any features that the bot may have been
       using from this cog'''
    # Check to make sure this cog is loaded so we can unload it
    if ext in currentcogs:
        bot.unload_extension("cogs.%s" % ext)
        currentcogs.remove(ext)
        await ctx.send("Cog unloaded successfully!")
    elif ext not in currentcogs:
        await ctx.send("This cog is not loaded and, therefore, cannot be unloaded.")
    
@bot.command(aliases = ["reload", "reloadcog"])
async def reload_cog(ctx, ext):
    '''Unloads and the loads a cog. Useful when the code of a cog is updated'''
    bot.reload_extension("cogs.%s" % ext)
    await ctx.send("Cog successfully reloaded!")

@bot.command(aliases = ["view", "viewcogs")
async def view_cogs(ctx):
    '''Shows a list of all the currently loaded cogs'''
    await ctx.send("Currently loaded cogs:")
    for cog in currentcogs:
        await ctx.send("-%s\n" % cog)

if __name__ == "__main__":
    for cog in allcogs: # For each cog in the list, we load it in automatically whenever we run the program
        bot.load_extension("cogs.%s" % cog)

bot.run(TOKEN) # Bring the bot online
