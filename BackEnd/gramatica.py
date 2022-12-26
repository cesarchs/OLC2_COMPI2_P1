


import sys
sys.setrecursionlimit(10**6)


from almacenar.error import Error

#t.type = tipo de token (como una cadena, id, etc)
#t.value = lexema del texto real coincidente
#t.lineno = numero de linea actual
#t.lexpos = posicion del token con relacion a la entrada
#t.lexer = actualiza el no. de linea


ListaErrores = []

#LISTA DE PALABRAS RESERVADAS PARA pytopy
reservadas = {
    'None'      : 'RNOTHING',
    'int'       : 'RINT',
    'bool'      : 'RBOOL',
    'Char'      : 'RCHAR',  
    'string'    : 'RSTRING',
    'struct'    : 'RSTRUCT',
    'mutable'   : 'RMUTABLE',
    'log10'     : 'RLOGT',
    'log'       : 'RLOG',
    'print'     : 'RPRINT',
    'println'   : 'RPRINTLN',
    'def'       : 'RFUNCTION',
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
    'elif'      : 'RELSEIF',
    'else'      : 'RELSE',
    'for'       : 'RFOR',
    'in'        : 'RIN',
    'push!'     : 'RPUSHFNA',
    'len'       : 'RLENGTHFNA',
    'True'      : 'RTRUE',
    'False'     : 'RFALSE',
    'break'     : 'RBREAK',
    'continue'  : 'RCONTINUE',
    'return'    : 'RRETURN',
    'Vector'    : 'RVECTOR',
    #nuevos por cambio de sitaxis del sistema
    'and'       : 'AND',
    'or'        : 'OR',
    'not'       : 'NOT',
    'range'     : 'RRANGE'
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
#t_AND           = r'&&'
#t_OR            = r'\|\|'
#t_NOT           = r'!'
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
lexer = lex.lex()
#---fin lexico---

#---INICIO SINTACTICO---

#Asociacion de operadores y presedencia  
precedence = (
    ('left', 'COMA','DP'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'UNOT'),                  #!5... !a 
    ('left','MAYORQ','MENORQ','MAYORIGUALQ','MENORIGUALQ','DIFERENTE','IGUALDAD'),
	('left', 'MAS', 'MENOS'),           #HACIA LA IZQUIERDA ASOCIA 4+5+8-> DE ESTA MANERA: (4+5)=9+8 asocia el primer mas con lo de la izquierda suc
	('left', 'POR', 'DIV','MOD'),
	('right','UMENOS'),                 #lo asocia asi -8+4+3 => -8 => (-8)+(4+3)
	('right', 'POTEN'),
	)




from instrucciones.imprimir import Imprimir, ImprimirLn
from instrucciones.insWhile import Mientras
from instrucciones.breeak import Break
from instrucciones.continuar import Continue
from instrucciones.retorn import Retorno
from instrucciones.funcs import Funcion
from instrucciones.InsIF import InstrSi
from instrucciones.Foor import Para,ParaArray,ParaArrayD,ParaStr
from instrucciones.llamda import Llamada
from instrucciones.declaraciones import Declaracion, DeclaracionLocal,DeclaracionGlobal,DeclaracionLocalSinValor,DeclaracionGlobalSinValor
from instrucciones.decarray import DeclaracionArreglo
from instrucciones.modifyarray import CambiarArreglo
from instrucciones.accesoarray import AccesoArreglo,AccesoArregloBE
from instrucciones.copyarrayy import CopiarArreglo
from instrucciones.structss import NuevoStruct,AtributosStruct
from instrucciones.accesostruc import AccesoStruct
from Nativas.tamañoarr import TamanoArreglo,TamanoArregloS
from instrucciones.pusharray import EmpujarArray,EmpujarArrayD,EmpujarArrayExp
from instrucciones.asigstruct import AsignacionStruct
from Expresiones.ids import Identificador
from Expresiones.primitivos import Primitivo
from Expresiones.aritmeticas import Aritmetica
from Expresiones.relacionales import Relacion
from Expresiones.logicas import Logica
from Nativas.uppers import Upper,Lower
from Nativas.parse import Parse
from Nativas.truncamiento import Trunc
from Nativas.floate import Flooaat
from Nativas.stringgg import Stringgss
from Nativas.typeoof import Typeoff
from Nativas.raiz import Raiz
from Nativas.popnf import PopArr
from Nativas.trigonometricas import *
from Nativas.logaritmo import *
from almacenar.tipo import *





def p_inicio(t):
    'inicio         : instrucciones'
    t[0] = t[1]

def p_instrucciones_lista(t):
    'instrucciones  : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])               #t1 es una lista entonces solo se agregan las instrucciones
    t[0] = t[1]                         #y luego se copia a t0

def p_instrucciones_instruccion(t):
    'instrucciones  : instruccion'              
    if t[1] == "":                      #padre: instrucciones hace una lista para meter a t1 que es instruccion
        t[0] = []
    else:    
        t[0] = [t[1]] 

#***********************************
#******INSTRUCCIONES POSIBLES*******
#***********************************

def p_instruccion(t):
                    # instr_declaracion:tambien puede ser instr_asignacion
    '''instruccion  : instr_imprimir opcion_ptcoma
                    | instr_imprimirln opcion_ptcoma
                    | instr_declaracion opcion_ptcoma
                    | instr_declaraciontipo opcion_ptcoma
                    | instr_if opcion_ptcoma
                    | instr_while opcion_ptcoma
                    | instr_break opcion_ptcoma
                    | instr_continue opcion_ptcoma
                    | instr_for opcion_ptcoma
                    | instr_func opcion_ptcoma
                    | instr_llamada opcion_ptcoma
                    | instr_return opcion_ptcoma
                    | instr_declararreglo opcion_ptcoma
                    | instr_copyarray opcion_ptcoma
                    | modify_array opcion_ptcoma
                    | instr_push opcion_ptcoma
                    | instr_crearstruct opcion_ptcoma                  
                    | isntr_asigatribstruct opcion_ptcoma
                    '''
    t[0] = t[1]

def p_opcion_ptcoma(t):
    ''' opcion_ptcoma   :   PTCOMA
                        |   '''
    t[0]=None                           # este lo dejamos por que lo podemos necesitar para cerrar algun metodo en la gramatica, pero no lo pide por se python, por esa razon la dejamos opcional

def p_instruccion_error(t):             # ACA en error tambiem debemos de dejar opcional el punto y coma, pero no lo hacemos por ahora, dado a que no sabemos como va a trabajar sin eso.
    'instruccion    : error PTCOMA'
    ListaErrores.append(Error("SINTACTICO","Sinxtaxis incorrecta "+str(t[1].value), t.lineno(1), buscar_columna(input, t.slice[1])))
    t[0] =""

#////////////////////////////////////////////////////////INSTRUCCION PRINT/////////////////////////////////////////////////////////////////

def p_instr_imprimir(t):
    #print(expresión);
    'instr_imprimir : RPRINT PARIZQ lexp PARDER '
    t[0] = Imprimir(t[3],t.lineno(1),buscar_columna(input, t.slice[1]))

def p_instr_imprimirln(t):
    #println(expresión);
    'instr_imprimirln : RPRINTLN PARIZQ lexp PARDER '
    t[0] = ImprimirLn(t[3],t.lineno(1),buscar_columna(input, t.slice[1]))
    
def p_exp_coma(t):
    'lexp   : lexp COMA expresion'
    #t[0] = Aritmetica(OpsAritmetico.COMA,t[1],t[3],t.lineno(2),buscar_columna(input,t.slice[2]))
    t[1].append(t[3])
    t[0]=t[1]

def p_expst(t):
    'lexp   : expresion'
    t[0] = [t[1]]
#////////////////////////////////////////////////////////INSTRUCCION DECLARACION/////////////////////////////////////////////////////////////////
#***SIN TIPO 
def p_instr_declaracion_sintipo(t):
    # ID = Expresión;  #SI NO TRAEN GLOBAL ES LOCAL EN EL AMBITO CORRESPONDIENTE
    #EN ESTA PRODUCCION NO SE SABE SI SERA UNA MODIFICACION GLOBAL O LOCAL
    'instr_declaracion : ID IGUAL expresion '
    t[0] = Declaracion(t[1],t[3],None,t.lineno(1),buscar_columna(input, t.slice[1]))
    
###CON PALABRA RESERVADA LOCAL###
def p_instr_declaracion_sintipo_local(t):
    # LOCAL ID = EXP;
    'instr_declaracion : RLOCAL ID IGUAL expresion '
    t[0] = DeclaracionLocal(t[2],t[4],None,t.lineno(1),buscar_columna(input, t.slice[1]))
    
def p_instr_declaracion_local(t):
    # LOCAL ID;
    'instr_declaracion : RLOCAL ID '
    t[0] = DeclaracionLocalSinValor(t[2],t.lineno(1),buscar_columna(input, t.slice[1]))

def p_instr_declaracion_global(t):
    # LOCAL ID;
    'instr_declaracion : RGLOBAL ID '
    t[0] = DeclaracionGlobalSinValor(t[2],t.lineno(1),buscar_columna(input, t.slice[1]))
    
###CON PALABRA RESERVADA GLOBAL###
def p_instr_declaracion_sintipo_global(t):
    # GLOBAL ID = EXP;
    'instr_declaracion : RGLOBAL ID IGUAL expresion '
    t[0] = DeclaracionGlobal(t[2],t[4],None,t.lineno(1),buscar_columna(input, t.slice[1]))
    
#***CON TIPO 
def p_instr_declaraciontipo(t):
    #EN ESTA PRODUCCION NO SE SABE SI SERA UNA MODIFICACION GLOBAL O LOCAL
    'instr_declaraciontipo : ID IGUAL expresion DP tipof '
    t[0] = Declaracion(t[1],t[3],t[5],t.lineno(1),buscar_columna(input, t.slice[1]))

###CON PALABRA RESERVADA LOCAL###
def p_instr_declaraciontipo_local(t):
    #LOCAL ID = EXP :: TIPO
    'instr_declaraciontipo : RLOCAL ID IGUAL expresion DP tipof'
    t[0] = DeclaracionLocal(t[2],t[4],t[6],t.lineno(1),buscar_columna(input, t.slice[1]))

###CON PALABRA RESERVADA LOCAL###
def p_instr_declaraciontipo_global(t):
    #LOCAL ID = EXP :: TIPO
    'instr_declaraciontipo : RGLOBAL ID IGUAL expresion DP tipof '
    t[0] = DeclaracionGlobal(t[2],t[4],t[6],t.lineno(1),buscar_columna(input, t.slice[1]))

#///////////////////////////////////////////////////////////////////////////DECLARACION Y MOD ARREGLOS///////////////////////////////////////////////////////////////////////////
def p_instr_declararreglo(t):
    
    'instr_declararreglo    : ID IGUAL CORIZQ tist CORDER '
    t[0] = DeclaracionArreglo(t[1],t[4],None,t.lineno(1),buscar_columna(input, t.slice[1]))

def p_instr_declararreglon(t):
    
    'instr_declararreglo    : ID IGUAL CORIZQ tist CORDER DP RVECTOR LLAVEA masrvector LLAVEC '
    t[0] = DeclaracionArreglo(t[1],t[4],t[9],t.lineno(1),buscar_columna(input, t.slice[1]))
    
def p_masrvector(t):
    'masrvector             : masrvector RVECTOR '
    t[0]=t[1]
    
def p_masrvectorr(t):
    'masrvector             : frevector '
    t[0]=t[1]

def p_frevector(t):
    'frevector              : tipof '
    t[0]=t[1]

def p_frevectorr(t):
    'frevector              : RVECTOR LLAVEA masrvector LLAVEC '
    t[0]=[t[3]]


def p_lista_ex(t):
    'tist      :  tist COMA fis'
    t[1].append(t[3])
    t[0]=t[1]
def p_lista_ex2(t):
    'tist       :  fis '
    t[0] = [t[1]]

def p_liss_un(t):
    'fis           : expresion  '
    t[0] = t[1]
    
def p_liss_und(t):
    'fis           : CORIZQ tist CORDER  '
    t[0] = t[2]
    
#///////////////////////////////////////////////////////////////////////////MOD ARREGLOS///////////////////////////////////////////////////////////////////////////
def p_modify_array(t):
    'modify_array   :   ID lista_corchetes IGUAL expresion'
    t[0] = CambiarArreglo(t[1],t[2],t[4],t.lineno(1),buscar_columna(input, t.slice[1]))
def p_listacorchetes(t):
    'lista_corchetes    :   lista_corchetes CORIZQ expresion CORDER'
    t[1].append(t[3])
    t[0] = t[1]

def p_listacorchetes_2(t):
    'lista_corchetes    :   CORIZQ expresion CORDER'  
    t[0] = [t[2]]

    #///////////////////////////////////////////////////////////////////////////STRUCTS///////////////////////////////////////////////////////////////////////////
#IN-MUTABLE
def p_instr_crearstruct(t):
    'instr_crearstruct  :   RSTRUCT ID listatributes PTCOMA '
                       #ID  atributs  mutable?
    t[0] = NuevoStruct(t[2], t[3],    False,    t.lineno(1),buscar_columna(input, t.slice[1]))
#MUTABLE
def p_instr_crearstructM(t):
    'instr_crearstruct  :   RMUTABLE RSTRUCT ID listatributes PTCOMA '
                    #    ID  ATRIBUTS  MUTABLE?
    t[0] = NuevoStruct(t[3], t[4],    True,    t.lineno(1),buscar_columna(input, t.slice[1]))

def p_listatributes(t):
    'listatributes    :   listatributes PTCOMA idss '
    t[1].append(t[3])
    t[0]=t[1]
def p_listatributesd(t):
    'listatributes    :   idss'
    t[0]=[t[1]]
def p_iddssu(t):
    'idss    : ID '
    #                     ID   ::    TIPO    bandera si puede cambiar tipo
    t[0]=AtributosStruct(t[1],     Tipo.NULO, True)
    
def p_iddss(t):
    'idss   : ID  DP tipof'
    #                    ID   ::  TIPO      bandera si puede cambiar tipo
    t[0]=AtributosStruct(t[1],     t[3],    False)

#///////////////////////////////////////////////////////////////////////////CONSTRUCCION STRUCT///////////////////////////////////////////////////////////////////////////
    
#def p_instr_consstruct(t):
#    'instr_consstruct   :   ID IGUAL instr_structcons opciontipocons'
#    t[0]=ConstruccionStruct(t[1],t[3],t[4],t.lineno(1),buscar_columna(input, t.slice[1]))
#
#def p_opciontipocons(t):
#    'opciontipocons     :   DDP tipof'
#    t[0]=t[2]
#    
#def p_opciontipoconss(t):
#    'opciontipocons     : '
#    t[0]=None
#
#def p_instr_structconsID(t):
#    'instr_structcons   :   ID PARIZQ listexpstruct PARDER'
#    #t[0]=[t[3]]
#    t[0]=Strucs(t[1],t[3])
#    
#def p_listexpstruct(t):
#    'listexpstruct      :   listexpstruct COMA expresion'          
#    t[1].append(t[3])
#    t[0]=t[1]
#    
#def p_listexpstructD(t):
#    'listexpstruct      :   expresion' 
#    t[0]=[t[1]] 

#//////////////////////////////////////////////////////////////////////////ASIGNACION ATRIBUTOS////////////////////////////////////////////////////////////////////////////
def p_isntr_asigatribstruct(t):
    'isntr_asigatribstruct  :   ID POINT atributospoint IGUAL expresion'
                        #  ID   ATRIBUTO    EXP
    t[0]=AsignacionStruct(t[1] , t[3],      t[5], t.lineno(1),buscar_columna(input, t.slice[1]))    
def p_atributospoint(t):
    'atributospoint         :   atributospoint POINT ID'
    t[1].append(t[3])
    t[0]=t[1]
def p_atributospointid(t):
    'atributospoint         :   ID'    
    t[0]=[t[1]]

#///////////////////////////////////////////////////////////////////////////COPY ARRAY ARREGLOS///////////////////////////////////////////////////////////////////////////
def p_instr_copyarray(t):
    #copiaArreglo = arreglo[:];
    'instr_copyarray    :   ID IGUAL ID CORIZQ DP CORDER'  
                        #idcopia       #id a copiar
    t[0] = CopiarArreglo(t[1]     ,       t[3]        ,t.lineno(1),buscar_columna(input, t.slice[1]) )

#///////////////////////////////////////////////////////////////////////////PUSH ARREGLOS///////////////////////////////////////////////////////////////////////////
def p_expresion_pushd(t):
     #push!(a,[exp])
    'instr_push      : RPUSHFNA PARIZQ ID COMA lista_corchetespush PARDER'
    t[0] = EmpujarArray(t[3],t[5],t.lineno(1),buscar_columna(input, t.slice[1]))

def p_expresion_pushc(t):
     #push!(a,[exp])
    'instr_push      : RPUSHFNA PARIZQ ID lista_corchetes COMA lista_corchetespush PARDER'
    t[0] = EmpujarArrayD(t[3],t[4],t[6],t.lineno(1),buscar_columna(input, t.slice[1]))
    
def p_expresion_push(t):
    #push!(a,exp)
    'instr_push      : RPUSHFNA PARIZQ ID COMA expresion PARDER'
    t[0] = EmpujarArrayExp(t[3],t[5],t.lineno(1),buscar_columna(input, t.slice[1]))



def p_listacorchetespushh(t):
    'lista_corchetespush    :    CORIZQ lista_corchetespush CORDER'
    t[0] = [t[2]]

def p_listacorchetespush_2(t):
    'lista_corchetespush    :   CORIZQ lexpresionessspush CORDER'  
    t[0] = t[2]

def p_lexpresionessspush(t):
    'lexpresionessspush     :   lexpresionessspush COMA expresion '
    t[1].append(t[3])
    t[0]=t[1]
    
def p_lexpresionessspush2(t):
    'lexpresionessspush     :   expresion '
    t[0]=[t[1]]
#///////////////////////////////////////////////////////////////////////////ACCESO ARREGLOS BEGIN: END///////////////////////////////////////////////////////////////////////////
def p_begin_end(t):
    'begin_end          : CORIZQ RBEGIN DP REND CORDER' 
    coleccion = []
    coleccion.append(t[2])
    coleccion.append(t[4])
    t[0]=coleccion

def p_begin_endun(t):
    'begin_end          : CORIZQ RBEGIN DP expresion CORDER'
    coleccion = []
    coleccion.append(t[2])
    coleccion.append(t[4])
    t[0]=coleccion

def p_begin_enddo(t):
    'begin_end          : CORIZQ expresion DP REND CORDER'
    coleccion = []
    coleccion.append(t[2])
    coleccion.append(t[4])
    t[0]=coleccion
  
    
def p_begin_endtre(t):
    'begin_end          : CORIZQ expresion DP expresion CORDER'
    coleccion = []
    coleccion.append(t[2])
    coleccion.append(t[4])
    t[0]=coleccion

#///////////////////////////////////////////////////////////////////////////TIPOS_VALIDOS_EN_pytopy/////////////////////////////////////////////////////////////////////
def p_tipof(t):
    '''tipof   : RNOTHING 
               | RINT
               | RFLOATFN
               | RBOOL
               | RCHAR
               | RSTRING 
               | ID
               '''
               
    if t[1] == 'None':
        t[0] = Tipo.NULO           
    elif t[1] == 'int':
        t[0] = Tipo.ENTERO
    elif t[1] == 'float':
        t[0] = Tipo.DECIMAL
    elif t[1] == 'bool':
        t[0] = Tipo.BOOLEANO
    elif t[1] == 'Char':
        t[0] = Tipo.CARACTER
    elif t[1] == 'string':
        t[0] = Tipo.CADENA 
    #le agrego un elif debido a que puede que sea tipo struct (id de struct)
    else:
        t[0] = t[1]

#////////////////////////////////////////////////////////INSTRUCCION IF//////////////////////////////////////////////////////////////////////
def p_ifIns(t):
    '''instr_if  :  RIF expresion instrucciones 
                 |  RIF expresion instrucciones  RELSE  instrucciones
                 |  RIF expresion instrucciones elseIfLists
    '''
    if len(t) == 4:
        t[0] = InstrSi(t[2],t[3],None,t.lineno(1),buscar_columna(input, t.slice[1]))
    elif len(t) == 6:
        t[0] = InstrSi(t[2],t[3],t[5],t.lineno(1),buscar_columna(input, t.slice[1]))
    elif len(t) == 5:
        t[0] = InstrSi(t[2],t[3],t[4],t.lineno(1),buscar_columna(input, t.slice[1]))

def p_elseIfList(t):
    '''elseIfLists   : RELSEIF expresion instrucciones
                    | RELSEIF expresion instrucciones RELSE instrucciones
                    | RELSEIF expresion instrucciones elseIfLists'''
    if len(t) == 4:
        t[0] = InstrSi(t[2], t[3],None,t.lineno(1),buscar_columna(input, t.slice[1]))
    elif len(t) == 6:
        t[0] = InstrSi(t[2], t[3],t[5],t.lineno(1),buscar_columna(input, t.slice[1]))
    elif len(t) == 5:
        t[0] = InstrSi(t[2], t[3],t[4],t.lineno(1),buscar_columna(input, t.slice[1]))
    
    




































#////////////////////////////////////////////////////////INSTRUCCION WHILE/////////////////////////////////////////////////////////////////
def p_instr_while(t):
    'instr_while    :   RWHILE expresion instrucciones '
                    #EXP  #INSTR
    t[0] = Mientras(t[2],  t[3],  t.lineno(1),buscar_columna(input, t.slice[1]))   
#////////////////////////////////////////////////////////INSTRUCCION FOR/////////////////////////////////////////////////////////////////
def p_instr_for(t):
    'instr_for      :   RFOR ID RIN lexpsfor instrucciones '
                #ID   #EXP   #instrs
    t[0] = Para(t[2], t[4],   t[5],     t.lineno(1),buscar_columna(input, t.slice[1]))
    
def p_instr_forarr(t):
    'instr_for      :   RFOR ID RIN lexpsforarray instrucciones '
                #ID   #EXP   #instrs
    t[0] = ParaArray(t[2], t[4],   t[5],     t.lineno(1),buscar_columna(input, t.slice[1]))

def p_instr_forarr2(t):
    'instr_for      :   RFOR ID RIN ID instrucciones '
                #ID   #EXP   #instrs
    t[0] = ParaArrayD(t[2], t[4],   t[5],     t.lineno(1),buscar_columna(input, t.slice[1]))

def p_instr_forstring(t):
    'instr_for      :   RFOR ID RIN CADENA instrucciones '
                #ID   #EXP   #instrs
    t[0] = ParaStr(t[2], t[4],   t[5],     t.lineno(1),buscar_columna(input, t.slice[1]))
    
def p_lexpsfor(t):
    'lexpsfor       : expresion RRANGE expresion'
    t[0]= Aritmetica(OpsAritmetico.DP,t[1],t[3],t.lineno(2),buscar_columna(input, t.slice[2]))
def p_lexpsforarray(t):
    'lexpsforarray       : CORIZQ list_expss CORDER'
    t[0]= t[2]
def p_list_expss(t):
    'list_expss     : list_expss COMA expresion '
    t[1].append(t[3])
    t[0]=t[1]
def p_list_expss1(t):
    'list_expss     : expresion '
    t[0]=[t[1]]    
#////////////////////////////////////////////////////////INSTRUCCION FUNCION/////////////////////////////////////////////////////////////////
def p_instr_func_params(t):
    'instr_func     :   RFUNCTION ID PARIZQ params PARDER opciontipo instrucciones '
                    #ID    #params   #INSTR
    t[0] = Funcion( t[2],   t[4],   t[6],  t[7],    t.lineno(1),buscar_columna(input, t.slice[1]))

def p_instr_func(t):
    'instr_func     :   RFUNCTION ID PARIZQ PARDER opciontipo instrucciones '
                    #ID          #INSTR
    t[0] = Funcion( t[2], [] , t[5]  ,t[6],    t.lineno(1),buscar_columna(input, t.slice[1]))

def p_tipo_o_no(t):
    'opciontipo       : DP tipof'
    t[0]=t[2]

def p_tipo_o_no_dos(t):
    'opciontipo       : '
    t[0]=None    
    
def p_paramsparams_param(t):
    'params         :   params COMA param'
    t[1].append(t[3])
    t[0]=t[1]

def p_params_param(t):
    'params         :  param'
    t[0]=[t[1]]
    
def p_param(t):
    'param          :   ID'
    t[0] = {'id':t[1],'tipo':Tipo.NULO,'vector':False}

def p_param_tip(t):
    'param          :   ID DP tipof'
    t[0] = {'id':t[1],'tipo':t[3],'vector':False}

def p_param_vec(t):
    'param          :   ID DP RVECTOR LLAVEA masrvector LLAVEC'
    t[0] = {'id':t[1],'tipo':t[5],'vector':True}

#////////////////////////////////////////////////////////INSTRUCCION LLAMADA/////////////////////////////////////////////////////////////////   
def p_instr_llamada(t):
    'instr_llamada  :   ID PARIZQ PARDER  '
                    #ID #param
    #print("instr_llamada")
    t[0] = Llamada( t[1],[], t.lineno(1),buscar_columna(input, t.slice[1]))
     
def p_instr_llamada_param(t):
    'instr_llamada  :   ID PARIZQ params_llam PARDER '
                    #ID  #params
    #print("instr_llamada")                    
    t[0] = Llamada( t[1],t[3] ,t.lineno(1),buscar_columna(input, t.slice[1]))
    
def p_llamada_params(t):
    'params_llam         :   params_llam COMA paramet'
    t[1].append(t[3])
    t[0]=t[1]

def p_llamada_params_param(t):
    'params_llam         :  paramet'
    t[0]=[t[1]]

def p_lla_param(t):
    'paramet  :   expresion'
    t[0] = t[1]

#//////////////////////////////////////////////////////INSTRUCCION RETURN/////////////////////////////////////////////////////////////////
def p_instr_return(t):
    'instr_return  : RRETURN expresion '
    t[0] = Retorno(t[2],t.lineno(1),buscar_columna(input, t.slice[1]))

#//////////////////////////////////////////////////////INSTRUCCION BREAK/////////////////////////////////////////////////////////////////
def p_instr_break(t):
    'instr_break    : RBREAK '
    t[0] = Break(t.lineno(1),buscar_columna(input, t.slice[1]))

#//////////////////////////////////////////////////////INSTRUCCION CONTINUE/////////////////////////////////////////////////////////////////
def p_instr_continue(t):
    'instr_continue :   RCONTINUE '
    t[0] = Continue(t.lineno(1),buscar_columna(input, t.slice[1]))
    

    
#//////////////////////////////////////////////////////EXPRESIONES/////////////////////////////////////////////////////////////////////////  
    
def p_expresion_binaria(t):
    '''expresion      : expresion MAS expresion
                      | expresion MENOS expresion
                      | expresion POR expresion
                      | expresion DIV expresion
                      | expresion MOD expresion
                      | expresion POTEN expresion
                      | expresion MAYORQ expresion
                      | expresion MENORQ expresion
                      | expresion MAYORIGUALQ expresion
                      | expresion MENORIGUALQ expresion
                      | expresion DIFERENTE expresion
                      | expresion IGUALDAD expresion
                      | expresion OR expresion
                      | expresion AND expresion                     
                      '''
    if t[2] == '+': 
        t[0] = Aritmetica(OpsAritmetico.MAS,t[1],t[3],t.lineno(2),buscar_columna(input,t.slice[2]))
    elif t[2] == '-': 
        t[0] = Aritmetica(OpsAritmetico.MENOS,t[1],t[3],t.lineno(2),buscar_columna(input,t.slice[2]))
    #elif t[2] == ':': 
    #    t[0] = Aritmetica(OpsAritmetico.DP,t[1],t[3],t.lineno(2),buscar_columna(input,t.slice[2]))
    elif t[2] == '*': 
        t[0] = Aritmetica(OpsAritmetico.POR,t[1],t[3],t.lineno(2),buscar_columna(input,t.slice[2]))
    elif t[2] == '/': 
        t[0] = Aritmetica(OpsAritmetico.DIV,t[1],t[3],t.lineno(2),buscar_columna(input,t.slice[2]))
    elif t[2] == '%': 
        t[0] = Aritmetica(OpsAritmetico.MOD,t[1],t[3],t.lineno(2),buscar_columna(input,t.slice[2]))
    elif t[2] == '**': 
        t[0] = Aritmetica(OpsAritmetico.POT,t[1],t[3],t.lineno(2),buscar_columna(input,t.slice[2]))
    elif t[2] == '>':
        t[0] = Relacion(OpsRelacional.MAYORQ,t[1],t[3],t.lineno(2),buscar_columna(input,t.slice[2]))
    elif t[2] == '<':
        t[0] = Relacion(OpsRelacional.MENORQ,t[1],t[3],t.lineno(2),buscar_columna(input,t.slice[2]))
    elif t[2] == '>=':
        t[0] = Relacion(OpsRelacional.MAYORIGUALQ,t[1],t[3],t.lineno(2),buscar_columna(input,t.slice[2]))
    elif t[2] == '<=':
        t[0] = Relacion(OpsRelacional.MENORIGUALQ,t[1],t[3],t.lineno(2),buscar_columna(input,t.slice[2]))
    elif t[2] == '!=':
        t[0] = Relacion(OpsRelacional.DIFERENTE,t[1],t[3],t.lineno(2),buscar_columna(input,t.slice[2]))
    elif t[2] == '==':
        t[0] = Relacion(OpsRelacional.IGUALQ,t[1],t[3],t.lineno(2),buscar_columna(input,t.slice[2])) 
    elif t[2] == 'or':
        t[0] = Logica(OpsLogical.OR,t[1],t[3],t.lineno(2),buscar_columna(input,t.slice[2]))   
    elif t[2] == 'and':
        t[0] = Logica(OpsLogical.AND,t[1],t[3],t.lineno(2),buscar_columna(input,t.slice[2]))  
        
        
def p_expresion_unaria(t):
    '''expresion      : MENOS expresion %prec UMENOS
                      | NOT expresion %prec UNOT
                      '''
    if t[1] == '-': 
        t[0] = Aritmetica(OpsAritmetico.UMENOS,t[2],None,t.lineno(1),buscar_columna(input,t.slice[1]))
    elif t[1] == 'not':
        t[0] = Logica(OpsLogical.NOT,t[2],None,t.lineno(1),buscar_columna(input,t.slice[1]))
        

        
def p_expresion_grupo(t):
    'expresion      : PARIZQ expresion PARDER'
    t[0] = t[2]

        
def p_expresion_llam(t):
    'expresion      : instr_llamada'
    #print("si ando aqui")
    t[0] = t[1]

def p_expresion_parse(t):
    'expresion      : RPARSEFN PARIZQ tipof COMA expresion PARDER'
                      #tipo    #expr
    t[0] =     Parse( t[3] ,   t[5] ,t.lineno(1),buscar_columna(input,t.slice[1]))

def p_expresion_length(t):
    'expresion      : RLENGTHFNA PARIZQ ID lista_corchetes PARDER'
                         #ID  #EPX=[[]][]
    t[0] = TamanoArreglo(t[3],  t[4],      t.lineno(1),buscar_columna(input,t.slice[1]))

def p_expresion_lengthdo(t):
    'expresion      : RLENGTHFNA PARIZQ ID PARDER'
                         #ID  
    t[0] = TamanoArregloS(t[3], t.lineno(1),buscar_columna(input,t.slice[1]))


def p_expresion_logDiez(t):
    #log10(exp)
    'expresion      : RLOGT PARIZQ lexp PARDER '
                             #exp
    t[0]=      LogaritmoDiez(t[3],t.lineno(1),buscar_columna(input,t.slice[1]))

def p_expresion_log(t):
    #log10(exp)
    'expresion      : RLOG PARIZQ lexp PARDER '
                             #exp->base,valor
    t[0]=        Logaritmoo(t[3],t.lineno(1),buscar_columna(input,t.slice[1]))


def p_expresion_trunc_tipof(t):
    'expresion      : RTRUNCFN PARIZQ tipof COMA expresion PARDER'
                      #tipo    #expr
    t[0] =     Trunc( t[3] ,   t[5] ,t.lineno(1),buscar_columna(input,t.slice[1]))

def p_expresion_trunc(t):
    'expresion      : RTRUNCFN PARIZQ expresion PARDER'
                      #tipo    #expr
    t[0] =     Trunc( None ,   t[3] ,t.lineno(1),buscar_columna(input,t.slice[1]))
 
def p_expresion_floaatt(t):
    'expresion      : RFLOATFN PARIZQ expresion PARDER'
                      #tipo    #expr
    t[0] =     Flooaat( None ,   t[3] ,t.lineno(1),buscar_columna(input,t.slice[1]))    

def p_expresion_uppercase(t):
    'expresion      : RUPPERCASEFN PARIZQ expresion PARDER'
    t[0] =     Upper(t[3],t.lineno(1),buscar_columna(input,t.slice[1]))

def p_expresion_lowecase(t):
    'expresion      : RLOWERCASEFN PARIZQ expresion PARDER'
    t[0] =     Lower(t[3],t.lineno(1),buscar_columna(input,t.slice[1]))


def p_expresion_id(t):
    'expresion  : ID'
    #print("si ando aqui")
    t[0] = Identificador(t[1],t.lineno(1),buscar_columna(input,t.slice[1]))    

def p_expresion_entero(t):
    'expresion      : ENTERO '
    t[0]  = Primitivo(Tipo.ENTERO,t[1],t.lineno(1), buscar_columna(input,t.slice[1]))

def p_expresion_decimal(t):
    'expresion      : DECIMAL'
    t[0] = Primitivo(Tipo.DECIMAL,t[1],t.lineno(1),buscar_columna(input,t.slice[1]))#slice es una funcion de py que devuelente un elemento o una serie de elementos especificados

def p_expresion_cadena(t):
    'expresion      : CADENA'
    t[0] = Primitivo(Tipo.CADENA,str(t[1]).replace('\\n','\n'),t.lineno(1), buscar_columna(input, t.slice[1]))

def p_expresion_caracter(t):
    'expresion      : CARACTER'
    t[0] = Primitivo(Tipo.CARACTER,str(t[1]),t.lineno(1), buscar_columna(input, t.slice[1]))

def p_expresion_booleano_true(t):
    'expresion      : RTRUE'
    t[0] = Primitivo(Tipo.BOOLEANO,True,t.lineno(1), buscar_columna(input, t.slice[1]))

def p_expresion_booleano_false(t):
    'expresion      : RFALSE'
    t[0] = Primitivo(Tipo.BOOLEANO,False,t.lineno(1), buscar_columna(input,t.slice[1]))

def p_expresion_nothing_false(t):
    'expresion      : RNOTHING'
    t[0] = Primitivo(Tipo.NULO,None,t.lineno(1), buscar_columna(input,t.slice[1]))
def p_expresion_acceso_array(t):
    ' expresion     : ID lista_corchetes '
    t[0] = AccesoArreglo(t[1],t[2], t.lineno(1), buscar_columna(input,t.slice[1]))

def p_expresion_accesoarraydos(t):
    ' expresion     : ID begin_end '
    t[0] = AccesoArregloBE(t[1],t[2], t.lineno(1), buscar_columna(input,t.slice[1]))

def p_expresion_accesarStruct(t):
    ' expresion     : ID POINT atributospoint'
    t[0] = AccesoStruct(t[1],t[3], t.lineno(1), buscar_columna(input,t.slice[1]))

    


    



#FIN SINTACTICO 

import ply.yacc as yacc
#import ply.yacc as yacc
parser = yacc.yacc()
input = ''

def getErrores():
    return ListaErrores

def parse(inp):
    #limpio todo para un nuevo analisis
    global ListaErrores
    global lexer
    ListaErrores = []
    lexer = lex.lex()
    parser = yacc.yacc()
    global input
    input = inp
    #genero un nuevo analisis y lo retorno
    return parser.parse(inp,lexer=lexer)

def getNativas(arbolito,tabla): #CREACION DE FUNCIONES NATIVAS
    id = 'nativaTrunc'
    params = [{'id':'totrunc_#_#_#_parameter','tipo':Tipo.ENTERO},{'id':'totrunc_#_#_#_parameterdos','tipo':Tipo.DECIMAL}]
    instrs=[]
    nativaTruc = Trunc(id,params,instrs,-1,-1)
    tabla.setSimboloEnTsFunc(nativaTruc,id,True)
    