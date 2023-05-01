class YALexGenerator(object):
    def __init__(self, path_file):
        self.path_file = path_file
        self.dict_value = {}
        #Lista que almacenará la expresión regular final
        self.regular_expression_result = list()
        #Diccionario que almacenará todas las rule tokens detectadas
        self.tokens_rule_list = {}
        #Variable de iteración que sirve para detectar si es un token o no
        self.is_token = False
        #Llamaremos de una vez a la función para construir la expresión regular,
        #de esa manera podremos llamar directamente a la variable regular expression result
        self.build_regular_expression_()
        
    
    #Función que se encarga de leer el archivo yalex
    def read_yal_file_(self):
        file = open(self.path_file, "r")
        self.file_list = file.readlines()
        file.close()
        return self.file_list


    #Función donde analizaremos línea por línea del archivo
    def build_regular_expression_(self):
        #Lista que almacenara temporalmente la nueva regex
        regular_expression_result_temp = list()
        #Recorremos las líneas recibidas del archivo.
        for line in self.read_yal_file_():
            #print(line)
            #Una vez leemos la línea haremos la separación entre lo que vendría siendo el nombre de la variable let, lo que vendría siendo el lado izquierdo
            #y tomaríamos el valor del lado derecho de nuestra expresión
            if line.startswith("let") or line.startswith("Let"):
                #Una vez habiendo hecho eso, lo que haremos será tomar el nombre de la variable y su valor
                #Para ello, haremos un split de la línea, donde el primer elemento será el nombre de la variable y el segundo elemento será el valor
                #de la variable
                equal_line = line.split("=")
                nombre = equal_line[0].strip().split()[1]
                valor = equal_line[1].strip()
                #print("valor del nombre: ", nombre)
                self.values_detect_(nombre, valor)
            #Ahora mandamos a llamar a nuestra función encargada de identificar los rule tokens de nuestro yalex
            elif line.startswith("rule") or line.startswith("Rule"):
                self.is_token = True
            elif (self.is_token):
                #print("Rule tokens: ", line)
                #Llamamos a la función encargada de detectar las rule tokens
                self.detect_rule_tokens(line)
                
    #Función que se encargará de analizar todos los valores encontrados
    def values_detect_(self, nombre, valor):
        #Primero, para analizar dichos valores, debemos de plantearnos si comienzan con [] o no, ya que esto determinará si es un charset o no
        #Si comienza con [], entonces es un charset, por lo que debemos de analizar los valores que se encuentran dentro de los corchetes
        self.let_values = []   
        if valor.startswith('['):
            #print("Detecte la llave, y este es el valor: " + valor)
            self.let_values.append('(')
            #Si detectamos que es un charset, entonces debemos de analizar los valores que se encuentran dentro de los corchetes
            #Para ello debemos de analizar el hecho de que se encuentren en comillas simples o dobles
            if valor[1].startswith("'"):
                #Printeamos lo que se obtiene al momento de leer esta línea
                #print("Detecte que es un charset con comillas simples", valor[1])
                #Como lo está, tomaremos en cuenta, cuantos guiones hay entre cada expresion, es decir, contaremos la cantidad de expresiones que tiene un guión
                guion = valor.count('-')
                #print("Cantidad de guiones: ", guion)
                #Una vez habiendo obtenido la cantidad de expresiones que poseen al menos 1 guion, debemos de comprobar que este sea diferente de 0, esto para evitar todas
                #Aquellas cadenas que lo sean. 
                if(guion != 0):
                    #Ya habiendo comprobado que si se encontró al menos un guión en nuestro charset, procederemos a sacar el primer valor encontrado después de tomar la 
                    #primera comilla simple, entonces, procederemos a sacar el segundo valor haciendo un proceso simlar.
                    # Se crea un ciclo while para iterar con respecto a la cantidad de ciclos de caracteres
                    iterador = 1
                    #Variables para guardar los caracteres iniciales y finales de un rango de caracteres en el charset
                    primer_char = ""
                    segundo_char = ""
                    comilla_simple1 = 0
                    comilla_simple2 = 0
                    """
                    iterador, primer_char, segundo_char, comilla_simple1, y comilla_simple2 son variables que se inicializan para su posterior uso en el ciclo while. 
                    iterador se inicializa en 1, porque el primer caracter a analizar es el segundo caracter del charset (el primer caracter es el corchete de apertura).
                    """
                    """
                     Es el inicio del ciclo while, que se ejecuta mientras el contador de guiones sea diferente de 0. 
                     El ciclo se usa para iterar sobre los caracteres dentro del charset y extraer los valores que conforman el charset.
                    """
                    while(guion != 0):
                        # Si se encuentra una comilla simple y no se ha detectado la primera comilla simple del rango actual
                        if(valor[iterador] == "'" and not comilla_simple1):
                            comilla_simple1 = iterador
                        # Si se encuentra una comilla simple y ya se había detectado la primera comilla simple del rango actual
                        elif(valor[iterador] == "'" and comilla_simple1):
                            comilla_simple2 = iterador

                        # Si se han detectado ambas comillas simples que delimitan el rango actual y aún no se ha procesado el primer caracter
                        if(comilla_simple1 and comilla_simple2 and primer_char == ""):
                            primer_char = valor[comilla_simple1 + 1]
                            comilla_simple1 = 0
                            comilla_simple2 = 0
                        # Si se han detectado ambas comillas simples que delimitan el rango actual y ya se ha procesado el primer caracter
                        elif(comilla_simple1 and comilla_simple2 and primer_char != ""):
                            segundo_char = valor[comilla_simple1 + 1]
                            comilla_simple1 = 0
                            comilla_simple2 = 0
                            # Se ha procesado un rango de caracteres, por lo que se disminuye en 1 el número de guiones sin procesar
                            guion -= 1  
                        # Si ya se tienen los dos caracteres que delimitan el rango actual
                        if(primer_char != "" and segundo_char != ""):
                            # Se convierten los caracteres a su valor ASCII
                            char_to_ascii1 = ord(primer_char)
                            char_to_ascii2 = ord(segundo_char)
                            # Se resetean las variables para el siguiente rango de caracteres
                            primer_char = ""
                            segundo_char = ""
                            #print("Lista de valores: ", self.let_values)
                            # Si ya hay al menos 2 valores en la lista de valores, se agrega un separador de OR '|'
                            if(len(self.let_values) > 2):
                                self.let_values.append('|')
                            # Se agrega cada valor del rango de caracteres a la lista de valores, separados por un separador de OR '|'
                            for i in range(char_to_ascii1, char_to_ascii2):
                                self.let_values.append(i)
                                self.let_values.append('|')
                            # Se agrega el último valor del rango sin separador de OR
                            self.let_values.append(char_to_ascii2) 
                        # Se avanza al siguiente caracter del charset para buscar el siguiente rango de caracteres    
                        iterador += 1
                #Si no se encontró ningún guión, entonces se procederá a analizar los valores que se encuentran dentro de los corchetes
                else:
                    #print("Valor del charset: ", valor)
                    #En este caso se analizarán todos los valores que no contengan guion, es decir, son todos aquellos valores como [' ''\t''\n'] los cuales deberán 
                    #Ser analizados para poder obtener su ASCII y así manejar mejor el tipo de char
                    # Se crea un ciclo while para iterar con respecto a la cantidad de ciclos de caracteres
                    iterador = 1
                    #Variables para guardar los caracteres iniciales y finales de un rango de caracteres en el charset
                    primer_char = ""
                    segundo_char = ""
                    comilla_simple1 = 0
                    comilla_simple2 = 0
                    """
                    iterador, primer_char, segundo_char, comilla_simple1, y comilla_simple2 son variables que se inicializan para su posterior uso en el ciclo while. 
                    iterador se inicializa en 1, porque el primer caracter a analizar es el segundo caracter del charset (el primer caracter es el corchete de apertura).
                    """
                    while iterador < len(valor) and valor[iterador] != ']':
                        # Se verifica si el carácter actual es una comilla simple y si no se ha encontrado ya una comilla simple previamente
                        if valor[iterador] == "'" and not comilla_simple1:
                            comilla_simple1 = iterador
                        # Si ya se encontró una comilla simple previamente, se establece el valor del índice de la segunda comilla simple
                        elif valor[iterador] == "'" and comilla_simple1:
                            comilla_simple2 = iterador
                            caracteres = []
                            # Se itera sobre los caracteres entre las comillas simples y se agregan a una lista 'caracteres'
                            for i in range(comilla_simple1 + 1, comilla_simple2):
                                caracteres.append(valor[i])
                            # Se une los caracteres en un string 'primer_char'
                            primer_char = ''.join(caracteres)
                            # Se restablecen los valores de 'comilla_simple1' y 'comilla_simple2'
                            comilla_simple1 = 0
                            comilla_simple2 = 0
                            # Si 'primer_char' contiene un espacio en blanco, se reemplaza por el valor entero del espacio en blanco
                            if primer_char.isspace():
                                primer_char = ord(primer_char)
                            # Si 'primer_char' comienza con una barra invertida, se elimina la barra y se reemplaza por el valor correspondiente
                            # (newline = \n, tab = \t)
                            elif (primer_char.startswith("\\")):
                                primer_char = primer_char.replace("\\", '')
                                if(primer_char == "n"):
                                    primer_char = ord("\n")
                                elif(primer_char == "t"):
                                    primer_char = ord("\t")
                            # Se imprime el mensaje "Nuevos valores encontrados: " seguido de la lista de valores actuales en 'let_values'
                            #print("Nuevos valores encontrados: ", self.let_values)
                            # Se agrega el valor de 'primer_char' a la lista 'let_values'
                            self.let_values.append(primer_char)
                            
                            # Si el siguiente carácter no es ']', se agrega un '|' a 'let_values' para separar los valores
                            if iterador + 1 != len(valor) and valor[iterador + 1] != ']':
                                self.let_values.append("|")
                        # Se incrementa el valor de 'iterador' en 1
                        iterador += 1
            #Ahora analizaremos los valores que se encuentren denntro de comillas dobles, para ello deberemos de evaluar la segunda posición de nuestro valor
            #El cual se obtiene de la partición de nuestra declaración Let
            elif valor[1].startswith('"'):
                #print("Este es el valor encontrado: ", valor)
                # Variable para saber si se está escapando un carácter
                escaped_char = False
                #Itera sobre el string, comenzando desde el tercer caracter
                for char in valor[2:]:
                    #Si se encuentra una comilla y no se está escapando un carácter
                    if char == '"' and not escaped_char:
                        #Termina el loop
                        break
                    # Si se encuentra una diagonal invertida 
                    elif char == "\\":
                        # Se está escapando un carácter 
                        escaped_char = True
                    # Si no se está escapando un carácter 
                    else:
                        # Si el caracter anterior era una diagonal invertida 
                        if escaped_char:
                            # Agrega el caracter escapado a let_values
                            self.let_values.append(valor[valor.index(char)-1:valor.index(char)+1])
                            # Reinicia escaped_char 
                            escaped_char = False
                        #Si el caracter anterior no era una diagonal invertida
                        else:
                            # Agrega el valor ASCII del caracter a let_values
                            self.let_values.append(ord(char))
                        # Si el siguiente caracter no es una comilla 
                        if valor[valor.index(char)+1] != '"':
                            # Agrega un separador (OR) de valores a let_values 
                            self.let_values.append('|') 
            self.let_values.append(')')
            self.dict_value[nombre] = self.let_values
            #print("Diccionario de valores: ", self.dict_value)
        
        #Ahora revisaremos todos los valores que no comienzan con [, eso quiere decir que el valor no es un charset
        else:
            #print("Qué valores detectamos acá__: ", valor)
            # Creamos una lista vacía para guardar los valores que se van a procesar
            lista_valores = []
            # Inicializamos una variable temporal para concatenar caracteres
            temporal = ''
            # Indicamos si se encuentra dentro de comillas
            comillas = False
            # Iteramos sobre cada caracter en la cadena de entrada
            for c in valor:
                # Si se encuentra dentro de comillas
                if comillas:
                    # Si el caracter actual es una comilla de cierre
                    if c == "'":
                        # Si la variable temporal tiene algún valor
                        if temporal:
                            # Agregamos el valor a la lista
                            lista_valores.append(temporal)
                            # Reiniciamos la variable temporal
                            temporal = ''
                        # Indicamos que ya no estamos dentro de comillas
                        comillas = False
                    else:
                        # Si el caracter actual no es una comilla de cierre, agregamos su valor ASCII a la lista
                        lista_valores.append(ord(c))
                # Si no se encuentra dentro de comillas
                else:
                    # Si el caracter actual es una comilla de apertura
                    if c == "'":
                        # Indicamos que ahora estamos dentro de comillas
                        comillas = True
                        # Si la variable temporal tiene algún valor, lo agregamos a la lista
                        if temporal:
                            lista_valores.append(temporal)
                            temporal = ''
                    # Si el caracter actual no es una comilla ni un carácter especial, lo agregamos a la variable temporal
                    elif c not in ".|*+?()":
                        temporal += c
                    # Si el caracter actual es un carácter especial
                    else:
                        # Si la variable temporal tiene algún valor, lo agregamos a la lista
                        if temporal:
                            lista_valores.append(temporal)
                            temporal = ''
                        # Agregamos el carácter especial a la lista
                        lista_valores.append(c)
            # Iteramos sobre los valores en la lista
            for i, valor in enumerate(lista_valores):
                # Si el valor se encuentra en el diccionario de valores, reemplazamos el valor en la lista por el valor del diccionario
                if valor in self.dict_value:
                    lista_valores[i:i+1] = self.dict_value[valor]
                    #print("Valores agregados: ", lista_valores)
            #Revisamos si existen charsets
            charsets_count = lista_valores.count("[")
            #print("Contador de cuantas existencias charsets hay: ", charsets_count)
            #Iteramos por cada charset existente de nuestro contador
            while(charsets_count != 0):
                # Se toma los indices de cada charset
                indice_inicial = lista_valores.index("[")
                #print("Indice inicial: ", indice_inicial)
                indice_final = lista_valores.index("]")
                #print("Indice final: ", indice_final)
                #Se insertan los símbolos de or entre cada valor de charset
                for i in range((indice_inicial + 1), (indice_final-1)):
                    lista_valores[(i + 1):(i + 1)] = '|'
                    #print("Lista de valores: ", lista_valores)
                charsets_count-=1
                #Ahora cambiaremos los valores que contengan [] a ()
                lista_valores[indice_inicial] = "("
                indice_final = lista_valores.index("]")
                lista_valores[indice_final] = ")"
            #Agregamos un último paréntesis para el valor de la definición
            lista_valores[0:0] = '('
            lista_valores[len(lista_valores):len(lista_valores)] = ')'
            #Se procede a guardar el valor con su nombre correspondiente en el diccionario de valores
            self.dict_value[nombre] = lista_valores
            #print("Nuevos valores del diccionario: ", self.dict_value)
    
    #Función encargada de detectar la línea en donde se encuentran las rule tokens
    def detect_rule_tokens(self, linea):
        #Variable que utilizaremos para saber en el token actual que nos estamos posicionando
        token_actual = ""
        # Verificamos si la línea que estamos leyendo encuentra un |, si lo encuentra, lo agregamos a nuestra lista final de la regex
        if '|' in linea:
            self.regular_expression_result.append('|')
        # Ahora revisamos si dicho valor posee comillas simples
        if "'" in linea:
            # Tomaremos la segunda comilla simple, y tomaremos el valor que se encuentra dentro de ellas, 
            # Para después poder obtener su valor en ASCII
            value_between_quotes = linea[linea.index("'")+1: linea.rindex("'")]
            value_ascii = [ord(v) for v in value_between_quotes]
            self.regular_expression_result.extend(value_ascii)
            self.regular_expression_result.append(f"#{value_between_quotes}")
            token_actual = f"#{value_between_quotes}"
        # Ahora revisaremos si el valor que se está analizando se encuentra dentro de dos comillas dobles
        elif '"' in linea:
            # Posterior a ello, vamos iterar sobre la línea en búsqueda de la primera comilla doble que se encuentre
            value_between_quotes = linea[linea.index('"')+1: linea.rindex('"')]
            value_ascii = [ord(v) for v in value_between_quotes]
            self.regular_expression_result.extend(value_ascii)
            self.regular_expression_result.append(f"#{value_between_quotes}")
            token_actual = f"#{value_between_quotes}"
        # Si el valor no se encuentra entre comillas, se procede a buscar el valor en el diccionario de valores
        else:
            # Iteramos sobre nuestra lista que contiene las llaves del diccionario
            for i in self.dict_value.keys():
                # Verificamos si dicho nombre i extraido de las llaves de nuestro diccionario se encuentra presente en la línea
                if i in linea:
                    self.regular_expression_result.extend(self.dict_value[i])
                    self.regular_expression_result.append(f"#{i}")
                    token_actual = f"#{i}"
                    break
        # Una vez habiendo evaluado cada tipo de expresión que podemos obtener, evaluamos si el token actual no se encuentra vacío
        if token_actual:
            # Para ello, obtendremos el indicie inicial donde se encuentre {
            indice_inicial = linea.index("{")
            # Ahora obtendremos el índice final donde se encuentre }
            indice_final = linea.index("}")
            # Con ello obtendremos el valor que se encuentra en la subcadena entre ambos índices
            subcadena = linea[indice_inicial + 2:indice_final - 1]
            self.tokens_rule_list[token_actual] = subcadena
              
"""yalex_test = YALexGenerator("./Archivos Yal/slr-3.yal")
print(yalex_test.regular_expression_result)
"""
    
    
        