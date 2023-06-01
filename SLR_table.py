import copy
import pandas as pd
from tabulate import tabulate
import itertools


class SLRTable(object):
    def __init__(self, transitions, conjuntos, numbers, reglas):
        self.transitions = transitions
        self.conjuntos = conjuntos
        self.reglas = reglas
        self.Noterminales = []
        
        self.state = numbers
        self.first = []
        self.action_filas = []
        self.action = []
        self.goto_filas = []
        self.goto = []
        
        for x in self.reglas:
            if x[0] not in self.Noterminales:
                self.Noterminales.append(x[0])

    def get_construction_table(self):
        # Removemos el punto de las producciones 
        self.remove_point()
        
        # Primero dividirlos por sus secciones correspondientes
        lowercase_set = set()
        uppercase_set = set()
        
        for x in self.transitions:
            if x[1].islower():
                lowercase_set.add(x[1])
            else:
                uppercase_set.add(x[1])
        
        self.goto_filas = list(lowercase_set - set(self.goto_filas))
        self.action_filas = list(uppercase_set - set(self.action_filas))
        self.action_filas.sort(reverse=True)
        
        first = self.reglas[0][1][0]
        
        # Primero llenar el goto
        self.goto = [[x, y, z[2]] for x in self.state for y in self.goto_filas for z in self.transitions if z[0] == x and z[1] == y]
        
        # Comenzar la armada de action pero los shift
        self.action = [[x, y, "acc"] if y == "$" else [x, y, "s" + str(z[2])] for x in self.state for y in self.action_filas for z in self.transitions if z[0] == x and z[1] == y]
        
        # Obtener los primeros o FIRST
        self.first = [[x[0], self.First(x[0])] for x in self.reglas if [x[0], self.First(x[0])] not in self.first]
        
        # Armar la action pero con el de follow/replace
        for x, conjunto in enumerate(self.conjuntos):
            for y in conjunto:
                if y[1][-1] == ".":
                    indice = y[1].index(".")
                    if y[1][indice - 1] != first:
                        trans_copy = copy.deepcopy(y)
                        trans_copy[1].remove(".")
                        for z, regla in enumerate(self.reglas):
                            if regla == trans_copy:
                                transaction = self.follow(trans_copy[0], first)
                                self.action += [[x, w, "r" + str(z)] for w in transaction]


    def find_transitions(self, review_transition):
        # Inicializar un conjunto para almacenar las transiciones
        transitions = set()
        # Crear un conjunto de símbolos de revisión
        review_symbols = set(review_transition)
        # Filtrar las reglas que contienen símbolos de revisión
        filtered_rules = [rule for rule in self.reglas if any(symbol in review_symbols for symbol in rule[1])]
        # Iterar sobre las reglas filtradas
        for rule in filtered_rules:
            # Encontrar el siguiente símbolo después de cada ocurrencia de un símbolo de revisión
            for index, symbol in enumerate(rule[1]):
                if symbol in review_symbols and index + 1 < len(rule[1]) and rule[1][index+1] not in self.Noterminales:
                    # Añadir el siguiente símbolo a las transiciones
                    transitions.add(rule[1][index+1])
        # Devolver el conjunto de transiciones
        return transitions


    def find_new_values(self, review_transition):
        # Inicializar un conjunto para almacenar los nuevos valores
        new_set = set()
        # Obtener todos los símbolos de las reglas en un solo conjunto
        symbols = set()
        for rule in self.reglas:
            symbols.update(rule[1])
        # Iterar sobre los elementos en review_transition
        for symbol in review_transition:
            # Iterar sobre las reglas
            for rule in self.reglas:
                # Si symbol está en la lista de símbolos de la regla
                if symbol in rule[1]:
                    # Encontrar el índice de symbol en la lista de símbolos de la regla
                    non_terminal_index = rule[1].index(symbol)
                    # Si non_terminal_index es igual a la longitud de la lista de símbolos de la regla menos uno
                    if non_terminal_index == len(rule[1])-1:
                        # Añadir el símbolo inicial de la regla al conjunto de nuevos valores
                        new_set.add(rule[0])
                    # Si el siguiente símbolo en la lista de símbolos de la regla está en los no terminales
                    elif rule[1][non_terminal_index+1] in self.Noterminales:
                        # Iterar sobre el conjunto de primeros símbolos
                        for first_symbol in self.first:
                            # Si el primer símbolo coincide con el siguiente símbolo en la lista de símbolos de la regla
                            if first_symbol[0] == rule[1][non_terminal_index+1]:
                                # Actualizar el conjunto de nuevos valores con el conjunto de primeros símbolos
                                new_set.update(first_symbol[1])
        # Devolver el conjunto de nuevos valores
        return new_set

    #Función para remover el punto de las producciones
    def remove_point(self):
        # Ubicamos el punto en las producciones y lo removemos
        for x in range(len(self.reglas)):
            for y in range(len(self.reglas[x][1])):
                if self.reglas[x][1][y] == ".":
                    self.reglas[x][1].remove(".")
                    break

    def follow(self, state, accept_state):
        # Inicializar un conjunto con el estado
        revisar = {state}
        # Inicializar un conjunto para almacenar las transiciones
        transitions = set()
        # Ejecutar el bucle hasta que no haya cambios en revisar
        while True:
            # Guardar el estado actual de revisar en previous_revisar
            previous_revisar = set(revisar)
            # Encontrar nuevos valores a partir de revisar
            nuevos_revisar = self.find_new_values(revisar)
            # Actualizar revisar con los nuevos valores
            revisar.update(nuevos_revisar)
            # Actualizar las transiciones con las nuevas transiciones encontradas
            transitions.update(self.find_transitions(revisar))
            # Si revisar no ha cambiado, salir del bucle
            if revisar == previous_revisar:
                break
        # Si accept_state + "'" está en revisar, añadir el símbolo de aceptación al conjunto de transiciones
        if accept_state + "'" in revisar:
            transitions.add("$")
        # Devolver la lista de transiciones
        return list(transitions)
    
    def First(self, symbol):
        # Inicializar la lista visited con el símbolo proporcionado
        visited = [symbol]
        # Bucle infinito que se ejecuta hasta que no haya cambios en la lista visited
        while True:
            # Almacenar el tamaño inicial de la lista visited
            visit_initial = len(visited)
            # Iterar sobre cada elemento en la lista visited
            for y in visited:
                # Iterar sobre cada regla en self.reglas
                for z in self.reglas:
                    # Si el elemento visitado actual coincide con el primer elemento de la regla actual
                    if y == z[0]:
                        # Si el segundo elemento de la regla actual no está en la lista visited
                        if z[1][0] not in visited:
                            # Añadir el segundo elemento de la regla actual a la lista visited
                            visited.append(z[1][0])
            # Almacenar el tamaño final de la lista visited
            final_visit = len(visited)
            # Si el tamaño inicial y final de la lista visited son iguales, salir del bucle
            if visit_initial == final_visit:
                break
        # Crear una nueva lista added con los elementos de visited que también están en self.action_filas
        added = [y for y in visited if y in self.action_filas]
        # Devolver la lista added
        return added


    def print_table(self):
        # Create an empty DataFrame with the specified columns
        columns = self.action_filas + self.goto_filas
        df = pd.DataFrame(columns=columns)

        # Fill the table with data from 'goto' and 'action'
        for row, col, value in self.goto + self.action:
            df.at[row, col] = value

        # Fill NaN values with empty strings
        df.fillna('', inplace=True)

        # Set the index column name
        df.index.name = 'state'

        # Add custom headers
        headers = ['ACTION'] * len(self.action_filas) + ['GOTO'] * len(self.goto_filas)
        df.columns = pd.MultiIndex.from_tuples(zip(headers, df.columns))
        
        # Sort it by state
        df.sort_index(inplace=True)

        # Convert the DataFrame to a table using the 'tabulate' library
        table = tabulate(df, headers='keys', tablefmt='grid', showindex=True)

        # Display the table in the console
        print(table)  
    



                
