"""
    José Rodrigo Barrera García
    Universidad del Valle de Guatemala
    Diseño de Lenguajes
    20807
    Laboratorio E
"""

from RegextoTree import *
from YalexReader import *
from AFD import *
from YalpReader import *

#Main que utilicé para el laboratorio E
regex = YALexGenerator("./Archivos Yal/yalp_analyzer.yal")
tree  = RegextoTree(regex.regular_expression_result)
tree.buildTree()
tree.print_tree("Test")

afd = AFD_construction()
afd.afd_direct_(regex.regular_expression_result)
afd.build_scanner("./Archivos Yal/yalp_analyzer.yal", "ScannerYal1")
afd.output_image("YalexTestAFD")
afd.simulate_afd("./Archivos Yalp/slr-1.yalp")

#print("Lista resultante: ", afd.token_list_file)

yalp_reader = YalpGenerator("./simulation_result.txt", "./Archivos Yal/yalp_analyzer.yal")
yalp_reader.detect_productions_file()





"""#Main a utilizar para el laboratorio E
yalp_lecture = YalpGenerator("./Archivos Yalp/slr-1.yalp")
#print(yalp_lecture.read_file())"""

