from RegextoTree import *
import graphviz
from collections import deque
from FA import FA


class AFD_construction(FA):
    def __init__(self, regex=None):
        self.regex = None
        self.states_counter = 0
        self.states = []
        self.transitions = []
        self.initial_state = []
        self.final_state = []
        self.symbols = []


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
        tree = RegextoTree(self.regex)
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
    
    #Función que se encarga de obtener los estados    
    def get_states(self, transitions):
        return {state for state in transitions}
    
    """
        Función que se encarga de buscar el grupo al que pertenece el estado resultante 
        de transicionar desde el estado element con el símbolo symbol. 
    
    """
    def get_group(self, element, groups, symbol):
        # Se obtiene el índice del símbolo en el alfabeto
        index = self.get_symbol_index_special(symbol)
        # Se obtiene la transición del elemento actual usando el símbolo dado
        transition = list(self.temp_transitions[element][index])[0]
        # Se busca en los grupos de la partición el grupo que contenga la transición del elemento
        for group in groups:
            if transition in group:
                # Se devuelve el grupo como una lista
                return list(group)
    """
        Función que se encarga de comparar todos los elementos de la lista tag para determinar si son iguales.
    
    """        
    def check_equal(self, tag):
        """
        Esta función comprueba si todos los elementos de una lista son iguales.
        
        Args:
            tag (list): Lista de elementos a comparar.
        
        Returns:
            bool: Devuelve True si todos los elementos de la lista son iguales, False en caso contrario.
        """
        # Asignamos el primer elemento de la lista a la variable last.
        last = tag[0]
        # Recorremos la lista. 
        for element in tag:
             # Si algún elemento de la lista es diferente a last
            if element != last:
                #devolvemos False.
                return False
            # Si los elementos son iguales, asignamos el valor actual a last.
            last = element 
        # Si llegamos al final de la lista sin encontrar elementos diferentes, devolvemos True.
        return True 

    """
        Función que se encarga de crear una nueva partición a partir de un grupo y sus etiquetas.
    
    """
    def create_partition(self, group, group_tag):
        # Diccionario auxiliar para agrupar elementos con la misma etiqueta
        group_dict_helper = {}
        
        # Para cada etiqueta del grupo
        for i in range(len(group_tag)):
            tag = tuple(group_tag[i])
            element = group[i]
            
            # Si la etiqueta ya existe en el diccionario, se agrega el elemento a su conjunto
            if tag in group_dict_helper:
                group_dict_helper[tag].add(element)
            # Si no existe, se crea una nueva entrada en el diccionario con el elemento como único miembro del conjunto
            else:
                group_dict_helper[tag] = {element}

        # Crear una nueva partición a partir del diccionario auxiliar
        new_partition = set()
        for key in group_dict_helper:
            # Convierte cada conjunto de elementos con la misma etiqueta en un frozenset (conjunto inmutable)
            new_partition.add(frozenset(group_dict_helper[key]))

        return new_partition

    """
        Este método toma como entrada un particionamiento de estados de un autómata, y devuelve dos cosas: una lista con los representantes de cada grupo, 
        y una tabla que asocia cada grupo con su respectivo representante.
    
    """
    def representatives(self, partition):
        # Se inicializan las variables necesarias
        table = {}
        representatives = []
        initial = list(self.initial_states)[0] # Se toma el estado inicial del autómata
        # Se itera sobre los grupos del particionamiento
        for element in partition:
            # Se verifica que el grupo no esté vacío
            if element:
                representative = None
                # Si el grupo tiene el estado muerto, este es el representante del grupo
                if self.dead_state in element:
                    representative = self.dead_state
                # Si el grupo tiene el estado inicial, este es el representante del grupo
                if initial in element:
                    representative = initial
                # Si no, se elige un estado arbitrario como representante del grupo
                else:
                    representative = list(element)[0]
                # Se guarda la relación entre el grupo y su representante en una tabla
                table[element] = representative
                # Se guarda el representante en una lista
                representatives.append(representative)
        # Se devuelven los representantes y la tabla de relación entre grupos y representantes
        return representatives, table

    """
        Función que se encarga de obtener el representante de un grupo de estados.
    """
    def get_transition_representative(self, element, table):
        # Obtenemos el primer elemento del grupo de estados "element"
        element = list(element)[0]
        # Buscamos en la tabla de representantes
        for key in table:
            # Si el estado "element" se encuentra en el grupo "key"
            if element in key:
                # Retornamos el representante de ese grupo
                return table[key]

    
    
    
    """
        Función que se encarga de hacer la simulación del AFD
    
    """
    def simulate_afd(self, string):
        # Verifica que los caracteres del string pertenezcan al alfabeto
        for element in string:
            if element not in self.alphabet:
                return "rechazada"
        # Inicia en el estado inicial
        s = self.initial_states
        # Si el string está vacío, se mueve con una transición vacía
        if not string:
            s = self.move(s, 'ε')
        else:
            # Se mueve a través de cada elemento del string
            for element in string:
                s = self.move(s, element)
        # Si el estado actual está en los estados de aceptación, se acepta el string
        if s.intersection(self.acceptance_states):
            return "aceptada"
        # Si no, se rechaza el string
        return "rechazada"

    
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

    
    # Funcion para graficar el automata
    def graphAF(self):
        
        # Se realiza el titulo del automata
        description = ("AFD")
        graph = Digraph()
        graph.attr(rankdir="LR", labelloc="t", label=description)

        # Por cada estado se crea la imagen para graficarlo
        for state in self.states:

            if(state in self.initial_state):
                graph.node(str(state), str(state), shape="circle", style="filled")
            if(state in self.final_state):
                graph.node(str(state), str(state), shape="doublecircle", style="filled")
            else:
                graph.node(str(state), str(state), shape="circle")

        # Se crean las transiciones de los estados
        for transition in self.transitions:
            graph.edge(str(transition[0]), str(transition[2]), label=str(transition[1]))

        # Se renderiza
        graph.render(f"./images/AFDDefault", format="png", view=True)