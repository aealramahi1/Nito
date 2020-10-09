import os
import asyncio
from discord.ext import commands
from discord.ext import tasks
import RoundClass


class roundCreator(commands.Cog):
    """
    This cog deals with the actions involved in managing rounds

    Loops:
        savePlayers: saves round information every 4 minutes

    Methods:
        getRound(gid, cid): Returns the current round, if found
        createRound(gid, cid, newrnd): Creates a new round

    Commands:
        q!load_players: Loads round information
        q!save_rounds: Saves round information
        q!create_round: Creates a new round or reactivates an existing one
        q!end_round: Ends the currently active round
        q!join: Joins the round in the current channel (if permission is
                granted by the round owner)
        q!leave: Leave the round in the current channel
        q!set_question_time: Sets the question time for this round
        q!check_question_time: Checks the current question time for this round
        q!set_buzz_time: Sets the buzz time for this round
        q!check_buzz_time: Checks the buzz time for this round
    """

    # Stores the Round objects in the format
    # {GUILD_ID : {CHANNEL_ID : ROUNDOBJ}}
    allr = {}

    def __init__(self, bot):
        """
        Initializer function that allows us to access the bot within this cog
        """
        self.bot = bot
        global playercog
        playercog = self.bot.get_cog("playerActions")

    @tasks.loop(minutes=4)
    async def autosaveRounds(self):
        """
        Saves round information every 4 minutes.
        """
        await self.save_rounds()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def load_rounds(self):
        """
        Loads round information. Only guild administrators may use this command.
        """
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
                roundCreator.allr[gid] = {}

                # Loop through all the channels and re-establish Round objects
                # We count by twos so that we shift to the next channel
                # each time instead of to a Round object
                for i in range(1, len(all_data) - 1, 2):
                    channel = int(all_data[i])
                    roundobj = all_data[i + 1]
                    roundCreator.allr[gid][channel] = eval(roundobj)

    @commands.command(aliases=["saver", "saverounds", "saveRounds"])
    @commands.has_permissions(manage_messages=True)
    async def save_rounds(self):
        """
        Saves round information. Only administrators may use this command.
        """
        # Open the file to write
        round_file = open("cogs/RoundData.txt", "w")

        write_data = ""
        # Write the data so that guilds are separated by @ and channels/rounds
        # objects are separated with *

        # Loop through and write all of the guild_ids
        for guild in roundCreator.allr:
            # We don't want the first character to be @
            if write_data == "":
                write_data += str(guild)
            else:
                write_data += "@" + str(guild)

            # Loop through the channels and the rounds and add them
            for channel in roundCreator.allr[guild]:
                the_round = roundCreator.allr[guild][channel]
                write_data += "*" + str(channel)
                # Grab the initializer for this Round object
                write_data += "*" + the_round.getInitializer()

        # Write the updated dictionary to the file
        round_file.write(write_data)

        # Close the file
        round_file.close()

    async def makeRound(self, gid, cid, newrnd):
        """
        Creates a new round and handles the case where the guild
        is not present in the allRounds dictionary

        Parameters:
            gid (int): The guild id
            cid (int): The channel id
            newrnd (Round Object): The new round
        """
        # If the guild id is not in the dictionary then we will get
        # an error
        try:
            roundCreator.allr[gid][cid] = newrnd
        except KeyError:
            # Create a key for the guild id
            roundCreator.allr[gid] = {}
            roundCreator.allr[gid][cid] = newrnd
            await self.save_rounds()

    @commands.command(aliases=["createround", "create", "cr", "start",
                               "startround", "sr"])
    async def create_round(self, ctx):
        """
        Generate a round with you set as the owner of the round
        """
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id

        # Make sure the user has a Player object
        try:
            round_owner = playercog.allp[guild_id][ctx.author.id]
            this_round, status = getRound(guild_id, channel_id)

            # One round object is created for each channel and then is activated
            # and deactivated subsequently so we check if one already exists

            # If the round exists, start it
            if this_round:
                this_round.startRound(round_owner)
                await ctx.send("Round created.")

            # If no round exists, create a new one
            elif this_round is None:
                new_round = RoundClass.Round()
                await self.makeRound(guild_id, channel_id, new_round)
                new_round.startRound(round_owner)
                await ctx.send("New round created")
        except KeyError:
            await ctx.send("You have not yet established yourself as a player!")

    @commands.command(aliases=["endround", "er"])
    async def end_round(self, ctx):
        """
        End the round generated by the create_round command and displays the
        leaderboard
        """
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id
        try:
            user = playercog.allp[guild_id][ctx.author.id]
            this_round, status = getRound(guild_id, channel_id)

            # If the round exists
            if this_round:
                # Active round
                if status:
                    # Make sure this is the round owner ending the round
                    if user == this_round.round_owner:
                        this_round.endRound()
                        await ctx.send("Round ended.")
                    else:
                        await ctx.send("You are not the round owner.")
                # Inactive round
                elif not status:
                    await ctx.send("This round was never started...")
                # Triggered by an error (status == None)
                else:
                    await ctx.send("An error occurred trying to end a round")

            # If the round doesn't exist
            elif not this_round:
                await ctx.send("Error: no round found.")
        except KeyError:
            await ctx.send("You have not yet established yourself as a player!")

    @commands.command(aliases=["j", "jo", "joi"])
    async def join(self, ctx):
        """
        Request to join a currently established round
        """
        this_round, status = getRound(ctx.guild.id, ctx.channel.id)
        new_player = getPlayer(ctx.guild.id, ctx.author.id)

        # Will be used later in this command
        def correctUser(context):
            """
            Makes sure that the user is round_owner and is messaging in the
            correct channel

            Parameters:
                context: The context

            Returns:
                result (Boolean): True if the user is round_owner
            """
            result = context.author == this_round.round_owner and \
                context.channel.id == ctx.channel.id
            return result

        # Round exists and the player isn't joining a round they're already in
        if this_round and new_player not in this_round.getPlayers():
            # Round active
            if status:
                # The mention strings for the relevant users (allows us
                # to mention them in the channel)
                mention_owner = this_round.getRoundOwner().mention
                mention_player = new_player.mention

                # Asks round_owner for permission to join
                await ctx.send("Hey %s, can %s join (y/n)?" %
                               (mention_owner, mention_player))

                # Errors can be triggered if this times out so we handle them
                try:
                    # Wait for 5 seconds for a response
                    response = await self.bot.wait_for('message', timeout=5.0,
                                                       check=correctUser)
                    response_content = response.content
                # todo: make sure this works
                except asyncio.TimeoutError:
                    # If the round owner doesn't respond, do nothing
                    await ctx.send("No response? Sorry %s, you" % mention_player,
                                   "can't join unless you get approval.")
                    response_content = "n"

                # If the round owner said yes, join the player
                if response_content == "y":
                    this_round.addPlayer(new_player)
                    await ctx.send("Welcome to the round %s" % mention_player)
                # If the round owner said no, do nothing and apologize
                elif response_content == "n":
                    await ctx.send("Sorry %s, tough luck!" % mention_player)
                # If the round owner put something else
                else:
                    await ctx.send("I asked for y or n...")

            # Round inactive
            elif not status:
                await ctx.send("No active round found.")

        # The user isn't joining a round they are already in
        elif new_player in this_round.getPlayers():
            await ctx.send("You are already in this round...")

        # No round found
        elif not this_round:
            await ctx.send("Error: no round found.")

        # No Player found
        elif not new_player:
            await ctx.send("You have not yet established yourself as a player!")

    @commands.command(aliases=["l", "leav", "lev"])
    async def leave(self, ctx):
        """
        Leave the round you are currently in
        """
        this_round, status = getRound(ctx.guild.id, ctx.channel.id)
        old_player = getPlayer(ctx.guild.id, ctx.author.id)

        # Make sure there is a round and a player
        if this_round and old_player:

            # ...and that it's active
            if status:
                this_round.removePlayer(old_player)
                await ctx.send("Goodbye %s" % old_player.mention)
            elif not status:
                await ctx.send("No active round found.")
            else:
                await ctx.send("An error occurred trying to leave a round")

        # No round found
        elif not this_round:
            await ctx.send("Error: no round found.")

        # No player found
        elif not old_player:
            await ctx.send("You have not yet established yourself as a player!")

    @commands.command(aliases=["setq", "setqt"])
    async def set_question_time(self, ctx, time):
        """
        Set the question time for this round. This command may only be used
        by the round owner if the round is active

        Parameters:
            ctx: The context
            time (float/int): The new time (seconds) of question_time
        """
        this_round, status = getRound(ctx.guild.id, ctx.channel.id)
        user = getPlayer(ctx.guild.id, ctx.author.id)

        # If the round is active, only the round owner may call this command
        if this_round.status and user:
            # The Round class will do all our checks for us
            msg = this_round.setQuestionTime(user, time)
            await ctx.send(msg)

        # If there is no round or the round is inactive, we can't change
        # the time
        elif not this_round.status or not this_round:
            await ctx.send("No round found.")

        # If the user has no Player object we don't want them changing anything
        elif not user:
            await ctx.send("You have not yet established yourself as a player!")


def getRound(gid, cid):
    """
    Returns the current round and status, if found

    Parameters:
        gid (int): The guild id
        cid (int): The channel id

    Returns:
        this_round (Round object): The current round (if there is no
                                   round found in this channel, None)
        status (Boolean): The status of the current round (or None)
    """
    # Check to make sure the round object exists and get its status
    try:
        this_round = roundCreator.allr[gid][cid]
        status = this_round.round_status
    except KeyError:
        this_round = None
        status = None
    return this_round, status


def getPlayer(gid, authid):
    """
    Returns the Player object for the user with aid, if found

    Parameters:
        gid (int): The guild id
        authid (int): The user id

    Returns:
        user (Player object): The Player object for the user (if there is no
                              player found, None)
    """
    # Make sure the Player object exists
    try:
        user = playercog.allp[gid][authid]
    except KeyError:
        user = None
    return user


def setup(bot):
    """
    Allows the bot to load this cog
    """
    bot.add_cog(roundCreator(bot))
