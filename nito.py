import discord                      # Discord.py API
from discord.ext import commands    # Load and unload commands come from here
from bot_token import TOKEN         # Allows us to load the token without
                                    # putting it in the code for security

# All command are called using the format q!cmdname
bot = commands.Bot(command_prefix = "q!")

# List of all the cogs that this bot will run by default. When new cogs are
# created, bots that ran the original code can either re-run this code
# (I will update this list) or they can use the load and reload functions
allcogs = ["defaults",
           "round_creator"]

# Contains all the loaded cogs (which will be all the cogs unless unloaded)
currentcogs = ["defaults",
               "round_creator"]

@bot.event
async def on_ready():
    '''
    Called when the bot runs
    '''
    print("Bot successfully connected!")

# The aliases allow the command to be used with other names
@bot.command(aliases = ["load", "loadcog"])
async def load_cog(ctx, ext):   # ctx is just the context
    '''
    Allows us to load in a cog from within the Discord guild. This makes it
    easier to add new features to the bot

    Parameters:
        ext (str): The name of the cog (without the .py)
    '''
    try:
        # Check to make sure we actually need to load this cog
        if ext not in currentcogs:
            # All cogs are in the cogs folder
            bot.load_extension("cogs.%s" % ext)
            currentcogs.append(ext)             
            if ext not in allcogs:
                # If the code hasn't been updated with the new list of all the
                # cogs then this line will add it to the list (this action will
                # be undone if the program restarts so the user should always
                # make sure they have the most up-to-date version of the file)
                allcogs.append(ext)
            await ctx.send("Cog loaded successfully!")
        elif ext in currentcogs:
            await ctx.send("This cog is already loaded")
    except:
        # if the cog doesn't exist and throws an error then we can deal with it
        await ctx.send("This cog does not exist.")

@bot.command(aliases = ["unload", "unloadcog"])
async def unload_cog(ctx, ext):
    '''
    Allows us to unlaod a cog from within the Discord guild. This will disable
    any features that the bot may have been using from this cog

    Parameters:
        ext (str): The name of the cog (without the .py)
    '''
    # Check to make sure this cog is loaded so we can unload it
    if ext in currentcogs:
        bot.unload_extension("cogs.%s" % ext)
        currentcogs.remove(ext)
        await ctx.send("Cog unloaded successfully!")
    elif ext not in currentcogs:
        await ctx.send("This cog is not loaded or doesn't exist.")
    
@bot.command(aliases = ["reload", "reloadcog"])
async def reload_cog(ctx, ext):
    '''
    Unloads and the loads a cog. Useful when the code of a cog is updated

    Parameters:
        ext (str): The name of the cog (without the .py)
    '''
    bot.reload_extension("cogs.%s" % ext)
    await ctx.send("Cog successfully reloaded!")

@bot.command(aliases = ["view", "viewcogs"])
async def view_cogs(ctx):
    '''
    Shows a list of all the currently loaded cogs
    '''
    await ctx.send("Currently loaded cogs:")
    for cog in currentcogs:
        await ctx.send("-%s\n" % cog)

@bot.command(aliases = ["stop", "end"])
async def halt(ctx):
    '''
    Halts the execution of the bot from within the Discord guild
    '''
    await ctx.send("Until next time :)")
    await bot.logout()

# Each cog in the list is loaded in automatically whenever we run the program
for cog in allcogs: 
    bot.load_extension("cogs.%s" % cog)
bot.run(TOKEN) # Bring the bot online
