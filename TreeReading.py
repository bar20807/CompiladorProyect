from Node import Node

class TreeReading():
    def __init__(self, regex):
        self.regex = regex
        self.alphabet = regex.alphabet
        self.stack = list(self.regex.to_postfix() + '#.')
        self.follow_pos = {}
        self.build_tree()
        self.count = 1
        self.post_order_assignment()
        
    
    def post_order_assignment(self):
        self.assignment_helper(self.root)

    """
        Esta función calcula los follow_pos de cada posición en el árbol sintáctico.
        Si el nodo actual es un operador '*', entonces se obtienen los últimos posibles del hijo izquierdo
        y se agregan los primeros posibles del hijo izquierdo a cada follow_pos correspondiente en el diccionario. 
        Si el nodo actual no es un operador '*', entonces se obtienen los últimos posibles del hijo izquierdo
        y se agregan los primeros posibles del hijo derecho a cada follow_pos correspondiente en el diccionario.
    """
    
    def compute_follow_pos(self, node):
        # Si el nodo actual es un operador '*'
        if node.value == '*':
            # Obtiene el hijo izquierdo del nodo
            child = node.left_child
            # Obtiene los últimos posibles del hijo
            last_pos = child.last_pos
            # Para cada elemento en los últimos posibles
            for element in last_pos:
                # Para cada clave en el diccionario follow_pos
                for key in self.follow_pos:
                    # Si el elemento se encuentra en la clave
                    if element in key:
                        # Agrega los primeros posibles del hijo a la clave
                        self.follow_pos[key] = self.follow_pos[key].union(child.first_pos)
        else:
            # Si el nodo actual no es un operador '*'
            # Obtiene los hijos izquierdo y derecho del nodo
            right_child = node.right_child
            left_child = node.left_child
            # Obtiene los últimos posibles del hijo izquierdo
            last_pos = left_child.last_pos
            # Para cada elemento en los últimos posibles
            for element in last_pos:
                # Para cada clave en el diccionario follow_pos
                for key in self.follow_pos:
                    # Si el elemento se encuentra en la clave
                    if element in key:
                        # Agrega los primeros posibles del hijo derecho a la clave
                        self.follow_pos[key] = self.follow_pos[key].union(right_child.first_pos)
        
    def get_followpos_table(self):
        return self.follow_pos
    
    """
        Función que se encarga de computar los follow pos de un árbol sintáctico de una expresión regular
        Recibe como parámetro el nodo raíz del árbol sintáctico
        Utiliza los atributos nullable, first_pos, last_pos y follow_pos de los nodos del árbol sintáctico
    
    """
    def assignment_helper(self, node):
        if node.value in '|.':
            self.assignment_helper(node.left_child)
            self.assignment_helper(node.right_child)
            if node.value == '.':
                # Si el nodo izquierdo es nullable, se unen las primeras posiciones de ambos hijos
                if node.left_child.nullable:
                    node.first_pos = node.left_child.first_pos.union(node.right_child.first_pos)
                else:
                    node.first_pos = node.left_child.first_pos
                # Si el nodo derecho es nullable, se unen las últimas posiciones de ambos hijos
                if node.right_child.nullable:
                    node.last_pos = node.left_child.last_pos.union(node.right_child.last_pos)
                else:
                    node.last_pos = node.right_child.last_pos
                # El nodo es nullable si ambos hijos lo son
                node.nullable = node.right_child.nullable and node.left_child.nullable
                self.compute_follow_pos(node)
            else:
                # Para la operación OR, se unen las primeras y últimas posiciones de ambos hijos
                node.first_pos = node.left_child.first_pos.union(node.right_child.first_pos)
                node.last_pos = node.left_child.last_pos.union(node.right_child.last_pos)
                # El nodo es nullable si cualquiera de sus hijos lo es
                node.nullable = node.right_child.nullable or node.left_child.nullable
        if node.value == '*':
            self.assignment_helper(node.left_child)
            # El nodo es nullable si su hijo lo es
            node.nullable = True
            # El primer y último símbolo son los mismos que el hijo
            node.first_pos = node.first_pos.union(node.left_child.first_pos)
            node.last_pos = node.last_pos.union(node.left_child.last_pos)
            self.compute_follow_pos(node)
        if node.value in self.alphabet or node.value == '#':
            node.number = self.count
            self.count += 1
            if node.value == 'ε':
                node.nullable = True
            else:
                # El primer y último símbolo es el número del nodo
                node.first_pos.add(node.number)
                node.last_pos.add(node.number)
                # El follow_pos se inicializa como un conjunto vacío
                self.follow_pos[(node.number, node.value)] = set()


    def build_tree(self):
        self.root = self.build_helper()

    """
        Esta función se encarga de construir un árbol de expresión regular a partir de una pila con los símbolos de la expresión.
        Utiliza un enfoque de recorrido postorden, en el que cada vez que encuentra un símbolo de operación, construye los nodos correspondientes
        en el árbol y asigna los hijos del nodo actual en función del tipo de operación.
        Devuelve el nodo raíz del árbol.
    """
    
    def build_helper(self):
        # Obtiene el último elemento de la pila
        #print("to_postfix afd directo: " + str(self.stack))
        current = self.stack.pop()
        # Crea un nodo con el valor obtenido de la pila
        node = Node(current)
        # Si el valor es el símbolo final o un caracter del alfabeto
        if current == '#' or current in self.alphabet:
            # Retorna el nodo con el valor obtenido
            return node
        # Si el valor es un operador de concatenación o de unión
        elif current in '|.':
            # Obtiene el hijo derecho y el hijo izquierdo del nodo
            right_child = self.build_helper()
            left_child = self.build_helper()
            
            # Asigna los hijos obtenidos al nodo actual
            node.right_child = right_child
            node.left_child = left_child  
        # Si el valor es un operador de cerradura de Kleene
        elif current == '*':
            # Obtiene el hijo del nodo
            child = self.build_helper()
            
            # Asigna el hijo obtenido al hijo izquierdo del nodo
            node.left_child = child 
        # Si el valor es un operador de uno o más
        elif current == '+':
            # Obtiene el hijo del nodo
            child = self.build_helper()
            # Asigna al nodo actual el valor de concatenación
            node.value = '.'
            # Crea un nodo de cerradura de Kleene para el hijo
            right_child = Node('*')
            # Asigna el hijo obtenido al hijo izquierdo del nodo de cerradura de Kleene
            node.right_child = right_child
            node.right_child.left_child = child
            # Asigna el hijo obtenido al hijo izquierdo del nodo actual
            node.left_child = child  
        # Retorna el nodo con los hijos asignados
        return node

    def get_last_pos(self):
        for key in self.follow_pos:
            if key[1] == '#':
                return key[0]
            
    #Función para visualizar el árbol formado
    def clen_regular_expression(self, regular_expression):
        valid_chars = '|*?.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789+-/();:=<> \t\n'
        return ''.join(c for c in regular_expression if c in valid_chars)