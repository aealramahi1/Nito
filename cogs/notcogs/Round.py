class Round:
{
    '''
    There will be one round object per channel in each guild to represent the
    area in which the bot is played

    Attributes:

    Methods:
    '''
    def __init__(self, thisplayer):
        '''Initializes the values for this object'''
        self.round_owner = thisplayer       # The person who created the round
                                            # is the only one who can control it

        self.player_list = [round_owner]    # List to contain all the players
                                            # for this round, including the owner

        self.question_time = 5              # Time (sec) between each sentence

        self.buzz_time = 6                  # Time (sec) to guess after buzzing

    def add_player(self, newplayer):
        '''Adds another player to the list of current players'''
        if newplayer not in self.player_list and \
        newplayer is not self.round_owner:
            self.player_list.append(newplayer)
            message = newplayer. ## pick up here
        elif newplayer in self.player_list:
            
            
}
