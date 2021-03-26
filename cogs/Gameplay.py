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

        global buzzed
        buzzed = False

    def __del__(self):
        self.question_data.close()

    # todo: make it so that the last part of the question runs properly (currently displays answer too soon)
    @commands.command()
    async def q(self, ctx):
        """
        Start the next question.

        Parameters:
            ctx (Context): The required context
        """

        # Only perform this action if the round exists and is active
        this_round = roundcog.allr[ctx.guild.id][ctx.channel.id]

        if this_round and this_round.round_status:

            # Pull in the next question and answer from the file
            question_and_answer = next(self.data_reader)
            answer = question_and_answer['Answer']

            # Split the question on the periods
            question_separated = question_and_answer['Question'].split('. ')

            i = 0
            answered = False
            global buzzed
            message = await ctx.send(question_separated[i] + '. ')

            # Loop while the question hasn't been answered and there is still more of the question to display
            while i < len(question_separated) - 1 and not answered:
                i += 1
                j = 0

                # Wait question_time seconds or until someone buzzes, checking every second
                while j < this_round.question_time and not answered:
                    await asyncio.sleep(1)

                    if buzzed:
                        # todo: add a check to make sure it's the user that buzzed

                        # Get the response of the user who buzzed
                        response = await self.bot.wait_for('message', timeout=this_round.buzz_time)
                        response_content = response.content
                        buzzed = False

                        # Check the answer
                        if (response_content == answer):
                            answered = True;

                            # Display the whole question
                            await message.edit(content=question_and_answer['Question'])
                            await ctx.send("Correct!")
                        else:
                            await ctx.send("Not quite...")

                    j += 1

                if not answered:
                    # Display the next part of the question if not yet guessed
                    await message.edit(content=message.content + question_separated[i] + '. ')

            # Display the answer if no one got it right
            if not answered:
                await ctx.send("Answer: " + answer)

    # todo: make sure that you can only buzz in when a question is active
    # todo: make sure only one player can buzz in at a time
    @commands.command()
    async def b(self, ctx):
        """
        Buzz in for the current question.

        Parameters:
            ctx (Context): The required context
        """
        global buzzed
        buzzed = True


def setup(bot):
    """
    Allow the bot to load this cog.
    """
    bot.add_cog(Gameplay(bot))
