"""
    Clase que se encargará de la construcción del autómata LR(0)
"""

from YalpReader import *
from FA import *
import copy
import graphviz
import networkx as nx
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


class ALR0 (FA):
    def __init__(self, regex=None, productions = None):
        #Inicializamos la clase padre
        super().__init__(regex)
        #Acá vamos a recibir nuestra lista de producciones
        self.productions = productions
        #Creamos una copia de la lista de producciones
        self.productions_copy = list()
        #Lista que nos ayudará con las iteraciones
        self.iterations = list()
        #Lista que nos ayudará con los conjuntos
        self.subsets_ = list()
        #Lista que nos ayudará con el número de conjuntos
        self.subsets_iterations = list()
        #Número de iteraciones
        self.number = 0
        #Ciclo de los conjuntos
        self.cycle = []
        
    def create_initial_production(self):
        # Obtener el valor de la primera producción
        value = self.productions[0][0]
        # Insertar una nueva producción al inicio de la lista de producciones
        self.productions.insert(0, [value + "'", [value]])
        # Copiar la lista de producciones
        self.productions_copy = copy.deepcopy(self.productions)
        # Agregar un punto al inicio de cada producción
        for i in range(len(self.productions)):
            self.productions[i][1].insert(0, ".")

    def create_subsets(self):
        # Crear la producción inicial, modificando la primera producción y agregándola al comienzo de la lista de producciones
        self.create_initial_production()
        # Calcular el cierre para la primera producción y actualizar el conjunto de subconjuntos y transiciones
        self.closure([self.productions[0]])
        # Mientras haya elementos en el ciclo, ejecutar la función goto para cada uno y actualizar el conjunto de subconjuntos y transiciones
        while self.cycle:
            self.goto(self.cycle.pop(0))
        # Establecer el estado inicial como el primer elemento de la primera producción
        initial_state = self.productions[0][0]
        # Iterar a través de todos los subconjuntos
        for subset in self.subsets_:
            # Iterar a través de todos los elementos en el subconjunto actual
            for item in subset:
                # Encontrar el índice del punto en la lista de elementos del subconjunto
                accept_index = item[1].index(".")
                # Verificar si el índice del punto menos 1 es mayor o igual a 0
                if accept_index - 1 >= 0:
                    # Verificar si el primer elemento del item es igual al estado inicial y si el elemento anterior al punto es igual al estado inicial sin el último carácter
                    if item[0] == initial_state and item[1][accept_index-1] == initial_state[:-1]:
                        # Encontrar el índice del subconjunto en la lista de subconjuntos
                        final_index = self.subsets_.index(subset)
                        # Agregar una nueva transición con el índice del subconjunto, el símbolo de fin de entrada y la acción de aceptar
                        self.transitions.append([self.subsets_iterations[final_index], "$", "accept"])

    def update_closure_array(self, closure):
        # Crea una lista vacía para almacenar los nuevos elementos que se encontrarán
        new_elements = []
        # Itera sobre cada item en la lista de entrada `closure`
        for x in closure:
            # Encuentra el índice del punto en la regla de producción
            dot_index = x[1].index(".")
            # Si el punto no está al final de la regla de producción
            if dot_index + 1 < len(x[1]):
                # Encuentra el siguiente símbolo en la regla de producción después del punto
                val = x[1][dot_index + 1]
                # Itera sobre todas las producciones para encontrar aquellas que empiecen con `val`
                for y in self.productions:
                    # Si encuentra una producción con `val` como símbolo no terminal y no está ya en `closure` ni en `new_elements`
                    if y[0] == val and y not in closure and y not in new_elements:
                        # Agrega la producción encontrada a la lista `new_elements`
                        new_elements.append(y)
        # Devuelve la lista `new_elements` con las producciones encontradas
        return new_elements

    def closure(self, input_item, input_elem=None, input_cycle=None):
        closure = list()
        # Copia el ítem y lo almacena en una lista para el cálculo de la clausura
        closure.extend(input_item)
        #Variable que se utilizará para las iteraciones
        iteration = 0
        while iteration != len(closure):
            iteration = len(closure)
            #Mandamos a llamar a la función para actualizar el closure
            closure.extend(self.update_closure_array(closure))
        # Ordena los elementos y los almacena en una lista de conjuntos si no existen en ella
        sort = sorted(closure, key=lambda x: x[0])
        if sort not in self.subsets_:
            self.subsets_.append(sort)
            self.subsets_iterations.append(self.number)
            self.number += 1
            self.cycle.append(sort)
        # Si los argumentos de entrada no son nulos, agrega una transición a la lista de transiciones
        if input_elem != None and input_cycle != None:
            start_index = self.subsets_.index(input_cycle)
            end_index = self.subsets_.index(sort)
            self.transitions.append([self.subsets_iterations[start_index],input_elem,self.subsets_iterations[end_index]])
        #print("Transiciones en la armada: ", self.transitions)

        
    def goto(self, iteraciones):
        # Crear una lista vacía para almacenar los elementos
        elements = list()
        # Iterar sobre las iteraciones
        for x in iteraciones:
            # Encontrar el índice del punto en la iteración
            indice = x[1].index(".")
            # Verificar si hay un carácter después del punto
            if indice + 1 < len(x[1]):
                # Verificar si el carácter después del punto no ha sido agregado a la lista de elementos
                if x[1][indice+1] not in elements: 
                    # Agregar el carácter después del punto a la lista de elementos
                    elements.append(x[1][indice+1])
        # Iterar sobre los elementos
        for x in elements:
            # Crear una lista vacía para almacenar las iteraciones que contienen el elemento
            temporal = list()
            # Iterar sobre las iteraciones
            for y in iteraciones:
                # Encontrar el índice del punto en la iteración
                indice = y[1].index(".")
                # Verificar si hay un carácter después del punto
                if indice + 1 < len(y[1]):
                    # Verificar si el carácter después del punto es igual al elemento actual
                    if y[1][indice+1] == x: 
                        # Agregar una copia profunda de la iteración a la lista temporal
                        temporal.append(copy.deepcopy(y))
            # Iterar sobre las iteraciones en la lista temporal
            for z in temporal:
                # Encontrar el índice del punto en la iteración
                indice = z[1].index(".")
                # Verificar si hay un carácter después del punto
                if indice + 1 < len(z[1]):
                    # Intercambiar el carácter después del punto con el punto
                    z[1][indice], z[1][indice+1] = z[1][indice+1], z[1][indice]
            # Calcular el cierre para la lista de iteraciones en la lista temporal
            self.closure(temporal, x, iteraciones)

        

    def output_image(self, filename):
        G = nx.DiGraph()
        dot = graphviz.Digraph(format='png')
        # Add nodes for each array
        for i, arr in enumerate(self.subsets_):
            label = f"I{i}\n"
            for item in arr:
                label += str(item) + "\n"
            G.add_node(i, label=label)

        # Add edges for each transition
        for t in self.transitions:
            from_node, label, to_node = t
            G.add_edge(from_node, to_node, label=label)
                
        # Add the missing "label" attribute for the nodes
        for node in G.nodes():
            if 'label' not in G.nodes[node]:
                G.nodes[node]['label'] = str(node)
                    
        # Add nodes with array labels
        for node, attrs in G.nodes(data=True):
            dot.node(str(node), label=str(attrs['label']).replace("'", "").replace('"', ''), fontsize="10", shape="rectangle")

        # Add edges with transition labels
        for source, target, attrs in G.edges(data=True):  # This line is modified
            dot.edge(str(source), str(target), label=attrs['label'], fontsize="10")

        # Render and save the graph as a PNG file
        dot.render(filename, view=False)