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
from ALR0 import *

#Main que utilicé para el laboratorio E
regex = YALexGenerator("./Archivos Yal/yalp_analyzer.yal")
tree  = RegextoTree(regex.regular_expression_result)
tree.buildTree()
tree.print_tree("Test")

afd = AFD_construction()
afd.afd_direct_(regex.regular_expression_result)
afd.build_scanner("./Archivos Yal/yalp_analyzer.yal", "ScannerYal1")
afd.output_image("YalexTestAFD")
afd.simulate_afd("./Archivos Yalp/slr-4.yalp")

#print("Lista resultante: ", afd.token_list_file)

yalp_reader = YalpGenerator("./simulation_result.txt")
yalp_reader.detect_productions_file()
#print(yalp_reader.productions_list)
alr0 = ALR0(productions= yalp_reader.productions_list)
first_sets = alr0.first()
follow_sets = alr0.follow(first_sets)
print("FIRST sets:", first_sets)
print("")
print("FOLLOW sets:", follow_sets)
"""alr0.create_subsets()
alr0.output_image("./ALR0/ALR0_Yalp4")"""

"""#Main a utilizar para el laboratorio E
yalp_lecture = YalpGenerator("./Archivos Yalp/slr-1.yalp")
#print(yalp_lecture.read_file())"""

