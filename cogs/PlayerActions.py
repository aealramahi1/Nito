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
        autosavePlayers: Save player information every 3 minutes.

    Commands:
        q!load_players: Load player information.
        q!save_players: Save player information.
        q!establish_player: Register as a player.
    """

    # Information about the administrator and general commands of the bot (in the dictionary format required by embeds)
    admin_cmds = [{'inline': False, 'name': 'q!load_players\tq!lp\tq!loadp\tq!loadplayers',
                   'value': 'Load player information.'},
                  {'inline': False, 'name': 'q!save_players\tq!sp\tq!savep\tq!saveplayers',
                   'value': 'Save player information.'}]

    general_cmds = [{'inline': False, 'name': 'q!establish_player\tq!ep\tq!establish\tq!establishplayer',
                     'value': 'Register as a player.'}]

    # Stores the Player objects in the format
    # {GUILD_ID : {USER_ID : PLAYEROBJ}}
    allp = {}

    def __init__(self, bot):
        """
        Initializer function that allows us to access the bot within this cog.
        """
        self.bot = bot

    @tasks.loop(minutes=3)
    async def autosavePlayers(self):
        """
        Save player information every 3 minutes.
        """
        await self.save_players()

    @commands.command(aliases=['lp', 'loadp', 'loadplayers'])
    @commands.has_permissions(manage_messages=True)
    async def load_players(self):
        """
        Load player information. Only administrators may use this command.
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

    @commands.command(aliases=['sp', 'savep', 'saveplayers'])
    @commands.has_permissions(manage_messages=True)
    async def save_players(self):
        """
        Save player information. Only users with administrative powers may use this command.
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
        Initialize a player object for the user that called this command.
        """

        # Make sure the guild is in the dictionary
        try:
            PlayerActions.allp[ctx.guild.id]
        except KeyError:
            PlayerActions.allp[ctx.guild.id] = {}

        # Make sure the person actually needs to establish a player
        try:
            PlayerActions.allp[ctx.guild.id][ctx.author.id]
            await ctx.send('You have already registered yourself as a player...')
        except KeyError:
            newplayer = PlayerClass.Player(ctx.author.id)
            PlayerActions.allp[ctx.guild.id][ctx.author.id] = newplayer
            await self.save_players()
            await ctx.send('Player established.')


def setup(bot):
    """
    Allows the bot to load this cog
    """
    bot.add_cog(PlayerActions(bot))
