"""
    José Rodrigo Barrera García
    Universidad del Valle de Guatemala
    Diseño de Lenguajes
    20807
    Laboratorio A 
"""


class Node (object):
    def __init__(self, character=None, isOperator = None, position=None):
        self.character = chr(character) if isinstance(character, int) else character
        self.right_child = None
        self.left_child = None
        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()
        self.followpos = set()
        self.position = position
        self.isOperator = isOperator
