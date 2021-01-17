import pandas
from discord.ext import commands

# todo: maybe implement pandas to pull in the data


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

    def __init__(self, bot):
        """
        Initializer function that allows us to access the bot within this cog.
        """
        self.bot = bot

    # todo: close the file when the round ends
    @commands.command()
    async def q(self, ctx):
        """
        Start the next question.

        Parameters:
            ctx (Context): The required context
        """

        # process the entire file
        question_file = open("cogs/Questions.csv", "r")
        whole_file = question_file.read()
        questions_and_answers = whole_file.split("\n")

        # todo: this won't work if there are comments in the questions
        # split up the file into questions and answers
        questions = []
        answers = []
        for pair in questions_and_answers:
            questions.append(pair.split(',')[0])
            answers.append(pair.split(',')[1])

        print(questions)
        print(answers)

        # Pull in the next question from the CSV file and store it in a list (separated on the periods)
        # Pull in the answer to this question from the same CSV file, storing it in a str variable
        # Send a message with one sentence
        # Wait question_time seconds
        # Edit the message to add another sentence
        # Halt if someone buzzes
        # Stop the loop when the question ends and display the correct answer
        # If time runs out and no-one has guessed correctly, display the correct answer

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
