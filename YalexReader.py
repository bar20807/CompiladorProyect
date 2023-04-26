class YALexGenerator(object):
    def __init__(self, path_file):
        self.path_file = path_file
        self.dict_value = {}
        self.let_values = []
    
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
        if valor[0] == '[':
            #print("Detecte la llave, y este es el valor: " + valor)
            self.let_values.append('(')
            #Si detectamos que es un charset, entonces debemos de analizar los valores que se encuentran dentro de los corchetes
            #Para ello debemos de analizar el hecho de que se encuentren en comillas simples o dobles
            if valor[1] == "'":
                #Printeamos lo que se obtiene al momento de leer esta línea
                #print("Detecte que es un charset con comillas simples", valor[1])
                #Como lo está, tomaremos en cuenta, cuantos guiones hay entre cada expresion
                guion = valor.count('-')
                #print("Cantidad de guiones: ", guion)

yalex_test = YALexGenerator("./Archivos Yal/slr-1.yal")
yalex_test.detect_special_lines()

    
    
        