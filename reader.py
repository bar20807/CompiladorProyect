archivo = "./Archivos Yal/slr-2.yal"
expresiones_regulares = {}
rule_tokens = []

rl = 0
with open(archivo, 'r') as f:
    lineas = f.readlines()
    for linea in lineas:
        # Expresiones regulares
        if linea.startswith("let"):
            partes = linea.split("=")
            nombre = partes[0].strip().split()[1]
            valor = partes[1].strip()
            expresiones_regulares[nombre] = valor

        # obtener el index de los rule tokens
        splited = linea.split(" ")
        if "rule" in splited and "tokens" in splited:
            rl = lineas.index(linea)

# Guardar el valor que esta antes de un or
before_or = True
for linea in lineas[rl+1:]:
    # Rule tokens
    if "|" in linea:
        nombre = linea.split("|")[1].split("{")[0].strip()
        rule_tokens.append(nombre)
    if before_or:
        name = linea.split("{")[0].split("{")[0].strip()
        rule_tokens.append(name)
        before_or = False


#limpiar las reges y poenr valoes reales
for key in expresiones_regulares:
    regex = expresiones_regulares[key]

    #print("turno de: ", expresiones_regulares[key])
    #print("\n" + regex)
    #si aparecen corchetes, anmalizar su contenido y reemplazarlo en la regex
    expressions_with_c = []
    if "[" in regex:
        #Encontrar todos los corchetes en el string, esto nos indica una regex espsecial
        # se reemplazaran en la regex resultante
        while True:
            start = regex.find('[')
            if start == -1:
                break
            end = regex.find(']')
            if end == -1:
                break
            substring = regex[start + 1:end]
            expressions_with_c.append(substring)
            regex = regex[end + 1:]

        print("regex encontradas: ", expressions_with_c)

        converted = ""
        for expression in expressions_with_c:
            print("Valor de expression: ", expression)
            if "\"" in expression:
                # Las comillas dobles indican un grna string, por lo que devemos reemplazar
                # el contenido del corchete con el grna string
                
                #ahora tenemos que ahcer el or de cada caracter en la linea
                #si incluye un "\" entonces se deben incluir ambos

                #Encontrar las expresiones dentro de los ""
                pos = expression.find('\"')
                exp = expression[pos + 1:]
                exp = exp[:exp.find('\"')]

                exp = exp.replace("\'", "")

                print("exp -", exp)

                #agregar comillas

                # ahora tenemos que separarlas y remoer los "" de la regex
                # necesitamos dejarlo en terminos de regex
                palo = False
                for char in exp:
                    if not palo:
                        converted += "("
                    if char != "\\":
                        palo = False
                        converted += char
                        converted += ")"
                        converted += "|"
                    else:
                        palo = True
                        converted += char
                #quitar or innecesario
                if converted[-1] == "|":
                    converted = converted[:-1]

                print("Expresion convertidaaAAAAAAA ", converted)

            if "\'" in expression:
                # con comillas simples es mas sencillo porque solo se trata de separar
                # existen 2 caminos:
                # se trata de una secuencia de ASCIIs o de ors ya echos, los reconoceremos
                # print("tiene comilla simples")

                #recorrer la cadena y revisar de que se trata
                palabras = []
                indice = 0

                exp = expression

                while indice < len(exp):
                    if exp[indice] == "'":
                        indice += 1
                        palabra = "'"
                        while indice < len(exp) and exp[indice] != "'":
                            palabra += exp[indice]
                            indice += 1
                        palabra += "'" 
                        print("Palabra: ", palabra)
                        palabras.append(palabra)
                    indice += 1
                
                # Revisar que no se trate de una secuencia de ASCIs
                # esto lo podremos saber si removemos los caracteres obtenidos
                # y nos quedan signos "-" en la regex
                lel = expression
                for palabra in palabras:
                    lel = lel.replace(palabra, "")
                
                # print("tiene -? ", lel)

                if len(lel) > 0:
                    # el caso de secuencia
                    # se una secuencua de ascis
                    converted = ""
                    for minus in lel:
                        der = palabras.pop()
                        izq = palabras.pop()
                        # print(izq, der)
                        codigo_inicial = ord(izq[1])
                        codigo_final = ord(der[1])

                        for codigo in range(codigo_inicial, codigo_final + 1):
                            caracter = chr(codigo)
                            converted += caracter
                            converted += "|"
                    # quitar el or innecesario
                    if converted[-1] == "|":
                        converted = converted[:-1]
                        # ahora armar el conjunto de ascis como un gran or

                else:
                    # caso normal
                    # solo agregar el caracter y su respectivo or
                    # se añaden con comillas si se trata de un oeprador regex
                    converted = ""
                    for palabra in palabras:
                        converted += palabra
                        converted += "|"
                            #print(converted)

                    # quitar el or innecesario
                    if converted[-1] == "|":
                        converted = converted[:-1]
                print("CONVERTIDAAAAAAAA ", converted)

            # ahora que hemos modificado la expresion, reemplazarla en el string

            print("Expresion a cambiar: ", expression)
            expresiones_regulares[key] = expresiones_regulares[key].replace(expression, converted)
            print("cambio aplciado -> ", expresiones_regulares[key])
            print("Diccionario actualizado: ", expresiones_regulares)
    
    # al terminar de revisar todas las expresiones, basta con remplazar corchetes por parentesis
    expresiones_regulares[key] = expresiones_regulares[key].replace("[", "(").replace("]", ")")
    # print(" Expresion resultante -> ", expresiones_regulares[key])

# al finalizar, mostrar el diccionaraio
print("Expresiones regulares:")
for key in expresiones_regulares:
    print(key + ":", expresiones_regulares[key])

print("Rule tokens:", rule_tokens)
print("diccionario final: ",expresiones_regulares)

def create_regex():
    expression = ""
    for token in rule_tokens:
        expression += token
        expression += "|"
    # quitar el or innecesario
    if expression[-1] == "|":
        expression = expression[:-1]
    
    print("\nexpresion inicial: ", expression)

    # ahora se trata de revisar las regex que aparecen e ir reemplazando
    # al encontrar una regex nueva, reinicicar la lectura y revisar de nuevo
    i = 0
    current_word = ""
    comilla = False
    while i < (len(expression)):
        # ahora comenzaremos a leer la expresion y reemplazar terminos
        char = expression[i]
        # print("simbolo actual: ", char)
        # leeremos una palabra hasta encontrar un operador
        if char not in "+|*?()":
            current_word += char
            i += 1
        else:
            # detectamos una regex, ahora a reemplazarla
            # print("regex detectada: ", current_word)
            try:
                regex = expresiones_regulares[current_word]
                word_len = len(current_word)
                # guardamos el indice done nos quedamos
                der = i
                # ahora efectuamos una resta para saber que rango debemos borrar en la expresion
                # la posicion izquierda sera la misma aunque borremos lo que esta a la derecha
                izq = i - word_len

                # hacemos el corte y agregamos la regex correspondiente
                expression = expression[:izq] + regex + expression[der:]

                i = 0
                current_word = ""
            except:
                # si no se trata de ninguna regex, solo limpiar la paalabvra y seguir adelante
                current_word = ""
                i += 1
            

        # print("Expresion actual: ", expression)
    print("\nexpresion resultante: ", expression)

create_regex()