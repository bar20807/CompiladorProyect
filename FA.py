from RegextoTree import *
class FA(object):
    def __init__(self, regex = None) -> None:
        self.regex = regex
        self.states = []
        self.transitions = []
        self.initial_state = []
        self.final_state = {}
        self.alphabet = []