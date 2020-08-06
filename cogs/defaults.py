import discord
from discord.ext import commands

class defaults(commands.Cog):

    def __init__(self, bot):
        '''
        Initializer function that allows us to access the bot within this cog
        '''
        self.bot = bot

    @commands.command()
    async def set_question_time(self, ctx): ## this may be wrong
        '''Sets the time in between each sentence for this round only'''
        ## implementation

    @commands.command()
    async def check_question_time(self, ctx):
        '''Checks the time in between each sentence for this round'''
        ## implementation

def setup(bot):
    '''Allows the bot to load this cog'''
    bot.add_cog(defaults(bot))
