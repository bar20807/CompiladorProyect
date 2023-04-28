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
        chr(character) if isinstance(character, int) else character
    """
    
    def afd_direct_(self, regex, name):
        # Se crea el árbol y se computan los followpos
        tree = RegextoTree(regex)
        tree.Node_properties(tree.node_list)
        # Se obtiene el alfabeto del árbol
        alphabet = tree.get_Alphabet()

        # Se crea el AFD
        afd = AFD_construction()
        afd.regex = regex
        afd.states = []
        afd.alphabet = alphabet
        afd.transitions = []
        afd.initial_state = "S0"
        afd.final_state = {}

        # Se crea el diccionario de estados
        Dstates = {"S0": tree.compute_first_pos(tree.tree_root)}

        # Se itera mientras haya nuevos estados por procesar
        unprocessed_states = ["S0"]
        while unprocessed_states:
            state = unprocessed_states.pop(0)
            # Se agrega el estado al conjunto de estados del AFD
            afd.states.append(state)
            # Se obtienen los followpos del estado actual para cada símbolo del alfabeto
            followpos = {symbol: set() for symbol in alphabet}
            for node in Dstates[state]:
                if node.value in alphabet:
                    followpos[node.value].update(node.followpos)
            # Se crea un nuevo estado para cada conjunto de followpos encontrado
            for symbol, followpos_set in followpos.items():
                if followpos_set:
                    if followpos_set not in Dstates.values():
                        Dstates[f"S{len(Dstates)}"] = followpos_set
                        unprocessed_states.append(f"S{len(Dstates)-1}")
                    # Se agrega la transición del estado actual al nuevo estado
                    afd.transitions.append([state, symbol, next(key for key, value in Dstates.items() if value == followpos_set)])
                    # Si el nuevo estado contiene un nodo final, se agrega al conjunto de estados finales del AFD
                    if any(node.value == "#" for node in followpos_set):
                        afd.final_state[state] = symbol

        # Se genera la imagen del AFD
        afd.output_image(name)

        return afd


    
    
    def simulate_afd(self, string):
        pass



    """
        Función que se encarga de realizar el e-closure
    
    """
    
    def e_closure(self, states):
        pass
    
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