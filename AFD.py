from RegextoTree import *
import graphviz
from collections import deque
from FA import FA
from YalexReader import *

"""

    Replanteamos el enfoque que le queremos de ahora en adelante.

"""

class AFD_construction(FA):
    def __init__(self, regex=None):
        super().__init__(regex)
        self.regex = regex
        #Lista para almacenar todos los valores que se detecten como token o error léxico
        self.token_list_file = []


    """
        
        Función que se encarga de hacer la construcción del AFD por medio de subconjuntos
    
    """
    def afd_(self, AFN):
        # Copia algunos atributos del NFA original
        self.regex = AFN.regex
        self.alphabet = AFN.alphabet
        self.external_transitions = AFN.transitions
        # Crea el alfabeto especial y establece el contador de estados
        self.alphabet
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
                    entry = [set() for element in self.alphabet]
                    self.transitions[D_states[U]] = entry
                # Crea una transición entre el estado actual y el estado resultante con el símbolo actual
                self.transitions[D_states[T]][self.alphabet.index(symbol)].add(D_states[U])
                
        # Actualiza el alfabeto del DFA y guarda las transiciones originales en una variable temporal
        self.alphabet = self.alphabet
        self.temp_transitions = self.transitions
        
        # Elimina los estados de muerte y actualiza la tabla de transiciones del DFA
        self.external_transitions = self.transitions



    """
        Función que se encarga de crear el AFD directo a partir de su expresión regular
    """
    
    def afd_direct_(self, regex):
        # Se crea un árbol a partir de una expresión regular
        tree = RegextoTree(regex)
        # Se obtiene la raíz del árbol y la lista de nodos
        root = tree.tree_root
        nodes = tree.node_list
        # Se inicializa el contador de estados en 0
        state_counter = 0
        # Se crea una lista con el estado inicial
        states = [state_counter]
        # Se crea una lista vacía para almacenar las transiciones
        transitions = list()
        # Se crea un diccionario vacío para almacenar los estados finales y su símbolo correspondiente
        final_states = {}
        # Se asignan las propiedades a cada nodo del árbol
        tree.Node_properties(nodes)
        # Se crea una lista con el primer estado, que es el firstpos de la raíz del árbol
        Dstates = [tree.compute_first_pos(root)]
        # Se itera hasta que se hayan procesado todos los estados
        while state_counter != len(Dstates):
            # Se itera sobre todos los símbolos del alfabeto del árbol
            for symbol in tree.get_Alphabet():
                # Se buscan los nodos que contienen el símbolo actual
                nodes_with_symbol = [node for node in Dstates[state_counter] if node.value == symbol]
                # Si no hay nodos con el símbolo actual, se salta a la siguiente iteración
                if not nodes_with_symbol:
                    continue
                # Se unen los followpos de los nodos encontrados para crear el nuevo estado
                new_state = set().union(*[node.followpos for node in nodes_with_symbol])
                # Si el nuevo estado es vacío, se salta a la siguiente iteración
                if not new_state:
                    continue
                # Si el nuevo estado no está en Dstates, se agrega a states y Dstates
                if new_state not in Dstates:
                    Dstates.append(new_state)
                    states.append(len(states))
                # Se busca el estado de transición y se agrega la transición a transitions
                new_state_counter = Dstates.index(new_state)
                transitions.append([states[state_counter], symbol, states[new_state_counter]])
            # Se buscan los estados finales y se asignan a final_states
            set_states = set(Dstates[state_counter])
            #print("set states: ", set_states)
            set_final_states = set(tree.compute_last_pos(root))
            node_final = set_states.intersection(set_final_states)
            #print("node final: ", node_final)
            if node_final:
                node_char = node_final.pop().value
                #print("node char: ", node_char)
                final_states[states[state_counter]] = node_char
                #print("Estados finales dentro del if: ", final_states)
            # Se incrementa el contador de estados
            state_counter += 1
        # Se almacenan los resultados en las variables de la clase
        self.regex = regex
        self.states = states
        self.alphabet = tree.get_Alphabet()
        self.transitions = transitions
        self.initial_state = states[0]
        self.final_state = final_states


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
        Función que se encarga de hacer la minimización
    """
    def minimize_function(self):
        #Obtenemos los estados del DFA
        states = self.get_states(self.temp_transitions)
        # Dividimos los estados en dos conjuntos: aceptación y no aceptación
        acceptance = frozenset({state for state in states if state in self.acceptance_states})
        non_acceptance = frozenset(states - acceptance)
        partition = {acceptance, non_acceptance}
        #Aplicamos el algoritmo de Hopcroft para obtener grupos de estados equivalentes
        final_partition = self.hopcroft(partition)
        #Obtenemos los representantes de cada grupo y construir una tabla de representantes
        representatives, table = self.representatives(final_partition)
        #Construimos el DFA mínimo a partir de la tabla de representantes
        transitions = {}
        for element in representatives:
            if element not in transitions:
                transitions[element] = [set() for element in self.alphabet]
            for symbol in self.alphabet:
                index = self.get_symbol_index(symbol)
                state = self.temp_transitions[element][index]
                transition_representative = self.get_transition_representative(state, table)
                transitions[element][index].add(transition_representative)
        #Eliminamos los estados muertos y actualizar las transiciones
        self.transitions = transitions
        self.delete_dead_state()
        self.external_transitions = self.transitions

    
    """
        El algoritmo de Hopcroft es un algoritmo de particionamiento que busca agrupar los estados del DFA en grupos de estados equivalentes. Para ello, 
        el algoritmo considera cada símbolo de entrada y agrupa los estados que producen la misma salida para ese símbolo en un mismo grupo. 
        Este proceso se repite hasta que no se puedan formar más grupos.
    """
    def hopcroft(self, partition):
        # Copiar la partición recibida para evitar modificarla directamente
        partition_new = list(partition.copy())
        # Para cada grupo en la partición
        for group in partition:
            # Si el grupo no está vacío
            if group:
                # Crear un nuevo grupo a partir del actual
                new_group = self.create_new_partition(group, partition)
                
                # Remover el grupo actual de la partición
                partition_new.remove(group)
                
                # Agregar el nuevo grupo a la partición
                for element in new_group:
                    partition_new.append(element)
        # Convertir la partición en un conjunto para compararla
        partition_new = set(partition_new)
        # Si la partición nueva es igual a la anterior, entonces se ha llegado a la partición final
        if partition_new == partition:
            return partition
        # De lo contrario, continuar iterando con la partición nueva
        else:
            return self.hopcroft(partition_new)

    
    """
        Función que se encarga de crear un nuevo grupo de particiones a partir de un grupo existente.

    """
    def create_new_partition(self, group, partition):
        # Se convierte la partición a una lista para facilitar la iteración
        groups = list(partition)
        # También se convierte el grupo actual a una lista
        group_list = list(group)
        # Se itera por cada símbolo del alfabeto
        for symbol in self.alphabet:
            # Se crea una lista vacía para guardar las etiquetas de cada elemento del grupo actual
            group_tag = []
            # Se itera por cada elemento del grupo actual
            for element in group_list:
                # Se obtiene la etiqueta correspondiente al elemento actual para el símbolo actual
                group_tag.append(self.get_group(element, groups, symbol))
            # Si las etiquetas son distintas, se crea una nueva partición y se retorna
            if not self.check_equal(group_tag):
                return self.create_partition(group_list, group_tag)
        # Si las etiquetas son iguales para todos los símbolos, no es necesario crear una nueva partición
        return {group}
        
            
    """
        Funciones que se encargarán de realizar la simulación de nuestro afd
    """
    
    def read_characters(self,filename):
        with open(filename, 'r') as file:
            return [ord(char) for char in file.read()]

    def write_simulation_result(self, token_list, filename='simulation_result.txt'):
        with open(filename, 'w') as file:
            for token_string, token in token_list:
                file.write(f"{repr(token_string)} {token}\n")

    def process_characters(self, chars):
        # Inicializa una lista vacía para almacenar los resultados de los tokens
        token_results = list()
        # Inicializa una lista vacía para almacenar los caracteres del token actual
        char_list = list()
        # Inicializa una variable para almacenar el token previo
        prev_token = None
        # Inicializa el estado actual con el estado inicial del autómata
        current_states = [self.initial_state]
        # Inicializa un índice para rastrear la posición actual en la lista de caracteres
        char_index = 0
        # Mientras el índice sea menor que la longitud de la lista de caracteres
        while char_index < len(chars):
            # Obtiene el carácter en la posición actual del índice
            char = chars[char_index]
            # Añade el carácter a la lista de caracteres del token actual
            char_list.append(char)
            # Actualiza los estados actuales usando el método move con los estados actuales y el carácter
            current_states = self.move(current_states, char)
            # Incrementa el índice en 1
            char_index += 1
            # Si no hay estados actuales (no se encontró ninguna transición)
            if not current_states:
                # Reinicia los estados actuales al estado inicial del autómata
                current_states = [self.initial_state]
                # Si hay un token previo
                if prev_token:
                    # Elimina el último carácter de la lista de caracteres del token actual
                    char_list.pop()
                    # Decrementa el índice en 1
                    char_index -= 1
                    # Convierte la lista de caracteres en una cadena y la guarda en token_str
                    token_str = "".join(chr(i) for i in char_list)
                    # Añade el par (token_str, prev_token) a la lista de resultados de tokens
                    token_results.append([token_str, prev_token])
                    # Reinicia la lista de caracteres del token actual
                    char_list = list()
                    # Reinicia el token previo
                    prev_token = None
                else:
                    # Si no hay un token previo, se genera un error léxico con el primer carácter de la lista de caracteres
                    error_character = chr(char_list[0])
                    token_results.append([error_character, "Error Lexico"])
                    # Reinicia la lista de caracteres del token actual
                    char_list = list()
            else:
                # Si hay estados actuales, crea conjuntos de estados actuales y estados finales
                state_set = set(current_states)
                final_state_set = set(self.final_state)
                # Si hay una intersección entre los conjuntos de estados actuales y estados finales
                if state_set.intersection(final_state_set):
                    # Obtiene el último estado final de la intersección
                    last_final_state = state_set.pop()
                    # Asigna el token correspondiente al último estado final como el token previo
                    prev_token = self.final_state[last_final_state]
        # Devuelve la lista de resultados de tokens
        return token_results
    

    

    def simulate_afd(self, filename):
        characters = self.read_characters(filename)
        token_list = self.process_characters(characters)
        self.write_simulation_result(token_list)
        self.token_list_file.extend(token_list)

            
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
    
    def move(self, states, character):
        # Método que mueve un conjunto de estados (states) a través de una transición con un carácter (character)
        # desde una configuración actual a una configuración resultante.
        states_result = set()
        while states:
            state = states.pop()
            # Se busca una transición que vaya desde el estado actual hacia un estado con el carácter dado
            new_states = {i[2] for i in self.transitions if i[0] == state and i[1] == character}
            states_result.update(new_states)
        # Al final, se devuelve la lista de estados resultantes
        return list(states_result)


    
    
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
        Función encargada de construir un archivo scanner
    """
    def build_scanner(self, path, name):
        file = open(f"./{name}.py", "w")  
        file.write("class ScannerClassAFD(object):\n")
        file.write("\tdef __init__(self):\n")
        file.write(f"\t\tself.regex = {self.regex}\n")
        file.write(f"\t\tself.states = {self.states}\n")
        file.write(f"\t\tself.transitions = {self.transitions}\n")
        file.write(f"\t\tself.initial_state = '{self.initial_state}'\n")
        file.write(f"\t\tself.final_state = {self.final_state}\n")
        file.write(f"\t\tself.alphabet = {self.alphabet}\n\n")
        file.write("\tdef tokens(token):\n")
        yal = YALexGenerator(path)
        #print("Lista de tokens del yal: ", yal.tokens_rule_list)
        for i in yal.tokens_rule_list:
            file.write(f"\t\tif(token == '{i}'):\n")
            file.write(f"\t\t\t{yal.tokens_rule_list[i]}\n")
        file.write(f"\n\t\treturn ERROR\n\n")
        file.close()
    
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
            if (state == self.states.index(self.initial_state)):
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