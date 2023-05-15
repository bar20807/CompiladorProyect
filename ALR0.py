"""
    Clase que se encargará de la construcción del autómata LR(0)
"""

from YalpReader import *
from FA import *
import copy
import graphviz
import networkx as nx

class ALR0 (FA):
    def __init__(self, regex=None, productions = None):
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
        
    def create_initial_production(self):
        # Copiar la lista de producciones
        productions_copy = [x[:] for x in self.productions]
        # Obtener el valor de la primera producción
        value = self.productions[0][0]
        # Insertar una nueva producción al inicio de la lista de producciones
        self.productions.insert(0, [value + "'", [value]])
        # Agregar un punto al inicio de cada producción
        for i in range(len(self.productions)):
            self.productions[i][1].insert(0, ".")  
        return productions_copy

    def create_subsets(self):
        # Crear la producción inicial
        self.create_initial_production()
        # Crear el array de clausura con la producción inicial
        closure_array = [self.productions[0]]
        # Actualizar el array de clausura hasta que ya no se puedan agregar más elementos
        new_elements = self.update_closure_array(closure_array)
        while new_elements:
            closure_array.extend(new_elements)
            new_elements = self.update_closure_array(closure_array)
        # Ordenar los elementos del array de clausura por el estado inicial de cada producción
        sorted_items = sorted(closure_array, key=lambda x: x[0])
        # Agregar los elementos del array de clausura al array de conjuntos
        self.subsets_.append(sorted_items)
        # Asignar el número 0 al conjunto actual y aumentar el número de conjunto en 1
        self.subsets_iterations.append(0)
        state = 1
        # Agregar el conjunto actual al ciclo de conjuntos
        self.iterations.append(sorted_items)
        # Mientras haya conjuntos en el ciclo, procesar el siguiente conjunto en el ciclo
        while len(self.iterations) > 0:
            self.goto(self.iterations.pop(0))
        # Agregar una transición de aceptación si se encuentra una producción que termine con un punto
        initial_prod = self.productions[0][0]
        final_index = -1
        for i in range(len(self.subsets_)):
            if any(y[0] == initial_prod and y[1][-1] == '.' for y in self.subsets_[i]):
                final_index = i
                break
        if final_index != -1:
            self.transitions.append([self.subsets_iterations[final_index], "$", "accept"])

    def update_closure_array(self, closure):
        # Crear una lista vacía para almacenar los nuevos elementos que se agregarán a closure_array
        new_elements = []
        # Iterar a través de cada elemento en closure_array
        for x in closure:
            # Encontrar el índice del punto (.) en la segunda parte del elemento (x[1])
            dot_index = x[1].index(".")
            # Verificar si el punto no está al final de la lista x[1]
            if dot_index + 1 < len(x[1]):
                # Obtener el valor que sigue al punto en la lista x[1]
                val = x[1][dot_index + 1]

                # Iterar a través de todas las producciones
                for y in self.productions:
                    # Verificar si el valor obtenido coincide con la primera parte de la producción (y[0])
                    # y si la producción no está ya en closure_array
                    if y[0] == val and y not in closure:
                        # Si se cumplen las condiciones, agregar la producción a la lista de nuevos elementos
                        new_elements.append(y)

        # Devolver la lista de nuevos elementos que se agregarán a closure_array
        return new_elements

    def closure(self, input_item, input_elem=None, input_cycle=None):
        # Copia el ítem y lo almacena en una lista para el cálculo de la clausura
        closure = input_item.copy()
        #Creamos la variable estado
        state = 0
        # Calcula la clausura del ítem actual
        new_elements = self.update_closure_array(closure)
        while new_elements:
            closure.extend(new_elements)
            new_elements = self.update_closure_array(closure)
        # Ordena los elementos y los almacena en una lista de conjuntos si no existen en ella
        sort = sorted(closure, key=lambda x: x[0])
        if sort not in self.subsets_:
            self.subsets_.append(sort)
            self.subsets_iterations.append(state)
            state += 1
            self.iterations.append(sort)
        # Si los argumentos de entrada no son nulos, agrega una transición a la lista de transiciones
        if input_elem is None and input_cycle is None:
            return
        initial = self.subsets_.index(input_cycle)
        end = self.subsets_.index(sort)
        self.transitions.append([self.subsets_iterations[initial], input_elem, self.subsets_iterations[end]])

        
    def goto(self, iteraciones):
        # Obtener los elementos a los que se puede transicionar
        elementos = {x[1][x[1].index(".") + 1] for x in iteraciones if x[1].index(".") + 1 < len(x[1])}
        # Crear nuevos items transicionando a los elementos encontrados
        nuevos_elementos_iteraciones = []
        for x in elementos:
            items_temporales = [
                [y[0], y[1][:posicion_punto] + [y[1][posicion_punto + 1], '.'] + y[1][posicion_punto + 2:]]
                for y in iteraciones
                if (
                    (posicion_punto := y[1].index(".")) + 1 < len(y[1])
                    and y[1][posicion_punto + 1] == x
                )
            ]
            # Agregar nuevos items a la lista
            nuevos_elementos_iteraciones.extend(
                item for item in items_temporales if item not in nuevos_elementos_iteraciones
            )
            # Obtener la cerradura de los nuevos items y agregar las transiciones
            self.closure(items_temporales, x, iteraciones)
        return nuevos_elementos_iteraciones
            
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

            
            
            