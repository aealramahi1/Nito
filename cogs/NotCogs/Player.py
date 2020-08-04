# Each user who plays with this bot will have a player object associated with them that stores all of their information
# The object will be created when the user invokes the q!establish_player command (a function that will be handled outside of this class)

class Player:
{
    def __init__(self, name):
        '''Initializes a Player object for the user that calls this function, stores the name, and initializes the scores to 0'''
        # I was originally going to check if the user's Discord name was actually passed in here, but that's not necessary since
        # the passing will be done by the programmer and not by the user AND because I'm going to be using the user's snowflake ID
        self.name = name # snowflake ID for the user (this way it doesn't matter if they change their username)
        self.total_score = 0
        self.round_score = 0
        self.question_index = 0 # current question index (questions stored in a list)

    ## GETTERS

    def getName(self):
        '''Returns the user's snowflake ID (special identifier)'''
        return name

    def getTotalScore(self):
        '''Returns the user's total score'''
        return self.total_score

    def getRoundScore(self):
        '''Returns the user's round score'''
        return self.round_score

    def getQuestionIndex(self):
        '''Returns the index of the question that the user is currently on'''
        return self.question_index

    ## SETTERS/CLEARERS

    def setTotalScore(self, num):
        '''Changes the total score of the user'''
        # we can add or subtract from this score by passing in either a positive or a negative integer
        self.total_score += num

    def setRoundScore(self, num):
        '''Changes the round score of the user'''
        # same as with changing the total score, we can add in negative numbers if the score of the user dropped
###### we are potentially going to want to implement this feature at the end of the round so that we don't have to keep a running total ######
        self.round_score += num
        changeTotalScore(num) # changing the total score in this function makes it easier for the client code

    def clearRoundScore(self):
        '''Sets the round score to 0'''
        self.round_score = 0

    def increaseIndex(self):
        '''Increases the index of the question that the user is on by 1'''
        self.question_index += 1

    def setIndex(self, newindex):
        '''Sets the index that the question is on to the new index'''
        self.question_index = newindex    
}
