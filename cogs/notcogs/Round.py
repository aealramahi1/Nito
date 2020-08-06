class Round:
{
    '''
    There will be one round object per channel in each guild to represent the
    area in which the bot is played

    Attributes:
        round_owner (Player object): Person who creates and controls the round
        player_list (list): Contains all players for the round
        question_time (float): Seconds in between each sentence
        buzz_time (float): Seconds the user has to guess after buzzing

    Methods:
        add_player(newplayer): Adds another player to player_list
    '''
    def __init__(self, thisplayer):
        '''
        Initializes the values for this object

        Parameters:
            thisplayer (Player object): Person who created the round
        '''
        # The person who created the round is the only one who can control it
        self.round_owner = thisplayer
        # List to contain all the players for this round, including the owner
        self.player_list = [round_owner]
        # Time (seconds) in between each sentence of the question
        self.question_time = 5.0
        # Time (seconds) the player has to guess after buzzing
        self.buzz_time = 6.0

    def add_player(self, newplayer):
        '''
        Adds another player to the list of current players

        Parameters:
            newplayer (Player object): Person who joined the round

        Returns:
            message (str): The message detailing the results of the function
                           (i.e. whether it worked or not)
        '''
        # Make sure the player is not the owner or already in the list of
        # current players
        if newplayer not in self.player_list and \
        newplayer is not self.round_owner:
            self.player_list.append(newplayer)
            message = newplayer.getPartialName() + " joined successfully!"

        # If the player attempted to join a second time
        elif newplayer in self.player_list:
            message = newplayer.getPartialName() + " has already joined..."

        # If the player is actually the round owner
        elif newplayer is self.round_owner:
            message = newplayer.getPartialName() + " created this round..."

        # Hopefully there shouldn't be an error because we'll check in the
        # client code if the user is a valid player, but just in case it
        # doesn't hurt to include an else statement
        else:
            message = "An error occurred :("

        return message
}
