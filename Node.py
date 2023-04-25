"""
    José Rodrigo Barrera García
    Universidad del Valle de Guatemala
    Diseño de Lenguajes
    20807
    Laboratorio A 
"""


class Node (object):
    def __init__(self, value, operator,  position = None):
        self.value = value
        self.firstpos = set()
        self.lastpos = set()
        self.followpos = set()
        self.position = position
        self.operator = operator
        self.left_child = None
        self.right_child = None
            