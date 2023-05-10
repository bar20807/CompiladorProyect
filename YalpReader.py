"""
    Este archivo será una clase lectora de archivos .yalp
"""

class YalpGenerator(object):
    def __init__(self, path_file):
        self.path_file = path_file
        #Declaramos un diccionario que servirá para almacenar las gramáticas detectadas
        self.grammars = {}

    #Función encargada de leer los archivos .yalp
    def read_file(self):
        file = open(self.path_file, "r", encoding="utf-8")
        file_lines = file.readlines()
        file.close()
        return file_lines
    
    #Función que detecta las gramáticas que se encuentran en los comentarios de nuestro yalp
    def detect_grammars(self):
        result_line = self.read_file()
        dic_keys = []
        dic_values = []
        for line in result_line:
            #print(line)
            #print("2222")
            #Detectamos si la línea contiene una flecha
            if "→" in line:
                #Hacemos un split del lado derecho de nuestra línea
                right_side = line.split("→")[0].strip().split()[1]
                #print("Este es el valor derecho: ", right_side)
                dic_keys.append(right_side)
                #Ahora tomamos el valor del lado derecho
                left_side = line.split("→")[1].strip()
                #print("Este es el valor del lado derecho: ", left_side)
                #Ahora en el lado derecho, detectamos cuando encuentre un |
                if "|" in left_side:
                    #Hacemos un split del lado derecho de nuestra línea
                    left_side_or = left_side.split("|")
                    #Quitamos todo valor */
                    left_side_or = [x.replace("*/", "") for x in left_side_or]
                    dic_values.append(left_side_or)
                    #print("Este es el valor del lado derecho: ", left_side_or)
                else:
                    dic_values.append(left_side)
                    #print("Este es el valor del lado derecho: ", left_side)
            elif "->" in line:
                #Hacemos un split del lado derecho de nuestra línea
                right_side = line.split("->")[0].strip().split()[1]
                #print("Este es el valor derecho: ", right_side)
                dic_keys.append(right_side)
                #Ahora tomamos el valor del lado derecho
                left_side = line.split("->")[1].strip()
                #print("Este es el valor del lado derecho: ", left_side)
                #Ahora en el lado derecho, detectamos cuando encuentre un |
                if "|" in left_side:
                    #Hacemos un split del lado derecho de nuestra línea
                    left_side_or = left_side.split("|")
                    #Quitamos todo valor */
                    left_side_or = [x.replace("*/", "") for x in left_side_or]
                    dic_values.append(left_side_or)
                    #print("Este es el valor del lado derecho: ", left_side_or)
                else:
                    dic_values.append(left_side)
            elif "=>" in line:
                #Hacemos un split del lado derecho de nuestra línea
                right_side = line.split("=>")[0].strip().split()[1]
                #print("Este es el valor derecho: ", right_side)
                dic_keys.append(right_side)
                #Ahora tomamos el valor del lado derecho
                left_side = line.split("=>")[1].strip()
                #print("Este es el valor del lado derecho: ", left_side)
                #Ahora en el lado derecho, detectamos cuando encuentre un |
                if "|" in left_side:
                    #Hacemos un split del lado derecho de nuestra línea
                    left_side_or = left_side.split("|")
                    #Quitamos todo valor */
                    left_side_or = [x.replace("*/", "") for x in left_side_or]
                    dic_values.append(left_side_or)
                    #print("Este es el valor del lado derecho: ", left_side_or)
                else:
                    dic_values.append(left_side)  
        #print(dic_keys)
        #print(dic_values)
        #Recorremos nuestro array con los valores del diccionario
        """for i in dic_values:
            #print(i)
            for j in i:
                #print(j)
            """
        #Mientras nuestra lista dic_keys no esté vacía
        iterador = 0 
        while iterador != len(dic_keys):
            #Asignamos la llave con respecto a su lista correspondiente a nuestro diccionario grammars
            self.grammars[dic_keys[iterador]] = dic_values[iterador]
            iterador+=1
        #Imprimimos de las gramáticas según como están en el yalp 
        #E → E + T
        #Según la llave del diccionario, sacamos cada uno de los valores se encuentran en la lista
        print("--+-- Gramática SLR --+--")
        for key in self.grammars:
            #print(key)
            for value in self.grammars[key]:
                print(key + " -> " + value)

            
yalp_reader = YalpGenerator("./Archivos Yalp/slr-1.yalp")
yalp_reader.detect_grammars()
        