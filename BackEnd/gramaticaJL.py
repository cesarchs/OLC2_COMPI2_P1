#gramatica para JuLia

#ANALIZADOR LEXICO------------------------------------------------------------------------------






from Instrucciones.StructCambioAtributos import StructCambioAtributos
from Instrucciones.StructAccesoAtributos import StructAccesoAtributos
from Instrucciones.StructLLamada import LlamadaStruct
from Instrucciones.Struct import Struct
from Instrucciones.LLamarArray import LLamarArray
import sys

sys.setrecursionlimit(5000)#para q no se muera el ackermann


from TS.Arbol import Arbol
from TS.TablaSimbolo import TablaSimbolos


# Las funciones se interpretan cuando se llaman a llamar ej: PINTAR(); aqui se interpretaria



from Expresiones.TypeOf import nfTypeof
from Expresiones.NfString import nfString
from Expresiones.NfFloat import nfFloat
from Expresiones.Trunc import Trunc
from Expresiones.Tangente import Tangente
from Expresiones.Coseno import Coseno
from Expresiones.Seno import Seno
from Expresiones.Raiz import Raiz
from Expresiones.Log import Log
from Expresiones.Log10 import Log10





import math
import os
from Abstract.NodoAST import NodoAST
from Nativas.Lowercase import Lowercase
from Nativas.Uppercase import Uppercase
from TS.Excepcion import Excepcion

errores=[]


PalabrasReservadas = {
    #MAIN NO VA EN JULIA
    #'main' : 'MAIN',
    
    'true' : 'RTRUE',
    'false' : 'RFALSE',
    
    
    'end':'END',

    'println':'RPRINTLN',
    'print':'RPRINT',

    
    #'uppercase':'UPPERCASE',
    #'lowercase':'LOWERCASE',



    #usadas en las (tipo de datos) converiones(no funcion nativa)
    'String':'RSTRING',
    'Char':'RCHAR',
    'Int64':'RINT64',
    'Float64':'RFLOAT64',
    'Bool':'RBOOL',
    'nothing' : 'RNOTHING',
    'Nothing' : 'RNOTHING2',
    
    'Vector':'RVECTORarray',

    'log10':'LOG10',
    'log':'LOG',
    'sin':'SIN',
    'cos':'COS',
    'tan':'TAN',
    'sqrt':'SQRT',

    'global':'GLOBAL',
    'local':'LOCAL',

    'for':'RFOR',
    'in':'RIN',

    'function':'FUNCTION',

    #funciones nativas
    'parse':'PARSE',
    'trunc':'TRUNC',
    'float':'NFFLOAT',
    'string':'NFSTRING',
    'typeof':'TYPEOF',
    'push':'PUSH',
    'pop':'POP',
    #'length':'LENGTH',

#-----------------------------
    'if' : 'IF',#si falla ponerle R a los tokens
    'else' : 'ELSE',
    'elseif' : 'ELSEIF',
#-----------------------------
    'while' : 'WHILE',

    'break' : 'BREAK',# sin el ; xd
    'continue' : 'CONTINUE',
    'return' : 'RETURN',

    'struct':'STRUCT',
    'mutable':'MUTABLE',
    

}

tokens  = [
    'coma',
    'pyc',
    'dp2',

    'dp1',

    'corizq',
    'corder',

    'pizq',
    'pder',
    'igual',
    'mas',
    'menos',
    'multiplicacion',
    'division',
    'potencia',
    'modular',

    'and',
    'or',
    'not',

    
    'igual2',
    'notigual',
    'menor',
    'mayor',
    'menorigual',
    'mayorigual',

    'punto',
    'hao',


    'entero',
    'decimal',
    'cadena',
    'character',
    'id'
] + list(PalabrasReservadas.values())#para detectar las palabras reserv. con mayor prioridad

# Tokens------------------------------------------------------------------------------------------------------
t_coma    = r','
t_pyc    = r';'
t_dp2    = r'::'#posible error colocar \

t_dp1    = r':'#posible error colocar \
t_hao = r'&'
t_corizq    = r'\['
t_corder    = r'\]'
t_pizq    = r'\('
t_pder    = r'\)'
t_igual     = r'='
t_mas       = r'\+'
t_menos     = r'-'
t_multiplicacion       = r'\*'
t_division  = r'/'
t_potencia = r'\^'#sin \^ no funciona
t_modular = r'%'#??? llevara \%
t_and    = r'&&'
t_or    = r'\|\|'
t_not    = r'!'
t_menor    = r'<'
t_mayor    = r'>'
t_menorigual = r'<='
t_mayorigual = r'>='
t_punto = r'\.'
t_igual2  = r'=='
t_notigual = r'!='

#------------------------------------------------------------------------------------------------------
# Comentario de múltiples líneas #= ...=#
def t_commitM(t):
    r'\#\=(.|\n)*?\=\#'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple  # ...
