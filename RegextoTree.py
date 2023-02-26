"""
    Este archivo se encargará de convertir mediante la clase Node, la expresión 
    regular brindada a un árbol.
"""

from Node import *
from graphviz import Digraph

class RegextoTree:
    def __init__(self, postfix):
        self.postfix = postfix
        self.stack = []
        self.root = None

    def convert(self):
        for i in self.postfix:
            if i == '.':
                node = Node()
                node.value = i
                node.right = self.stack.pop()
                node.left = self.stack.pop()
                self.stack.append(node)
            elif i == '|':
                node = Node()
                node.value = i
                node.right = self.stack.pop()
                node.left = self.stack.pop()
                self.stack.append(node)
            elif i == '*':
                node = Node()
                node.value = i
                node.left = self.stack.pop()
                node.right = None
                self.stack.append(node)
            else:
                node = Node()
                node.value = i
                node.left = None
                node.right = None
                self.stack.append(node)
        self.root = self.stack.pop()
        return self.root
    
    def generate_dot(self):
        dot = Digraph(comment='RegEx to Tree')
        id = 0
        self._generate_dot(dot, self.root, id)
        return dot
    
    def _generate_dot(self, dot, node, id):
        if node:
            dot.node(str(id), str(node.value))
            if node.left:
                dot.edge(str(id), str(id*2+1))
                self._generate_dot(dot, node.left, id*2+1)
            if node.right:
                dot.edge(str(id), str(id*2+2))
                self._generate_dot(dot, node.right, id*2+2)
                
    def save_dot_png(self, filename):
        dot = self.generate_dot()
        dot.format = 'png'
        dot.render(filename, view=True)