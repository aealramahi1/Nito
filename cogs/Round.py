class Round(object):
    """
    There will be one round object per channel in each guild to represent the
    area in which the bot is played

    Attributes:
        question_time (float): Seconds in between each sentence
        buzz_time (float): Seconds the user has to guess after buzzing
        round_owner (Player object): Person who creates and controls the round
        player_list (list): Contains all players for the round
        round_status (boolean): True if the round is playing, False if not

    Methods:
        startRound(thisplayer): Starts the round with thisplayer as round_owner
        endRound(): Ends the round and sets variables to null
        addPlayer(new_player): Adds another player to player_list
        removePlayer(oldplayer): Removes a player from player_list
        setQuestionTime(num): Sets question_time to num
        resetQuestionTime(): Resets question_time to default (5.0)
        setBuzzTime(num): Sets buzz_time to num
        resetBuzzTime(): Resets buzz_time to default (6.0)
        
        getInitializer(): Returns the statement needed to initialize the current round
    """

    def __init__(self, ro=None, qt=5.0, bt=6.0, pl=None, stat=False):
        """
        Initializes the values for this object

        Parameters:
            ro (Player object): The round owner (default None)
            qt (float): The question time (default 5.0)
            bt (float): The buzz time (default 6.0)
            pl (list): The list of players (default None)
            stat (boolean): The round status (default False)
        """
        self.question_time = qt
        self.buzz_time = bt
        self.round_owner = ro
        self.player_list = pl
        self.round_status = stat

    def startRound(self, thisplayer):
        """
        Starts the round with the player who called this command as the round owner.

        Parameters:
            thisplayer (Player object): Person who created the round
        """
        # The person who created the round is the only one who can control it
        self.round_owner = thisplayer

        # List to contain all the players for this round, including the owner
        self.player_list = [self.round_owner]

        # Indicates whether the round is currently active or not
        self.round_status = True

    def endRound(self):
        """
        Ends the round and sets all relevant variables to null
        """
        self.round_owner = None
        self.player_list = []
        self.round_status = False

    def addPlayer(self, new_player):
        """
        Adds another player to the list of current players

        Parameters:
            new_player (Player object): Person who joined the round

        Returns:
            message (str): The message detailing the results of the function (i.e. whether it worked or not)
        """
        message = 'An error has occurred.'

        # Make sure the player is not the owner or already in the list of current players
        if new_player not in self.player_list and new_player is not self.round_owner:
            self.player_list.append(new_player)
            message = new_player.getPartialName() + ' joined successfully!'

        # If the player attempted to join a second time
        elif new_player in self.player_list:
            message = new_player.getPartialName() + ' has already joined...'

        # If the player is actually the round owner
        elif new_player is self.round_owner:
            message = new_player.getPartialName() + ' created this round...'
        return message

    def removePlayer(self, oldplayer):
        """
        Removes a current player from the list of players

        Parameters:
            oldplayer (Player object): The player who wishes to leave

        Returns:
            message (str): The message detailing the results of the function (i.e. whether it worked or not)
        """
        message = 'An error has occurred.'

        # Make sure the player is already in the list of players, but not the owner
        if oldplayer in self.player_list and oldplayer is not self.round_owner:
            self.player_list.remove(oldplayer)
            message = oldplayer.getPartialName() + ' has quit.'

        # Check to see if the player is the round owner
        elif oldplayer is self.round_owner:
            self.endRound()
            message = 'The round owner has quit. Round ended.'

        # Check to see if the user wasn't even playing
        elif oldplayer not in self.player_list:
            message = 'You\'re not even playing, how can you quit???'
        return message

    def setQuestionTime(self, player, num):
        """
        Changes question_time

        Parameters:
            player (Player object): The user requesting to change question_time
            num (float/int): The time to set question_time to

        Returns:
            message (str): The message detailing the results of the function (i.e. whether it worked or not)
        """
        if player is self.round_owner:

            # Prevent negative time
            if num < 0:
                message = 'You cannot have negative time.'

            # Pretty reasonable numbers for now
            elif 0 <= num <= 60:
                self.question_time = float(num)
                message = 'Question time set to: ' + num + '.'

            # Prevent super big numbers
            elif num > 60:
                message = 'That number is way too big.'

            # Prevents anything other than numbers
            else:
                message = 'Please enter a number.'
        else:
            message = 'You cannot do that. You are not the round owner.'

        return message

    def resetQuestionTime(self):
        """
        Resets question_time to default

        Returns:
            message (str): Lets us know that this function works properly
        """
        self.question_time = 5.0
        message = 'Question time reset to 5.0 seconds'
        return message

    def setBuzzTime(self, num):
        """
        Changes buzz_time, preventing invalid values from being passed in

        Parameters:
            num (float/int): The time to set buzz_time to

        Returns:
            message (str): The message detailing the results of the function (i.e. whether it worked or not)
        """
        # Prevent negative time
        if float(num) < 0:
            message = 'You cannot have negative time'

        # Pretty reasonable numbers for now
        elif 0 <= float(num) <= 60:
            self.buzz_time = float(num)
            message = 'Question time set to: ' + num

        # Prevent super big numbers
        elif float(num) > 60:
            message = 'That number is way too big'

        # Hopefully this never runs, but you can't be too safe
        else:
            message = 'An error has occurred'

        return message

    def resetBuzzTime(self):
        """
        Resets buzz_time to default

        Returns:
            message (str): Lets us know that this function works properly
        """
        self.buzz_time = 6.0
        message = 'Buzz time reset to 6.0 seconds'
        return message

    def getInitializer(self):
        """
        Returns the initializer for the current Round object
        """
        init = 'RoundClass.Round(' + str(self.question_time) + ','
        init += str(self.buzz_time) + ',' + 'None,False)'
        return init
