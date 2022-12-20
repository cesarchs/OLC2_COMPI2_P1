#IMPORTS:
#clase optimizador
# GENERAL
from Optimizador.Instrucciones.MathGo import MathFunc
from Optimizador.Optimizador import *

# INSTRUCCIONES GENERALES
from Optimizador.Instrucciones.Asignacion import *
from Optimizador.Instrucciones.LlamadaFuncion import *
from Optimizador.Instrucciones.Funcion import *
from Optimizador.Instrucciones.Label import *
from Optimizador.Instrucciones.Print import *
from Optimizador.Instrucciones.Return import *

# INSTRUCCIONES DE CAMBIO DE FLUJO
from Optimizador.Gotos.If import *
from Optimizador.Gotos.Goto   import *

# INSTRUCCIONES DE EXPRESION
from Optimizador.Expresiones.Acceso import *
from Optimizador.Expresiones.Expresiones import *
from Optimizador.Expresiones.Literal import *

#ListaErrores = []

#LEX
rw = {
    "FLOAT64": "FLOAT64",
    "INT": "INT",
    "FUNC": "FUNC",
    "RETURN": "RETURN",
    "IF": "IF",
    "GOTO" : "GOTO",
    "FMT": "FMT",
    "PRINTF": "PRINTF",
    "PACKAGE": "PACKAGE",
    "IMPORT": "IMPORT",
    "VAR": "VAR",
    "MATH":"MATH",
    "MOD":"MOD"
}

tokens = [
    "ID",
    "ENTERO",               #INTLITERAL
    "DECIMAL",              #FLOATLITERAL
    "CADENA",               #STRINGLITERAL

    "MUL",                  #MUL
    "DIV",                  #DIV
    "MAS",                  #PLUS
    "MENOS",                #MINUS


    "MAYOR",
    "MENOR",
    "MAYORIGUAL",
    "MENORIGUAL",
    "IGUALIGUAL",
    "DIFERENTE",

    "IGUAL",        #"EQUALS",                    
    "PTCOMA",       # "SEMICOLON",
    "DP",           # "COLON",  
    "PUNTO",        # "POINT",  

    'LLAVEIZQ',     #"LEKEY",
    'LLAVEDER',     #"RIKEY",

    'PARIZQ',        #"LEPAR",
    'PARDER',        #"RIPAR",

    "CORIZQ",        #CORIZQ   
    "CORDER",        #CORIZQ

    "COMMA"
] + list(rw.values())




#SIGNOS Y SIMBOLOS
t_LLAVEIZQ                  = r'{'
t_LLAVEDER                  = r'}'

t_PARIZQ                    = r'\('
t_PARDER                    = r'\)'

t_CORIZQ                    = r'\['
t_CORDER                    = r'\]'

t_IGUAL                     = r'='
t_PTCOMA                    = r';'
t_DP                        = r':'
t_PUNTO                     = r'\.'
t_COMMA                     = r','
#ARITMETICOS
t_MUL                       = r'\*'
t_DIV                       = r'/'
t_MAS                       = r'\+'
t_MENOS                     = r'-'
#RELACIONALES
t_MAYOR                     = r'>'
t_MENOR                     = r'<'
t_MAYORIGUAL                = r'>='
t_MENORIGUAL                = r'<='
t_IGUALIGUAL                = r'=='
t_DIFERENTE                 = r'!='

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = rw.get(t.value.upper(), 'ID')
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("ERROR IN PARSE TO FLOAT")
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("ERROR IN PARSE TO INT")
        t.value = 0
    return t

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t
 #caracteres ignorados
t_ignore = " \t\r"

