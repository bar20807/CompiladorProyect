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
        if operator is '(':
            return 1
        if operator is '*+?':
            return 4
        if operator is '.':
            return 3
        if operator is '|':
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







