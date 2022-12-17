


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

# | instr_consstruct opcion_ptcoma
def p_opcion_ptcoma(t):
    ''' opcion_ptcoma   :   PTCOMA
                        |   '''
    t[0]=None                           # este lo dejamos por que lo podemos necesitar para cerrar algun metodo en la gramatica, pero no lo pide por se python, por esa razon la dejamos opcional

def p_instruccion_error(t):             # ACA en error tambiem debemos de dejar opcional el punto y coma, pero no lo hacemos por ahora, dado a que no sabemos como va a trabajar sin eso.
    'instruccion    : error PTCOMA'
    ListaErrores.append(Error("SINTACTICO","Sinxtaxis incorrecta "+str(t[1].value), t.lineno(1), buscar_columna(input, t.slice[1])))
    t[0] =""
