import os
from discord.ext import commands
from discord.ext import tasks
import cogs.Player as PlayerClass


class PlayerActions(commands.Cog):
    """
    This cog deals with commands that have to do with the user's Player
    object and its methods

    Attributes:
        allp: Nested dictionary storing the Player objects in the format of {GUILD_ID : {USER_ID : PLAYEROBJ}}

    Loops:
        autosavePlayers: Saves player information every 3 minutes

    Commands:
        q!load_players: Loads player information
        q!save_players: Saves player information
        q!establish_player: Initializes a player object for the user that called the command
    """

    # Information about the administrator and general commands of the bot (in the dictionary format required by embeds)
    admin_cmds = [{'inline': False, 'name': 'q!load_players\tq!lp\tq!loadp\tq!loadplayers',
                   'value': 'Loads player information.'},
                  {'inline': False, 'name': 'q!save_players\tq!sp\tq!savep\tq!saveplayers',
                   'value': 'Saves player information.'}]

    general_cmds = [{'inline': False, 'name': 'q!establish_player\tq!ep\tq!establish\tq!establishplayer',
                     'value': 'Initializes a player object for the user that called this command.'}]

    # Stores the Player objects in the format
    # {GUILD_ID : {USER_ID : PLAYEROBJ}}
    allp = {}

    def __init__(self, bot):
        """
        Initializer function that allows us to access the bot within this cog
        """
        self.bot = bot

    @tasks.loop(minutes=3)
    async def autosavePlayers(self):
        """
        Saves player information every 3 minutes.
        """
        await self.save_players()

    @commands.command(aliases=['lp', 'loadp', 'loadplayers'])
    @commands.has_permissions(manage_messages=True)
    async def load_players(self):
        """
        Loads player information. Only administrators may use this command.
        """
        if os.stat('cogs/PlayerData.txt').st_size != 0:
            # Open the data file for reading
            playerdata = open('cogs/PlayerData.txt', 'r')
            contents = playerdata.read()

            # Gather all the player data by guild
            # Each guild is separated by a \n character
            guilds = contents.split('\n')

            # Loop through each guild
            for guild in guilds:
                # The users and Player objects are split by *
                all_data = guild.split('*')
                # The guild ID is the first element
                gid = int(all_data[0])
                # Make this dictionary nested
                PlayerActions.allp[gid] = {}

                # Loop through all the users and re-establish Player objects
                # We count by twos so that we shift to the next user each time
                # instead of to a Player object
                for i in range(1, len(all_data) - 1, 2):
                    user = int(all_data[i])
                    playerobj = all_data[i + 1]
                    PlayerActions.allp[gid][user] = eval(playerobj)

    @commands.command(aliases = ['sp', 'savep', 'saveplayers'])
    @commands.has_permissions(manage_messages=True)
    async def save_players(self):
        """
        Saves player information. Only users with administrative powers may use this command
        """
        # Open the file to write
        playerfile = open('cogs/PlayerData.txt', 'w')

        write_data = ''

        # Write the data so that guilds are separated by \n and users/player
        # objects are separated with *

        # Loop through and write all of the guild_ids
        for guild in PlayerActions.allp:

            # We don't want the first character to be \n
            if write_data == '':
                write_data += str(guild)
            else:
                write_data += '\n' + str(guild)

            # Loop through the users and the Players and add them
            for user in PlayerActions.allp[guild]:
                player = PlayerActions.allp[guild][user]
                write_data += '*' + str(user)

                # Grab the initializer for this Player object
                write_data += '*' + player.getInitializer()

        # Write the updated dictionary to the file
        playerfile.write(write_data)

        # Close the file
        playerfile.close()

    @commands.command(aliases=['ep', 'establish', 'establishplayer'])
    async def establish_player(self, ctx):
        """
        Initializes a player object for the user that called this command
        """
        user = ctx.author  # The author of the message
        guild_id = ctx.guild.id  # Current guild

        # Make sure the user doesn't have multiple Player objects
        try:

            # result is True if the user already has a Player object
            result = False

            # flag is False unless we reach the end of the dictionary
            flag = False
            all_users = PlayerActions.allp[guild_id].keys()
            numelements = len(all_users) - 1
            i = 0
            while not result and not flag:
                # Loop through the list of players until we find the user
                for person in PlayerActions.allp[guild_id]:
                    if person == user.id:
                        result = True
                    if i == numelements:
                        flag = True
                    i += 1

        # If a KeyError was produced, the guild isn't in the dictionary
        except KeyError:
            result = False

        if not result:
            # Create a Player object
            newplayer = PlayerClass.Player(user.id)

            # Make sure this guild is in the dictionary
            try:
                PlayerActions.allp[guild_id][user.id] = newplayer
            except KeyError:
                PlayerActions.allp[guild_id] = {}
                PlayerActions.allp[guild_id][user.id] = newplayer

            # This way, we can access a user's Player object using the
            # member object of the user
            await self.save_players()
            await ctx.send('Player established.')
        else:
            await ctx.send('Cannot establish player. Perhaps you already ' +
                           'used this command...')


def setup(bot):
    """
    Allows the bot to load this cog
    """
    bot.add_cog(PlayerActions(bot))
