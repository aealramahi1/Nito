import os
import csv
import asyncio
from discord.ext import commands
from discord.ext import tasks
import cogs.Round as RoundClass


class RoundCreator(commands.Cog):
    """
    This cog deals with the actions involved in managing rounds.

    Loops:
        savePlayers: Save round information every 4 minutes

    Methods:
        getRound(gid, cid): Return the current round, if found.
        createRound(gid, cid, newrnd): Create a new round.

    Commands:
        q!load_rounds: Load round information.
        q!save_rounds: Save round information.
        q!create_round: Create a new round or reactivates an existing one.
        q!end_round: End the currently active round.
        q!join: Join the round in the current channel (if permission is granted by the round owner).
        q!leave: Leave the round in the current channel.
        q!set_question_time: Set the question time for this round.
        q!check_question_time: Check the current question time for this round.
        q!set_buzz_time: Set the buzz time for this round.
        q!check_buzz_time: Check the buzz time for this round.
    """

    # Information about the administrator and general commands of the bot (in the dictionary format required by embeds)
    admin_cmds = [{'inline': False, 'name': 'q!load_rounds',
                   'value': 'Load round information.'},
                  {'inline': False, 'name': 'q!save_rounds\tq!saver\tq!saverounds',
                   'value': 'Save round information.'}]

    general_cmds = [
        {'inline': False, 'name': 'q!create_round\tq!createround\tq!create\tq!cr\tq!start\tq!startround \tq!sr',
         'value': 'Create a new round or reactivates an existing one.'},
        {'inline': False, 'name': 'q!end_round\tq!endround\tq!er',
         'value': 'End the currently active round.'},
        {'inline': False, 'name': 'q!join',
         'value': 'Join the round in the current channel (if permission is granted by the round owner).'},
        {'inline': False, 'name': 'q!leave',
         'value': 'Leave the round in the current channel.'},
        {'inline': False, 'name': 'q!set_question_time\tq!setq\tq!setqt',
         'value': 'Set the question time for this round.'},
        {'inline': False, 'name': 'q!check_question_time\tq!checkq\tq!checkqt',
         'value': 'Check the question time for this round.'},
        {'inline': False, 'name': 'q!set_buzz_time\tq!setb\tq!setbt',
         'value': 'Set the buzz time for this round.'},
        {'inline': False, 'name': 'q!check_buzz_time\tq!checkb\tq!checkbt',
         'value': 'Check the buzz time for this round.'}]

    # Stores the Round objects in the format
    # {GUILD_ID : {CHANNEL_ID : ROUNDOBJ}}
    allr = {}

    def __init__(self, bot):
        """
        Initializer function that allows us to access the bot within this cog
        """
        self.bot = bot
        global playercog
        playercog = self.bot.get_cog('PlayerActions')

    @tasks.loop(minutes=4)
    async def autosaveRounds(self):
        """
        Save round information every 4 minutes.
        """
        await self.save_rounds()

    # todo: make sure there aren't type errors with the list

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def load_rounds(self):
        """
        Load round information. Only guild administrators may use this command.
        """
        # Import the round data if we have any
        if os.stat('cogs/RoundData.csv').st_size != 0:
            with open('cogs/RoundData.csv', 'r') as round_data:

                # Each line of data_reader is a dictionary whose keys are the file headers
                # Keys: Guild ID, Channel, ID, Round Owner, Question Time, Buzz Time, Player List, Round Status
                data_reader = csv.DictReader(round_data)
                for row in data_reader:

                    # Create the Round object for this round
                    try:
                        RoundCreator.allr[int(row['Guild ID'])][int(row['Channel ID'])]
                    except KeyError:
                        RoundCreator.allr[int(row['Guild ID'])] = {}

                    # ro=None, qt=5.0, bt=6.0, pl=None, stat=False
                    RoundCreator.allr[int(row['Guild ID'])][int(row['Channel ID'])] = RoundClass.Round(
                        ro=row['Round Owner'], qt=float(row['Question Time']), bt=float(row['Buzz Time']),
                        pl=list(row['Player List']),
                        stat=bool(row['Round Status']))

    @commands.command(aliases=['saver', 'saverounds'])
    @commands.has_permissions(manage_messages=True)
    async def save_rounds(self):
        """
        Save round information. Only administrators may use this command.
        """
        with open('cogs/RoundData.csv', 'w') as round_data:
            data_writer = csv.DictWriter(round_data,
                                         fieldnames=['Guild ID', 'Channel ID', 'Round Owner', 'Question Time',
                                                     'Buzz Time', 'Player List', 'Round Status'])
            data_writer.writeheader()

            # Write all the data to the csv file
            for guild_id, channel_dict in RoundCreator.allr.items():
                for channel_id, round_obj in channel_dict.items():
                    data_writer.writerow(
                        {'Guild ID': guild_id, 'Channel ID': channel_id, 'Round Owner': round_obj.round_owner,
                         'Question Time': round_obj.question_time, 'Buzz Time': round_obj.buzz_time,
                         'Player List': round_obj.player_list, 'Round Status': round_obj.round_status})

    async def makeRound(self, gid, cid, newrnd):
        """
        Create a new round and handles the case where the guild is not present in the allRounds dictionary.

        Parameters:
            gid (int): The guild id
            cid (int): The channel id
            newrnd (Round Object): The new round
        """

        # If the guild id is not in the dictionary then we will get an error
        try:
            RoundCreator.allr[gid][cid] = newrnd
        except KeyError:

            # Create a key for the guild id
            RoundCreator.allr[gid] = {}
            RoundCreator.allr[gid][cid] = newrnd
            await self.save_rounds()

    @commands.command(aliases=['createround', 'create', 'cr', 'start',
                               'startround', 'sr'])
    async def create_round(self, ctx):
        """
        Generate a round with you set as the owner of the round.
        """
        round_owner = getPlayer(ctx.guild.id, ctx.author.id)
        this_round = getRound(ctx.guild.id, ctx.channel.id)

        # Make sure the user has a Player object
        if round_owner is None:
            await ctx.send('You have not yet established yourself as a player!')
        else:

            # One round object is created for each channel and then is activated and deactivated subsequently so we
            # check if one already exists

            # If the round exists, start it
            if this_round:
                this_round.startRound(round_owner)
                await ctx.send('Round created.')

            # If no round exists, create a new one
            else:
                new_round = RoundClass.Round()
                await self.makeRound(ctx.guild.id, ctx.channel.id, new_round)
                new_round.startRound(round_owner)
                await ctx.send('New round created')

    @commands.command(aliases=['endround', 'er'])
    async def end_round(self, ctx):
        """
        End the round generated by the create_round command and display the leaderboard.
        """
        user = getPlayer(ctx.guild.id, ctx.author.id)
        this_round = getRound(ctx.guild.id, ctx.channel.id)

        if user is None:
            await ctx.send('You have not yet established yourself as a player!')
        elif this_round is None:
            await ctx.send('Error: no round found.')
        else:

            # Active round
            if this_round.round_status:

                # Make sure this is the round owner ending the round
                if user == this_round.round_owner:
                    this_round.endRound()
                    await ctx.send('Round ended.')
                else:
                    await ctx.send('You are not the round owner.')

            # Inactive round
            else:
                await ctx.send('This round was never started...')

    @commands.command(aliases=['j', 'jo', 'joi'])
    async def join(self, ctx):
        """
        Request to join a currently established round.
        """
        this_round = getRound(ctx.guild.id, ctx.channel.id)
        new_player = getPlayer(ctx.guild.id, ctx.author.id)

        # Will be used later in this command
        def correctUser(context):
            """
            Make sure that the user is round_owner and is messaging in the correct channel.

            Parameters:
                context: The context

            Returns:
                result (Boolean): True if the user is round_owner
            """
            result = context.author == this_round.round_owner and context.channel.id == ctx.channel.id
            return result

        if new_player is None:
            await ctx.send('You have not yet established yourself as a player!')
        elif this_round is None:
            await ctx.send('Error: no round found.')

        # Make sure the user isn't joining a round they are already in
        elif new_player in this_round.getPlayers():
            await ctx.send('You are already in this round...')

        # Round exists and the player isn't joining a round they're already in
        else:

            # Round inactive
            if not this_round.round_status:
                await ctx.send('No active round found.')

            # Round active
            else:

                # The mention strings for the relevant users (allows us to mention them in the channel)
                mention_owner = this_round.getRoundOwner().mention
                mention_player = new_player.mention

                # Asks round_owner for permission to join
                await ctx.send('Hey %s, can %s join (y/n)?' % (mention_owner, mention_player))

                # Errors can be triggered if this times out so we handle them
                try:

                    # Wait for 5 seconds for a response
                    response = await self.bot.wait_for('message', timeout=5.0, check=correctUser)
                    response_content = response.content
                # todo: make sure this works
                except asyncio.TimeoutError:

                    # If the round owner doesn't respond, do nothing
                    await ctx.send('No response? Sorry %s, you can\'t join unless you get approval.' % mention_player)
                    response_content = 'n'

                # If the round owner said yes, join the player
                if response_content == 'y':
                    this_round.addPlayer(new_player)
                    await ctx.send('Welcome to the round %s' % mention_player)

                # If the round owner said no, do nothing and apologize
                elif response_content == 'n':
                    await ctx.send('Sorry %s, tough luck!' % mention_player)

                # If the round owner put something else
                else:
                    await ctx.send('I asked for y or n...')

    @commands.command(aliases=['l', 'leav', 'lev'])
    async def leave(self, ctx):
        """
        Leave the round you are currently in.
        """
        this_round = getRound(ctx.guild.id, ctx.channel.id)
        old_player = getPlayer(ctx.guild.id, ctx.author.id)

        # Make sure there is a round and a player, and that the round is active
        if this_round is None or not this_round.round_status:
            await ctx.send('No active round found')
        elif old_player is None:
            await ctx.send('You have not yet established yourself as a player!')
        else:
            this_round.removePlayer(old_player)
            await ctx.send('Goodbye %s' % old_player.mention)

    @commands.command(aliases=['setq', 'setqt'])
    async def set_question_time(self, ctx, time):
        """
        Set the question time for this round. This command may only be used by the round owner if the round is active.

        Parameters:
            ctx: The context
            time (float/int): The new time (seconds) of question_time
        """
        this_round = getRound(ctx.guild.id, ctx.channel.id)
        user = getPlayer(ctx.guild.id, ctx.author.id)

        # If there is no round or the round is inactive, we can't change the time
        if this_round is None or this_round.round_status:
            await ctx.send('No round found.')

        # If the user has no Player object we don't want them changing anything
        elif user is None:
            await ctx.send('You have not yet established yourself as a player!')

        # If the round is active, only the round owner may call this command
        else:

            # The Round class will do all our checks for us
            await ctx.send(this_round.setQuestionTime(user, time))

    @commands.command(aliases=['checkq', 'checkqt'])
    async def check_question_time(self, ctx):
        """
        Check the question time for this round. This command may only be used by the round owner if the round is
        active.

        Paramters:
            ctx: The context
        """
        this_round = getRound(ctx.guild.id, ctx.channel.id)
        user = getPlayer(ctx.guild.id, ctx.author.id)

        # If there is no round or the round is inactive, we can't change the time
        if this_round is None or this_round.round_status:
            await ctx.send('No round found.')

        # If the user has no Player object we don't want them changing anything
        elif user is None:
            await ctx.send('You have not yet established yourself as a player!')

        # If the round is active, only the round owner may call this command
        else:

            # The Round class will do all our checks for us
            await ctx.send(this_round.question_time)

    @commands.command(aliases=['setb', 'setbt'])
    async def set_buzz_time(self, ctx, time):
        """
        Set the buzz time for this round. This command may only be used by the round owner if the round is active.

        Paramters:
            ctx: The context
            time (float/int): The new time (seconds) of buzz_time
        """
        this_round = getRound(ctx.guild.id, ctx.channel.id)
        user = getPlayer(ctx.guild.id, ctx.author.id)

        # If there is no round or the round is inactive, we can't change the time
        if this_round is None or this_round.round_status:
            await ctx.send('No round found.')

        # If the user has no Player object we don't want them changing anything
        elif user is None:
            await ctx.send('You have not yet established yourself as a player!')

        # If the round is active, only the round owner may call this command
        else:

            # The Round class will check that the time is valid for us
            await ctx.send(this_round.setBuzzTime(time))

    @commands.command(aliases=['checkb', 'checkbt'])
    async def check_buzz_time(self, ctx):
        """
        Check the buzz time for this round. This command may only be used by the round owner if the round is active.

        Paramters:
            ctx: The context
        """
        this_round = getRound(ctx.guild.id, ctx.channel.id)
        user = getPlayer(ctx.guild.id, ctx.author.id)

        # If there is no round or the round is inactive, we can't change the time
        if this_round is None or not this_round.round_status:
            await ctx.send('No round found.')

        # If the user has no Player object we don't want them changing anything
        elif user is None:
            await ctx.send('You have not yet established yourself as a player!')

        # If the round is active, only the round owner may call this command
        else:

            # The Round class will do all our checks for us
            await ctx.send(str(this_round.buzz_time))


def getRound(gid, cid):
    """
    Return the current round, if found.

    Parameters:
        gid (int): The guild id
        cid (int): The channel id

    Returns:
        this_round (Round object): The current round (if there is no round found in this channel, None)
    """

    # Check to make sure the round object exists
    try:
        this_round = RoundCreator.allr[gid][cid]
    except KeyError:
        this_round = None
    return this_round


def getPlayer(gid, authid):
    """
    Return the Player object for the user with aid, if found.

    Parameters:
        gid (int): The guild id
        authid (int): The user id

    Returns:
        user (Player object): The Player object for the user (if there is no player found, None)
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
    bot.add_cog(RoundCreator(bot))
