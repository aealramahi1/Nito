import RoundClass
import discord
from discord.ext import commands

class defaults(commands.Cog):
    '''
    This cog houses the commands involved in setting defaults for rounds and
    players. Please note that anything in brackets represents a value to be
    inputted (i.e. [number] means that you would type a number)

    Commands:
        q!set_question_time [number]: Sets the time in between each sentence
                                   for this round and future rounds until
                                   changed
    '''
    def __init__(self, bot):
        '''
        Initializer function that allows us to access the bot within this cog
        '''
        self.bot = bot

    @commands.command()
    async def set_question_time(self, ctx, time):
        '''
        Sets the time in between each sentence for this round and future rounds

        Paramteters:
           time (float/int): The time in seconds 
        '''
        ## implementation

    @commands.command()
    async def check_question_time(self, ctx):
        '''
        Checks the time in between each sentence for this round
        '''
        ## implementation

def setup(bot):
    '''
    Allows the bot to load this cog
    '''
    bot.add_cog(defaults(bot))
