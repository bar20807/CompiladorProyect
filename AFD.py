from RegextoTree import *
import graphviz
from collections import deque
from FA import FA

"""

    Replanteamos el enfoque que le queremos de ahora en adelante.

"""


class AFD_construction(FA):
    def __init__(self, regex=None):
        self.regex = regex


    """
        
        Función que se encarga de hacer la construcción del AFD por medio de subconjuntos
    
    """
    def afd_(self, AFN):
        pass



    """
        Función que se encarga de crear el AFD directo a partir de su expresión regular
    """
    
    def afd_direct_(self, regex,name):
        # Se crea el arbol
        tree = RegextoTree(regex)
        # Se obtiene la raiz y la lista de nodos
        tree_root = tree.tree_root
        node_list = tree.node_list
        # Se crean los estados y transiciones del AFD
        states = ["S0"]
        transitions = []
        final_states = {}
        symbols = tree.get_Alphabet()

        # Se ejecutan las propiedades de los nodos
        tree.Node_properties(node_list)
        
        # Se crea dstates
        Dstates = [tree.compute_first_pos(tree_root)]
        state_counter = 0
        # Mientras no haya ninguno marcado se continua
        while(state_counter != len(Dstates)):
            # Se itera por cada simbolo
            for symbol in symbols:
                # Se crea el nuevo set
                new_state = set()
                # Por cada nodo de dstates
                for node in Dstates[state_counter]:
                    # Une cada followpos
                    if(node.value == symbol):
                        new_state = new_state.union(node.followpos)
                # Si el nuevo estado es vacio no se toma en cuenta
                if(len(new_state) != 0):
                    # Si el estado no esta en Dstates se ingresa
                    if(new_state not in Dstates):
                        Dstates.append(new_state)
                        states.append("S" + str(len(states)))
                    # Se busca el estado de transicion
                    new_state_counter = Dstates.index(new_state)
                    # Se realiza la transicion
                    transitions.append([states[state_counter], symbol, states[new_state_counter]])

            # Se hacen dos sets para lograr hacer operaciones de conjuntos entre ellos
            set_states = set(Dstates[state_counter])
            set_final_states = set(tree.compute_last_pos(tree_root))

            # Se verifica que los estados encontrados se encuentren en el conjunto de estados finales
            if(set_states.intersection(set_final_states).__len__() != 0):
                node_final = set_states.intersection(set_final_states)
                node_char = node_final.pop().value
                final_states[states[state_counter]] = node_char

            # Se agrega un contador para marcar los estados
            state_counter += 1
            
        # Se crea el AFD
        afd = AFD_construction()
        afd.regex = regex
        afd.states = states
        afd.alphabet = symbols
        afd.transitions = transitions
        afd.initial_state = states[0]
        afd.final_state = final_states
        afd.output_image(name)
        return afd


    
    
    def simulate_afd(self, string):
        pass



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
       pass


    
    # Funcion para graficar el automata
    def output_image(self, name):
        #Si name es null, poner por defecto AFD
        if name == None:
            self.afd_name = "AFD"
        else: 
            self.afd_name = name
        graph = Digraph()
        graph.attr(rankdir="LR", labelloc="t")
        # Por cada estado se crea la imagen para graficarlo
        for state in self.states:
            if(state in self.initial_state):
                graph.node(str(state), str(state), shape="circle", style="filled", color="red")
            if(state in self.final_state):
                graph.node(str(state), str(state), shape="doublecircle", style="filled", color="green")
            else:
                graph.node(str(state), str(state), shape="circle")
        # Se crean las transiciones de los estados
        for transition in self.transitions:
            graph.edge(str(transition[0]), str(transition[2]), label=str(transition[1]))

        # Se renderiza
        graph.render(f"./AFDs_LabD/AFDDefault", format="png", view=True)