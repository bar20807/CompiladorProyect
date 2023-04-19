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
        self.rule_tokens_line = ''    
        
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
        rule_tokens_index = 0
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
                #print("Diccionario resultante: ", self.values_dict)
            #Ahora miramos donde se encuentran las rule tokens
            split = values.split(" ")
            if "rule" in split and "tokens" in split:
                rule_tokens_index = self.read_yal_file_().index(values)
        #print("Diccionario resultante: ", self.values_dict)
        #print("Índice de rule tokens: ", self.rule_tokens_index)
        return rule_tokens_index
    
    def detect_rule_tokens_expression(self):
        # Obtenemos la línea donde se encuentran las rule tokens
        self.rule_tokens_line = self.read_yal_file_()[self.detect_regular_definitions()+1:]
        #Rule tokens_list
        self.rules_tokens_list = []
        # Primero se guardará el primer valor de nuestra rule token
        for rule in self.rule_tokens_line:
            if "|" in rule:
                # Verificar si hay un valor antes del or
                if "|" in rule.split("|")[0]:
                    first_value = rule.split("|")[0].split("|")[0].split("{")[0].strip()
                    self.rules_tokens_list.append(first_value)
                second_value = rule.split("|")[1].split("{")[0].strip()
                self.rules_tokens_list.append(second_value)
            else:
                first_value= rule.split("{")[0].split("{")[0].strip()
                self.rules_tokens_list.append(first_value)
        print("Lista de rule tokens: ", self.rules_tokens_list)
        return self.rules_tokens_list

    # Función que se encargará de armar la expresión regular
    def build_regular_expression(self):
        #Variable que almacenará la expresión regular resultante
        self.regular_expression_result = ""
        # Primero, se obtiene la lista de rule tokens
        rule_tokens= self.detect_rule_tokens_expression()
        # Lista temporal para almacenar los valores resultantes de las expresiones regulares especiales
        special_regular_expressions = []
        # Primero recorremos el diccionario de las definiciones regulares
        for def_regular in self.values_dict:
            expression = self.values_dict[def_regular]
            print("Expresión a analizar: ", expression)
            new_special_regex = self.find_special_regex(expression)
            if new_special_regex:
                special_regular_expressions.extend(new_special_regex)
            # Leemos nuestra lista de expresiones regulares especiales
            for special_regex in special_regular_expressions:
                print("Expresión regular especial: ", special_regex)
                new_expression_result = self.convert_special_regex(special_regex)
                self.values_dict[def_regular] = self.values_dict[def_regular].replace(special_regex, new_expression_result)
            self.values_dict[def_regular] = self.values_dict[def_regular].replace("[", "(").replace("]", ")")
        print("Nuevos valores del diccionario: ", self.values_dict)
        #print("Rule Tokens: ", rule_tokens)
        #Con los valores que ya tenemos construimos nuestra expresión regular
        for rule in rule_tokens:
            print("Este es el rule_token_tomado: ", rule)
            self.regular_expression_result += rule
            self.regular_expression_result += "|"
            print("Valores de la expresión: ", self.regular_expression_result)
        #Eliminamos el or innecesario
        if self.regular_expression_result[-1] == "|":
            self.regular_expression_result = self.regular_expression_result[:-1]
        print("Expresión regular inicial: ", self.regular_expression_result)
        # Inicializamos los valores de los tokens de la clave-valor y del iterador
        key_token_value = ""
        itera = 0
        while itera < (len(self.regular_expression_result)):
            # Obtenemos el carácter actual de la expresión regular
            char = self.regular_expression_result[itera]
            # Si el carácter actual no es un operador de expresión regular, lo agregamos al token clave-valor actual
            if char not in "+|*?()\'":
                key_token_value += char
                itera += 1
            else:
                # Si es un operador de expresión regular, verificamos si el token clave-valor actual es una clave en el diccionario
                if key_token_value in self.values_dict:
                     # Si la clave existe en el diccionario, reemplazamos el token clave-valor actual con su valor correspondiente
                    regex = self.values_dict[key_token_value]
                    word_len = len(key_token_value)
                     # Guardamos los índices donde debemos cortar la expresión regular
                    der = itera
                    izq = itera - word_len
                    # Hacemos el corte y agregamos la regex correspondiente
                    self.regular_expression_result = self.regular_expression_result[:izq] + regex + self.regular_expression_result[der:]
                    # Reiniciamos los valores de los tokens y el iterador
                    itera = -1 # Colocamos -1 en vez de 0, ya que se le suma 1 en la siguiente línea y de esta forma iniciaría en 0
                    key_token_value = "" 
                else:
                    # Si la clave no existe en el diccionario, simplemente reiniciamos el valor del token clave-valor actual
                    key_token_value = ""
                     # Incrementamos el iterador en cada iteración
                    itera += 1
        return self.regular_expression_result
        

    #Función que convierte las expresiones regulares especiales a regex
    def convert_special_regex(self, special_regex):
        converted_regex = ""
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
            #print("Expresion especial: ", exp)
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
            #print("Nueva expresión con los ors agregados: ", converted_regex[:-1])
            return converted_regex[:-1]
        elif "\'" in special_regex:
            # Se crea una lista vacía llamada 'chars'
            chars = []
            # Se inicializa un iterador en cero
            iterador = 0
            # Se recorre la cadena 'special_regex' mientras el iterador sea menor que la longitud de 'special_regex'
            while iterador < len(special_regex):
                # Si el carácter actual es una comilla simple
                if special_regex[iterador] == "'":
                    # Se incrementa el iterador para evitar la comilla simple inicial
                    iterador += 1
                    # Se crea una variable 'char' con una comilla simple inicial
                    char = "'"
                    # Se recorre la cadena 'special_regex' mientras el iterador sea menor que la longitud de 'special_regex'
                    # y el carácter actual no sea una comilla simple
                    while iterador < len(special_regex) and special_regex[iterador] != "'":
                        # Se agrega el carácter actual a la variable 'char'
                        char += special_regex[iterador]
                        # Se incrementa el iterador
                        iterador += 1
                    # Se agrega una comilla simple final a la variable 'char'
                    char += "'"
                    # Se agrega la variable 'char' a la lista 'chars'
                    chars.append(char)
                # Se incrementa el iterador
                iterador += 1
            # Se imprime la lista de caracteres encontrados
            print("Lista de caracteres: ", chars)
            # Se copia la cadena 'special_regex' en la variable 'position'
            position = special_regex
            # Se recorre cada caracter en la lista 'chars'
            for char in chars:
                # Se reemplaza cada ocurrencia del caracter actual en la cadena 'position' con una cadena vacía
                position = position.replace(char, "")
            # Si 'position' no es una cadena vacía
            if len(position) > 0:
                # Se recorre cada carácter restante en 'position'
                for char_p in position:
                    # Se extrae el último caracter de la lista 'chars' y se guarda en la variable 'der'
                    der = chars.pop()
                    # Se extrae el último caracter de la lista 'chars' y se guarda en la variable 'izq'
                    izq = chars.pop()
                    # Se obtiene el código ASCII del primer caracter en la cadena 'izq'
                    left_char = ord(izq[1])
                    # Se obtiene el código ASCII del primer caracter en la cadena 'der'
                    right_char = ord(der[1])
                    # Se genera una lista de códigos ASCII que va desde 'left_char' hasta 'right_char'
                    ascii_list = range(left_char, right_char + 1)
                    # Se convierte cada código ASCII en su carácter correspondiente y se agrega a la cadena de expresión regular convertida
                    for ascii_ in ascii_list:
                        new_char = chr(ascii_)
                        converted_regex += new_char
                        converted_regex += "|"
            else:
                # Se recorre cada carácter en la lista 'chars'
                for char in chars:
                    # Si el carácter actual contiene una barra invertida ('\')
                    if '\\' in char:
                        # Se remueve la comilla simple
                        char_n = char.replace("'", "")
                        # Se agrega el carácter modificado a la cadena de expresión regular convertida
                        converted_regex += char_n
                    else:
                        # Se agrega el carácter actual a la cadena de expresión regular convertida
                        converted_regex += char
                    # Se agrega un '|' después de cada carácter procesado
                    converted_regex += '|'
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
        #Imprimimos el resultado
        print("Special regular expressions found: ", special_regular_expressions)
        return special_regular_expressions if special_regular_expressions else None    

    