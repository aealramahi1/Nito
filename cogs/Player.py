# Each user who plays with this bot will have a player object associated with them that stores all of their information
# The object will be created when the user invokes the q!establish_player command (a function that will be handled outside of this class)

class Player:
{
    def __init__(self, name):
        '''Initializes a Player object for the user that calls this function, stores the name, and initializes the scores to 0'''
        # we want to make sure that the user's Discord name and discriminator are passed in here
        if name.contains("#"):
            self.name = name
        else:
            print("An error occurred! Could not initialize Player object. Please report this error :(")
            ####
            # perhaps at some point in the future there can be a place where issues for this bot are reported
            ####
}
