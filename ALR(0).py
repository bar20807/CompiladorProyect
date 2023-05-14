"""
    Clase que se encargará de la construcción del autómata LR(0)
"""

from YalpReader import *
from FA import *

class ALR0 (FA):
    def __init__(self, regex=None, productions = None):
        super().__init__(regex)
        #Acá vamos a recibir nuestra lista de producciones
        self.productions = productions
    