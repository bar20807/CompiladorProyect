"""
    José Rodrigo Barrera García
    Universidad del Valle de Guatemala
    Diseño de Lenguajes
    20807
    Laboratorio A 
"""


from Regex import Regex
from Thompson import *
from RegextoTree import RegextoTree

print('\n¡ADVERTENCIA! Deberá ingresar las expresiones regulares sin "." en la concatenación, el programa los agregará.')

#Hacemos un menú para la interación
it= 0
while it != 4: 
    print("Por favor, ingrese una de la siguientes tres opciones: " + "\n1) Obtener AFN de la expresión regular: " + "\n2) Obtener el AFD de la expresión regular: " + "\n3) Generar el árbol sintáctico del regex"+ "\n4) Salir")
    it = int(input("\nIngrese una de las opciones: "))
    if it == 1:
        postfix = input("Ingrese su expresión regular: ")
        save = postfix
        regex = Regex(postfix)
        afn = Thompson(regex)
        afn.output_image('AFNTest3')
    elif it == 2:
        break
    elif it == 3:
        postfix = input("Ingrese su expresión regular: ")
        tree = RegextoTree(postfix)
        tree.convert()
        tree.save_dot_png('TreeTest.png')
    elif it == 4:
        print("¡Hasta luego!")
    else:
        print("¡Opción inválida!")