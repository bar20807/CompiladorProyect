from RegextoTree import *
import graphviz
from collections import deque
from FA import FA
from TreeReading import TreeReading

class AFD_construction(FA):
    def __init__(self, regex=None):
        super().__init__(regex)
        self.dead_state = None
        self.temp_transitions = None
        if regex: 
            self.afd_direct_()

    """
        
        Función que se encarga de hacer la construcción del AFD por medio de subconjuntos
    
    """
    def afd_(self, AFN):
        # Copia algunos atributos del NFA original
        self.regex = AFN.regex
        self.alphabet = AFN.alphabet
        self.external_transitions = AFN.transitions
        # Crea el alfabeto especial y establece el contador de estados
        self.create_special_alphabet()
        count_states = 1
        # Crea un diccionario para los estados del DFA y establece el primer estado
        D_states = {}
        first_state = frozenset(self.e_closure(AFN.initial_states))
        D_states[first_state] = count_states
        # Crea la entrada para el primer estado en la tabla de transiciones del DFA
        entry = [set() for element in self.special_alphabet]
        self.transitions[D_states[first_state]] = entry
        # Agrega el primer estado a la lista de estados no marcados y actualiza el contador de estados
        unmarked_states = [first_state]
        count_states += 1
        # Establece el estado inicial del DFA
        self.initial_states = {D_states[first_state]}
        # Mientras hayan estados no marcados por analizar
        while unmarked_states:
            # Toma un estado no marcado
            T = unmarked_states.pop()
            # Verifica si es un estado de aceptación y lo agrega de ser necesario
            for element in T:
                if element in AFN.acceptance_states:
                    self.acceptance_states.add(D_states[T])
            # Para cada símbolo en el alfabeto especial
            for symbol in self.special_alphabet:
                # Calcula la clausura-épsilon del estado actual moviéndose con el símbolo actual
                U = frozenset(self.e_closure(self.move(T, symbol)))
                # Si el estado resultante aún no ha sido visitado
                if U not in D_states:
                    # Lo agrega a los estados no marcados y actualiza el contador de estados
                    D_states[U] = count_states
                    # Si el estado resultante es vacío, es un estado de muerte
                    if not U:
                        self.dead_state = count_states
                    # Agrega el estado resultante a la lista de estados no marcados
                    unmarked_states.append(U)
                    count_states += 1
                # Si el estado resultante aún no tiene una entrada en la tabla de transiciones del DFA
                if D_states[U] not in self.transitions:
                    # Crea la entrada correspondiente en la tabla de transiciones del DFA
                    entry = [set() for element in self.special_alphabet]
                    self.transitions[D_states[U]] = entry
                # Crea una transición entre el estado actual y el estado resultante con el símbolo actual
                self.transitions[D_states[T]][self.special_alphabet.index(symbol)].add(D_states[U])
                
        # Actualiza el alfabeto del DFA y guarda las transiciones originales en una variable temporal
        self.alphabet = self.special_alphabet
        self.temp_transitions = self.transitions
        
        # Elimina los estados de muerte y actualiza la tabla de transiciones del DFA
        self.delete_dead_state()
        self.external_transitions = self.transitions



    """
        Función que se encarga de crear el AFD directo a partir de su expresión regular
    """
    
    def afd_direct_(self):
        # Contador de estados
        count = 1
        # Se crea el árbol de lectura a partir de la expresión regular
        tree = TreeReading(self.regex)
        # Se obtiene la tabla de followpos del árbol de lectura
        table = tree.get_followpos_table()
        # Se establece el primer estado del DFA
        first_state = frozenset(tree.root.first_pos)
        # Se crea el alfabeto especial
        self.create_special_alphabet()
        # Diccionario de estados del DFA
        states = {first_state: count}
        # Lista de estados no marcados
        unmarked_states = [first_state]
        # Entrada para el primer estado en la tabla de transiciones del DFA
        entry = [set() for element in self.special_alphabet]
        self.transitions[count] = entry
        # Se aumenta el contador de estados
        count += 1
        # Se obtiene el último followpos
        pos_augmented = tree.get_last_pos()
        # Se agrega el primer estado como estado inicial del DFA
        self.initial_states.add(states[first_state])
        # Si el último followpos está en el primer estado, se agrega como estado de aceptación
        if pos_augmented in first_state:
            self.acceptance_states.add(states[first_state])

        # Se itera hasta que no hayan más estados no marcados
        while unmarked_states:
            # Se obtiene un estado no marcado
            S = unmarked_states.pop()
            # Se itera por cada símbolo del alfabeto especial
            for symbol in self.special_alphabet:
                # Se obtiene el conjunto U de followpos de S y el símbolo actual
                U = set()
                for state in S:
                    if (state, symbol) in table:
                        U = U.union(table[(state, symbol)])
                U = frozenset(U)
                # Si U no ha sido agregado a los estados del DFA
                if U not in states:
                    # Se agrega U como nuevo estado del DFA
                    states[U] = count
                    # Si U es un estado vacío, se establece como estado de muerte del DFA
                    if not U:
                        self.dead_state = count
                    # Se crea una nueva entrada en la tabla de transiciones del DFA para U
                    entry = [set() for element in self.special_alphabet]
                    self.transitions[count] = entry
                    # Se agrega U a la lista de estados no marcados
                    unmarked_states.append(U)
                    # Se aumenta el contador de estados
                    count += 1
                # Se crea una transición de S a U con el símbolo actual
                self.create_transition(states[S], states[U], symbol)
                # Si U contiene el último followpos, se agrega como estado de aceptación
                if pos_augmented in U:
                    self.acceptance_states.add(states[U])

        # Se establece el alfabeto del DFA como el alfabeto especial
        self.alphabet = self.special_alphabet
        # Se guarda la tabla de transiciones temporalmente
        self.temp_transitions = self.transitions
        # Se elimina el estado de muerte del DFA
        self.delete_dead_state()
        # Se establece la tabla de transiciones del DFA como la tabla externa
        self.external_transitions = self.transitions

        
    
    
    def create_special_alphabet(self):
        self.special_alphabet = [element for element in self.alphabet]
        self.special_alphabet.remove('ε')

    def get_symbol_index_special(self, symbol):
         for i in range(len(self.special_alphabet)):
            if self.special_alphabet[i] == symbol:
                return i

    def create_transition(self, initial_states, acceptance_states, symbol):
        symbol_index = self.get_symbol_index_special(symbol)
        self.transitions[initial_states][symbol_index].add(acceptance_states)

    """
    
    Función que se encarga de eliminar el estado muerto del autómata.
    
    """
    def delete_dead_state(self):
        # Copia el diccionario de transiciones para no modificar el original
        transitions = self.transitions.copy()
        for transition in self.transitions:
            # Si la transición actual es el estado muerto, se elimina del diccionario
            if transition == self.dead_state:
                transitions.pop(transition)
            else:
                new_element = []
                # Se itera sobre los elementos de la transición actual
                for element in self.transitions[transition]:
                    # Si el estado muerto está en el elemento actual, se reemplaza por un conjunto vacío
                    if self.dead_state in element:
                        new_element.append(set())
                    else:
                        new_element.append(element)
                # Se actualiza el valor de la transición actual en el diccionario
                transitions[transition] = new_element
        # Se actualiza el diccionario de transiciones del objeto actual con el diccionario actualizado
        self.transitions = transitions

    """
        Función que se encarga de devolver el index del símbolo del alfabeto
    
    """
    
    def get_symbol_index(self, symbol):
        # Si el símbolo se encuentra en el alfabeto del autómata
        if symbol in self.alphabet:
            # Devolvemos su índice en el alfabeto.
            return self.alphabet.index(symbol) 
        else:
            # Si no se encuentra, se devuelve None.
            return None
        
    """
        Función que se encarga de realizar el e-closure
    
    """
    
    def e_closure(self, states):
        # Creamos una copia de los estados para no modificar el original
        # Si no hay transiciones externas, usamos las transiciones internas
        transitions = self.external_transitions.copy() if self.external_transitions else self.transitions.copy()
        # Creamos una pila y agregamos los estados iniciales a la pila
        stack = []
        for state in states:
            stack.append(state)
        # Inicializamos el conjunto de estados resultante con los estados iniciales
        result = states.copy()
        # Realizamos un bucle mientras la pila no esté vacía
        while stack:
            # Sacamos un estado de la pila
            t = stack.pop()
            # Obtenemos las transiciones del estado actual
            transition = transitions[t]
            # Obtenemos el índice del símbolo "ε" en el alfabeto
            index = self.get_symbol_index('ε')
            # Obtenemos los estados alcanzados por la transición "ε"
            states_reached = transition[index]
            # Iteramos sobre los estados alcanzados por la transición "ε"
            for element in states_reached:
                # Si el estado no está en el conjunto de estados resultante, lo agregamos y lo ponemos en la pila
                if element not in result:
                    result.add(element)
                    stack.append(element)
        # Devolvemos el conjunto de estados resultante
        return result

    
    """
        Función que se encarga de realizar el move
    
    """
    
    def move(self, states, symbol):
        """
        Esta función calcula el conjunto de estados alcanzables desde un conjunto de estados dados con un símbolo de entrada.

        Parámetros:
        - states: conjunto de estados a partir del cual se realizará la transición.
        - symbol: símbolo de entrada para realizar la transición.
        """
        # Inicializamos el conjunto de estados resultantes vacío.
        result = set()
        #Obtenemos las transiciones externas o internas del autómata, según corresponda.
        transitions = self.external_transitions.copy() if self.external_transitions else self.transitions.copy()
        #Recorremos los estados del conjunto de estados de entrada.
        for state in states:
            #Obtenemos el índice del símbolo en la tabla de transiciones.  
            index = self.get_symbol_index(symbol)
            #Obtenemos la transición correspondiente al estado actual. 
            transition = transitions[state]
            #Obtenemos el conjunto de estados alcanzables con el símbolo actual.
            states_reached = transition[index]
            #Recorremos los estados alcanzables.
            for element in states_reached:
                #Agregamos cada estado alcanzable al conjunto de estados resultantes.
                result.add(element)
        #Devolvemos el conjunto de estados alcanzables.
        return result

    
    def output_image(self, path=None):
        # Si no se especifica una ruta, se establece una por defecto.
        if not path:
            path = "AFD"
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
        visual_graph.render(directory='Pre-laboratorio B',view=True)