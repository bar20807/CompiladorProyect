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
    
    def afd_direct_(self, regex, name):
        #Mañana veremos y afinaremos detalles.
        pass


    
    
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