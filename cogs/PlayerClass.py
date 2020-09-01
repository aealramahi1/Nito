import discord
from discord.ext import commands

class Player():
    '''
    Each user who plays with this bot will have a Player object associated with
    them that stores all of their information. The object will be created when
    the user invokes the q!establish_player command (handled outside the class)

    Attributes:
        memberobj (Member object): The member object of the user
        total_score (int): Summation of all round scores for the user
        round_score (int): The score the user got in their most recent round
        question_index (int): Current question index

    Methods:
        getInitializer(): Returns the call to create a new object with the
                          data of the current object
    '''

    def __init__(self, theid, totscore=0, rndscore=0, index=0):
        '''
        Initializes a Player object for a user in the guild

        Parameters:
            memobj (Member object): The member object of the user   
        '''
        self.theid = theid
        self.total_score = totscore
        self.round_score = rndscore
        self.question_index = index # The questions are stored in a list

    def __str__(self):
        '''
        Prints vital information about the Player

        Returns:
            message (str): Represents all the information about the Player
        '''
        # The name of the user calling the command should be taken care of
        # in the client
        message += "\tTotal Score: " + str(self.total_score)
        message += "\n\tQuestion Number: " + str(self.question_index + 1)
        # We add one to the message because indexing always starts at zero
        # but in everyday life we start counting from one
        return message

    def getInitializer(self):
        '''
        Returns the call to create a new object with the same data as the
        current one
        '''
        call = "PlayerClass.Player(" + str(self.theid) + "," + \
               str(self.total_score) + "," + str(self.round_score) + "," + \
               str(self.question_index) + ")"
        return call
