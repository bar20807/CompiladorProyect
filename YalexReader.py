"""
    Clase que será encargada de leer los archivos .yal, 
    y en base a cada uno de los tokens que reconozca, poder armar la 
    expresión regular, y con dicha expresión poder obtener el árbol resultante 
    de dicho tokens.
"""


class YALexGenerator:
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.values_dict = {}
        self.rules_tokens_list = []
        self.rule_tokens_index = 0
        self.rule_tokens_line = ''
        self.regular_expression_result = ''
        
        
    def read_yal_file_(self):
        # Abrir el archivo para lectura
        with open(self.file_path, 'r') as file:
            # Leer todo el contenido del archivo
            file_content = file.readlines()
            # Eliminar los comentarios
            file_content_without_comments = []
            for line in file_content:
                line_without_comment = line.split("(*")[0].strip()
                if line_without_comment:
                    file_content_without_comments.append(line_without_comment)
            # Devolver el contenido limpio
            return file_content_without_comments
    
    #Función que se encarga de detectar las definiciones regulares con base a la lista del archivo creada
    def detect_regular_definitions(self):
        #Primero, detectamos todas las expresiones que empiezan con let, en donde, las dividiremos en dos partes
        #La primera parte consiste en el nombre que recibe dicha definición (ejemplo: let delim) siendo este el lado izquierdo,
        # y dejando para el lado derecho su valor (ejemplo: [' ''\t''\n'])
        for values in self.read_yal_file_():
            if values.startswith('let') or values.startswith('Let'):
                #Quitamos el signo = de la expresión
                character_split = values.split('=')
                #Obtenemos el nombre que será el valor izquierdo
                left_value_name = character_split[0].strip().split()[1]
                #Obtenemos el valor de la derecha
                right_value_ = character_split[1].strip()
                #Llenamos y establecemos nuestro diccionario con nombre y su valor
                self.values_dict[left_value_name] = right_value_
                #Imprimimos cada uno de los valores obtenidos
                #print("Nombre de nuestra regla: ", left_value_name)
                #print("Valor del nombre: ", right_value_)
                #Imprimimos el diccionario resultante
            #Ahora miramos donde se encuentran las rule tokens
            split = values.split(" ")
            if "rule" in split and "tokens" in split:
                self.rule_tokens_index = self.read_yal_file_().index(values)
        print("Diccionario resultante: ", self.values_dict)
        #print("Índice de rule tokens: ", self.rule_tokens_index)
        return self.rule_tokens_index
    
    def detect_rule_tokens_expression(self):
        # Obtenemos la línea donde se encuentran las rule tokens
        self.rule_tokens_line = self.read_yal_file_()[self.detect_regular_definitions()+1:]
        # Primero se guardará el primer valor de nuestra rule token
        for rule in self.rule_tokens_line:
            if "|" in rule:
                second_value = rule.split("|")[1].split("{")[0].strip()
                #print("Este es el segundo valor: ", second_value)
                self.rules_tokens_list.append(second_value.strip("'"))
            else:
                first_value= rule.split("{")[0].split("{")[0].strip()
                #print("Este es el primer valor: ", first_value)
                self.rules_tokens_list.append(first_value.strip("'"))
        return self.rules_tokens_list

    # Función que se encargará de armar la expresión regular
    def build_regular_expression(self):
        # Primero, se obtiene la lista de rule tokens
        self.detect_rule_tokens_expression()
        # Lista temporal para almacenar los valores resultantes de las expresiones regulares especiales
        special_regular_expressions = []
        # Primero recorremos el diccionario de las definiciones regulares
        for def_regular in self.values_dict:
            expression = self.values_dict[def_regular]
            #print("Expresión a analizar: ", expression)
            new_special_regex = self.find_special_regex(expression)
            #print("Valor de new_special_regex: ", new_special_regex)
            if new_special_regex:
                special_regular_expressions.extend(new_special_regex)
        print("Special regular expressions found: ", special_regular_expressions)
        # Leemos nuestra lista de expresiones regulares especiales
        for special_regex in special_regular_expressions:
            print("Expresión regular especial: ", special_regex)
            new_expression_result = self.convert_special_regex(special_regex)
            print("Nueva expresión con los ors agregados: ", new_expression_result)

    #Función que convierte las expresiones regulares especiales a regex
    def convert_special_regex(self, special_regex):
        converted_regex = ''
        # Se busca el primer caracter '"' en la expresión regular.
        # Esto indica que la expresión regular es una cadena de caracteres
        # y no un conjunto de caracteres.
        if "\"" in special_regex:
            # Se divide la cadena original en subcadenas utilizando '"' como separador.
            substrings = special_regex.split('"')
            # Se toma la subcadena que está después del primer '"' y antes del siguiente '"'.
            exp = substrings[1]
            # Se reemplazan todas las comillas simples por una cadena vacía.
            exp = ''.join(exp.split("'"))
            # Se imprime la expresión especial encontrada.
            print("Expresion especial: ", exp)
            # Inicio del bucle for que recorre cada carácter en la expresión regular
            for char in exp:
                # Si el carácter no es una barra invertida "\"...
                if char != "\\":
                    # Se añade el carácter actual y un "|" al final de la cadena
                    converted_regex += char
                    converted_regex += "|"
                # Si el carácter es una barra invertida "\"...
                else:
                    # Se añade el carácter actual ("\") a la cadena
                    converted_regex += char
            # Se retorna la expresión regular convertida.
            return converted_regex[:-1]
        elif "\'" in special_regex:
            # Si la expresión regular incluye comillas simples, significa que es una lista de caracteres
            # que pueden estar separados por ORs o ser una secuencia de caracteres ASCII
            chars = special_regex.split("\'")[1::2]
            if "-" in special_regex and special_regex == "'A'-'Z''a'-'z'":
                # Si la secuencia de caracteres es 'A'-'Z''a'-'z', construimos la lista de caracteres apropiada
                for ascii_val in range(ord('a'), ord('z')+1):
                    converted_regex += f"{chr(ascii_val)}|"
                for ascii_val in range(ord('A'), ord('Z')+1):
                    converted_regex += f"{chr(ascii_val)}|"
            #Ahora hacemos el caso para los números
            elif "-" in special_regex and special_regex == "'0'-'9'":
                for ascii_val in range(ord('0'), ord('9')+1):
                    converted_regex += f"{chr(ascii_val)}|"
            else:
                # Si no hay guión, entonces son caracteres separados por ORs
                for char in chars:
                    converted_regex += f"'{char}'|"
            return converted_regex[:-1]


    # Función que encuentra las expresiones regulares especiales en una expresión regular
    def find_special_regex(self, expression):
        # Inicializamos una lista vacía para almacenar las expresiones regulares especiales
        special_regular_expressions = []
        # Iteramos sobre los caracteres de la expresión regular
        for i, char in enumerate(expression):
            # Si encontramos un corchete abierto, buscamos el siguiente corchete cerrado
            if char == "[":
                j = i + 1
                while j < len(expression) and expression[j] != "]":
                    j += 1
                
                # Si encontramos un corchete cerrado, agregamos la expresión regular especial a la lista
                if j < len(expression):
                    special_regular_expressions.append(expression[i+1:j])        
        return special_regular_expressions if special_regular_expressions else None
 
    def build_expression_tree(self, content):
        # Implementar construcción del árbol de expresión a partir de la especificación en lenguaje YALex
        pass
    
    def validate_specification(self):
        # Implementar verificación de la especificación en lenguaje YALex para detectar errores sintácticos o semánticos
        pass
    
    def generate_lexer(self):
        # Implementar generación de analizador léxico funcional a partir de la especificación de los tokens
        pass
    
    def get_token_tree(self):
        return self.token_tree

    