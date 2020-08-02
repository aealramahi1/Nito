# NEXT STEPS:
    # create player variables and player class
    # create_round
        # assign current round owner
    # end_round
        # remove all players from their roles
    # join
        # ask the round owner for permission to join
        # assign role for player if allowed
    # leave
        # remove the caller from role
    # remember, role here does not mean guild role, more like object/alias
    # begin to implement timed in these commands

import discord
from discord.ext import commands

class round_creator(commands.Cog):

    def __init__(self, bot):
        '''Initializer function that allows us to access the bot within this cog'''
        self.bot = bot # now we can interact with the bot using self.bot

    #### @commands.command() for commands
    #### @commands.Cog.listener() for events
    #### remember to always pass in self since this is a class

    @commands.command()
    async def create_round(self, ctx):
        '''Generate a round with you set as the owner of the round'''
        ## implementation

    @commands.command()
    async def end_round(self, ctx):
        '''End the round generated by the create_round command and displays the leaderboard'''
        ## implementation

    @commands.command()
    async def join(self, ctx):
        '''Request to join a currently established round'''
        ## implementation

    @commands.command()
    async def leave(self, ctx):
        '''Leave the round you are currently in'''
        ## implementation

def setup(bot):
    '''Allows the bot to load this cog'''
    bot.add_cog(round_creator(bot))