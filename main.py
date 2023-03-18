"""
    José Rodrigo Barrera García
    Universidad del Valle de Guatemala
    Diseño de Lenguajes
    20807
    Laboratorio A 
"""

from Thompson import *
from RegextoTree import RegextoTree
from AFD import AFD_construction

print('\n¡ADVERTENCIA! Deberá ingresar las expresiones regulares sin "." en la concatenación, el programa los agregará.')

"""

    Expresiones regulares dadas en el pre-laboratorio:
    ●ab∗ab∗
    ●0? (1? )? 0 ∗
    ●(a*|b*)c
    ●(b|b)*abb(a|b)*
    ●(a|ε)b(a+)c?
    ●(a|b)*a(a|b)(a|b)
    
"""

"""
    Expresiones regulares dadas en el pre-laboratorio b: 
    '(a*|b*)c'
    '(b|b)*abb(a|b)*'
    '(a|ε)b(a+)c?'
    '(a|b)*a(a|b)(a|b)'
    'b*ab?'
    'b+abc+'
    'ab*ab*'
"""

postfix = input("Ingrese su expresión regular: ")
cadena = input("Ingrese la cadena que desea evaluar: ")
regex = RegextoTree(postfix)
print("to_postfix: " + regex.to_postfix())
afn = Thompson(regex)
result = afn.simulate_afn(cadena)
print("La expresión ", cadena, " ha sido ", result, " por el AFN ")
afn.output_image('AFN#1PreLabB')

#Construción de AFD a partir del AFN
dfa = afn.to_dfa()
dfa.output_image('AFNtoAFD#1PreLabB')

#Construcción de AFD directamente
dfa_direct = AFD_construction(regex)
dfa_direct.output_image('AFD_DIRECT#1PreLabB')

#Evaluación de la cadena en el AFD
result = dfa_direct.simulate_afd(cadena)
print("La expresión ", cadena, " ha sido ", result, " por el AFD directo")

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