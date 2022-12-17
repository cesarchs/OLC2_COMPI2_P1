


import sys
sys.setrecursionlimit(10**6)


from almacenar.error import Error


ListaErrores = []

#LISTA DE PALABRAS RESERVADAS PARA pytopy
reservadas = {
    'None'   : 'RNOTHING',
    'int'     : 'RINT',
    'bool'      : 'RBOOL',
    'Char'      : 'RCHAR',  
    'string'    : 'RSTRING',
    'struct'    : 'RSTRUCT',
    'mutable'   : 'RMUTABLE',
    'log10'     : 'RLOGT',
    'log'       : 'RLOG',
    'print'     : 'RPRINT',
    'println'   : 'RPRINTLN',
    'function'  : 'RFUNCTION',
    'global'    : 'RGLOBAL',
    'begin'     : 'RBEGIN',
    'end'       : 'REND',
    'local'     : 'RLOCAL',
    'while'     : 'RWHILE',
    'parse'     : 'RPARSEFN',
    'trunc'     : 'RTRUNCFN',
    'upper'     : 'RUPPERCASEFN',
    'lower'     : 'RLOWERCASEFN',
    'float'     : 'RFLOATFN',
    'if'        : 'RIF',
    'elseif'    : 'RELSEIF',
    'else'      : 'RELSE',
    'for'       : 'RFOR',
    'in'        : 'RIN',
    'push!'     : 'RPUSHFNA',
    'length'    : 'RLENGTHFNA',
    'True'      : 'RTRUE',
    'False'     : 'RFALSE',
    'break'     : 'RBREAK',
    'continue'  : 'RCONTINUE',
    'return'    : 'RRETURN',
    'Vector'    : 'RVECTOR',
    #nuevos por cambio de sitaxis del sistema
    'and'       : 'AND',
    'or'        : 'OR',
    'not'       : 'NOT'
}

#SIMBOLOS EN LENGUAJE pytopy
tokens = [
    'PTCOMA',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'LLAVEA',
    'LLAVEC',
    'DDP', #::
    'DP',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'MOD', # %
    'POTEN', #^ - ese deberia de ser, pero se pidio **
    'IGUALDAD',
    'DIFERENTE',
    'MAYORQ',
    'MENORQ',
    'MAYORIGUALQ',
    'MENORIGUALQ',
    'AND',
    'OR',
    'NOT',
    'COMA',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CARACTER',
    'IGUAL',
    'ID' ,
    'POINT'  
] + list(reservadas.values())

#DEFINIENDO PALABRAS CON SIMBOLOS
t_PTCOMA        = r';'
t_PARIZQ        = r'\('
t_PARDER        = r'\)'
t_CORIZQ        = r'\['
t_CORDER        = r'\]'
t_LLAVEA        = r'{'
t_LLAVEC        = r'}'
t_DDP           = r'::'
t_DP            = r':'
t_MAS           = r'\+'
t_MENOS         = r'-'
t_POR           = r'\*'
t_DIV           = r'/'
t_MOD           = r'%'
t_POTEN         = r'\*\*'
t_IGUALDAD      = r'=='
t_DIFERENTE     = r'!='
t_MAYORQ        = r'>'
t_MENORQ        = r'<'
t_MAYORIGUALQ   = r'>='
t_MENORIGUALQ   = r'<='
t_AND           = r'&&'
t_OR            = r'\|\|'
t_NOT           = r'!'
t_IGUAL         = r'='
t_COMA          = r','
t_POINT         = r'\.'
#t_DOLAR         = r'\$='

#ER PARA VALIDAR ENTRE IDENTIFICADORES Y PALABRAS RESERVADAS
def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*[\!]?'
    t.type = reservadas.get(t.value,'ID')
    #print(str(t.value))
    return t

def t_COMENTARIO_MULTILINEA(t):
    r'\#\=(.|\n)*?\=\#'
    t.lexer.lineno += t.value.count('\n')

def t_COMENTARIO_UNILINEA(t):
    r'\#.*\n'
    t.lexer.lineno += 1



