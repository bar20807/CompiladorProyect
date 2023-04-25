"""
    Clase que será encargada de leer los archivos .yal, 
    y en base a cada uno de los tokens que reconozca, poder armar la 
    expresión regular, y con dicha expresión poder obtener el árbol resultante 
    de dicho tokens.
"""


class YALexGenerator(object):
    # Se inicializan los atributos del archivo
    def __init__(self, filename):
        self.filename = filename
        self.regular_expressions = {}
        self.regex = []
        self.build_regex_expression()

    #Creamos la expresión regular a partir de la lectura del archivo
    def build_regex_expression(self):
        with open(self.filename, "r") as file:  
            tokens = None
            final_regex = []
            #Hacemos la iteración línea por línea del archivo
            for line in file:
                # Verificamos en qué línea se encuentra un let
                if('let' in line):
                    # Se reemplazan los espacios vacios
                    line = line.replace('let ', '')
                    line = line.replace(" ", "")
                    # Se divide entre la definicion y el valor de esta
                    definition, value = line.split('=')
                    # Se crea la lista con la definicion final
                    value_definition = []
                    # Si el primer elemento del valor es una llave significa que es un charset
                    if(value[0] == '['):
                        # Se cambian las llaves por parentesis
                        value_definition.append('(')

                        # Si son comillas simples es que seran por separados o elementos de uno hasta otro
                        if(value[1] == "'"):
                            # Se revisa si se debe de realiza un ciclo con los elementos
                            separator_counter = value.count('-')
                            # Si se debe de realizar un ciclo 
                            if(separator_counter != 0):
                                # Se crea un ciclo while para iterar con respecto a la cantidad de ciclos de caracteres
                                index_counter = 1
                                first_value = ""
                                second_value = ""
                                first_apostrophe = None
                                second_apostrophe = None
                                while(separator_counter != 0):
                                    # Se visualiza que exista una apostrofe y la segunda
                                    # Para conocer que elemento inicia el ciclo
                                    if(value[index_counter] == "'" and not first_apostrophe):
                                        first_apostrophe = index_counter
                                    elif(value[index_counter] == "'" and first_apostrophe):
                                        second_apostrophe = index_counter

                                    # Se toma el primer valor del ciclo
                                    if(first_apostrophe and second_apostrophe and first_value == ""):
                                        first_value = value[first_apostrophe + 1]
                                        first_apostrophe = None
                                        second_apostrophe = None
                                    # Se toma el segundo valor del ciclo
                                    elif(first_apostrophe and second_apostrophe and first_value != ""):
                                        second_value = value[first_apostrophe + 1]
                                        first_apostrophe = None
                                        second_apostrophe = None
                                        separator_counter -= 1
                                    # Se convierten los valores en ascii y se realiza el ciclo
                                    if(first_value != "" and second_value != ""):
                                        first_ascii = ord(first_value)
                                        second_ascii = ord(second_value)
                                        first_value = ""
                                        second_value = ""
                                        # Se guardan los valores en la lista del valor de la definicion
                                        # Se toma en cuenta que se deben de guardar como un elemento or otro elemento
                                        if(len(value_definition) > 2):
                                            value_definition.append('|')
                                        for i in range(first_ascii, second_ascii):
                                            value_definition.append(i)
                                            value_definition.append('|')
                                        value_definition.append(second_ascii)
                                    # Se itera en todos los elementos
                                    index_counter += 1
                            # Si no se realizan ciclos de caracteres
                            else:
                                # Se itera sobre el valor
                                index_counter = 1
                                first_value = ""
                                first_apostrophe = None
                                second_apostrophe = None

                                while(value[index_counter] != ']'):
                                    # Se buscan las apostrofes
                                    if(value[index_counter] == "'" and not first_apostrophe):
                                        first_apostrophe = index_counter
                                    elif(value[index_counter] == "'" and first_apostrophe):
                                        second_apostrophe = index_counter
                                    # Se encuentra el valor dentro de las apostrofes y se guarda como tal
                                    if(first_apostrophe and second_apostrophe):
                                        first_value = value[(first_apostrophe + 1):second_apostrophe]
                                        first_apostrophe = None
                                        second_apostrophe = None
                                        if(first_value == ''):
                                            first_value = ' '
                                        value_definition.append(first_value)
                                    # Se itera en todos los valores
                                    index_counter += 1
                        # Si el charset se define entre comillas dobles, por lo tanto son valores uno despues de otro
                        elif(value[1] == '"'):
                            # Se itera entre cada valor despues de las comillas
                            index_counter = 2
                            while(value[index_counter] != '"'):
                                # Se revisa si son valores como \n
                                # Se hace una forma distinta con el contador
                                if(value[index_counter] == "\\"):
                                    value_definition.append(value[index_counter:(index_counter + 2)])
                                    index_counter += 2
                                # En otro caso se itera de manera normal y el valor se convierte en ascii
                                else:
                                    ascii_value = ord(value[index_counter])
                                    value_definition.append(ascii_value)
                                    index_counter += 1
                                # Si el siguiente valor no es el fin del charset se agrega el or para los valores
                                if(value[index_counter] != '"'):
                                    value_definition.append('|')
                                
                        # Para la definicion nueva se agrega con el parentesis de cierre al final
                        value_definition.append(')') 
                        # Se guarda la definicion con el valor final de esta
                        self.regular_expressions[definition] = value_definition 
                    # Si no es un charset se revisa
                    else:
                        # Se revisa si tiene charsets o caracteres entre el valor
                        first_apostrophe = None
                        value_list = []
                        new_string = ""
                        # Se itera entre cada caracter del valor y se guarda en una lista
                        for i in range(len(value) - 1):
                            # Si el caracter no es un operador y no esta entre comillas se guarda en el string que se realiza
                            if(value[i] not in ".|*+?()" and value[i] != "'" and not first_apostrophe):
                                new_string += value[i]
                            # Si el caracter es una primera comilla el valor del string anterior se guarda en la lista
                            # Se guarda donde inicia la comilla
                            elif(value[i] == "'" and not first_apostrophe):
                                first_apostrophe = i
                                if(new_string != ""):
                                    value_list.append(new_string)
                                    new_string = ""
                            # Si el valor es una comilla y existe la primera
                            # Se guarda el valor que esta dentro de las comillas como un ascii
                            elif(value[i] == "'" and first_apostrophe):
                                apostrophes_value = value[(first_apostrophe + 1):i]
                                value_ascii = ord(apostrophes_value)
                                value_list.append(value_ascii)
                                first_apostrophe = None
                            # En cualquier otro caso se guarda el valor dentro del nuevo string
                            else:
                                if(new_string != ""):
                                    value_list.append(new_string)
                                    new_string = ""
                                if(not first_apostrophe):
                                    value_list.append(value[i])
                        # Se tienen el diccionario con las definiciones
                        dictionary_keys = list(self.regular_expressions.keys())
                        # Se itera entre las definiciones para ver si existen en el valor
                        for i in dictionary_keys:
                            # Si se encuentra un definicion en la lista, se cambia por el valor que se definio antes
                            if(i in value_list):
                                # Se revisa la cantidad de iteraciones de la definicion en el valor y se cambia la cantidad de veces
                                # que este aparezca en el valor de definicion actual
                                element_counter = value_list.count(i)
                                while(element_counter != 0):
                                    index = value_list.index(i)
                                    # Se ingresan los valores en vez de la definicion que se tenia
                                    value_list[index:(index + 1)] = self.regular_expressions[i]
                                    element_counter -= 1
                        # Se revisa si existen charsets
                        bracket_counter = value_list.count("[")
                        # Por cada charset se itera
                        while(bracket_counter != 0):
                            # Se toma los indices de cada charset
                            initial_bracket = value_list.index("[")
                            final_bracket = value_list.index("]")
                            # Se insertan los simbolos de or entre cada valor del charset
                            for i in range((initial_bracket + 1), (final_bracket - 1)):
                                value_list[(i + 1):(i + 1)] = '|'
                            # Y se disminuye dependiendo cuantas instancias existan
                            bracket_counter -= 1
                            # Se cambian los [] por ()
                            value_list[initial_bracket] = '('
                            final_bracket = value_list.index("]")
                            value_list[final_bracket] = ')'
                        # Para el valor final de la definicion se agregan en el primero y ultimo valor un parentesis
                        value_list[0:0] = '('
                        value_list[len(value_list):len(value_list)] = ')'
                        # Se guarda la definicion con su valor en el diccionario
                        self.regular_expressions[definition] = value_list
                # Si se encuentra la linea de rule tokens se pone como verdadera la variables
                elif('rule tokens' in line):
                    tokens = True
                # Si esta verdadera la variable de rule tokens
                elif(tokens):
                    # Se toman las llaves del diccionario
                    dictionary_keys = list(self.regular_expressions.keys())
                    # Si la linea tiene un or se agrega a la expresion final
                    if('|' in line):
                        final_regex.append('|')

                    # Si tiene comillas simples el caracter se revisa
                    if("'" in line):
                        # Se itera en la linea y se buscan los dos apostrofes
                        first_apostrophe = None
                        for i in range(len(line)):
                            # Se toma el primero
                            if(line[i] == "'" and first_apostrophe == None):
                                first_apostrophe = i
                            # Se toma el segundo
                            # Se toma el valor entre los apostrofes y se guarda como ascii
                            elif(line[i] == "'" and first_apostrophe != None):
                                apostrophes_value = line[(first_apostrophe + 1):i]
                                value_ascii = ord(apostrophes_value)
                                final_regex.append(value_ascii)
                                first_apostrophe = None
                    # Si tiene comillas dobles el caracter se revisa
                    elif('"' in line):
                        # Se itera en busqueda de las comillas
                        first_apostrophe = None
                        for i in range(len(line)):
                            # Se busca la primera
                            if(line[i] == '"' and first_apostrophe == None):
                                first_apostrophe = i
                            # Se busca la segunda
                            # Se guarda el valor como tal y se guarda en la expresion
                            elif(line[i] == '"' and first_apostrophe != None):
                                apostrophes_value = line[(first_apostrophe + 1):i]
                                final_regex.append(apostrophes_value)
                                first_apostrophe = None
                    # Si no tiene nada de lo anterior
                    else:
                        # Se itera en el diccionario
                        for i in dictionary_keys:
                            # Si existe una definicion en la linea se agrega a la expresion final
                            if i in line:
                                final_regex[len(final_regex):len(final_regex)] = self.regular_expressions[i]
        # Se guarda la expresion regular final en el atributo de la clase
        self.regex = final_regex
                        
                            
                        
                        
                            
                                    
                                    
                    
                    
                    
    
            
        
        