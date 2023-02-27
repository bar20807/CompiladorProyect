"""
    José Rodrigo Barrera García
    Universidad del Valle de Guatemala
    Diseño de Lenguajes
    20807
    Laboratorio A 
"""



import graphviz
from collections import deque

class AFN(object):
    def __init__(self, regex = None):
            self.regex = regex
            self.alphabet = regex.alphabet
            self.count = 1
            self.transitions = {}
            self.initial_states = set()
            self.acceptance_states = set()
            self.current_nodes = set()
        
class Thompson(AFN):

    def __init__(self, regex=None):
        # Llama al constructor de la clase base (Automata) y pasa como parámetro la expresión regular.
        super().__init__(regex)
        # Obtiene la raíz del árbol sintáctico de la expresión regular.
        self.root = self.regex.get_root()
        #Crea los estados del autómata.
        self.create_states()
        # Crea los estados y transiciones del autómata basado en el árbol sintáctico de la expresión regular.
        first, last = self.compile(self.root)
        # Agrega el primer estado del autómata al conjunto de estados iniciales.
        self.initial_states.add(first)
        # Agrega el último estado del autómata al conjunto de estados de aceptación.
        self.acceptance_states.add(last)

    def create_states(self):
        self.transitions[0] = [set() for _ in self.alphabet]
        self.transitions[1] = [set() for _ in self.alphabet]
        # Crea una transición epsilon entre el estado inicial y el estado de aceptación del autómata.
        self.create_transition(0, 1, 'ε') 

    def get_symbol_index(self, symbol):
        # Si el símbolo se encuentra en el alfabeto del autómata
        if symbol in self.alphabet:
            # Devolvemos su índice en el alfabeto.
            return self.alphabet.index(symbol) 
        else:
            # Si no se encuentra, se devuelve None.
            return None


    def compile(self, node):
        if not node:
            return None

        left = self.compile(node.left_child)
        right = self.compile(node.right_child)

        if node.value == '*':
            return self.kleen_(left)
        elif node.value == '+':
            return self.positive_kleen(left)
        elif node.value == '|':
            return self.Or_(left, right)
        elif node.value == '.':
            return self.Conca_(left, right)
        else:
            return self.create_unit(node)
    
    def positive_kleen(self, child):
        first = self.count
        self.count += 1
        last = self.count
        self.count += 1
        
        # Crear entrada de matriz
        """
            La matriz de transiciones es un diccionario que tiene como claves los estados del autómata y como valores, 
            una lista de conjuntos, donde cada conjunto representa las transiciones que se pueden realizar desde ese 
            estado por cada símbolo del alfabeto.
        """
        entry = [set() for element in self.alphabet]
        self.transitions[first] = entry
        entry = [set() for element in self.alphabet]
        self.transitions[last] = entry

        self.create_transition(first, child[0], 'ε')
        self.create_transition(child[1], last, 'ε')
        self.create_transition(child[1], child[0], 'ε')
        self.create_transition(last, first, 'ε')

        return first, last


    def kleen_(self, child):
        first = self.count
        self.count += 1
        last = self.count
        self.count += 1

        # Crear entrada de matriz
        """
            La matriz de transiciones es un diccionario que tiene como claves los estados del autómata y como valores, 
            una lista de conjuntos, donde cada conjunto representa las transiciones que se pueden realizar desde ese 
            estado por cada símbolo del alfabeto.
        """
        entry = [set() for element in self.alphabet]
        self.transitions[first] = entry
        entry = [set() for element in self.alphabet]
        self.transitions[last] = entry

        self.create_transition(first, last, 'ε')
        self.create_transition(first, child[0], 'ε')
        self.create_transition(child[1], last, 'ε')
        self.create_transition(child[1], child[0], 'ε')

        return first, last
    
    def Or_(self, left, right):
        first = self.count
        self.count += 1
        last = self.count
        self.count += 1

        # Crear entrada de matriz
        """
            La matriz de transiciones es un diccionario que tiene como claves los estados del autómata y como valores, 
            una lista de conjuntos, donde cada conjunto representa las transiciones que se pueden realizar desde ese 
            estado por cada símbolo del alfabeto.
        """
        entry = [set() for element in self.alphabet]
        self.transitions[first] = entry
        entry = [set() for element in self.alphabet]
        self.transitions[last] = entry

        self.create_transition(first, left[0], 'ε')
        self.create_transition(first, right[0], 'ε')
        self.create_transition(left[1], last, 'ε')
        self.create_transition(right[1], last, 'ε')

        return first, last

    def Conca_(self, left, right):
        # Obtenemos cada una de las transiciones del nuevo estado
        new_state_transitions = self.transitions[left[1]]
        # Recorremos las transiciones del antiguo estado para posteriormente unirlos con el de nuevo estado
        for i in range(len(self.transitions[right[0]])):
            # Realizamos la union de las transiciones del nuevo estado conn respecto al antiguo
            new_state_transitions[i] = new_state_transitions[i].union(self.transitions[right[0]][i])
        # Eliminamos el estado del diccionario de transiciones
        self.transitions.pop(right[0])
        return left[0], right[1]
    
    def replace_transitions(self, old_state, new_state):
        new_state_transitions = self.transitions[new_state]
        
        for i in range(len(self.transitions[old_state])):
            new_state_transitions[i] = new_state_transitions[i].union(self.transitions[old_state][i])
        
        self.transitions.pop(old_state)

    def create_unit(self, node):
        symbol = node.value
        first = self.count
        self.count += 1
        last = self.count
        self.count += 1

        # Crear entrada de matriz
        """
            La matriz de transiciones es un diccionario que tiene como claves los estados del autómata y como valores, 
            una lista de conjuntos, donde cada conjunto representa las transiciones que se pueden realizar desde ese 
            estado por cada símbolo del alfabeto.
        """
        entry = [set() for element in self.alphabet]
        self.transitions[first] = entry
        entry = [set() for element in self.alphabet]
        self.transitions[last] = entry
        #Se manda a llamar que creará la transición desde la primera a la última posición y con qué simbolo se realizó
        self.create_transition(first, last, symbol)
        return first, last
    
    def create_transition(self, initial_states, acceptance_states, symbol):
        symbol_index = self.get_symbol_index(symbol)
        self.transitions[initial_states][symbol_index].add(acceptance_states)

    def output_image(self, path=None):
        if not path:
            path = "AFN"
        visual_graph = graphviz.Digraph(format='png', graph_attr={'rankdir':'LR'}, name=path)
        visual_graph.node('fake', style='invisible')
        queue = deque(self.initial_states)
        visited = set(self.initial_states)
        while queue:
            state = queue.popleft()
            if state in self.acceptance_states:
                visual_graph.node(str(state), shape="doublecircle")
            elif state in self.initial_states:
                visual_graph.edge("fake", str(state), style="bold")
                visual_graph.node(str(state), root="true")
            else:
                visual_graph.node(str(state))
            transitions = self.transitions[state]
            for i, transition in enumerate(transitions):
                if not transition:
                    continue
                for element in transition:
                    if element not in visited:
                        visited.add(element)
                        queue.append(element)
                        if element in self.acceptance_states:
                            visual_graph.node(str(element), shape="doublecircle")
                        else:
                            visual_graph.node(str(element))
                    visual_graph.edge(str(state), str(element), label=str(self.alphabet[i]))
        visual_graph.render(directory='Pre-laboratorio A',view=True)