#ER PARA VALIDAR CADENAS 
def t_CADENA(t):
    r'\"(\\\'|\\"|\\\\|\\n|\\t|[^\'\\\"])*?\"'
    t.value = t.value[1:-1]

    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\"', '\"')
    t.value = t.value.replace("\\'", "\'")
    t.value = t.value.replace('\\\\', '\\')

    return t

def t_CARACTER(t):
    r'\'(\\\'|\\"|\\t|\\n|\\\\|[^\'\\\"])?\''
    t.value = t.value[1:-1]
    #print(t.value)
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\"', '\"')
    t.value = t.value.replace("\\'", "\'")
    t.value = t.value.replace('\\\\', '\\')
    return t

#ER para numeros decimales
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("VALOR MUY GRANDE %d",t.value)
        t.value = 0
    return t

#ER PAARA NUMEROS ENTEROS
def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("VALOR MUY GRANDE %d",t.value)
        t.value = 0
    return t

 #caracteres ignorados
t_ignore = " \t\r"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    #print("Ilegal character '%s'" % t.value[0])
    ListaErrores.append(Error("ERROR LEXICO", t.value[0],t.lexer.lineno,buscar_columna(input,t)))
    t.lexer.skip(1)

def buscar_columna(inp, token):
    linea = inp.rfind('\n',0,token.lexpos) + 1
    return (token.lexpos - linea)+1



import ply.lex as lex
#import ply.lex as lex
lexer = lex.lex()
#---fin lexico---

#---INICIO SINTACTICO---

#Asociacion de operadores y presedencia  
precedence = (
    ('left', 'COMA','DP'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'UNOT'), #!5... !a 
    ('left','MAYORQ','MENORQ','MAYORIGUALQ','MENORIGUALQ','DIFERENTE','IGUALDAD'),
	('left', 'MAS', 'MENOS'), #HACIA LA IZQUIERDA ASOCIA 4+5+8-> DE ESTA MANERA: (4+5)=9+8 asocia el primer mas con lo de la izquierda suc
	('left', 'POR', 'DIV','MOD'),
	('right','UMENOS'), #lo asocia asi -8+4+3 => -8 => (-8)+(4+3)
	('right', 'POTEN'),
	)


    
    
    #id = "uppercase"
    #params = [{'id':'toupperss_#_#_#_parameter','tipo':Tipo.CADENA}]
    #instrs= []
    #uppercase = Upper(id,params,instrs,-1,-1)
    #arbolito.agregarFuncs(uppercase)
    #
    #id = "lowercase"
    #params = [{'id':'lowercase_#_#_#_parameter','tipo':Tipo.CADENA}]
    #instrs= []
    #lowercase = Lower(id,params,instrs,-1,-1)
    #arbolito.agregarFuncs(lowercase)
    #
    #id = "float"
    #params = [{'id':'float_#_#_#_parameter','tipo':Tipo.ENTERO}]
    #instrs=[]
    #flooaat= Flooaat(id,params,instrs,-1,-1)
    #arbolito.agregarFuncs(flooaat)
    #
    #id = "string"
    #params = [{'id':'string_#_#_#_parameter','tipo':Tipo.NULO}]
    #instrs=[]
    #stringgss= Stringgss(id,params,instrs,-1,-1)
    #arbolito.agregarFuncs(stringgss)
    #
    #id = "typeof"
    #params = [{'id':'typeof_#_#_#_parameter','tipo':Tipo.NULO}]
    #instrs=[]
    #typeoof= Typeoff(id,params,instrs,-1,-1)
    #arbolito.agregarFuncs(typeoof)
    #
    #id = "sin"
    #params = [{'id':'sin_#_#_#_parameter','tipo':Tipo.NULO}]
    #instrs=[]
    #seno= Seno(id,params,instrs,-1,-1)
    #arbolito.agregarFuncs(seno)
    #
    #id = "cos"
    #params = [{'id':'cos_#_#_#_parameter','tipo':Tipo.NULO}]
    #instrs=[]
    #coss= Coseno(id,params,instrs,-1,-1)
    #arbolito.agregarFuncs(coss)
    #
    #id = "tan"
    #params = [{'id':'tan_#_#_#_parameter','tipo':Tipo.NULO}]
    #instrs=[]
    #tannn= Tangente(id,params,instrs,-1,-1)
    #arbolito.agregarFuncs(tannn)
    #
    #id = "sqrt"
    #params = [{'id':'raizsqrt_#_#_#_parameter','tipo':Tipo.NULO}]
    #instrs=[]
    #raizez= Raiz(id,params,instrs,-1,-1)
    #arbolito.agregarFuncs(raizez)
    #
    #id = "pop!"
    #params = [{'id':'popsarray_#_#_#_parameter','tipo':Tipo.NULO}]
    #instrs=[]
    #popsi=PopArr(id,params,instrs,-1,-1)
    #arbolito.agregarFuncs(popsi)

    