"""

[[['expression', ['.', 'expression', 'PLUS', 'term']], ['expression', ['.', 'term']], ["expression'", ['.', 'expression']], ['factor', ['.', 'LPAREN', 'expression', 'RPAREN']], ['factor', ['.', 'ID']], ['term', ['.', 'term', 'TIMES', 'factor']], ['term', ['.', 'factor']]], [['expression', ['expression', '.', 'PLUS', 'term']], ["expression'", ['expression', '.']]], [['expression', ['term', '.']], ['term', ['term', '.', 'TIMES', 'factor']]], [['expression', ['.', 'expression', 'PLUS', 'term']], ['expression', ['.', 'term']], ['factor', ['LPAREN', '.', 'expression', 'RPAREN']], ['factor', ['.', 'LPAREN', 'expression', 'RPAREN']], ['factor', ['.', 'ID']], ['term', ['.', 'term', 'TIMES', 'factor']], ['term', ['.', 'factor']]], [['factor', ['ID', '.']]], [['term', ['factor', '.']]], [['expression', ['expression', 'PLUS', '.', 'term']], ['factor', ['.', 'LPAREN', 'expression', 
'RPAREN']], ['factor', ['.', 'ID']], ['term', ['.', 'term', 'TIMES', 'factor']], ['term', ['.', 'factor']]], [['factor', ['.', 'LPAREN', 'expression', 'RPAREN']], ['factor', ['.', 'ID']], ['term', ['term', 'TIMES', '.', 'factor']]], [['expression', ['expression', '.', 'PLUS', 'term']], ['factor', ['LPAREN', 'expression', '.', 'RPAREN']]], [['expression', ['expression', 'PLUS', 'term', '.']], ['term', ['term', '.', 'TIMES', 'factor']]], [['term', ['term', 'TIMES', 'factor', '.']]], [['factor', ['LPAREN', 'expression', 'RPAREN', '.']]]]

[[['E', ['.', 'E', '+', 'T']], ['E', ['.', 'T']], ["E'", ['.', 'E']], ['F', ['.', '(', 'E', ')']], ['F', ['.', 'id']], ['T', ['.', 'T', '*', 'F']], ['T', ['.', 'F']]], [['E', ['E', '.', '+', 'T']], ["E'", ['E', '.']]], [['E', ['T', '.']], ['T', ['T', '.', '*', 'F']]], [['E', ['.', 'E', '+', 'T']], ['E', ['.', 'T']], ['F', ['(', '.', 'E', ')']], ['F', ['.', '(', 'E', ')']], ['F', ['.', 'id']], ['T', ['.', 'T', '*', 'F']], ['T', ['.', 'F']]], [['F', ['id', '.']]], [['T', ['F', '.']]], [['E', ['E', '+', '.', 'T']], ['F', ['.', '(', 'E', ')']], ['F', ['.', 'id']], ['T', ['.', 'T', '*', 'F']], ['T', ['.', 'F']]], [['F', ['.', '(', 'E', ')']], ['F', ['.', 'id']], ['T', ['T', '*', '.', 'F']]], [['E', ['E', '.', '+', 'T']], ['F', ['(', 'E', '.', ')']]], [['E', ['E', '+', 'T', '.']], ['T', ['T', '.', '*', 'F']]], [['T', ['T', '*', 'F', '.']]], [['F', ['(', 'E', ')', '.']]]]

"""

