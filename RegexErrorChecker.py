"""
    José Rodrigo Barrera García
    Universidad del Valle de Guatemala
    Diseño de Lenguajes
"""
class RegexErrorChecker(object):
    def __init__(self, regex):
        self.regex = regex
        self.alphabet = ['ε']
        self.operators_list = ['|', '?', '*', '+']
        self.operators = []
        self.postfix_expression = []
        self.ERROR_CHECKER()
    
    """
         Este código verifica si los paréntesis en una expresión regular están correctamente balanceados 
         y contienen contenido válido entre ellos, y genera mensajes de error si se encuentra algún problema.
    
    """
    def check_parenthesis(self):
        # Inicializamos una pila vacía para almacenar índices de paréntesis abiertos
        stack = []
        # Inicializamos una lista vacía para almacenar índices de paréntesis abiertos            
        opening_parenthesis = []
        # Inicializamos un contador para llevar el índice actual
        i = 0
        # Iteramos a través de cada elemento de la expresión regular                        
        for element in self.expression:
            # Si encontramos un paréntesis de apertura     
            if element == '(':
                # Almacenamos su índice en la pila              
                stack.append(i)
                # Almacenamos su índice en la lista de paréntesis abiertos             
                opening_parenthesis.append(i)
                # Si encontramos un paréntesis de cierre: 
            elif element == ')':
                #Se verifica si la pila está vacía, si lo está,  significa que no hay paréntesis de apertura correspondientes            
                if not stack:
                    # Agregamos un error al registro de errores              
                    error = f"No coinciden los paréntesis en el índice: {i}." 
                    self.error_logs.append(error)
                #Si hay paréntesis de apertura correspondientes
                else:
                    # Eliminamos el índice del paréntesis de apertura de la pila                       
                    stack.pop()
                    # Obtenemos el índice del paréntesis de apertura correspondiente           
                    opening_index = opening_parenthesis.pop()
                    #Obtenemos la subcadena que está entre los dos paréntesis  
                    substring = self.expression[opening_index+1:i]
                    # Si la subcadena está vacía, hay un error  
                    if not substring:       
                        error = f"Los paréntesis no tienen nada entre ellos."
                        self.error_logs.append(error)
            # Incrementamos el contador de índices
            i += 1
        # Después de iterar a través de todos los elementos de la expresión regular, si la pila no está vacía                          
        while stack:
            #Obtenemos el índice del paréntesis de apertura correspondiente                        
            error_index = stack.pop()
            # Agregamos un error al registro de errores       
            error = f"Falta cerrar un paréntesis en el índice: {error_index}." 
            self.error_logs.append(error)

    def check_sequence_operators(self):
        # Recorremos la expresión caracter por caracter
        for i in range(len(self.expression)):
            # Verificamos que no estemos en el último caracter de la expresión
            if i + 1 < len(self.expression):
                # Obtenemos el caracter actual y el siguiente
                current = self.expression[i]
                next_char = self.expression[i + 1]
                # Si el caracter actual es un operador binario y el siguiente también lo es, generamos un error
                if current in self.binary and next_char in self.binary:
                    error = f"Operador binario seguido de otro operador binario en el índice: {i}."
                    self.error_logs.append(error)
                # Si el caracter actual es un operador binario y el siguiente es un operador unario, generamos un error
                elif current in self.binary and next_char in self.unary:
                    error = f"Operador binario seguido de operador unario en el índice: {i}."
                    self.error_logs.append(error)
    
    """
        Funciónn que se encarga de evaluar si al comienzo de la función hay un operador binario o unario.
        
    """
    def check_ends_expression(self):
        # Si la expresión está vacía, no hay nada que comprobar
        if not self.expression:
            return
        # Comprobamos si el primer elemento es un operador
        first_element = self.expression[0]
        if first_element in self.binary or first_element in self.unary:
            # Generamos un error
            error = r"Operador al comienzo de la expresión."
            self.error_logs.append(error)

    """
        Función que se encarga de agregar un error a la lista de errores.
    
    """
    def add_error(self, error):
        self.error_logs.append(error)
    
    def ERROR_CHECKER(self):
        # Verificar que la expresión no comienza con un operador
        if self.regex[0] in self.operators_list:
            raise Exception("ERROR: No se puede iniciar con simbolo de operacion")
        # Verificar que la cantidad de paréntesis sea correcta
        count = 0
        for char in self.regex:
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
                if count < 0:
                    raise Exception("ERROR: Cantidad de Parentesis Incorrecta")
        if count != 0:
            raise Exception("ERROR: Cantidad de Parentesis Incorrecta")


    def precedence(self, operator):
        if operator == '(':
            return 1
        if operator == '*+?':
            return 4
        if operator == '.':
            return 3
        if operator == '|':
            return 2
        else:
            return 5

    # Algoritmo Shunting-Yard
    def to_postfix(self):
        # Lista donde se guardan los caracteres que aún no han sido procesados
        characters_queue = []
        # Iteramos sobre los caracteres de la expresión regular
        for i in range(len(self.regex)):
            char = self.regex[i]

            # Si hay al menos un caracter después de char
            if((i + 1) < len(self.regex)):
                next_char = self.regex[i + 1]
                # Agregamos char a la lista de caracteres que aún no han sido procesados
                characters_queue.append(char)
                # Si char no es un paréntesis abierto, next_char no es un paréntesis cerrado, ni un operador,
                # y char no es un '|' (OR), agregamos un punto (concatenación) a la lista de caracteres sin procesar
                if((char != '(') and (next_char != ')') and (next_char not in self.operators_list) and (char != '|')):
                    characters_queue.append('.')
        # Agregamos el último caracter a la lista de caracteres sin procesar
        characters_queue.append(self.regex[len(self.regex) - 1])
        # Iteramos sobre los caracteres que aún no han sido procesados
        for char in characters_queue:
            # Si el caracter es un paréntesis abierto, lo agregamos a la pila de operadores
            if(char == '('):
                self.operators.append(char)
            # Si el caracter es un paréntesis cerrado
            elif(char == ')'):
                # Desapilamos operadores y los agregamos a la lista postfix hasta encontrar el paréntesis abierto correspondiente
                while(self.operators[-1] != '('):
                    self.postfix_expression.append(self.operators.pop())
                # Desapilamos el paréntesis abierto correspondiente
                self.operators.pop()
            # Si el caracter es un operador
            else:
                # Desapilamos operadores con mayor o igual precedencia que char, agregándolos a la lista postfix
                while(len(self.operators) > 0):
                    last_char = self.operators[-1]
                    last_char_precedence = self.precedence(last_char)
                    char_precedence = self.precedence(char)
                    if(last_char_precedence >= char_precedence):
                        self.postfix_expression.append(self.operators.pop())
                    else:
                        break
                # Agregamos char a la pila de operadores
                self.operators.append(char)
        # Desapilamos todos los operadores restantes y los agregamos a la lista postfix
        while(len(self.operators) > 0):
            self.postfix_expression.append(self.operators.pop())
        # Devolvemos la expresión en notación postfix
        return self.postfix_expression







