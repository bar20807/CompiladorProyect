"""
    José Rodrigo Barrera García
    Universidad del Valle de Guatemala
    Diseño de Lenguajes
    20807
    Laboratorio A 
"""


class RegexErrorChecker(object):
    def __init__(self, expression, alphabet):
        self.error_logs = []
        self.binary = '.|'
        self.unary = '?*+'
        self.expression = expression
        self.alphabet = alphabet
        self.check_parenthesis()
        self.check_sequence_operators()
        self.check_ends_expression()

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

    """
        Función que se encarga de retornar el tamaño de la lista de errores.
    
    """
    def get_size(self):
        return len(self.error_logs)
    
    def get_error_logs(self):
        return self.error_logs
    
    """
        Función que se encarga de generar un string con todos los errores que se han encontrado en la expresión regular.
        
    """
    def get_error_result(self):
        # Se verifica si no hay errores, en cuyo caso se retorna una cadena indicando que la expresión es válida.
        if not self.error_logs:
            return "La expresión es válida."
        else:
            # En caso contrario, se obtiene la cantidad de errores.
            error_count = len(self.error_logs)
            # Si solo hay un error, se retorna una cadena con el error encontrado.
            if error_count == 1:
                return f"Se encontró un error en la expresión:\n{self.error_logs[0]}"
            else:
                # En caso contrario, se construye una lista de errores enumerados.
                error_list = ''.join(f'{i+1}. {error}\n' for i, error in enumerate(self.error_logs))
                # Se retorna una cadena indicando la cantidad de errores encontrados y la lista de errores.
                return f"Se encontraron {error_count} errores en la expresión:\n{error_list}"

