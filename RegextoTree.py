"""
    Este archivo se encargará de convertir mediante la clase Node, la expresión 
    regular brindada a un árbol sintáctico.
    
"""

"""
    José Rodrigo Barrera García
    Universidad del Valle de Guatemala
    Diseño de Lenguajes
    20807
    Laboratorio A 
"""



from Node import *
from graphviz import Digraph

class RegextoTree:
    def __init__(self, postfix=None):
        self.postfix = postfix
        self.stack = []
        self.root = None

    def convert(self):
        for i in self.postfix:
            if i == '.':
                node = Node()
                node.value = i
                node.right_child = self.stack.pop()
                node.left_child = self.stack.pop()
                self.stack.append(node)
            elif i == '|':
                node = Node()
                node.value = i
                node.right_child = self.stack.pop()
                node.left_child = self.stack.pop()
                self.stack.append(node)
            elif i == '*':
                node = Node()
                node.value = i
                node.left_child = self.stack.pop()
                node.right_child = None
                self.stack.append(node)
            else:
                node = Node()
                node.value = i
                node.left_child = None
                node.right_child = None
                self.stack.append(node)
        self.root = self.stack.pop()
        return self.root
    
    def set_root(self, node):
        self.root = node

    def postorder(self):
        return self.postorder_helper(self.root).replace('?', 'ε|')
        
    def postorder_helper(self, node):
        res = ""
        if node:
            if node.value in '?*+':
                res += self.postorder_helper(node.left_child)
            elif node.value in '|.':
                res += self.postorder_helper(node.left_child)
                res += self.postorder_helper(node.right_child)
            return res + node.value
    
    def generate_dot(self):
        dot = Digraph(comment='RegEx to Tree')
        id = 0
        self._generate_dot(dot, self.root, id)
        return dot
    
    def _generate_dot(self, dot, node, id):
        if node:
            dot.node(str(id), str(node.value))
            if node.left_child:
                dot.edge(str(id), str(id*2+1))
                self._generate_dot(dot, node.left_child, id*2+1)
            if node.right_child:
                dot.edge(str(id), str(id*2+2))
                self._generate_dot(dot, node.right_child, id*2+2)
    
    def save_dot_png(self, filename):
        dot = self.generate_dot()
        dot.format = 'png'
        dot.render(filename, view=True)
    