"""
    self.action:  [[0, 'LPAREN', 's3'], [0, 'ID', 's4'], [1, 'PLUS', 's6'], [1, '$', 'acc'], [2, 'TIMES', 's7'], [3, 'LPAREN', 's3'], [3, 'ID', 's4'], [6, 'LPAREN', 's3'], [6, 'ID', 's4'], [7, 'LPAREN', 's3'], [7, 'ID', 's4'], [8, 'RPAREN', 's11'], [8, 'PLUS', 's6'], [9, 'TIMES', 's7']]

    self.action:  [[0, 'id', 's4'], [0, '(', 's3'], [1, '+', 's6'], [1, '$', 'acc'], [2, '*', 's7'], [3, 'id', 's4'], [3, '(', 's3'], [6, 'id', 's4'], [6, '(', 's3'], [7, 'id', 's4'], [7, '(', 's3'], [8, '+', 's6'], [8, ')', 's11'], [9, '*', 's7'], [2, '+', 'r2'], [2, ')', 'r2'], [2, '$', 'r2'], [4, '*', 'r6'], [4, '+', 'r6'], [4, ')', 'r6'], [4, '$', 'r6'], [5, '*', 'r4'], [5, '+', 'r4'], [5, ')', 'r4'], [5, '$', 'r4'], [9, '+', 'r1'], [9, ')', 'r1'], [9, '$', 'r1'], [10, '*', 'r3'], [10, '+', 'r3'], [10, ')', 'r3'], [10, '$', 'r3'], [11, '*', 'r5'], [11, '+', 'r5'], [11, ')', 'r5'], [11, '$', 'r5']]
    
"""


