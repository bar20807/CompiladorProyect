"""
    José Rodrigo Barrera García
    Universidad del Valle de Guatemala
    Diseño de Lenguajes
    20807
    Laboratorio A 
"""


class Node(object):
    def __init__(self, value=None):
        self.value = value
        self.right_child = None
        self.left_child = None
        self.nullable = False
        self.first_pos = set()
        self.last_pos = set()
        self.number = None
        
    def set_right_child(self, node):
        self.right_child = node
    
    def set_left_child(self, node):
        self.left_child = node