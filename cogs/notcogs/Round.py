# This class will create the round object and store its attributes

class Round:
{
    def __init__(self, thisplayer):
        '''Initializes the values for this object'''
        self.roundowner = thisplayer # The person who created the round is the only one who can control it
        self.question_time = 5
        self.buzztime = 6

    def add_player(self, newplayer):
}
