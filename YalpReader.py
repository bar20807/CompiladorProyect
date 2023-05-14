"""
    Este archivo será una clase lectora de archivos .yalp
"""
from YalexReader import *

class YalpGenerator(object):
    def __init__(self, path_file, yal_file):
        self.path_file = path_file
        #Declaramos un diccionario que servirá para almacenar las gramáticas detectadas
        self.grammars = {}
        #Obtenemos nuestra lista de rule tokens que logramos armar del YalexReader
        self.rule_tokens = YALexGenerator(yal_file).tokens_rule_list
        #Declaramos la lista donde estarán los tokens
        self.tokens_list = list()
        #Declaramos la lista para las producciones que vamos a realizar
        self.productions_list = list()
        #print(self.productions_list)
        
        
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

    #Funciones que se encargarán de detectar donde si es minúscula es porque son los no terminales, y si son mayusculas son los terminales.
    def process_token_line(self, input_line):
        # Eliminar espacios y comillas de la línea
        input_line = input_line.replace(" ", "").replace("'", "")
        # Dividir la línea usando el carácter "#"
        split_input_line = input_line.split("#")
        # Tomar el primer elemento de la línea dividida como el nuevo token
        new_token = split_input_line[0]
        # Agregar el nuevo token a la lista de tokens
        self.tokens_list.append(new_token)


    def process_production_line(self, input_line, prod_count, prev_prod):
        # Si la línea contiene "#|", incrementar el contador de producciones y agregar una nueva producción a la lista
        if "#|" in input_line:
            prod_count += 1
            self.productions_list.append([prev_prod, "->"])
        else:
            # Eliminar espacios y comillas de la línea y dividirla usando el carácter "#"
            input_line = input_line.replace(" ", "").replace("'", "")
            split_line = input_line.split("#")
            # Tomar el primer elemento de la línea dividida como el nuevo token
            new_token = split_line[0]
            # Agregar el nuevo token a la producción actual en la lista de producciones
            self.productions_list[prod_count].append(new_token)
        # Devolver el contador de producciones actualizado
        return prod_count

    def detect_productions_file(self):
        # Inicialización de variables
        is_production = False
        current_production = None
        prod_counter = -1
        # Leer todo el archivo y separar las líneas
        with open(self.path_file, "r") as file:
            lines = file.read().splitlines()
        # Procesar cada línea del archivo
        for line in lines:
            # Si la línea contiene "#%token", continuar con la siguiente línea
            if "#%token" in line:
                continue
            # Si la línea contiene "#mayusword" y la producción no ha comenzado, procesar la línea como un token
            if "#mayusword" in line and not is_production:
                self.process_token_line(line)
            # Si la lista de tokens no está vacía y la línea contiene "#production", procesar la línea como una producción
            elif len(self.tokens_list) != 0 and "#production" in line:
                line = line.replace(" ", "").replace("'", "").replace(":", "")
                current_production = line.split("#")[0]
                prod_counter += 1
                self.productions_list.append([current_production, "->"])
                is_production = True
            # Si la línea contiene "#;" y no contiene "#mayusword", la producción ha terminado
            elif "#;" in line and not is_production:
                continue
            elif "#;" in line and "#mayusword" not in line:
                is_production = False
            # Si la producción está activa y la línea no contiene "#ws", procesar la línea como parte de la producción actual
            elif is_production and "#ws" not in line:
                prod_counter = self.process_production_line(line, prod_counter, current_production)



        
        
            




    