def t_commitS(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados (DEFINIDA POR PLY)
t_ignore = " \t"# el espacio en blanco y tab

#nueva linea (DEFINIDA POR PLY)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")# con esto obtengo la #linea y #columna a reportar 

#error (DEFINIDA POR PLY)  LEXICOS
def t_error(t):
    print("Error lexico en la [linea "+str(t.lexer.lineno) +" y columna "+str(find_column(input,t))+"] token no definido '%s'" % t.value[0])
    #le meto a mi array los errores Exception(clase) asi ordenadito
    errores.append(Excepcion("Lexico","Error lexico: "+t.value[0],t.lexer.lineno, find_column(input,t)))
    t.lexer.skip(1)


#metodo que halla la columna del error
def find_column(inp,token):
    line_start= inp.rfind('\n',0,token.lexpos)+1
    return (token.lexpos-line_start)




#---------------------------------------------------------------------------------
#soy float
def t_decimal(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t


#soy int
def t_entero(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


#soy string
def t_cadena(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t    


#soy char
def t_character(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # remuevo las comillas simples
    return t        


# identificadores
#quizas falte q el id pueda empesar con _
def t_id(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = PalabrasReservadas.get(t.value,'id')    # Check for reserved words t.value.lower() con esto no me funciona nada xd  (((((((((((((((((((((((())))))))))))))))))))))))
     return t




# Construyendo el analizador léxico--------------------------------------------------------------------------------
import ply.lex as lex
lexer = lex.lex()




#SINTACTICO *u*
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#PLY ES ASCENDENTE

from Abstract.instruccion import instruccion        #clase abstracta
from Instrucciones.imprimir import Imprimir
from Expresiones.primitivos import Primitivos
from TS.Tipo import operador_aritmetico, tipo,operador_relacional,operador_logico
from Expresiones.aritmetica import Aritmetica
from Expresiones.relacional import Relacional
from Expresiones.logica import Logica
from Instrucciones.declaracion import Declaracion
from Expresiones.identificador import Identificador
from Instrucciones.asignacion import Asignacion
from Instrucciones.If_instr import If
from Instrucciones.While import While
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
#from Instrucciones.Main import Main #SOY main (julia no tiene xd)
from Instrucciones.FuncionSimple import FuncionSP #SOY UNA FUNCION SIN PARAMS 
from Instrucciones.LlamadaFuncion import LlamadaFuncion#sirve para llamar funcion sin params
from Instrucciones.Return import Return
from Expresiones.Casteo import Casteo
from Instrucciones.DeclaracionArrays import DeclaracionArray
from Instrucciones.Push import Push
from Instrucciones.Pop import Pop
from Nativas.Lenght import Length
from Instrucciones.WFor import For



input=''



#precedencia            HAKAI
precedence=(
    ('left','coma','dp2','dp1'),
    ('left','or'),
    ('left','and'),
    ('right','negado'),#not
    ('left','menor','mayor','igual2','menorigual','mayorigual',"notigual"),
    
    ('left','mas','menos'),
    ('left','multiplicacion','division','modular'),
    ('right','negativo'),#negativos
    ('right','potencia')
    
)

#definicion de la gramatica-----------------------

def p_init(t):
    '''
    init : instrucciones
    '''
    t[0]=t[1]

def p_instrucciones_instrucciones_instruccion(t):
    '''
        instrucciones : instrucciones instruccion 
    '''    
    if t[2]!='':
        t[1].append(t[2])#paso la instruccion a su hermano instrucciones
    
    t[0]=t[1]#instrucciones padre le paso todas las intrucciones


def p_instrucciones_instruccion(t):
    '''
    instrucciones : instruccion
    '''
    if t[1]=='':
        t[0]=''
    else:
        t[0]=[t[1]]#le meto a la lista de instrucciones una instruccion mas

   

def p_instruccion_imprimir(t):#expresionPrint finisnt a borrar solo lo tengo de prueba
    '''
    instruccion : imprimir finisnt
                | declaracion finisnt
                | asignacion finisnt
                | expresionPrint finisnt
                | if_instruccion finCMP
                | while_instruccion finCMP

                | for_instruccion finCMP

                | break_instruccion finisnt
                | continue_instruccion finisnt
                
                | funcion_instruccion finCMP
                | llamada_funcion finisnt
                | return_instruccion finisnt
                | push_inst finisnt
                | pop_inst finisnt
                | globalLocal finisnt
                | globalLocal2 finisnt

                | declaracionArray finisnt
               

                | structs_instr finCMP
               

    '''        
    t[0]=t[1]




def p_finisnt(t):#para recuperacion de error con ; y aqui se define si el ; es opcional
    '''
    finisnt : pyc
    | 
             
    '''
    t[0]=None #ERROR '' no None

def p_finCMP(t):#para recuperacion de error con ; y aqui se define si el ; es opcional
    '''
    finCMP : END pyc
            | 
             
    '''
    t[0]=None #ERROR '' no None


#produccion para recuperarme de errores sintacticos++++++++++++++++++
def p_instruccion_error(t):
    'instruccion : error pyc'

    #print(">> ayudo el aux XD a recuperarme del error <<")

    errores.append(Excepcion("Sintactico","Error sintactico: "+str(t[1].value),t.lineno(1), find_column(input,t.slice[1])) )    
    t[0]=''





def p_imprimir(t):# va PRINT y no print porq lo q va despues de : es el token
    '''
    imprimir : RPRINT pizq expresionPrint pder
             | RPRINTLN pizq expresionPrint pder
    '''
    if t[1]=="print":
        t[0]= Imprimir(t[3],t.lineno(1),find_column(input,t.slice[1]),0)  
    else:
        t[0]= Imprimir(t[3],t.lineno(1),find_column(input,t.slice[1]),1)  


def p_imprimir2(t):# va PRINT y no print porq lo q va despues de : es el token
    '''
    imprimir : RPRINT pizq ListaPrints pder
             | RPRINTLN pizq ListaPrints pder
    '''
    if t[1]=="print":
        t[0]= Imprimir(t[3],t.lineno(1),find_column(input,t.slice[1]),0)  
    else:
        t[0]= Imprimir(t[3],t.lineno(1),find_column(input,t.slice[1]),1) 


def p_ListaPrint(t):
    '''
    ListaPrints : ListaPrints coma ListaPrint
    '''
    t[1].append(t[3])#paso la param a su hermano params [2]
    t[0]=t[1]#params padre le paso todas las params


def p_ListaPrint2(t):
    '''
    ListaPrints : ListaPrint
    '''
    t[0]=[t[1]]

def p_ListaPrint3(t):
    '''
    ListaPrint : expresionPrint
    '''
    t[0]=t[1]


#@@@@@@@@@@@@@@@@@@@@
def p_expresionPrint_binaria(t):
    '''
    expresionPrint : expresionPrint mas expresionPrint
                    | expresionPrint menos expresionPrint
                    | expresionPrint multiplicacion expresionPrint
                    | expresionPrint division expresionPrint

                    | expresionPrint modular expresionPrint
                    | expresionPrint potencia expresionPrint


                    | expresionPrint igual2 expresionPrint
                    
                    | expresionPrint notigual expresionPrint
                    
                    | expresionPrint menor expresionPrint
                    | expresionPrint mayor expresionPrint
                    | expresionPrint menorigual expresionPrint
                    | expresionPrint mayorigual expresionPrint
                    | expresionPrint and expresionPrint
                    | expresionPrint or expresionPrint
                
    '''

    #porq en lineno y slice coloco 2 y no 1 debido a que en 2 osea el mas y menos son los primeros T q tengo sino F
    if t[2] == '+':
        t[0]=Aritmetica(operador_aritmetico.MAS,t[1],t[3],t.lineno(2), find_column(input,t.slice[2]))

    elif t[2] == '-':
        t[0]=Aritmetica(operador_aritmetico.MENOS,t[1],t[3],t.lineno(2), find_column(input,t.slice[2]))

    elif t[2] == '*':
        t[0]=Aritmetica(operador_aritmetico.POR,t[1],t[3],t.lineno(2), find_column(input,t.slice[2]))

    elif t[2] == '/':
        t[0]=Aritmetica(operador_aritmetico.DIV,t[1],t[3],t.lineno(2), find_column(input,t.slice[2]))    

    elif t[2] == '^':
        t[0]=Aritmetica(operador_aritmetico.POTENCIA,t[1],t[3],t.lineno(2), find_column(input,t.slice[2]))  

    elif t[2] == '%':
        t[0]=Aritmetica(operador_aritmetico.MODULO,t[1],t[3],t.lineno(2), find_column(input,t.slice[2]))  

        #********************    FALTAN LAS DEMAS OPERAICONES     ********************

#--------------------------------
    elif t[2] == '==':
        t[0]=Relacional(operador_relacional.IGUALIGUAL,t[1],t[3],t.lineno(2), find_column(input,t.slice[2]))

    elif t[2] == '!=':
        t[0]=Relacional(operador_relacional.DIFERENTE,t[1],t[3],t.lineno(2), find_column(input,t.slice[2]))        

    elif t[2] == '<':
        t[0]=Relacional(operador_relacional.MENOR,t[1],t[3],t.lineno(2), find_column(input,t.slice[2]))

    elif t[2] == '>':
        t[0]=Relacional(operador_relacional.MAYOR,t[1],t[3],t.lineno(2), find_column(input,t.slice[2]))

    elif t[2] == '<=':
        t[0]=Relacional(operador_relacional.MENORQUE,t[1],t[3],t.lineno(2), find_column(input,t.slice[2]))

    elif t[2] == '>=':
        t[0]=Relacional(operador_relacional.MAYORQUE,t[1],t[3],t.lineno(2), find_column(input,t.slice[2]))
#--------------------------------
    elif t[2] == '&&':
        t[0]=Logica(operador_logico.AND,t[1],t[3],t.lineno(2), find_column(input,t.slice[2]))

    elif t[2] == '||':
        t[0]=Logica(operador_logico.OR,t[1],t[3],t.lineno(2), find_column(input,t.slice[2]))

    #elif t[2] == ',':
        




#@@@@@@@@@@@@@@@@@@@@
def p_expresionPrint_unaria(t):
    '''
    expresionPrint :  menos expresionPrint   %prec negativo
                   | not expresionPrint   %prec negado
    '''
    if t[1] == '-':
        t[0]=Aritmetica(operador_aritmetico.UMENOS,t[2],None,t.lineno(1), find_column(input,t.slice[1]))
    
    elif t[1] == '!':
        t[0]=Logica(operador_logico.NOT,t[2],None,t.lineno(1), find_column(input,t.slice[1]))



def p_expresionPrint_AGRUPACION(t):
    '''
    expresionPrint : pizq expresionPrint pder
    '''  
    t[0]=t[2]#solo se lleva el valor q nos importa


def p_expresionPrint_entero(t):
    '''
    expresionPrint : entero
    '''
    t[0]= Primitivos(tipo.ENTERO,t[1],t.lineno(1),find_column(input,t.slice[1]))#funcion_instruccion


def p_expresionPrint_decimal(t):
    '''
    expresionPrint : decimal
    '''
    t[0]= Primitivos(tipo.DECIMAL,t[1],t.lineno(1),find_column(input,t.slice[1]))

   
def p_expresionPrint_cadena(t):
    '''
    expresionPrint : cadena
    '''
    t[0]= Primitivos(tipo.CADENA,str(t[1]).replace('\\n','\n'),t.lineno(1),find_column(input,t.slice[1]))


def p_expresionPrint_char(t):
    '''
    expresionPrint : character
    '''
    t[0]= Primitivos(tipo.CHARACTER,str(t[1]).replace('\\n','\n'),t.lineno(1),find_column(input,t.slice[1]))


#true o false ya agregados

def p_expresionPrint_booleano(t):#arreglado :D
    '''
    expresionPrint : RFALSE
                    | RTRUE
                    | RNOTHING
                    | RNOTHING2
                   
    '''
    if t[1]=='true':
        t[0]= Primitivos(tipo.BOOLEANO,True, t.lineno(1), find_column(input,t.slice[1]))

    elif t[1]=='false': 
        t[0]= Primitivos(tipo.BOOLEANO,False, t.lineno(1), find_column(input,t.slice[1]))
    else:
        t[0]= Primitivos(tipo.NULO,None, t.lineno(1), find_column(input,t.slice[1]))








#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    







#IMPORTANTE----- video 6
#PARA OBTENER EL VALOR DE UNA VARIABLE DECLARADA AFF=90::INT64 OBTENEMOS EL 90
def p_expresionPrint_Identificador(t):
    '''
    expresionPrint : id
    '''
    t[0]= Identificador(t[1],t.lineno(1),find_column(input,t.slice[1]))#con ayuda el id lo obtenemos en la tabla de simbolos


def p_expresionPrint_IdentificadorGlobalLocal(t):
    '''
    globalLocal : GLOBAL id
                   | LOCAL id
    '''
    t[0]= Identificador(t[2],t.lineno(1),find_column(input,t.slice[1]))#con ayuda el id lo obtenemos en la tabla de simbolos

def p_expresionPrint_IdentificadorGlobalLocal2(t):
    '''
    globalLocal2 : GLOBAL id igual expresionPrint
                   | LOCAL id igual expresionPrint
    '''
    t[0]= Asignacion(t[2],t[4],t.lineno(1),find_column(input,t.slice[1]))







#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    






#**************************************************************************************************************************************************

#DECLARACION VARIABLES       ID = Expresión :: TIPO;   ||  ID = Expresión;
def p_declaracion(t):
    '''
    declaracion : id igual expresionPrint TipoAtributo
    '''
                    # tipo,id,fila,col,expresion
    t[0]= Declaracion(t[4],t[1],t.lineno(1),find_column(input,t.slice[1]),t[3])
   
    #creo q la produccion de declaracion q tiende TipoAtributo-> epsilon mejor la quito seria inalcanzable gracias a asignacion 
    #porq si no existe en la tabla lo creo y guardo en ella si existe lo edito


def p_asignacion(t):
    '''
    asignacion : id igual expresionPrint
    '''
                    # identificador , expresion, fila, columna
    t[0]= Asignacion(t[1],t[3],t.lineno(1),find_column(input,t.slice[1]))






def p_TipoAtributo(t):#creo q la produccion epsilon de TipoAtributo ya no es necesario porq ya no entraria gracias a asignacion q crea o modifica
    '''
    TipoAtributo : dp2 tipoPrimitivo
    '''
    try:
        t[0]=t[2]#enviar si es string char etc.
    except:
        
        #print("MALI11ERAADARRRR")
        t[0]=tipo.NULO 

def p_tipoPrimitivo(t):#falta array
    '''
    tipoPrimitivo : RSTRING
                | RCHAR
                | RINT64
                | RFLOAT64
                | RBOOL
                | RNOTHING
                | RNOTHING2
                | RVECTORarray
    '''
    if t[1] == 'String':
        t[0]=tipo.CADENA

    elif t[1] == 'Char':
        t[0]=tipo.CHARACTER 

    elif t[1] == 'Int64':
        t[0]=tipo.ENTERO  

    elif t[1] == 'Float64':
        t[0]=tipo.DECIMAL 

    elif t[1] == 'Bool':
        t[0]=tipo.BOOLEANO 

    elif t[1] == 'Vector':
        t[0]=tipo.ARREGLO 

    elif t[1] == 'nothing' or 'Nothing':
        t[0]=tipo.NULO 

    


    '''else:

        print(":::::::::::::::::::::::::::")
        print(str(t[1]))
        t[0]=t[1]


    elif t[1] !='' and None != ast.getStruct(t[1].identificador):

        #verifico q el tipo struct del dato exista sino F
        struct_type = ast.getStruct(t[1].identificador)
        if struct_type==None:
            print("FFFFFFFF no existe el tipo")

        t[0]=struct_type.nombre

'''





#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    






#jueves 26/8
#///////////////////////////////////////////////////////                IF              ////////////////////////////////////////////////////

def p_if1(t):#falta cerrar con end;
    '''
    if_instruccion : IF  expresionPrint  instrucciones 
              
                    
    '''
# expresion,instrucciones,instruccioneselse,NODO_IF
    t[0]= If(t[2], t[3],None,None, t.lineno(1),find_column(input,t.slice[1]))# el 1 en lineno y slice es porq es un lexema = if
    #  t[0]= If(t[2], t[3],None,None, t.lineno(1),find_column(input,t.slice[1]))# el 1 en lineno y slice es porq es un lexema = if

def p_if2(t):
    '''
    if_instruccion : IF expresionPrint instrucciones ELSE instrucciones 
                   
    '''
    t[0]= If(t[2], t[3],t[5], None ,t.lineno(1),find_column(input,t.slice[1]))# el 1 en lineno y slice es porq es un lexema = if
#  t[0]= If(t[2], t[3],t[5],None ,t.lineno(1),find_column(input,t.slice[1]))# el 1 en lineno y slice es porq es un lexema = if


def p_if3(t):#ELSE if_instruccion 
    '''
    if_instruccion : IF expresionPrint instrucciones ELSE_CONDICIONAL
                    
    '''
    t[0]= If(t[2], t[3], None, t[4],t.lineno(1), find_column(input,t.slice[1]))# el 1 en lineno y slice es porq es un lexema = if
# t[0]= If(t[2], t[3],None ,t[5] ,t.lineno(1),find_column(input,t.slice[1]))# el 1 en lineno y slice es porq es un lexema = if



#-----------------------if_instruccion : IF pizq expresionPrint pder pizq instrucciones pder ELSE if_instruccion , a t[8]-> t[9] y borrar lo de ELSEIF

#ELSEIF

def p_ifelse1(t):                                               
    '''ELSE_CONDICIONAL : if_instruccion2'''
    t[0]= t[1]


def p_if1A(t):#falta cerrar con end;
    '''
    if_instruccion2 : ELSEIF  expresionPrint instrucciones         
    '''
    t[0]= If(t[2], t[3],None,None, t.lineno(1),find_column(input,t.slice[1]))
    #  t[0]= If(t[2], t[3],None,None, t.lineno(1),find_column(input,t.slice[1]))# el 1 en lineno y slice es porq es un lexema = if


def p_if2A(t):
    '''
    if_instruccion2 : ELSEIF expresionPrint instrucciones ELSE instrucciones          
    '''
    t[0]= If(t[2], t[3],t[5], None ,t.lineno(1),find_column(input,t.slice[1]))
#  t[0]= If(t[2], t[3],t[5],None ,t.lineno(1),find_column(input,t.slice[1]))# el 1 en lineno y slice es porq es un lexema = if


def p_if3A(t):
    '''
    if_instruccion2 : ELSEIF expresionPrint instrucciones ELSE_CONDICIONAL              
    '''
    t[0]= If(t[2], t[3], None, t[4],t.lineno(1), find_column(input,t.slice[1]))
# t[0]= If(t[2], t[3],None ,t[5] ,t.lineno(1),find_column(input,t.slice[1]))# el 1 en lineno y slice es porq es un lexema = if






#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    




#///////////////////////////////////////////////////////                WHILE              ////////////////////////////////////////////////////


def p_while(t):
    '''
    while_instruccion : WHILE expresionPrint instrucciones
    '''
                    # condicion , instruccion, fila, columna
    t[0]= While(t[2],t[3],t.lineno(1),find_column(input,t.slice[1]))

#///////////////////////////////////////////             FOR CASO      for i in 1:4        ////////////////////////////////////////////////////


def p_for1(t):
    '''
    for_instruccion : RFOR expresionPrint RestoCondicionFor instrucciones
    '''
                    # condicion,condicion2 , instruccion, fila, columna 
    t[0]= For(t[2],t[3],t[4],t.lineno(1),find_column(input,t.slice[1]))


#///////////////////////////////////////////             FOR CASO      for i in "cadena"        ////////////////////////////////////////////////////
def p_for_cuerpo(t):
    '''
    RestoCondicionFor : RIN expresionPrint
    '''
    t[0]={'inicio_for':None,'fin_for':None,'forString':t[2]}



#///////////////////////////////////////////             FOR CASO      for i in 1:4        ////////////////////////////////////////////////////
def p_for_cuerpo2(t):
    '''
    RestoCondicionFor : RIN expresionPrint dp1 expresionPrint
    '''
    t[0]={'inicio_for':t[2],'fin_for':t[4],'forString':None}





#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    





#break

def p_while_break(t):
    '''
    break_instruccion : BREAK
    '''
                    #  fila, columna
    t[0]= Break(t.lineno(1),find_column(input,t.slice[1]))


#continue

def p_while_continue(t):
    '''
    continue_instruccion : CONTINUE
    '''
                    #  fila, columna
    t[0]= Continue(t.lineno(1),find_column(input,t.slice[1]))








#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    



def p_tipoRetFunc(t):
    '''
    TIPO_RET : TipoAtributo
             | 
    '''
    try:
        t[0]=t[1]
    except :
        t[0]=tipo.ENTERO



#///////////////////////////////////////////////////////              FUNCION con PARAMS y void             ////////////////////////////////////////////////////

def p_funcion_instruccion(t):#falta cerrar con end y adaptarla a JULIA hecho ya
    '''
    funcion_instruccion : FUNCTION id pizq parametros pder TIPO_RET instrucciones               
    '''
    t[0]= FuncionSP(t[6],t[2],t[4],t[7],t.lineno(1),find_column(input,t.slice[1]))



#///////////////////////////////////////////////////////              FUNCION SIN PARAMS y void             ////////////////////////////////////////////////////

def p_funcion_instruccion2(t):#falta cerrar con end y adaptarla a JULIA hecho ya
    '''
    funcion_instruccion : FUNCTION id pizq pder TIPO_RET instrucciones               
    '''
    t[0]= FuncionSP(t[5],t[2],[],t[6],t.lineno(1),find_column(input,t.slice[1]))






#///////////////////////////////////////////////////////              PARAMETROS            ////////////////////////////////////////////////////

def p_parametros_1(t):
    '''
    parametros : parametros coma parametro        
    '''
    t[1].append(t[3])#paso la param a su hermano params [2]
    t[0]=t[1]#params padre le paso todas las params


def p_parametros_2(t):
    '''
    parametros : parametro
    '''
    t[0]=[t[1]]#le meto a la lista de instrucciones una instruccion mas


#///////////////////////////////////////////////////////              PARAMETRO(corregir a version JULIA)           ////////////////////////////////////////////////////

def p_parametro(t):
    '''
    parametro : id dp2 tipoPrimitivo      
    '''
    t[0] = {'tipo':t[3], 'identificador':t[1] }#lista con este objeto de param ordenado


def p_parametro2(t):
    '''
    parametro : id       
    '''
    t[0] = {'tipo':tipo.NULO, 'identificador':t[1] }#lista con este objeto de param ordenado



def p_parametro3(t):#caso de que el param sea tipo OBJETO=STRUCT
    '''
    parametro : id dp2 id      
    '''
    t[0] = {'tipo':t[3], 'identificador':t[1] }#lista con este objeto de param ordenado


#///////////////////////////////////////////////////////              LLAMADA FUNCION SIN PARAMS             ////////////////////////////////////////////////////

def p_llamadaFuncion_SinParams(t):
    '''
    llamada_funcion : id pizq pder               
    '''
    #como id es un Terminal va 1 en slice,lineno
    t[0]= LlamadaFuncion(t[1],[],t.lineno(1),find_column(input,t.slice[1]))



#///////////////////////////////////////////////////////              LLAMADA FUNCION con PARAMS             ////////////////////////////////////////////////////

def p_llamadaFuncion_ConParams(t):
    '''
    llamada_funcion : id pizq parametros_llamada pder               
    '''
    #como id es un Terminal va 1 en slice,lineno
    t[0]= LlamadaFuncion(t[1],t[3],t.lineno(1),find_column(input,t.slice[1]))



#///////////////////////////////////////////////////////              PARAMETROS            ////////////////////////////////////////////////////

def p_parametrosLLAMADA_1(t):
    '''
    parametros_llamada : parametros_llamada coma parametroLLAMDA       
    '''
    t[1].append(t[3])#paso la param a su hermano params [2]
    t[0]=t[1]#params padre le paso todas las params


def p_parametrosLLAMADA_2(t):
    '''
    parametros_llamada : parametroLLAMDA
    '''
    t[0]=[t[1]]#le meto a la lista de instrucciones una instruccion mas


#///////////////////////////////////////////////////////              PARAMETRO(corregir a version JULIA)           ////////////////////////////////////////////////////

def p_parametroLLAMADA(t):
    '''
    parametroLLAMDA : expresionPrint       
    '''
    t[0] = t[1]




#///////////////////////////////////////////////////////              RETURN            ////////////////////////////////////////////////////

def p_returnInstruccion(t):
    '''
    return_instruccion : RETURN expresionPrint             
    '''
    #como id es un Terminal va 1 en slice,lineno
    t[0]= Return(t[2],t.lineno(1),find_column(input,t.slice[1]))#SOLO OJO PORQ SE PUEDE RETORNAR nothing creo

    '''
    """
    return_instruccion : RETURN expresionPrint    
    | RETURN 
    """ 

    try:
        t[0]= Return(t[2],t.lineno(1),find_column(input,t.slice[1]))


    catch:
        t[0]= Return(None,t.lineno(1),find_column(input,t.slice[1]))#SOLO OJO PORQ SE PUEDE RETORNAR nothing creo
    '''



def p_expresion_llamada(p):#para q los print(llamadaFuncion()); se pueda dar
    '''
    expresionPrint : creacion_struct_inst pyc
                   | llamada_funcion
                    
                   
                    
    '''
    if (len(p) == 3):
        p[0]=p[1]
    elif (len(p) == 2):
        p[0]=p[1]



#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    








#///////////////////////////////////////////////////////              LOG                   ////////////////////////////////////////////////////

def p_log(t):
    '''
    expresionPrint : LOG pizq expresionPrint coma expresionPrint pder
    '''
    #          base,num
    t[0] = Log(t[3],t[5],t.lineno(1),find_column(input,t.slice[1]))#hacer


#///////////////////////////////////////////////////////              LOG10              ////////////////////////////////////////////////////


def p_log10(t):
    '''
    expresionPrint : LOG10 pizq expresionPrint pder
    '''
    #          num
    t[0] = Log10(t[3],t.lineno(1),find_column(input,t.slice[1]))#hacer


#///////////////////////////////////////////////////////              SQRT              ////////////////////////////////////////////////////

def p_RaizCuadrada(t):
    '''
    expresionPrint : SQRT pizq expresionPrint pder
    '''
    #          num
    t[0] = Raiz(t[3],t.lineno(1),find_column(input,t.slice[1]))#hacer


#///////////////////////////////////////////////////////              SIN                ////////////////////////////////////////////////////

def p_Seno(t):
    '''
    expresionPrint : SIN pizq expresionPrint pder
    '''
    #          num
    t[0] = Seno(t[3],t.lineno(1),find_column(input,t.slice[1]))#hacer




#///////////////////////////////////////////////////////              COS               ////////////////////////////////////////////////////

def p_Coseno(t):
    '''
    expresionPrint : COS pizq expresionPrint pder
    '''
    #          num
    t[0] = Coseno(t[3],t.lineno(1),find_column(input,t.slice[1]))#hacer

#///////////////////////////////////////////////////////              TAN              ////////////////////////////////////////////////////

def p_Tangente(t):
    '''
    expresionPrint : TAN pizq expresionPrint pder
    '''
    #          num
    t[0] = Tangente(t[3],t.lineno(1),find_column(input,t.slice[1]))#hacer


#///////////////////////////////////////////////////////              PARSER           ////////////////////////////////////////////////////

def p_parser(t):
    '''
    expresionPrint : PARSE pizq tipoPrimitivo coma expresionPrint pder
    '''
    #          destino,a transformar
    t[0] = Casteo(t[3],t[5],t.lineno(1),find_column(input,t.slice[1]))#hacer




#///////////////////////////////////////////////////////              TRUNC           ////////////////////////////////////////////////////

def p_trunc(t):
    '''
    expresionPrint : TRUNC pizq RINT64 coma expresionPrint pder
    '''
    #          num
    t[0] = Trunc(t[5],t.lineno(1),find_column(input,t.slice[1]))#hacer




#///////////////////////////////////////////////////////              FLOAT          ////////////////////////////////////////////////////

def p_NFfloat(t):
    '''
    expresionPrint : NFFLOAT pizq expresionPrint pder
    '''
    #          num
    t[0] = nfFloat(t[3],t.lineno(1),find_column(input,t.slice[1]))#hacer



#///////////////////////////////////////////////////////              STRING         ////////////////////////////////////////////////////

def p_NFstring(t):
    '''
    expresionPrint : NFSTRING pizq expresionPrint pder
    '''
    #          num
    t[0] = nfString(t[3],t.lineno(1),find_column(input,t.slice[1]))#hacer



#///////////////////////////////////////////////////////              TYPEOF          ////////////////////////////////////////////////////

def p_NFTypeOF(t):
    '''
    expresionPrint : TYPEOF pizq expresionPrint pder
    '''
    #          num
    t[0] = nfTypeof(t[3],t.lineno(1),find_column(input,t.slice[1]))#hacer












#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    












#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++             EPSILON        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
def p_expresionPrint_Epsilon(t):
    '''
    expresionPrint : 
    '''
    t[0]= Primitivos(tipo.NULO,None,-1,-1)#posiblemente crear aqui el epsilon como tipo primitivo









#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    






#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                 ARRAYS   V1.0 con ASIGNACION SE AYUDA....      ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   
def p_creacionArray2(t):
    '''
     expresionPrint : corizq lista_array corder
    '''
    t[0]= Primitivos(tipo.ARREGLO,t[2],t.lineno(1),find_column(input,t.slice[1]))#posiblemente crear aqui el epsilon como tipo primitivo
#@@@
   


#///////////////////////////////////////////////////////              LISTA ITEMS EN ARRAY            ////////////////////////////////////////////////////

def p_listaArray(t):
    '''
    lista_array : lista_array coma itemArray      
    '''
    t[1].append(t[3])#paso la param a su hermano params [2]
    t[0]=t[1]#params padre le paso todas las params


def p_listaArray2(t):
    '''
    lista_array : itemArray  
    '''
    t[0]=[t[1]]#le meto a la lista de instrucciones una instruccion mas


#///////////////////////////////////////////////////////              ITEM EN ARRAY           ////////////////////////////////////////////////////

def p_listaArray3(t):
    '''
    itemArray   : expresionPrint       
    '''
    t[0] = t[1]


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    






#////////////////////////////////////////////////////////////   ACCEDER A ARRAY     /////////////////////////////////////////////////    

def p_FlistaArrayAccessxcxcxcx(t):
    '''
    declaracionArray : id ListaDimensiones igual expresionPrint
    '''
    t[0]=DeclaracionArray(t[1],t[2],t[4],t.lineno(3),find_column(input,t.slice[3]))

#////////////////////////////////////////////////////////////   ACCEDER A ARRAY     /////////////////////////////////////////////////    

def p_FlistaArrayAccess2(t):
    '''
    ListaDimensiones : ListaDimensiones Dimension
    '''
    t[1].append(t[2])
    t[0]=t[1]



def p_FlistaArrayAccess3(t):
    '''
    ListaDimensiones : Dimension
    '''
    t[0]=[t[1]]

def p_FlistaArrayAccess4(t):
    '''
    Dimension : corizq expresionPrint corder
    '''
    t[0]=t[2]





#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    





#////////////////////////////////////////////////////////////   ACCEDER A ARRAY     /////////////////////////////////////////////////    
def p_imprimirArraysporEXP(t):
    '''
    expresionPrint : declaracionArray2
    '''
    t[0]=t[1]


def p_FlistaArrayAccessVER(t):
    '''
    declaracionArray2 : id ListaDimensiones
    '''
    t[0]=LLamarArray(t[1],t[2],t.lineno(1),find_column(input,t.slice[1]))



    

#////////////////////////////////////////////////////////////   ACCEDER A ARRAY     /////////////////////////////////////////////////    


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    





#///////////////////////////////////////////////////////              ARRAY.PUSH            ////////////////////////////////////////////////////
'''
arr = [1,2,3,4,5,6];
push!(arr,7); # arr = [1,2,3,4,5,6,7]
'''

def p_array_push(t):
    '''
    push_inst : PUSH not pizq id coma expresionPrint pder      
    '''
    #como id es un Terminal va 1 en slice,lineno
    t[0]= Push(t[4],t[6],t.lineno(1),find_column(input,t.slice[1]))





#///////////////////////////////////////////////////////              ARRAY.POP           ////////////////////////////////////////////////////
'''
arr = [1,2,3,4,5,6];
pop!(arr); # arr = [1,2,3,4,5,6] y devolver 7
'''

def p_array_pop(t):
    '''
    pop_inst : POP not pizq id pder      
    '''
    #como id es un Terminal va 1 en slice,lineno
    t[0]= Pop(t[4],t[4],t.lineno(1),find_column(input,t.slice[1]))


#///////////////////////////////////////////////////////               ARRAY.LENGHT ESTA EN NATIVAS             ////////////////////////////////////////////////////


def p_array_lengthAAAA(t):
    '''
    expresionPrint : funcion_instruccion
    '''
    t[0]=t[1]






#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    




def p_clasesNoMutables(t):
    '''
    structs_instr : STRUCT id cuerpoSTRUCT
    '''
    #           id,cuerpo,tipo,fila,columna
    t[0]=Struct(t[2],t[3],0,t.lineno(1),find_column(input,t.slice[1]))


def p_clasesMutables(t):
    '''
    structs_instr : MUTABLE STRUCT id cuerpoSTRUCT
    '''
    #           id,cuerpo,tipo,fila,columna
    t[0]=Struct(t[3],t[4],1,t.lineno(1),find_column(input,t.slice[1]))



#///////////////////////////////////////////////////////              CREACION STRUCT con PARAMS             ////////////////////////////////////////////////////

def p_creacionStruct_ConParams(t):
    '''
    creacion_struct_inst : id pizq parametros_structs pder             
    '''
    #como id es un Terminal va 1 en slice,lineno

    #if t[1]!='length':
    t[0]= LlamadaStruct(t[1],t[3],t.lineno(1),find_column(input,t.slice[1]))
    #else:
        #p_array_lengthAAAA(t)


#///////////////////////////////////////////////////////              PARAMETROS            ////////////////////////////////////////////////////

def p_parametrosLLAMADA_1_structs(t):
    '''
    parametros_structs : parametros_structs coma parametroLLAMDA_structs       
    '''
    t[1].append(t[3])#paso la param a su hermano params [2]
    t[0]=t[1]#params padre le paso todas las params


def p_parametrosLLAMADA_2_structs(t):
    '''
    parametros_structs : parametroLLAMDA_structs
    '''
    t[0]=[t[1]]#le meto a la lista de instrucciones una instruccion mas


#///////////////////////////////////////////////////////              PARAMETRO(corregir a version JULIA)           ////////////////////////////////////////////////////

def p_parametroLLAMADA_structs(t):
    '''
    parametroLLAMDA_structs : expresionPrint       
    '''
    t[0] = t[1]








def p_cuerpoStructNM(t):
    '''
    cuerpoSTRUCT : cuerpoSTRUCT instruccion_STRUCT
    '''
    t[1].append(t[2])#paso la param a su hermano params [2]
    t[0]=t[1]#params padre le paso todas las params


def p_cuerpoStructNM1(t):
    '''
    cuerpoSTRUCT : instruccion_STRUCT
    '''
    t[0]=[t[1]]

def p_cuerpoStructNM2(t):
    '''
    instruccion_STRUCT : declaracionSTRUCT
    '''
    t[0]=t[1]
    
#***************************************************************      CREACION DE ATRIBUTOS EN STRUCT      *******************************************************************


def p_declaracionSTRUCT(t):
    '''
    declaracionSTRUCT : id heroku finisnt
    '''
                    # tipo,id,fila,col,expresion
    t[0]= Declaracion(t[2],t[1],t.lineno(1),find_column(input,t.slice[1]),None)
   

def p_declaracionSTRUCT_TYPEO(t):
    '''
    heroku : TipoAtributo
    '''

    t[0]=t[1]
    
def p_declaracionSTRUCT_TYPEO2(t):
    '''
    heroku : dp2 id
    '''
    t[0]=t[2]


def p_declaracionSTRUCT_TYPEO3(t):
    '''
    heroku : 
    '''
    t[0]=tipo.NULO


#///////////////////////////////////////////////////////              ACCESO A ATRIBUTOS DE UN STRUCT            ////////////////////////////////////////////////////



def p_Struct_acceso_atributos(t):
    '''
    expresionPrint : Struct_atributo
    '''
    t[0]=t[1]

def p_Struct_acceso_atributos1(t):
    '''
    Struct_atributo : id punto id
    '''
    #                 struct,atributo
    t[0]=StructAccesoAtributos(t[1],t[3],t.lineno(2),find_column(input,t.slice[2]))#con ayuda el id lo obtenemos en la tabla de simbolos



def p_Struct_acceso_atributos2(t):
    '''
    Struct_atributo : id punto id igual expresionPrint finisnt
    '''
    #                 struct,atributo
    t[0]=StructCambioAtributos(t[1],t[3],t[5],t.lineno(2),find_column(input,t.slice[2]))#con ayuda el id lo obtenemos en la tabla de simbolos


#obligatoria para recuperarme de error
##error (DEFINIDA POR PLY)  SINTACTICOS

#OJO GRACIAS A ESTO NO ENTRABA EN EL ELSEIF
#def p_error(t):
 #   print('error sintactico en la [linea '+str(t.lexer.lineno) +" y columna "+str(find_column(input,t))+ '] error '+str(t.value) )
    #errores.append(Excepcion("Sintactico","Error sintactico: "+t.value[0],t.lexer.lineno, find_column(input,t)))
    



import ply.yacc as yacc
parser = yacc.yacc()




def getErrores():
    return errores

def ParseJV(inpuuut):
    global errores
    global lexer
    global parser
    errores=[]#reset
    lexer = lex.lex()#reset
    parser = yacc.yacc()#reset
    global input
    input=inpuuut
    #print("---------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>"+str(len(errores)))
    return parser.parse(inpuuut, lexer=lexer)



#VIDEO 13 DE COMO HACER FUNCIONES NATIVAS ~ ~ ~ ~
#PARA FUNCIONES NATIVAS-----------------     creacion de funciones nativas
#QUITAR TOKENS DE SIN,COS,TAN ETC.
def crearNativas(ast):#no tocara la gramatica sino el flujo
    nombre0 = "uppercase"
    parametros0 = [{'tipo':tipo.CADENA, 'identificador':'toUpper##Param1' } ]
    #si queremos otro param seria asi
    #parametros = [{'tipo':tipo.CADENA, 'identificador':'toUpper##Param1' }, {'tipo':tipo.CADENA, 'identificador':'toUpper##Param1' }  ]
    instrucciones0 = []#como heredan de funcion las tenemos q poner pero vacias porq no tienen nada para funciones NATIVAS

    uppercase = Uppercase(nombre0,parametros0,instrucciones0,-1,-1)#se ponen -1 en fila y col porq esto nos va a indicar q es una nativa
    ast.addFuncion(uppercase) #guardamos ahora en el ast la funcion nativa recien hecha

    
    nombre1 = "lowercase"
    parametros1 = [{'tipo':tipo.CADENA, 'identificador':'toLower##Param1' } ]
    #si queremos otro param seria asi
    #parametros = [{'tipo':tipo.CADENA, 'identificador':'toUpper##Param1' }, {'tipo':tipo.CADENA, 'identificador':'toUpper##Param1' }  ]
    instrucciones1 = []#como heredan de funcion las tenemos q poner pero vacias porq no tienen nada para funciones NATIVAS

    lowercase = Lowercase(nombre1,parametros1,instrucciones1,-1,-1)#se ponen -1 en fila y col porq esto nos va a indicar q es una nativa
    ast.addFuncion(lowercase) #guardamos ahora en el ast la funcion nativa recien hecha


    nombre1 = "length"
    parametros1 = [{'tipo':tipo.ARREGLO, 'identificador':'longitudArray##Param1' } ]
    #si queremos otro param seria asi
    #parametros = [{'tipo':tipo.CADENA, 'identificador':'toUpper##Param1' }, {'tipo':tipo.CADENA, 'identificador':'toUpper##Param1' }  ]
    instrucciones1 = []#como heredan de funcion las tenemos q poner pero vacias porq no tienen nada para funciones NATIVAS

    lowercase = Length(nombre1,parametros1,instrucciones1,-1,-1)#se ponen -1 en fila y col porq esto nos va a indicar q es una nativa
    ast.addFuncion(lowercase) #guardamos ahora en el ast la funcion nativa recien hecha



    print("FUNCIONES NATIVAS ON")
#PARA PARSER HICE UNA PRODUCCION PORQ AHI NECEISTABA (DESTINO,FUENTE) p_parser buscar








'''
#aqui viene mi flujo de trabajo *****************       KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK
#KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK
#KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK

#print(str(pow(2,300000)))

print()




from TS.Entorno import TablaSimbolosV2

from TS.Generador import Generator


f = open("./entrada1.txt","r")
entrada = f.read()
#print(input)#imprimo el txt
#ply------------------
print("--------------------------------------INICIO----------------------------------")
#parser.parse(entrada)




#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#creo el generador de c3d++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#                                                        ____________
#                                    (`-..________....---''  ____..._.-`
#                                    \\`._______.._,.---''     ,'
#                                    ; )`.      __..-'`-.      /
#                                    / /     _.-' _,.;;._ `-._,'
#                                    / /   ,-' _.-'  //   ``--._``._
#                                ,','_.-' ,-' _.- (( =-    -. `-._`-._____
#                                ,;.''__..-'   _..--.\\.--'````--.._``-.`-._`.
#                _          |\,' .-''        ```-'`---'`-...__,._  ``-.`-.`-.`.
#    _     _.-,'(__)\__)\-'' `     ___  .          `     \      `--._
#    ,',)---' /|)          `     `      ``-.   `     /     /     `     `-.
#    \_____--.  '`  `               __..-.  \     . (   < _...-----..._   `.
#    \_,--..__. \\ .-`.\----'';``,..-.__ \  \      ,`_. `.,-'`--'`---''`.  )
#            `.\`.\  `_.-..' ,'   _,-..'  /..,-''(, ,' ; ( _______`___..'__
#                    ((,(,__(    ((,(,__,'  ``'-- `'`.(\  `.,..______   SSt
#    
genAux = Generator()
genAux.ResetC3D()
generator = genAux.getInstance()


#TSGlobalP2 = TablaSimbolosV2()#para q funcione todo sino F es un entorno OPTIMO DONDE ESTA TANTO FUNCIONES Y TS COMO STRUCTS EN 1


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




instrucciones = ParseJV(entrada+"\n")#obtengo el arbol ast      aqui se ejecuta PLY
ast = Arbol(instrucciones)
TSGlobal = TablaSimbolos()
ast.setTablaSimbolosGlobal(TSGlobal)





#PARA TODAS LAS FUNCIONES NATIVAS--------------------------------------
crearNativas(ast)
#-----------------------------------------------------------------------



#captura de errores lexicos y sintacticos y los meto al AST----------------------------
#pasada de errores
print("\nERRORES LEXICOS Y SINTACTICOS metidos al AST")
for error in errores:#scanner y parser errores
    ast.getExcepciones().append(error)
    #ast.updateConsola(error.toString(),1)
#------------------------------------------------------------------------------------

print("\n\n__________________________________________________pasadas")



# pasada para recolectar solo los structs
for struct in ast.getInstrucciones():
    
        if isinstance(struct,Struct):#si detecto una funcion la meto a la lista de funciones del AST
           ast.addStruct(struct) 

#[quitar commit ESTA ES LA ORIGINAL JULIA VERSION]
#$$$$$$$$$$$$$$$$$$$$$$$$$$$#$$$$$$$$$$$$$$$$$$$$$$$$$$$#$$$$$$$$$$$$$$$$$$$$$$$$$$$#$$$$$$$$$$$$$$$$$$$$$$$$$$$#$$$$$$$$$$$$$$$$$$$$$$$$$$$#$$$$$$$$$$$$$$$$$$$$$$$$$$$
# pasada para recolectar solo las funciones
for instruccion in ast.getInstrucciones():

        if isinstance(instruccion,FuncionSP):#si detecto una funcion la meto a la lista de funciones del AST
           ast.addFuncion(instruccion) 
                  
#--------------------------------------------------------------------------------------------------------------------------------------------


#video 10 min 43 poner atencion acerca de las funciones y las pasadas para guardar en el AST
         
#ESTA ES 2nda PASADA OJO AL ENUNCIADO CON JULIA
#******** PASADA DE DECLARACIONES Y ASIGNACIONES ********
for instruccion in ast.getInstrucciones():#parser y realizar lo que van entre print ( expresionPrint )

    if not isinstance(instruccion,FuncionSP) and not isinstance(instruccion,Struct):#si NO detecto una funcion ,tonces las interpreto 
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    
#                                                        ____________
#                                    (`-..________....---''  ____..._.-`
#                                    \\`._______.._,.---''     ,'
#                                    ; )`.      __..-'`-.      /
#                                    / /     _.-' _,.;;._ `-._,'
#                                    / /   ,-' _.-'  //   ``--._``._
#                                ,','_.-' ,-' _.- (( =-    -. `-._`-._____
#                                ,;.''__..-'   _..--.\\.--'````--.._``-.`-._`.
#                _          |\,' .-''        ```-'`---'`-...__,._  ``-.`-.`-.`.
#    _     _.-,'(__)\__)\-'' `     ___  .          `     \      `--._
#    ,',)---' /|)          `     `      ``-.   `     /     /     `     `-.
#    \_____--.  '`  `               __..-.  \     . (   < _...-----..._   `.
#    \_,--..__. \\ .-`.\----'';``,..-.__ \  \      ,`_. `.,-'`--'`---''`.  )
#            `.\`.\  `_.-..' ,'   _,-..'  /..,-''(, ,' ; ( _______`___..'__
#                    ((,(,__(    ((,(,__,'  ``'-- `'`.(\  `.,..______   SSt
#                                                        ``--------..._``--.__


        generator.addCommit("-------------INICIO INSTRUCCION-----------------")
        value=instruccion.compilar(ast,TSGlobal)# >>>>>>>>>>>>>>>>>>> punto donde defino si es proyecto 1 o 2 OLC2 <<<<<<<<<<<<<<<<<<<<<<<<<<<
        #value=instruccion.compilar(ast,TSGlobal,TSGlobalP2)# >>>>>>>>>>>>>>>>>>> punto donde defino si es proyecto 1 o 2 OLC2 <<<<<<<<<<<<<<<<<<<<<<<<<<<

        #aqui ya previamente cree el GENERATOR ESTE ME GURADARA TODO
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        
        if isinstance(value, Excepcion):
            ast.getExcepciones().append(value)
            #ast.updateConsola(value.toString(),1)

        if isinstance(value, Break):#para detectar los breaks como error afuera de whiles, falta continue y return
            error = Excepcion("Semantico","Error semantico break fuera de ciclo",instruccion.fila,instruccion.columna)
            ast.getExcepciones().append(error)#agregamos el error
            #ast.updateConsola(error.toString(),1)#e imprimimos 


        if isinstance(value, Continue):#para detectar los breaks como error afuera de whiles, falta continue y return
            error = Excepcion("Semantico","Error semantico continue fuera de ciclo",instruccion.fila,instruccion.columna)
            ast.getExcepciones().append(error)#agregamos el error
            #ast.updateConsola(error.toString(),1)#e imprimimos 


        if isinstance(value, Return):#para detectar los return como error afuera de whiles,funciones etc. falta continue
            error = Excepcion("Semantico","Error semantico return fuera de ciclo o funcion",instruccion.fila,instruccion.columna)
            ast.getExcepciones().append(error)#agregamos el error
            #ast.updateConsola(error.toString(),1)#e imprimimos 
            
#$$$$$$$$$$$$$$$$$$$$$$$$$$$#$$$$$$$$$$$$$$$$$$$$$$$$$$$#$$$$$$$$$$$$$$$$$$$$$$$$$$$#$$$$$$$$$$$$$$$$$$$$$$$$$$$#$$$$$$$$$$$$$$$$$$$$$$$$$$$#$$$$$$$$$$$$$$$$$$$$$$$$$$$





#EN ESTE PUNTO YA TENDRIA TODOS LOS ERRORES EN LA TB


#ARBOL SINTACTICO--------------------------------------
init =NodoAST("RAIZ")
instr =NodoAST("INSTRUCCIONES")

for instruccio in ast.getInstrucciones():
    instr.agregarHijoNodo(instruccio.getNodo())

init.agregarHijoNodo(instr)



grafo = ast.getDot(init)#retorna el AST graphviz
dirname = os.path.dirname(__file__)#posiciono en lugar actual
direcc=os.path.join(dirname,'ast.dot')
arch = open(direcc,'w+')
arch.write(grafo)
arch.close()
#os.system("dot -T pdf -o ast.pdf ast.dot")







print("\n\n************ CONSOLA ***********")
print(ast.getConsola())
print("\n\n--------------------------------------ERRORES----------------------------------")

for excpt in  ast.getExcepciones():
    print(excpt.toString())

print("\n\n---------------------            FUNCIONES           -----------------------")
print(ast.getFunciones())


print("\n\n---------------------            STRUCTS          -----------------------")
print(ast.getStructssss())


print("\n\n--------------------------------------FIN PROGRAMA----------------------------------")
#colocar los decimales antes de los ints al igual q JISON sino F



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#                                                        ____________
#                                    (`-..________....---''  ____..._.-`
#                                    \\`._______.._,.---''     ,'
#                                    ; )`.      __..-'`-.      /
#                                    / /     _.-' _,.;;._ `-._,'
#                                    / /   ,-' _.-'  //   ``--._``._
#                                ,','_.-' ,-' _.- (( =-    -. `-._`-._____
#                                ,;.''__..-'   _..--.\\.--'````--.._``-.`-._`.
#                _          |\,' .-''        ```-'`---'`-...__,._  ``-.`-.`-.`.
#    _     _.-,'(__)\__)\-'' `     ___  .          `     \      `--._
#    ,',)---' /|)          `     `      ``-.   `     /     /     `     `-.
#    \_____--.  '`  `               __..-.  \     . (   < _...-----..._   `.
#    \_,--..__. \\ .-`.\----'';``,..-.__ \  \      ,`_. `.,-'`--'`---''`.  )
#            `.\`.\  `_.-..' ,'   _,-..'  /..,-''(, ,' ; ( _______`___..'__
#                    ((,(,__(    ((,(,__,'  ``'-- `'`.(\  `.,..______   SSt
#                                                        ``--------..._``--.__

C3D_FINAL=generator.getCodigo()
#print("====================================C3D====================================\n"+C3D_FINAL)#obtengo todo el C3D

#escribo para ejecutar en goolang sin web sino local
f2222 = open("./salida.go","w")
f2222.write(C3D_FINAL)
f2222.close()
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#from OptimizadorGram import *

f2222 = open("./salida2.txt","w")
f2222.write(C3D_FINAL)
f2222.close()






#from datetime import datetime
#now = datetime.now()
#DATE_TIME =str(now.day)+"/"+str(now.month)+"/"+str(now.year)+" "+str(now.hour)+":"+str(now.minute)
#print("\n\n\n\n"+DATE_TIME)


#'''

