"""
    Este archivo se encargará de convertir mediante la clase Node, la expresión 
    regular brindada a un árbol sintáctico.
    
"""

"""
    José Rodrigo Barrera García
    Universidad del Valle de Guatemala
    Diseño de Lenguajes
    20807
    Laboratorio A 
"""
from Node import *
import re
from RegexErrorChecker import RegexErrorChecker

class RegextoTree(object):
    def __init__(self, expression = None):
        self.alphabet = ['ε']
        self.operators = {'.', '|', '*', '+', '?'}
        self.binarios = {'|'}
        self.error_checker = RegexErrorChecker(expression, self.alphabet)
        self.expression = expression.strip()

        if '.' in self.expression:
            error = "ERROR EN LA EXPRESIÓN REGULAR. NO LA PUEDES COLOCAR CON EL OPERADOR '.' DE LA CONCATENACIÓN."
            self.error_checker.add_error(error)

        if not self.expression:
            error = "EXPRESIÓN VACÍA"
            self.error_checker.add_error(error)

        whitespace = r"\s+"
        self.expression = re.sub(whitespace, "", self.expression)
        self.create_alphabet()
        self.add_concatenation_symbol()
        self.idempotency()
        self.build_AST()

        if self.error_checker.get_size() > 0:
            raise Exception(self.error_checker.get_error_result())

    """ 
       Función que se encarga de extraer el alfabeto contenido en la expresión regular ingresada
        
    """
    def create_alphabet(self):
        for element in self.expression:
            if element not in self.operators and element not in '()':
                self.alphabet.append(element)

    """
        Función que sirve para agregar el operador de concatenación '.' a la expresión regular
    """
    def add_concatenation_symbol(self):
        new_expression = []
        for i, current in enumerate(self.expression):
            new_expression.append(current)
            
            if i + 1 < len(self.expression):
                next = self.expression[i + 1]
                if (current != "(" and next != ")") and next not in self.operators and current not in self.binarios:
                    new_expression.append('.')
        self.expression = ''.join(new_expression)

    """
        Función que sirve para simplificar la expresión regular eliminando la redundancia de 
        operadores '*' y '+' consecutivos, mejorando así su rendimiento.
    """
    def idempotency(self):
        last = ''
        expression_list = list(self.expression)

        for i in range(len(expression_list)):
            if expression_list[i] == '*' or expression_list[i] == '+':
                if last == expression_list[i]:
                    expression_list[i] = ''
                else:
                    last = expression_list[i]
            else:
                last = ''
        self.expression = ''.join(expression_list)

    """
        Función que se encarga de construir el árbol de sintaxis abstracta para una expresión regular, 
        a través de la construcción de nodos y su organización en una pila, y verifica que se utilicen 
        correctamente los operadores unarios y binarios.
    """
    def build_tree(self, operator, stack):
        # Se crea un nuevo nodo con el operador actual.
        new_node = Node(operator) 
        # Variable de control para manejar errores.
        has_error = False  
        # Si el operador es unario
        if operator in '*+?':
            # Miramos si el stack está vacío
            #Si lo está
            if not stack:  
                error = f"El operador unario {operator} no se aplica a ningún símbolo."
                # Se agrega un error al gestor de errores.
                self.error_checker.add_error(error)
                # Se marca la variable de control como True.
                has_error = True
            #Si el stack no está vacío
            else:
                #Se obtiene el nodo del símbolo al que se aplicará el operador.
                o1 = stack.pop()
                # Si el operador es '?'  
                if operator == '?':
                     # El valor del nuevo nodo se cambia por '|' (operador 'o' en expresiones regulares)  
                    new_node.value = '|'
                    # El nodo obtenido se coloca como hijo izquierdo del nuevo nodo. 
                    new_node.set_left_child(o1)
                    # Se crea un nodo para representar la transición vacía.  
                    epsilon_node = Node('ε')
                    # El nodo creado se coloca como hijo derecho del nuevo nodo.  
                    new_node.set_right_child(epsilon_node)
                # Si el operador es '*' o '+' 
                else:
                    # El nodo obtenido se coloca como hijo izquierdo del nuevo nodo.
                    new_node.set_left_child(o1)
         # Si el operador es binario ('|' o '.')
        elif operator in '|.':
            # Si hay menos de dos nodos en el stack 
            if len(stack) < 2:  
                error = f"El operador binario {operator} no tiene los operadores necesarios."
                # Se agrega un error al gestor de errores.
                self.error_checker.add_error(error)
                # Se marca la variable de control como True. 
                has_error = True
            # Si hay al menos dos nodos en el stack  
            else:
                # Se obtiene el segundo nodo.  
                o2 = stack.pop()
                 # Se obtiene el primer nodo.  
                o1 = stack.pop()
                # El primer nodo se coloca como hijo izquierdo del nuevo nodo. 
                new_node.set_left_child(o1)
                # El segundo nodo se coloca como hijo derecho del nuevo nodo.  
                new_node.set_right_child(o2)  
        # Si no hubo errores
        if not has_error:
            # Se agrega el nuevo nodo al stack.  
            stack.append(new_node)
        # Se retorna el stack actualizado. 
        return stack  


    """
        Función que implementa el algoritmo de Shunting Yard para construir un árbol de sintaxis abstracta (AST) a partir de una expresión regular.
        
    """
    def build_AST(self):
        # Se inicializa una lista vacía que se usará como stack para almacenar los nodos del árbol de sintaxis abstracta
        output_stack = []
        # Se inicializa otra lista vacía que se usará como stack para almacenar los operadores
        operator_stack = []
         # Se define una cadena que contiene los operadores que se pueden usar en la expresión regular
        operators = ".*+|?"
        # Se itera sobre los elementos de la expresión regular
        for element in self.expression:
            # Si el elemento es un símbolo del alfabeto de la expresión regular
            if element in self.alphabet:
                #Se crea un nodo con el símbolo y se añade al stack de nodos
                output_stack.append(Node(element))
                # Si el elemento es un paréntesis izquierdo
            elif element == '(':
                #Se añade al stack de operadores
                operator_stack.append(element)
                # Si el elemento es un paréntesis derecho
            elif element == ')':
                #Mientras que el stack de operadores no esté vacío y el último elemento no sea un paréntesis izquierdo
                while operator_stack and operator_stack[-1] != '(':
                    #Se saca el último operador del stack de operadores  
                    pop_element = operator_stack.pop()
                    # Se construye un árbol con el operador y los últimos dos nodos del stack de nodos 
                    output_stack = self.build_tree(pop_element, output_stack)
                    # Si el stack de operadores no está vacío 
                if operator_stack:
                    #Se saca el paréntesis izquierdo
                    operator_stack.pop()
                    # Si el elemento es un operador
            elif element in operators:
                # Mientras que el stack de operadores no esté vacío, el último operador no sea un paréntesis izquierdo y la precedencia del operador actual sea menor o igual que la del último operador en el stack de operadores  
                while operator_stack and operator_stack[-1] != '(' and self.precedence(element) <= self.precedence(operator_stack[-1]):
                    #Se saca el último operador del stack de operadores  
                    pop_element = operator_stack.pop()
                    #Se construye un árbol con el operador y los últimos dos nodos del stack de nodos
                    output_stack = self.build_tree(pop_element, output_stack)
                    # Se añade el operador actual al stack de operadores 
                operator_stack.append(element)  
        # Cuando se ha terminado de iterar sobre todos los elementos de la expresión regular
        while operator_stack:
            # Se saca el último operador del stack de operadores 
            pop_element = operator_stack.pop()
            # Se construye un árbol con el operador y los últimos dos nodos del stack de nodos  
            output_stack = self.build_tree(pop_element, output_stack)
        # Si todavía quedan nodos en el stack de nodos
        if output_stack:
            # Se saca el último nodo del stack de nodos y se usa como raíz del árbol de sintaxis abstracta
            root = output_stack.pop()
            #Se asigna la raíz al árbol de la clase. 
            self.set_root(root)  

    def to_postfix(self):
        return self.postorder()
        
    def get_root(self):
        return self.root

    def precedence(self, element):
        if element in '()':
            return 4
        if element in '*+?':
            return 3
        if element == '.':
            return 2
        if element in '|':
            return 1
    
    def set_root(self, node):
        self.root = node

    def postorder(self):
        return self.postorder_helper(self.root).replace('?', 'ε|')
    
    """
        Función que realiza un recorrido postorden del árbol comenzando desde el nodo pasado como argumento, 
        concatenando los valores de los nodos visitados en el orden correcto para obtener la 
        expresión regular correspondiente.
    """
    def postorder_helper(self, node):
        # Creamos una variable vacía para guardar el resultado
        res = ""
        # Si el nodo existe
        if node:
            # Si el valor del nodo es un operador unario (*, +, ?)
            if node.value in '?*+':
                # Aplicamos la función de postorder_helper al nodo hijo izquierdo
                res += self.postorder_helper(node.left_child)
            # Si el valor del nodo es un operador binario (|, .)
            elif node.value in '|.':
                # Aplicamos la función de postorder_helper al nodo hijo izquierdo y al nodo hijo derecho
                res += self.postorder_helper(node.left_child)
                res += self.postorder_helper(node.right_child)
            # Concatenamos el valor del nodo al resultado
            return res + node.value
