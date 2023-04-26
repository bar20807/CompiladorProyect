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
            if line.startswith("let") and line.startswith("Let"):
                #Si detectamos que la línea empieza con let, primero verificaremos de que no hayan espacios vacíos, si los hay, serán reemplazados
                #por un espacio en blanco
                line = line.replace('let ', '')
                line = line.replace(" ", "")
                
            

"""yalex_test = YALexGenerator("./Archivos Yal/slr-1.yal")
yalex_test.detect_special_lines()"""
    
    
        