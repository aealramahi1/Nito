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

    def getName():
        '''Returns the user's Discord name including the discriminator'''
        return name

    def getTotalScore():
        '''Returns the user's total score'''
        return self.total_score

    def getRoundScore():
        '''Returns the user's round score'''
        return self.round_score

    def getQuestionIndex():
        '''Returns the index of the question that the user is currently on'''
        return self.question_index
}
