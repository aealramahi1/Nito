import discord
from discord.ext import commands
from discord.ext import tasks
import cogs.RoundClass as RoundClass
import os

class roundCreator(commands.Cog):
    '''
    This cog deals with the actions involved in managing rounds

    Loops:
        savePlayers: saves round information every 4 minutes

    Methods:
        getRound(gid, cid): Returns the current round, if found
        createRound(gid, cid, newrnd): Creates a new round

    Commands:
        q!save_rounds: Saves round information
        q!create_round: Creates a new round or reactivates an existing one
        q!end_round: Ends the currently active round
        q!join: Joins the round in the current channel (if permission is
                granted by the round owner)
        q!leave: Leave the round in the current channel
    '''

    # Stores the Round objects in the format
    # {GUILD_ID : {CHANNEL_ID : ROUNDOBJ}}
    allrounds = {}
 
    # Import the round data if we have any
    if os.stat("cogs/RoundData.txt").st_size != 0:
        # Open the data file for reading
        rounddata = open("cogs/RoundData.txt", "r")
        contents = rounddata.read()

        # Gather all the round data by guild
        # Each guild is separated by a @ character
        guilds = contents.split("@")

        # Loop through each guild
        for guild in guilds:
            # The channels and Round objects are split by *
            all_data = guild.split("*")
            # The guild ID is the first element
            gid = int(all_data[0])
            # Make this dictionary nested
            allrounds[gid] = {}

            # Loop through all the channels and re-establish Round objects
            # We count by twos so that we shift to the next channel each time
            # instead of to a Round object
            for i in range(1, len(all_data) - 1, 2):
                channel = int(all_data[i])
                roundobj = all_data[i + 1]
                allrounds[gid][channel] = eval(roundobj)   

    def __init__(self, bot):
        '''
        Initializer function that allows us to access the bot within this cog
        '''
        self.bot = bot # now we can interact with the bot using self.bot
        self.autosaveRounds.start()

    @tasks.loop(minutes = 4)
    async def autosaveRounds(self):
        '''
        Saves round information every 4 minutes
        '''
        await self.save_rounds()

    @commands.command(aliases = ["saver", "saverounds", "saveRounds"])
    async def save_rounds(self):
        '''
        Saves round information
        '''
        # We'll use this dictionary extensively here, so an alias is useful
        ar = roundCreator.allrounds

        # Open the file to write
        roundfile = open("cogs/RoundData.txt", "w")

        write_data = ""
        # Write the data so that guilds are separated by @ and channels/rounds
        # objects are separated with *

        # Loop through and write all of the guild_ids
        for guild in ar:
            # We don't want the first character to be @
            if write_data == "":
                write_data += str(guild)
            else:
                write_data += "@" + str(guild)

            # Loop through the channels and the rounds and add them
            for channel in ar[guild]:
                theround = ar[guild][channel]
                write_data += "*" + str(channel)
                # Grab the initializer for this Round object
                write_data += "*" + theround.getInitializer()

        # Write the updated dictionary to the file
        roundfile.write(write_data)
                
        # Close the file
        roundfile.close()


    def getRound(self, gid, cid):
        '''
        Returns the current round and status, if found

        Paramters:
            gid (int): The guild id
            cid (int): The channel id

        Returns:
            this_round (Round object): The current round (if there is no
                                       round found in this channel, None)
            status (Boolean): The status of the current round (or None)
        '''
        # Check to make sure the round object exists and get its status
        try:
            this_round = roundCreator.allrounds[gid][cid]
            status = this_round.getRoundStatus()
        except:
            this_round = None
            status = None
        return this_round, status

    async def makeRound(self, gid, cid, newrnd):
        '''
        Creates a new round and handles the case where the guild
        is not present in the allRounds dictionary

        Parameters:
            gid (int): The guild id
            cid (int): The channel id
        '''
        # If the guild id is not in the dictionary then we will get
        # an error
        try:
            roundCreator.allrounds[gid][cid] = newrnd
        except:
            # Create a key for the guild id
            roundCreator.allrounds[gid] = {}
            roundCreator.allrounds[gid][cid] = newrnd
            await self.save_rounds()
    
    @commands.command(aliases = ["createround", "create", "cr", "start",
                                 "startround", "sr"])
    async def create_round(self, ctx):
        '''
        Generate a round with you set as the owner of the round
        '''
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id
        round_owner = ctx.author

        this_round, status = self.getRound(guild_id, channel_id)

        # One round object is created for each channel and then is activaated
        # and deactivated subsequently so we check if one already exists

        # If the round exists, start it
        if this_round:
            this_round.startRound(round_owner)
            await ctx.send("Round created.")
       
        # If no round exists, create a new one, add it to the list, then
        # start it
        elif this_round == None:
            new_round = RoundClass.Round()
            await self.makeRound(guild_id, channel_id, new_round)
            new_round.startRound(round_owner)
            await ctx.send("New round created")

    @commands.command(aliases = ["endround", "er"])
    async def end_round(self, ctx):
        '''
        End the round generated by the create_round command and displays the
        leaderboard
        '''
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id
        user_id = ctx.author.id

        this_round, status = self.getRound(guild_id, channel_id)

        # If the round exists
        if this_round:
            # Active round
            if status == True:
                # Make sure this is the round owner ending the round
                if user_id == this_round.getRoundOwner().id:
                    this_round.endRound()
                    await ctx.send("Round ended.")
                else:
                    await ctx.send("You are not the round owner.")
            # Inactive round
            elif status == False:
                await ctx.send("This round was never started...")
            # Triggered by an error (status == None)
            else:
                await ctx.send("An error occurred trying to end a round")
       
       # If the round doesn't exist
        elif not this_round:
            await ctx.send("Error: no round found.")

    @commands.command(aliases = ["j", "jo", "joi"])
    async def join(self, ctx):
        '''
        Request to join a currently established round
        '''
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id
        new_player = ctx.author

        this_round, status = self.getRound(guild_id, channel_id)

        # Will be used later in this command
        def correctUser(ctx):
            '''
            Makes sure that the user is round_owner and is messaging in the
            correct channel

            Returns:
                result (Boolean): True if the user is round_owner
            '''
            result = ctx.author == this_round.getRoundOwner() and \
                     ctx.channel.id == channel_id
            return result

        # Round exists and the player isn't joining a round they're in
        if this_round and new_player not in this_round.getPlayers():
            # Round active
            if status == True:
                # The mention strings for the relevant useres (allows us
                # to mention them in the channel)
                mentionowner = this_round.getRoundOwner().mention
                mentionplayer = new_player.mention

                # Asks round_owner for permission to join
                await ctx.send ("Hey %s, can %s join (y/n)?" % 
                                (mentionowner, mentionplayer))
                
                # Errors can be triggered if this times out so we handle them
                try:
                    # Wait for 5 seconds for a response
                    response = await self.bot.wait_for('message', timeout = 5.0,
                                                  check = correctUser)
                except:
                    # If the round owner doesn't respond, do nothing
                    await ctx.send("No response? Sorry %s, you" % mentionplayer,
                            "can't join unless you get approval.")

                # If the round owner said yes, join the player
                if response.content  == "y":
                    await ctx.send("Welcome to the round %s" % mentionplayer)
                # If the round owner said no, do nothing and apologize
                elif response.content  == "n":
                    await ctx.send("Sorry %s, tough luck!" % mentionplayer)
                # If the round owner put something else
                else:
                    await ctx.send("I asked for y or n...")
            
            # Round inactive
            elif status == False:
                await ctx.send("No active round found.")
            
        elif not this_round:
            await ctx.send("Error: no round found.")

        # The user isn't joining a round they are already in
        elif new_player in this_round.getPlayers():
            await ctx.send("You are already in this round...")

    @commands.command(aliases = ["l", "leav", "lev"])
    async def leave(self, ctx):
        '''
        Leave the round you are currently in
        '''
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id
        old_player = ctx.author

        this_round, status = self.getRound(guild_id, channel_id)

        # The same nested if as above
        if this_round:
            if status == True:
                this_round.removePlayer(old_player)
                await ctx.send("Goodbye %s" % old_player.mention)
            elif status == False:
                await ctx.send("No active round found.")
            else:
                await ctx.send("An error occurred trying to leave a round")
        elif not this_round:
            await ctx.send("Error: no round found.")

def setup(bot):
    '''
    Allows the bot to load this cog
    '''
    bot.add_cog(roundCreator(bot))
