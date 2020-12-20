from discord.ext import commands

class Gameplay(commands.Cog):
    """
    This cog deals with actions involving the actual gameplay within a round.

    Commands:
        q!q: Start the next question.
        q!b: Buzz in for the current question.
    """

    def __init__(self, bot):
        """
        Initializer function that allows us to access the bot within this cog.
        """
        self.bot = bot

    @commands.command()
    async def q(self, ctx):
        """
        Start the next question.

        Parameters:
            ctx (Context): The required context
        """

    @commands.command()
    async def b(self, ctx):
        """
        Buzz in for the current question.

        Parameters:
            ctx (Context): The required context
        """

def setup(bot):
    """
    Allows the bot to load this cog
    """
    bot.add_cog(Gameplay(bot))