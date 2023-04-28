class YALexGenerator(object):
    def __init__(self, path_file):
        self.path_file = path_file
        self.dict_value = {}
    
    #Función que se encarga de leer el archivo yalex
    def read_yal_file_(self):
        file = open(self.path_file, "r")
        self.file_list = file.readlines()
        file.close()
        return self.file_list

    #Función donde analizaremos línea por línea del archivo
    def detect_special_lines(self):
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
                print("valor del nombre: ", nombre)
                self.values_detect_(valor)
                
    #Función que se encargará de analizar todos los valores encontrados
    def values_detect_(self, valor):
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
                #Como lo está, tomaremos en cuenta, cuantos guiones hay entre cada expresion
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
                            print("Lista de valores: ", self.let_values)
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
                    #print("Detecte que es un charset con comillas simples, pero no hay guiones")
                    print("Valor del charset: ", valor)
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
                            print("Nuevos valores encontrados: ", self.let_values)
                            # Se agrega el valor de 'primer_char' a la lista 'let_values'
                            self.let_values.append(primer_char)
                            
                            # Si el siguiente carácter no es ']', se agrega un '|' a 'let_values' para separar los valores
                            if iterador + 1 != len(valor) and valor[iterador + 1] != ']':
                                self.let_values.append("|")
                        # Se incrementa el valor de 'iterador' en 1
                        iterador += 1


                    
                    
                    

                
yalex_test = YALexGenerator("./Archivos Yal/slr-1.yal")
yalex_test.detect_special_lines()

    
    
        