#EN OTRO ARCHIVO
#def desempaquetarvalor(diccionario):
#    valor =""
#    tamano=1
#    valor=str(diccionario['##_nombre_padre_struct_##']['id'])+"("
#    for key in diccionario:
#        if key!='##_nombre_padre_struct_##' and isinstance(diccionario[key],dict) and '##_nombre_padre_struct_##' in diccionario[key]: 
#            valor+=desempaquetarvalor(diccionario[key])
#            tamano+=1
#            continue
#        if  diccionario[key]['valor'] != '':
#            if isinstance(diccionario[key]['valor'],dict):
#                valor+= desempaquetarvalor(diccionario[key]['valor'])
#            else:
#                valor += str(diccionario[key]['valor'])
#                if tamano <= len(diccionario):valor += ','
#    valor+=")"
#    return valor
#
#
#
#
#
#def generarDot(t):
#    if len(t)!=0:
#        with open('arbol.txt', "w",encoding="utf-8") as f:
#            f.write(t)
#    else:
#        with open('reporteAST.dot', "w") as f:
#            f.write('digraph G {\"No hay instrucciones\"}')
#        return ""
#
#
#f = open("entradas\entrada.txt","r",encoding="utf-8")
#entrada = f.read()
##print(parse(entrada))
#from almacenar.ts import TablaSimbolos
#from almacenar.arbol import Arbol
##->->->->->-->->->->->->->->->->->->->->->->->->->->->->->->->->->
#from almacenar.generador import Generador
#
#genAux = Generador()
#genAux.limpiarTodo()
#generator = genAux.getInstance()
#
##->->->->->-->->->->->->->->->->->->->->->->->->->->->->->->->->->
#
#listaInstrucciones = parse(entrada+"\n") #Aqui obtengo todos los objetos creados en el recorrido de la entrada vs gramtica
#ast = Arbol(listaInstrucciones)         #Creo arbol con la lista de instrucciones
#TsGlobal = TablaSimbolos(None)          #Creo una nueva tabla de símbolos global
#ast.setTsGlobal(TsGlobal)               #Le añado la tabla de simbolos a el árbol creado.
##getNativas(ast,TsGlobal)               #####agregar en clase interpreter*********************
#
##err lex y sin
#for error in ListaErrores: #para cada error en la lista de errores
#    ast.getListaErrores().append(error) #lo agrego en la lista de errores del arbol
#    ast.actualizarConsola(error.toString()) #actualizo consola con error
#
#
#for instruccion in ast.getInstrucciones():
#    if isinstance(instruccion,Funcion):
#    #print(instruccion.id)
#    #resuladdFunc=ast.agregarFuncs(instruccion) #guardo funciones en arbol
#        retornoInstruccion = instruccion.compilar(ast, TsGlobal)
#        if isinstance(retornoInstruccion,Error):
#            ast.getListaErrores().append(retornoInstruccion)
#            ast.actualizarConsola(retornoInstruccion.toString()) 
#    
##semant
##2DA PASADA
#for instruccion in ast.getInstrucciones(): #realizar acciones #Para cada instruccion en arbol
#
#    if isinstance(instruccion,NuevoStruct):#guardo declaracion de structs
#        resuladdstruct=ast.agregarStruct(instruccion)
#        if isinstance(resuladdstruct,Error):
#            ast.getListaErrores().append(resuladdstruct)
#            ast.actualizarConsola(resuladdstruct.toString())
#        continue
#    
#    retornoInstruccion = instruccion.compilar(ast, TsGlobal) 
#    if isinstance(retornoInstruccion, Error):
#        ast.getListaErrores().append(retornoInstruccion)
#        ast.actualizarConsola(retornoInstruccion.toString())
#    
#    #////ESTO SE AGREGO, AUN NO ESTA EN PINTERPRETE PARA COMUNICACION CON EL FRONTED(*NO OLVIDAR AGREGAR)
#    if isinstance(retornoInstruccion,Break):#///
#        repor=Error("SEMANTICO","INSTRUCCION BREAK FUERA DE LOOP",retornoInstruccion.fila,retornoInstruccion.columna)#///
#        ast.getListaErrores().append(repor)#///
#        ast.actualizarConsola(repor.toString())#///
#    if isinstance(retornoInstruccion,Continue):#///
#        repor=Error("SEMANTICO","INSTRUCCION CONTINUE FUERA DE LOOP",retornoInstruccion.fila,retornoInstruccion.columna)#///
#    if isinstance(retornoInstruccion,Retorno):#///
#        repor=Error("SEMANTICO","INSTRUCCION RETORNO FUERA DE FUNC",retornoInstruccion.fila,retornoInstruccion.columna)#///
#        ast.getListaErrores().append(repor)#///
#        ast.actualizarConsola(repor.toString())#///
#
#print(ast.getConsola())
#print(generator.getCode())
##print("FUNCS: ")
#
#
#ast.ListaTablas.insert(0,('GLOBAL',TsGlobal))
#
#for tabla in ast.getListaTablas(): #POR CADA TABLA EN LISTA DE TABLAS OMBTENGO AMBITO Y TABLA
#    #print(tabla[0])
#    ambito=tabla[0]
#    simbolos=tabla[1].getSimbolos()
#    for simbolo in simbolos:
#        if simbolos[simbolo].getTipo()==Tipo.STRUCT:
#            valorret = desempaquetarvalor(simbolos[simbolo].getValor())
#            #valor = simbolos[simbolo].getValor()
#            #valorret="("
#            #tamano=1
#            #for key in valor:
#            #    tamano+=1
#            #    if valor[key]['valor'] != '':
#            #        valorret += str(valor[key]['valor'])
#            #        if tamano <= len(valor):valorret += ','
#            #
#            #valorret+=")"
#            
#            print("ambito: "+ambito+" ID: "+simbolos[simbolo].getId()+ " valor: "+str(valorret)+ " tipo: "+str(simbolos[simbolo].getTipo()))
#            #print("ambito: "+ambito+" ID: "+simbolos[simbolo].getId()+ " valor: "+str(simbolos[simbolo].getValor())+ " tipo: "+str(simbolos[simbolo].getTipo()))
#        else:
#            print("ambito: "+ambito+" ID: "+simbolos[simbolo].getId()+ " valor: "+str(simbolos[simbolo].getValor())+ " tipo: "+str(simbolos[simbolo].getTipo()))
#
##->for error in ast.getListaErrores():
##->    print(str(error.getTipo())+str(error.getDescripcion()))
#    #for simbolo in t[1]:
#    #    print("AMBITO: "+t[0]+"id: "+str(t[1][simbolo].getId())+"\n")
#
##dic = ast.getTsGlobal().getSimbolos()
##for simb in dic:
##    print(dic[simb].getTipo())
##    if isinstance(simb,Simbolo):
##        print("simbolo en tabla: "+str(simb.getId())+"\n")
#
##inicio = NodoArbol("INICIO")
##instrucciones = NodoArbol("INSTRUCCIONES")
##
##for instruccion in ast.getInstrucciones():
##    instrucciones.agregarHijoConNodo(instruccion.getNode())
##
##inicio.agregarHijoConNodo(instrucciones)
##grafo = ast.getDot(inicio)
##generarDot(grafo)
#
#
#    
#