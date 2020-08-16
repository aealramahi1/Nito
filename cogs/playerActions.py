import cogs.PlayerClass as PlayerClass
import cogs.RoundClass as RoundClass
import discord
from discord.ext import commands
# import pickle

class playerActions(commands.Cog):
    '''
    This cog deals with commands that have to do with the user's Player
    object and its methods

    Commands:
    q!establish_player: Initializes a player object for the user that
                            called the command
    '''
    
    # THIS IS TEMPORARY AND WILL BE MOVED LATER
    # Stores the player object with the user's snowflake ID
    allplayers = {}

    def __init__(self, bot):
        '''
        Initializer function that allows us to access the bot within this cog
        '''
        self.bot = bot

    @commands.command()
    async def establish_player(self, ctx):
        '''
	    Initializes a player object for the user that called this command
    	'''
        ## NEED TO CHECK IF THE CHANNEL THAT THE USER IS IN HAS A ROUND
        ## RUNNING RIGHT NOW
        user = ctx.author # The author of the message
        channel = ctx.channel # Current guild channel
        result = user in playerActions.allplayers # True if the user already
        # has a Player object, False if not
	
        # Prevents duplicate Player objects for one user
        if result == False:
            newplayer = PlayerClass.Player(user)
            playerActions.allplayers[user.id] = newplayer
            # This way, we can access a user's Player object using the
            # member object of the user
            await ctx.send("Player established.")
        else:
            await ctx.send("Cannot establish player. Perhaps you already",
            "used this command...")
	
    @commands.command()
    async def test(self, ctx):
        user = ctx.author
        await ctx.send(playerActions.allplayers[user.id])

def setup(bot):
    '''
    Allows the bot to load this cog
    '''
    bot.add_cog(playerActions(bot))
