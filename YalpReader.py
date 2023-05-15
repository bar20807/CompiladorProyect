"""
    Este archivo será una clase lectora de archivos .yalp
"""
from YalexReader import *

class YalpGenerator(object):
    def __init__(self, path_file):
        self.path_file = path_file
        #Declaramos un diccionario que servirá para almacenar las gramáticas detectadas
        self.grammars = {}
        #Declaramos la lista donde estarán los tokens
        self.tokens_list = list()
        #Declaramos la lista para las producciones que vamos a realizar
        self.productions_list = list()
        #print(self.productions_list)
        
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
            self.productions_list.append([prev_prod, []])
        else:
            # Eliminar espacios y comillas de la línea y dividirla usando el carácter "#"
            input_line = input_line.replace(" ", "").replace("'", "")
            split_line = input_line.split("#")
            # Tomar el primer elemento de la línea dividida como el nuevo token
            new_token = split_line[0]
            # Agregar el nuevo token a la producción actual en la lista de producciones
            self.productions_list[prod_count][1].append(new_token)
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
                self.productions_list.append([current_production, []])
                is_production = True
            # Si la línea contiene "#;" y no contiene "#mayusword", la producción ha terminado
            elif "#;" in line and not is_production:
                continue
            elif "#;" in line and "#mayusword" not in line:
                is_production = False
            # Si la producción está activa y la línea no contiene "#ws", procesar la línea como parte de la producción actual
            elif is_production and "#ws" not in line:
                prod_counter = self.process_production_line(line, prod_counter, current_production)





        
        
            




    