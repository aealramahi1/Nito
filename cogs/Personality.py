import asyncio
import random
from discord.ext import commands


class Personality(commands.Cog):
    """
    This cog gives Nito a little bit of character. He's fun and sweet, but can get a little cranky and sassy if you bug
    him too much.

    Commands:
        q!happiness_rate: Allow the user to rate their happiness.

    Events:
        on_message: Checks if messages sent in the guild contain keywords that trigger responses from Nito
    """

    admin_cmds = []

    # Information about the general commands of the bot (in the dictionary format required by embeds)
    general_cmds = [{'inline': False, 'name': 'q!happiness_rate', 'value': 'Rate your happiness!'}]

    responses = ['let me go back to bed >:(', 'stop bugging me.', 'leave me alone.', 'play my game!',
                 'tell me a joke :)']
    yes_responses = ['y', 'yes', 'sure', 'why not', 'yeah', 'ya', 'yas', 'yeas', 'yea', 'fine']

    def __init__(self, bot):
        """
        Initializer function that allows us to access the bot within this cog.
        """
        self.bot = bot

    # TODO: If the person gives less than a 5 nito asks if they want to see a cute picture or video
    @commands.command()
    async def happiness_rate(self, ctx):
        """
        Allow the user to rate their happiness.

        Parameters:
            ctx (Context): The required context
        """
        await ctx.send('On a scale of 1-10 how would you rate the amount of happiness you felt today?')

        try:
            response = await self.bot.wait_for('message', timeout=5.0)
            response_content = response.content

            if int(response_content) < 5:
                await ctx.send('I hope you find happiness soon. Do you want me to tell you a joke?')

                response = await self.bot.wait_for('message', timeout=5.0)
                response_content = response.content

                if response_content.lower() in Personality.yes_responses:
                    await ctx.send(
                        'Did you hear about the actor who fell through the floorboards? He was just going through a ' +
                        'stage. :)')
                else:
                    raise ValueError
            else:
                await ctx.send('I hope you feel this happiness everyday.')
        except asyncio.TimeoutError:
            await ctx.send('You seem tired, try getting some sleep :D')
        except ValueError:
            await ctx.send('Wow what a rule-breaker! I love your creativity!')

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Scans messages sent in the guild for keywords that trigger responses.

        Args:
            message (str): The message that was sent in the guild
        """
        if 'what are you doing nito' in message.content.lower():
            await message.channel.send(
                'I\'m waiting for you to ' + Personality.responses[random.randint(0, len(Personality.responses) - 1)])


def setup(bot):
    """
    Allows the bot to load this cog
    """
    bot.add_cog(Personality(bot))
