# This class will create the round object and store its attributes

class Round:
{
    def __init__(self, thisplayer):
        '''Initializes the values for this object'''
        self.round_owner = thisplayer # The person who created the round is the only one who can control it
        self.player_list = [round_owner] # List to contain all the players for this round, including the owner
        # The round owner is always the first player in the list
        self.question_time = 5
        self.buzz_time = 6

    def add_player(self, newplayer):
        '''Adds another player to the list of current players'''
        if newplayer not in self.player_list and \
        newplayer is not self.round_owner:
            
}
