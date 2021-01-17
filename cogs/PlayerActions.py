import os
import csv
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
    general_cmds = [{'inline': False, 'name': 'q!establish_player\tq!ep\tq!establish\tq!establishplayer',
                     'value': 'Register as a player.'}]

    # Stores the Player objects in the format {GUILD_ID : {USER_ID : PLAYEROBJ}}
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

    async def load_players(self):
        """
        Load player information. Only administrators may use this command.
        """
        if os.stat('cogs/PlayerData.csv').st_size != 0:
            with open('cogs/PlayerData.csv', 'r') as player_data:

                # Each line of data_reader is a dictionary whose keys are the file headers
                # Keys: Guild ID, Player ID, Total Score, Round Score, Player Index
                data_reader = csv.DictReader(player_data)
                for row in data_reader:

                    # Create the Player object for this user
                    try:
                        PlayerActions.allp[row['Guild ID']][row['Player ID']] = PlayerClass.Player(row['Player ID'],
                                                                                                   row['Total Score'],
                                                                                                   row['Round Score'],
                                                                                                   row['Player Index'])
                    except KeyError:
                        PlayerActions.allp[row['Guild ID']] = {}
                        PlayerActions.allp[row['Guild ID']][row['Player ID']] = PlayerClass.Player(row['Player ID'],
                                                                                                   row['Total Score'],
                                                                                                   row['Round Score'],
                                                                                                   row['Player Index'])

    async def save_players(self):
        """
        Save player information. Only users with administrative powers may use this command.
        """
        with open('cogs/PlayerData.csv', 'w') as player_data:
            data_writer = csv.DictWriter(player_data, fieldnames=['Guild ID', 'Player ID', 'Total Score', 'Round Score',
                                                                  'Player Index'])
            data_writer.writeheader()

            # Write all the data to the csv file
            for guild_id, user_dict in PlayerActions.allp.items():
                for user_id, player_obj in user_dict.items():
                    data_writer.writerow(
                        {'Guild ID': guild_id, 'Player ID': user_id, 'Total Score': player_obj.total_score,
                         'Round Score': player_obj.round_score, 'Player Index': player_obj.question_index})

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
