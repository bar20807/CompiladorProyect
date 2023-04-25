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
        iterator = 1
        for char in self.postfix:
            if (isinstance(char, str) and char is '+'):  # suma unaria
                node = Node(char,True)
                node.left_child = node_stack.pop()
                node_stack.append(node)
                self.node_list.append(node)
            elif (isinstance(char, str) and char is '*'):  # cierre de Kleene
                node = Node(char,True)
                node.left_child = node_stack.pop()
                node_stack.append(node)
                self.node_list.append(node)
            elif (isinstance(char, str) and char is '?'):  # opcionalidad
                node = Node(char,True)
                node.left_child = node_stack.pop()
                node_stack.append(node)
                self.node_list.append(node)
            elif (isinstance(char, str) and char is '.'):  # concatenación
                node = Node(char,True)
                node.right_child = node_stack.pop()
                node.left_child = node_stack.pop()
                node_stack.append(node)
                self.node_list.append(node)
            elif (isinstance(char, str) and char is '|'):  # alternancia
                node = Node(char,True)
                node.right_child = node_stack.pop()
                node.left_child = node_stack.pop()
                node_stack.append(node)
                self.node_list.append(node)
            else:  # símbolo
                node = Node(char, False, iterator)
                node_stack.append(node)
                self.node_list.append(node)
        self.tree_root = node_stack.pop()  # el último nodo es la raíz

    # Define una función llamada compute_nullable que recibe como argumento un nodo
    def compute_nullable(self, node):
        # Si el nodo es un operador, se entra en este bloque
        if node.operator:
            # Si el valor del nodo es uno de los símbolos especiales (ε, ?, o *), entonces el nodo es nulo y se retorna True
            if node.value in "ε?*":
                return True
            # Si el valor del nodo es el operador OR ('|'), se evalúa si al menos uno de los dos hijos es nulo
            elif node.value == "|":
                # Se aplica la función compute_nullable a cada uno de los dos hijos y se verifica si alguno es nulo usando la función any
                return any(self.compute_nullable(child) for child in [node.left_child, node.right_child])
            # Si el valor del nodo es el operador AND ('.'), se evalúa si ambos hijos son nulos
            elif node.value == ".":
                # Se aplica la función compute_nullable a cada uno de los dos hijos y se verifica si ambos son nulos usando la función all
                return all(self.compute_nullable(child) for child in [node.left_child, node.right_child])
            # Si el valor del nodo es el operador de cerradura positiva ('+'), se evalúa si el hijo es nulo
            elif node.value == "+":
                # Se aplica la función compute_nullable al hijo y se retorna el resultado
                return self.compute_nullable(node.left_child)
        # Si el nodo no es un operador, entonces no es nulo y se retorna False
        else:
            return False


    def compute_first_pos(self, node):
        first_pos = set()
        # Si el nodo es un caracter, su first_pos es solo la posición del nodo
        if not node.operator:
            first_pos.add(node)
        # Si el nodo es una cerradura, su first_pos es el first_pos de su hijo
        elif node.value in "*+?":
            first_pos.update(self.compute_first_pos(node.left_child))
        # Si el nodo es un OR, su first_pos es la unión de los first_pos de sus hijos
        elif node.value == "|":
            first_pos.update(self.compute_first_pos(node.left_child))
            first_pos.update(self.compute_first_pos(node.right_child))
        # Si el nodo es una concatenación, su first_pos es el first_pos de su hijo izquierdo,
        # a menos que este sea nullable, en cuyo caso se agrega el first_pos de su hijo derecho
        elif node.value == ".":
            first_pos.update(self.compute_first_pos(node.left_child))
            if self.compute_nullable(node.left_child):
                first_pos.update(self.compute_first_pos(node.right_child))
        # Si el nodo es un epsilon, su first_pos es vacío
        elif node.value == "ε":
            pass
        return first_pos



    def compute_last_pos(self, node):
        last_pos = set()
        # Si el nodo es un caracter, su last_pos es solo la posición del nodo
        if not node.operator:
            last_pos.add(node)
        # Si el nodo es una cerradura, su last_pos es el last_pos de su hijo
        elif node.value in "*+?":
            last_pos.update(self.compute_last_pos(node.left_child))
        # Si el nodo es un OR, su last_pos es la unión de los last_pos de sus hijos
        elif node.value == "|":
            last_pos.update(self.compute_last_pos(node.left_child))
            last_pos.update(self.compute_last_pos(node.right_child))
        # Si el nodo es una concatenación, su last_pos es el last_pos de su hijo derecho,
        # a menos que este sea nullable, en cuyo caso se agrega el last_pos de su hijo izquierdo
        elif node.value == ".":
            last_pos.update(self.compute_last_pos(node.right_child))
            if self.compute_nullable(node.right_child):
                last_pos.update(self.compute_last_pos(node.left_child))
        # Si el nodo es un epsilon, su last_pos es vacío
        elif node.value == "ε":
            pass
        return last_pos


    def compute_follow_pos(self, node):
        # Si es un nodo final, no se hace nada
        if not node.left_child and not node.right_child:
            return
        # Si es un nodo de concatenación
        elif node.value == '.':
            # Se toman los nodos de lastpos del nodo izquierdo
            for i in self.compute_last_pos(node.left_child):
                # A cada nodo de lastpos se le añade el followpos del nodo derecho
                i.followpos |= self.compute_first_pos(node.right_child)
        # Si es un nodo de cerradura (tanto * como +)
        elif node.value in '*+':
            # Se toman los nodos de lastpos del nodo izquierdo
            for i in self.compute_last_pos(node.left_child):
                # A cada nodo de lastpos se le añade el followpos del nodo izquierdo
                i.followpos |= self.compute_first_pos(node.left_child)
            # Se aplica lo mismo a los nodos del nodo derecho
            self.compute_follow_pos(node.left_child)
        # Si es un nodo alternativo, se aplica lo mismo a ambos nodos
        elif node.value == '|':
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
    
    def get_Alphabet(self):
        return sorted(set(filter(lambda i: isinstance(i, int) or (i.isalpha() and i not in ".|*+?()"), self.regex)))

    # Función para graficar cada nodo del árbol
    def generate_dot(self, node, graph):
        # Se crea un nodo en el grafo con un ID único y el valor del nodo del árbol de expresión regular
        if(isinstance(node.value, int)):
            graph.node(str(id(node)), chr(node.value))
        else:
            graph.node(str(id(node)), str(node.value))
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

