"""
    José Rodrigo Barrera García
    Universidad del Valle de Guatemala
    Diseño de Lenguajes
    20807
    Laboratorio D
"""

from RegextoTree import *
from YalexReader import *
from AFD import *

#Nuevo main limpio
regex = YALexGenerator("./Archivos Yal/yalp_analyzer.yal")
tree  = RegextoTree(regex.regular_expression_result)
tree.buildTree()
tree.print_tree("TestNewYalex")

afd = AFD_construction()
afd.afd_direct_(regex.regular_expression_result)
afd.build_scanner("./Archivos Yal/yalp_analyzer.yal", "scannerYal_Yalp")
afd.output_image("YalexTestAFD")
afd.simulate_afd("./Archivos Yal/yalp_analyzer.yal")