def t_COMENMULTI(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count("\n")

def t_COMENTARIO(t):
    r'//.*\n'
    t.lexer.lineno += 1
    
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
lexer1 = lex.lex()


#inicia sintactico

def p_inicio(t):
    'inicio     :  PACKAGE ID PTCOMA IMPORT PARIZQ CADENA PARDER PTCOMA declarations codeList'
    t[0]    =   Optimizador(t[6],t[9],t[10])
    
def p_iniciod(t):
    'inicio     :  PACKAGE ID PTCOMA IMPORT PARIZQ CADENA PTCOMA CADENA PARDER PTCOMA declarations codeList '
    t[0]    =   Optimizador(t[6]+'\";\"'+t[8],t[11],t[12])

def p_declarations(t):
    '''declarations : declarations declaration
                    | declaration'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]

def p_declaration(t):
    '''declaration :     VAR idList CORIZQ ENTERO CORDER FLOAT64 PTCOMA
                   |     VAR idList type PTCOMA'''
    if len(t) == 5:
        t[0] = f'{t[2]} {t[3]};'
    else:
        t[0] = f'{t[2]}[{t[4]}] float64;'

def p_type(t):
    '''type : INT
            | FLOAT64'''
    if t[1] == "int":
        t[0] = "int"
    else:
        t[0] = "float64"

def p_idList(t):
    '''idList :   idList COMMA ID
                | ID'''
    if len(t) == 2:
        t[0] = f'{t[1]}'
    else:
        t[0] = f'{t[1]}, {t[3]}'
        
def p_codeList(t):
    '''codeList : codeList code
                | code'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]
        
def p_code(t):
    'code : FUNC ID PARIZQ PARDER statement'
    t[0] = Function(t[5], t[2], t.lineno(1), t.lexpos(1))
    
def p_statement(t):
    '''statement : LLAVEIZQ instructions LLAVEDER'''
    t[0] = t[2]

def p_instructions(t):
    '''instructions : instructions instruction
                    | instruction'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]

def p_instruction(t):
    '''instruction :  assign opcion_ptcoma
                    | print opcion_ptcoma
                    | if
                    | gotoSt opcion_ptcoma
                    | label
                    | callFunc opcion_ptcoma
                    | retSt opcion_ptcoma'''
    t[0] = t[1]
    
# | instr_consstruct opcion_ptcoma
def p_opcion_ptcoma(t):
    ''' opcion_ptcoma   :   PTCOMA
                        |   '''
    t[0] = None 

def p_return(t):
    'retSt : RETURN'
    t[0] = Return(t.lineno(1), t.lexpos(1))

def p_callFunc(t):
    'callFunc : ID PARIZQ PARDER'
    t[0] = CallFun(t[1], t.lineno(2), t.lexpos(2))

def p_label(t):
    'label : ID DP'
    t[0] = Label(t[1], t.lineno(2), t.lexpos(2))  

def p_goto(t):
    'gotoSt : GOTO ID'
    t[0] = Goto(t[2], t.lineno(1), t.lexpos(1))
    
def p_if(t):
    'if : IF expression LLAVEIZQ GOTO ID PTCOMA LLAVEDER'
    t[0] = If(t[2], t[5], t.lineno(1), t.lexpos(1))

def p_assign(t):
    'assign : access IGUAL finalExp'
    t[0] = Asignacion(t[1], t[3], t.lineno(2), t.lexpos(2))
    
def p_assign2(t):
    '''assign :   ID IGUAL expression
                | ID IGUAL modul
                | ID IGUAL access'''
    aux = Literal(t[1], t.lineno(1), t.lexpos(1))
    t[0] = Asignacion(aux, t[3], t.lineno(2), t.lexpos(2))

def p_mod(t):
    '''
    modul       :   MATH PUNTO MOD PARIZQ ENTERO COMMA ENTERO PARDER
                |   MATH PUNTO MOD PARIZQ ID COMMA ID PARDER
                |   MATH PUNTO MOD PARIZQ ID COMMA ENTERO PARDER
                |   MATH PUNTO MOD PARIZQ ENTERO COMMA ID PARDER
    
    '''
    t[0]=FuncionMath(t[5],t[7], t.lineno(2), t.lexpos(2))

def p_print(t):
    'print : FMT PUNTO PRINTF PARIZQ CADENA COMMA printValue PARDER'
    t[0] = Print(t[5], t[7], t.lineno(1), t.lexpos(1))

def p_printValue(t):
    '''printValue :   INT PARIZQ finalExp PARDER
                  |   finalExp'''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[3].haveInt = True
        t[0] = t[3]

def p_expression(t):
    '''expression :   finalExp MAS finalExp
                    | finalExp MENOS finalExp
                    | finalExp MUL finalExp
                    | finalExp DIV finalExp
                    | finalExp MAYOR finalExp
                    | finalExp MENOR finalExp
                    | finalExp MAYORIGUAL finalExp
                    | finalExp MENORIGUAL finalExp
                    | finalExp IGUALIGUAL finalExp
                    | finalExp DIFERENTE finalExp
                    | finalExp'''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = Expresion(t[1], t[3], t[2], t.lineno(2), t.lexpos(2))

def p_finalExp(t):
    '''finalExp : ID
                | ENTERO
                | MENOS ENTERO
                | DECIMAL'''
    if len(t) == 3:
        t[0] = Literal(0-t[2], t.lineno(1), t.lexpos(1))
    else:
        t[0] = Literal(t[1], t.lineno(1), t.lexpos(1))

def p_access(t):
    '''access :   ID CORIZQ INT PARIZQ finalExp PARDER CORDER
                | ID CORIZQ finalExp CORDER'''
    if len(t) == 5:
        t[0] = Access(t[1], t[3], t.lineno(2), t.lexpos(2))
    else:
        t[0] = Access(t[1], t[5], t.lineno(2), t.lexpos(2))
        t[0].haveInt = True

def p_error(t):
    print(t)
    print("Syntactic error in '%s'" % t.value)

import ply.yacc as yacc
parser2 = yacc.yacc()
input=''

def parseOP(inp):
    #se limpia todo para un nuevo analisis
    global lexer1
    global parser2
    lexer1 = lex.lex()
    parser2 = yacc.yacc()
    global input
    input = inp
    return parser2.parse(inp, lexer=lexer1)

#f = open("entradas\entradaop.txt","r",encoding="utf-8")
#entrada = f.read()  
#
#instrucciones = parseOP(entrada)  
#
#if instrucciones != None:
#    instrucciones.Mirilla()
#    salida = instrucciones.getCode()
#    print(salida)