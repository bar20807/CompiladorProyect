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
import RegexErrorChecker as re
from graphviz import Digraph

class RegextoTree(object):
    # Se inicia con la expresion regular
    def __init__(self, regex):
        self.regex = regex
        # Se agrega la raiz al final de la expresion
        self.postfix =  re.RegexErrorChecker(self.regex).to_postfix()
        self.postfix.append("#")
        self.postfix.append(".")
        self.node_list = []
        self.tree_root = None
        self.buildTree()

    def buildTree(self):
        node_stack = []  # pila de nodos
        pos_counter = 1  # contador de posiciones
        for char in self.postfix:
            if char == '+':  # suma unaria
                node = Node(char)
                node.left_child = node_stack.pop()
                node_stack.append(node)
                self.node_list.append(node)
            elif char == '*':  # cierre de Kleene
                node = Node(char)
                node.left_child = node_stack.pop()
                node_stack.append(node)
                self.node_list.append(node)
            elif char == '?':  # opcionalidad
                node = Node(char)
                node.left_child = node_stack.pop()
                node_stack.append(node)
                self.node_list.append(node)
            elif char == '.':  # concatenación
                node = Node(char)
                node.right_child = node_stack.pop()
                node.left_child = node_stack.pop()
                node_stack.append(node)
                self.node_list.append(node)
            elif char == '|':  # alternancia
                node = Node(char)
                node.right_child = node_stack.pop()
                node.left_child = node_stack.pop()
                node_stack.append(node)
                self.node_list.append(node)
            else:  # símbolo
                node = Node(char, pos_counter)
                pos_counter += 1
                node_stack.append(node)
                self.node_list.append(node)
        self.tree_root = node_stack.pop()  # el último nodo es la raíz

    # Función para calcular si un nodo es nulo o no
    def compute_nullable(self, node):
        # Se retornan nulos los simbolos que lo son
        if(node.isOperator and node.character in "ε?*"):
            return True
        # Para el or se retorna los nulos de los dos hijos con or
        elif(node.isOperator and node.character == "|"):
            return (self.compute_nullable(node.left_child) or self.compute_nullable(node.right_child))
        # Para concatenacion se retorna el nulo de los dos hijos con and
        elif(node.character == "." and node.isOperator):
            return (self.compute_nullable(node.left_child) and self.compute_nullable(node.right_child))
        # Para la cerradura positiva se regresa el nulo del hijo
        elif(node.character == "+" and node.isOperator):
            return self.compute_nullable(node.left_child)
        # Si es un caracter no es nulo
        else:
            return False

    def compute_first_pos(self, node):
        # Si es epsilon se regresa un vacio
        if(node.isOperator and node.character == "ε"):
            return set()
        # Si es un or se regresa la union de los dos hijos
        elif(node.isOperator and node.character == "|"):
            return (self.compute_first_pos(node.right_child).union(self.compute_first_pos(node.left_child)))
        # Si es concatenacion se regresa la union si el izquierdo es nulo, del contrario es el izquierdo
        elif(node.isOperator and node.character == "."):
            if(self.compute_nullable(node.left_child)):
                return (self.compute_first_pos(node.right_child).union(self.compute_first_pos(node.left_child)))
            else:
                return self.compute_first_pos(node.left_child)
        # Para las cerraduras se regresa el firstpos de su hijo
        elif(node.isOperator and node.character in "*+?"):
            return self.compute_first_pos(node.left_child)
        # Si es un caracter se regresa solo la posicion
        else:
            return {node}


    def compute_last_pos(self, node):
        # Para epsilon se regresa un vacio
        if(node.isOperator and node.character == "ε"):
            return set()
        # Si es un or se regresa la union de los dos hijos
        elif(node.isOperator and node.character == "|"):
            return (self.compute_last_pos(node.right_child).union(self.compute_last_pos(node.left_child)))
        # Si es concatenacion se regresa la union si el derecho es nulo, del contrario es el derecho
        elif(node.isOperator and node.character == "."):
            if(self.compute_nullable(node.right_child)):
                return (self.compute_last_pos(node.right_child).union(self.compute_last_pos(node.left_child)))
            else:
                return self.compute_last_pos(node.right_child)
        # Para las cerraduras se regresa el firstpos de su hijo
        elif(node.isOperator and node.character in "*+?"):
            return self.compute_last_pos(node.left_child)
        # Si es un caracter se regresa solo la posicion
        else:
            return {node}

    def compute_follow_pos(self, node):
        # Si es un nodo final, no se hace nada
        if not node.left_child and not node.right_child:
            return
        # Si es un nodo de concatenación
        elif node.character == '.':
            # Se toman los nodos de lastpos del nodo izquierdo
            for i in self.compute_last_pos(node.left_child):
                # A cada nodo de lastpos se le añade el followpos del nodo derecho
                i.followpos |= self.compute_first_pos(node.right_child)
        # Si es un nodo de cerradura (tanto * como +)
        elif node.character in '*+':
            # Se toman los nodos de lastpos del nodo izquierdo
            for i in self.compute_last_pos(node.left_child):
                # A cada nodo de lastpos se le añade el followpos del nodo izquierdo
                i.followpos |= self.compute_first_pos(node.left_child)
            # Se aplica lo mismo a los nodos del nodo derecho
            self.compute_follow_pos(node.left_child)
        # Si es un nodo alternativo, se aplica lo mismo a ambos nodos
        elif node.character == '|':
            self.compute_follow_pos(node.left_child)
            self.compute_follow_pos(node.right_child)
            
    def Node_properties(self, nodes):
        # Crea un conjunto de nodos procesados
        processed_nodes = set()
        # Procesa los nodos
        while nodes:
            # Obtén el siguiente nodo
            node = nodes.pop()
            # Si el nodo ya ha sido procesado, continua con el siguiente
            if node in processed_nodes:
                continue
            # Marca el nodo como procesado
            processed_nodes.add(node)
            # Calcula las propiedades del nodo
            node.nullable = self.compute_nullable(node)
            node.firstpos = self.compute_first_pos(node)
            node.lastpos = self.compute_last_pos(node)
            self.compute_follow_pos(node)
            # Agrega los hijos del nodo a la lista de nodos por procesar
            if node.left_child:
                nodes.append(node.left_child)
            if node.right_child:
                nodes.append(node.right_child)
                

    """
        Esta función recibe un objeto de la clase regex y devuelve el alfabeto de la expresión regular
    
    """
    def get_Alphabet(self): 
        symbols = []
        for i in self.regex:
            if(isinstance(i, int) and i not in symbols):
                symbols.append(i)
        return symbols
    
    
    # Función para graficar cada nodo del árbol
    def generate_dot(self, node, graph):
        # Se crea un nodo en el grafo con un ID único y el valor del nodo del árbol de expresión regular
        graph.node(str(id(node)), str(node.character))
        # Si el nodo actual tiene un hijo izquierdo, se genera un nodo y se conecta con una arista
        if(node.left_child):
            graph.edge(str(id(node)), str(id(node.left_child)))
            # Se llama de forma recursiva a la función con el hijo izquierdo como argumento para continuar generando el grafo
            self.generate_dot(node.left_child, graph)
        # Si el nodo actual tiene un hijo derecho, se genera un nodo y se conecta con una arista
        if(node.right_child):
            graph.edge(str(id(node)), str(id(node.right_child)))
            # Se llama de forma recursiva a la función con el hijo derecho como argumento para continuar generando el grafo
            self.generate_dot(node.right_child, graph)

    # Función para generar el grafo completo del árbol de expresión regular y guardarlo en un archivo PNG
    def print_tree(self, nameTree=None):
        #Si el nombre está vacío, poner por defecto el nombre de tree_test
        if(nameTree is None):
            nameTree = "tree_test"
        # Se crea un nuevo grafo
        graph = Digraph()
        # Se agrega un título al grafo
        graph.attr(labelloc="t")
        # Se llama a la función que genera el grafo a partir del nodo raíz del árbol
        self.generate_dot(self.tree_root, graph)
        # Se guarda el grafo como un archivo PNG en la carpeta de imágenes, con el nombre del árbol
        graph.render(f"./LaboratorioC/{nameTree}", format="png", view=True)

