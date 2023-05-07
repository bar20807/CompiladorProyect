"""
    Este archivo será una clase lectora de archivos .yalp
"""

class YalpGenerator(object):
    def __init__(self, path_file):
        self.path_file = path_file

    #Función encargada de leer los archivos .yalp
    def read_file(self):
        file = open(self.path_file, "r")
        file_lines = file.readlines()
        file.close()
        return file_lines
    