import discord
from discord.ext import commands
from discord.ext import tasks
import cogs.PlayerClass as PlayerClass
import cogs.RoundClass as RoundClass
import os
import ast
import pickle
import dill

class playerActions(commands.Cog):
    '''
    This cog deals with commands that have to do with the user's Player
    object and its methods

    Loops:
        savePlayers: Saves player information every 3 minutes

    Commands:
    q!establish_player: Initializes a player object for the user that
                            called the command
    q!save_players: Saves player information
    '''
   
    # If there is no player data written yet, just make a new dictionary
    if os.stat("cogs/PlayerData.txt").st_size == 0:
        allplayers = {}
    
    # Load the player data if it exists
    else:
        # Open the file for reading
        playerfile = open("cogs/PlayerData.txt", "r")


        # Load in the information
        ####filecontents = playerfile.read()
        # Convert the information from string to dictionary
        ####allplayers = ast.literal_eval(filecontents)

        ###allplayers = pickle.load(playerfile)
        allplayers = dill.load(playerfile)

        # Always close the file after using
        playerfile.close()

    def __init__(self, bot):
        '''
        Initializer function that allows us to access the bot within this cog
        '''
        self.bot = bot
        self.autosave.start()

    @tasks.loop(minutes = 3)
    async def autosave(self):
        '''
        Saves player information every 3 minutes
        '''
        await self.save_players()

    @commands.command(aliases = ["savep", "sp", "saveplayers", "savePlayers"])
    async def save_players(self):
        '''
        Saves player information
        '''
        # Open the file to write
        playerfile = open("cogs/PlayerData.txt", "w")


        # Write the data to the file
        ####stringrep = str(playerActions.allplayers)
        ####playerfile.write(stringrep)


        ###pickle.dump(playerActions.allplayers, playerfile, -1)
        dill.dump_session(playerfile)

        # Close the file
        playerfile.close()

    @commands.command(aliases = ["ep", "establish", "establishplayer", "est"])
    async def establish_player(self, ctx):
        '''
	    Initializes a player object for the user that called this command
    	'''
        user = ctx.author # The author of the message
        guild_id = ctx.guild.id # Current guild

        # Make sure the user doesn't have multiple Player objects
        try:
            # result is True if  user already has a Player object
            result = False
            while result == False:
                # Loop through the list of players until we find the user
                for player in allplayers[guild_id]:
                    if player.id == user.id:
                        result = True
       
        # If a KeyError was produced, the guild isn't in the dictionary
        except:
            result = False
	
        if result == False:
            # Create a Player object
            newplayer = PlayerClass.Player(user)
            
            # Make sure this guild is in the dictionary
            try:
                playerActions.allplayers[guild_id][user.id] = newplayer
            except:
                playerActions.allplayers[guild_id] = {}
                playerActions.allplayers[guild_id][user.id] = newplayer
           
           # This way, we can access a user's Player object using the
            # member object of the user
            await self.save_players()
            await ctx.send("Player established.")
        else:
            await ctx.send("Cannot establish player. Perhaps you already",
            "used this command...")

def setup(bot):
    '''
    Allows the bot to load this cog
    '''
    bot.add_cog(playerActions(bot))
