class FA(object):
    def __init__(self, regex = None) -> None:
        if regex:
            self.regex = regex
            self.alphabet = regex.alphabet
        self.count = 1
        self.transitions = {}
        self.initial_states = set()
        self.acceptance_states = set()
        self.external_transitions = None