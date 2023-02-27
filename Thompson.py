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

    """
        Función que recorre el árbol generado a partir de una expresión regular y aplica diferentes operaciones según el tipo de nodo que se esté procesando. 
        En cada paso de la recursión, el método se mueve hacia abajo en el árbol, procesando los subárboles izquierdo y derecho del nodo actual.
    """
    def compile(self, node):
        # Si el nodo es nulo, no hay nada que compilar, así que se retorna None.
        if not node:
            return None
        # Se compilan los hijos izquierdo y derecho del nodo actual.
        left = self.compile(node.left_child)
        right = self.compile(node.right_child)
        # Dependiendo del valor del nodo actual, se selecciona la operación a realizar.
        if node.value == '*':
            # Se aplica el operador de cerradura de Kleene al hijo izquierdo.
            return self.kleen_(left)
        elif node.value == '+':
            # Se aplica el operador de cerradura de Kleene positiva al hijo izquierdo.
            return self.positive_kleen(left)
        elif node.value == '|':
            # Se aplica el operador OR al hijo izquierdo y derecho.
            return self.Or_(left, right)  
        elif node.value == '.':
            # Se aplica el operador de concatenación al hijo izquierdo y derecho.
            return self.Conca_(left, right)
        else:
            # Se crea un nodo con valor unitario.
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
        
        #Se hace la transición de un estado a otro mediante el símbolo al menos 1 vez
        #Se crea dicha transición
        """print("Valores de child[0]: " + str(child[0]))
        print("Valores de child[1]: " + str(child[1]))"""
        
        self.create_transition(first, child[0], 'ε')
        self.create_transition(child[1], last, 'ε')
        self.create_transition(child[1], child[0], 'ε')
        self.create_transition(first, last, 'ε')

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
    
    """
        Método que crea una transición entre dos estados con un símbolo.
    
    """
    
    def create_transition(self, initial_states, acceptance_states, symbol):
        symbol_index = self.get_symbol_index(symbol)
        self.transitions[initial_states][symbol_index].add(acceptance_states)

    def output_image(self, path=None):
        # Si no se especifica una ruta, se establece una por defecto.
        if not path:
            path = "AFN"
        # Se crea un objeto visual_graph de la clase Digraph de graphviz en formato PNG y con una orientación izquierda-derecha.
        visual_graph = graphviz.Digraph(format='png', graph_attr={'rankdir':'LR'}, name=path)
        # Se agrega un nodo falso al gráfico para conectar los nodos iniciales.
        visual_graph.node('fake', style='invisible')
        # Se crea una cola (queue) con los estados iniciales del autómata.
        queue = deque(self.initial_states)
        # Se crea un conjunto (visited) para almacenar los estados ya visitados.
        visited = set(self.initial_states)
        # Mientras la cola no esté vacía.
        while queue:
            # Se obtiene y elimina el primer elemento de la cola.
            state = queue.popleft()
            # Si el estado es uno de los estados finales del autómata, se agrega un nodo doblecírculo al gráfico.
            if state in self.acceptance_states:
                visual_graph.node(str(state), shape="doublecircle")
            # Si el estado es uno de los estados iniciales del autómata, se agrega una arista al nodo falso y se agrega una etiqueta "root".
            elif state in self.initial_states:
                visual_graph.edge("fake", str(state), style="bold")
                visual_graph.node(str(state), root="true")
            # Si el estado no es ni un estado final ni un estado inicial, se agrega un nodo normal al gráfico.
            else:
                visual_graph.node(str(state))
            # Se obtienen las transiciones del estado actual.
            transitions = self.transitions[state]
            # Para cada transición:
            for i, transition in enumerate(transitions):
                if not transition:
                    continue
                # Para cada elemento de la transición:
                for element in transition:
                    # Si el elemento no ha sido visitado, se agrega al gráfico y se marca como visitado.
                    if element not in visited:
                        visited.add(element)
                        if element in self.acceptance_states:
                            visual_graph.node(str(element), shape="doublecircle")
                        else:
                            visual_graph.node(str(element))
                        # Se agrega el elemento a la cola.
                        queue.append(element)
                    # Se agrega una arista del estado actual al elemento, etiquetada con el símbolo del alfabeto correspondiente.
                    visual_graph.edge(str(state), str(element), label=str(self.alphabet[i]))
        # Se guarda el gráfico en un directorio específico y se muestra en la pantalla.
        visual_graph.render(directory='Pre-laboratorio A',view=True)
