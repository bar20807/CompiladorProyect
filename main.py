"""
    José Rodrigo Barrera García
    Universidad del Valle de Guatemala
    Diseño de Lenguajes
    20807
    Laboratorio C 
"""

from Thompson import *
from RegextoTree import RegextoTree
from AFD import AFD_construction
from YalexReader import YALexGenerator
from TreeReading import TreeReading

print('\n¡ADVERTENCIA! Deberá ingresar las expresiones regulares sin "." en la concatenación, el programa los agregará.')

"""

    Expresiones regulares dadas en el pre-laboratorio:
    ●ab∗ab∗
    ●0? (1? )? 0 ∗
    ●(a*|b*)c
    ●(b|b)*abb(a|b)*
    ●(a|b)*a(a|b)(a|b)
    
"""

"""
    Expresiones regulares dadas en el pre-laboratorio b: 
    ● ab ∗ ab ∗
    ● 0? (1? )? 0 ∗
    ● (a*|b*)c
    ● (b|b)*abb(a|b)*
    ● (a|b)*a(a|b)(a|b)
"""

"""
    Laboratorio C
    
"""
#yal = YALexGenerator("./Archivos Yal/slr-2.yal")
#print(yal.read_yal_file_())
#print("Lista del archivo: ", yal.file_list)
#print("Valor: ",yal.detect_rule_tokens_expression())
#print("detected: ", yal.detect_regular_definitions())
#Expresión regular formada desde el yalex
#print("Expresión regular resultante: ",yal.build_regular_expression())

"""postfix = input("Ingrese su expresión regular: ")
cadena = input("Ingrese la cadena que desea evaluar: ")
regex = RegextoTree(postfix)

#Creación del AFN a partir de su expresión regular. 
afn = Thompson(regex)
result = afn.simulate_afn(cadena)
print("La expresión ", cadena, " ha sido ", result, " por el AFN ")
afn.output_image('AFN#11PreLabB')

#Construción de AFD a partir del AFN
dfa = afn.to_dfa()
dfa.output_image('AFNtoAFD#11PreLabB')

#Construcción de AFD directamente
dfa_direct = AFD_construction(regex)
dfa_direct.output_image('AFD_DIRECT#11PreLabB')

#Evaluación de la cadena en el AFD directo
result = dfa_direct.simulate_afd(cadena)
print("La expresión ", cadena, " ha sido ", result, " por el AFD directo")

#Minimizamos el AFD obtenido del AFN
dfa.minimize_function()
result = dfa.simulate_afd(cadena)
print("La expresión ", cadena, " ha sido ", result, " por el AFD minimizado del AFN")
dfa.output_image('AFNtoAFD_MIN#11PreLabB')

#Minimizamos el AFD directo
dfa_direct.minimize_function()
result = dfa_direct.simulate_afd(cadena)
print("La expresión ", cadena, " ha sido ", result, " por el AFD directo minimizado")
dfa_direct.output_image('AFD_DIRECT_MIN#11PreLabB')
"""

#Construcción de AFD directamente
yal = YALexGenerator("./Archivos Yal/slr-0.yal")
regex = RegextoTree(yal.build_regular_expression())
print("Expresión regular resultante: ",yal.build_regular_expression())
#Construimos el árbol
regex.build_AST()
#Mostramos el árbol formado
regex.print_tree()
"""regex.build_AST()
#Árbol de la expresión regular
regex.print_tree()"""

"""postfix = yal.build_regular_expression()
regex = RegextoTree(postfix)
dfa_direct = AFD_construction(regex)
dfa_direct.output_image('AFD_Direct_YalexFile')"""

#Hacemos un menú para la interación
"""it= 0
while it != 4: 
    print("Por favor, ingrese una de la siguientes tres opciones: " + "\n1) Obtener AFN de la expresión regular: " + "\n2) Obtener el AFD de la expresión regular: " + "\n3) Generar el árbol sintáctico del regex"+ "\n4) Salir")
    it = int(input("\nIngrese una de las opciones: "))
    if it == 1:
        postfix = input("Ingrese su expresión regular: ")
        save = postfix
        regex = RegextoTree(postfix)
        print("to_postfix: " + regex.to_postfix())
        afn = Thompson(regex)
        afn.output_image('AFNTest8')
    elif it == 2:
        break
    elif it == 3:
        pass
    elif it == 4:
        print("¡Hasta luego!")
    else:
        print("¡Opción inválida!")"""