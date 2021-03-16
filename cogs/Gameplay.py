import asyncio
import csv
from discord.ext import commands


class Gameplay(commands.Cog):
    """
    This cog deals with actions involving the actual gameplay within a round.

    Commands:
        q!q: Start the next question.
        q!b: Buzz in for the current question.
    """

    admin_cmds = []

    # Information about the general commands of the bot (in the dictionary format required by embeds)
    general_cmds = [{'inline': False, 'name': 'q!q', 'value': 'Start the next question.'},
                    {'inline': False, 'name': 'q!b', 'value': 'Buzz in for the current question.'}]

    # todo: randomize questions and make questions in different rounds independent of each other
    def __init__(self, bot):
        """
        Initializer function that allows us to access the bot within this cog.
        """
        self.bot = bot

        # Each line of data_reader is a dictionary whose keys are the file headers
        # Keys: Question, Answer
        self.question_data = open('cogs/Questions.csv', 'r')
        self.data_reader = csv.DictReader(self.question_data)

        global roundcog
        roundcog = self.bot.get_cog('RoundCreator')

    def __del__(self):
        self.question_data.close()

    # todo: make sure you can only queue a question if there is an active round in this channel
    @commands.command()
    async def q(self, ctx):
        """
        Start the next question.

        Parameters:
            ctx (Context): The required context
        """
        # Pull in the next question from the CSV file and store it in a list (separated on the periods)
        # Pull in the answer to this question from the same CSV file, storing it in a str variable
        # Send a message with one sentence
        # Wait question_time seconds
        # Edit the message to add another sentence
        # Halt if someone buzzes
        # Stop the loop when the question ends and display the correct answer
        # If time runs out and no-one has guessed correctly, display the correct answer

        if roundcog:
            pass

        # Pull in the next question and answer from the file
        question_and_answer = next(self.data_reader)
        answer = question_and_answer['Answer']

        # Split the question on the periods
        question_separated = question_and_answer['Question'].split('. ')

        i = 0
        answered = False
        while i < len(question_separated) and not answered:
            await ctx.send(question_separated[i] + '. ')
            i += 1



            pass

        # While the question hasn't been answered and there is still more question:
        #   print one sentence of the question
        #   wait question_time seconds or until someone buzzes
        #   if someone buzzes
        #       check if the answer was right (ignore case) and change the flag
        # Display the answer

    # todo: make sure that you can only buzz in when a question is active
    # todo: make sure only one player can buzz in at a time
    @commands.command()
    async def b(self, ctx):
        """
        Buzz in for the current question.

        Parameters:
            ctx (Context): The required context
        """
        # Halt the question reading
        # Wait buzz_time seconds
        # If the buzz is correct, display the rest of the question along with the answer


def setup(bot):
    """
    Allow the bot to load this cog.
    """
    bot.add_cog(Gameplay(bot))
