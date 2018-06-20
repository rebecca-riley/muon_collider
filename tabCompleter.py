import os
import sys 
import readline
import glob

class tabCompleter(object):
    """ 
    A tab completer that can either complete from
    the filesystem or from a list.
    
    Partially taken from:
    http://stackoverflow.com/questions/5637124/tab-completion-in-pythons-raw-input

    --Modified by Rebecca Riley, 06/20/2018
    """

    def __init__(self):
        readline.set_completer_delims('\t')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.pathCompleter)


    def pathCompleter(self,text,state):
        """ 
        This is the tab completer for systems paths.
        Only tested on *nix systems
        """
        line   = readline.get_line_buffer().split()

        return [x for x in glob.glob(text+'*')][state]
