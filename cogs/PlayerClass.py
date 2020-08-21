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
        changeTotalScore(num): Adds num to total_score
        changeRoundScore(num): Adds num to round_score
        clearRoundScore(): Sets round_score to 0
        increaseIndex(): Increments question_index by 1
        setIndex(newindex): Sets question_index to newindex

        getTotalScore(): Returns total score
        getRoundScore(): Returns round score
        getQuestionIndex(): Returns question index
        getId(): Returns the snowflake ID
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

    ## SETTERS

    def changeTotalScore(self, num):
        '''
        Changes the total score of the user

        To decrease the score a negative int should be passed
        '''
        self.total_score += num

    def changeRoundScore(self, num):
        '''
        Changes the round score of the user

        To decrease the score a negative int should be passed
        '''
        self.round_score += num
        # Changing the total score in this function makes it easier for the
        # client code
        changeTotalScore(num)

    def clearRoundScore(self):
        '''Sets the round score to 0'''
        self.round_score = 0

    def increaseIndex(self):
        '''
        Increases the index of the question that the user is on by 1
        '''
        self.question_index += 1

    def setIndex(self, newindex):
        '''
        Sets the index that the question is on to the new index
        '''
        self.question_index = newindex

    ## GETTERS

    def getTotalScore(self):
        '''
        Returns the user's total score
        '''
        return self.total_score

    def getRoundScore(self):
        '''
        Returns the user's round score
        '''
        return self.round_score

    def getQuestionIndex(self):
        '''
        Returns the index of the question that the user is currently on
        '''
        return self.question_index

    def getId(self):
        '''
        Returns the snowflake ID of the player
        '''
        return self.theid

    def getInitializer(self):
        '''
        Returns the call to create a new object with the same data as the
        current one
        '''
        call = "PlayerClass.Player(" + str(self.getId()) + "," + \
               str(self.total_score) + "," + str(self.round_score) + "," + \
               str(self.question_index) + ")"
        return call
