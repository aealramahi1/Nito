class Player:
{
    '''
    Each user who plays with this bot will have a Player object associated with
    them that stores all of their information. The object will be created when
    the user invokes the q!establish_player command (handled outside this class)

    Attributes:
        theid (int): The snowflake ID of the user
        name (str): Most updated Discord name and discriminator of the user
        total_score (int): Summation of all round scores for the user
        round_score (int): The score the user got in their most recent round
        question_index (int): Current question index

    Methods:
        getID(): Returns the snowflake ID
        getWholeName(): Returns Discord name and discriminator
        getPartialName(): Returns only Discord name
        getTotalScore(): Returns total score
        getRoundScore(): Returns round score
        getQuestionIndex(): Returns question index

        changeName(newname): Updates the user's Discord name
        changeTotalScore(num): Adds num to total_score
        changeRoundScore(num): Adds num to round_score
        clearRoundScore(): Sets round_score to 0
        increaseIndex(): Increments question_index by 1
        setIndex(newindex): Sets question_index to newindex
    '''

    
    def __init__(self, theid, name):
        '''
        Initializes a Player object for a user in the guild

        Parameters:
            
        '''
        
        self.theid = theid      # The snowflake ID will remain the same if the
                                # username is changed
        self.name = name        # There is a # in between name and discriminator
        self.total_score = 0
        self.round_score = 0
        self.question_index = 0 # The questions are stored in a list

    ## GETTERS

    def getID(self):
        '''Returns the user's snowflake ID (special identifier)'''
        return self.theid

    def getWholeName(self):
        '''
        Returns the user's Discord name and discriminator.
        
        If the user's name changed after using the q!establish_player command
        then the user must update their name
        '''
        return name

    def getPartialName(self):
        '''Returns the user's Discord name (without the discriminator)'''
        splitup = name.split("#")   # Creates a list with the Discord name as
                                    # the first element and the discriminator
                                    # as the second
        return splitup[0]

    def getTotalScore(self):
        '''Returns the user's total score'''
        return self.total_score

    def getRoundScore(self):
        '''Returns the user's round score'''
        return self.round_score

    def getQuestionIndex(self):
        '''Returns the index of the question that the user is currently on'''
        return self.question_index

    ## SETTERS

    def updateName(self, newname):
        '''Updates the user's Discord name and discriminator'''
        self.name = newname

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
        changeTotalScore(num)   # Changing the total score in this function
                                # makes it easier for the client code

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
