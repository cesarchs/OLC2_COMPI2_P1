from instrucciones.funcs import Funcion
from almacenar.tipo import Tipo
from almacenar.error import Error

#from instrucciones.funcs import Funcion
#from almacenar.tipo import Tipo
#from almacenar.error import Error
import math

class Seno(Funcion):
    def __init__(self,id,params,instrs, fila, columna):
        self.id = id
        self.parametros = params
        self.instrucciones = instrs
        self.fila = fila
        self.columna = columna
        self.tipo = Tipo.NULO
        self.struct = False
        self.mutable = False
    
    def compilar(self, arbol, tabla):
        simbolo = tabla.getSimboloEnTs("sin_#_#_#_parameter")
        if simbolo == None:return Error("SEMANTICO","NO SE ENCONTRO PARAMETRO PARA sin",self.fila,self.columna)

        try:       
            ret=math.sin(simbolo.getValor())   
            self.tipo = self.getTipo(ret)     
            return ret
        except:
            return Error("SEMANTICO","FUNCION SEN() UNICAMENTE RECIBE EXPRESION DE TIPO NUMERICO",self.fila,self.columna)
        
    def getTipo(self, val):
        if isinstance(val,int):
            return Tipo.ENTERO
        elif isinstance(val,float):
            return Tipo.DECIMAL
        elif isinstance(val,bool):
            return Tipo.BOOLEANO
        return Tipo.CADENA
        
        
class Coseno(Funcion):
    def __init__(self,id,params,instrs, fila, columna):
        self.id = id
        self.parametros = params
        self.instrucciones = instrs
        self.fila = fila
        self.columna = columna
        self.tipo = Tipo.NULO
        self.struct = False
        self.mutable = False
    
    def compilar(self, arbol, tabla):
        simbolo = tabla.getSimboloEnTs("cos_#_#_#_parameter")
        if simbolo == None:return Error("SEMANTICO","NO SE ENCONTRO PARAMETRO PARA cos",self.fila,self.columna)

        try:
            #self.tipo= simbolo.getTipo()
            ret=math.cos(simbolo.getValor())   
            self.tipo = self.getTipo(ret)     
            return ret
        except:
            return Error("SEMANTICO","FUNCION COS() UNICAMENTE RECIBE EXPRESION DE TIPO NUMERICO",self.fila,self.columna)
        
    def getTipo(self, val):
        if isinstance(val,int):
            return Tipo.ENTERO
        elif isinstance(val,float):
            return Tipo.DECIMAL
        elif isinstance(val,bool):
            return Tipo.BOOLEANO
        return Tipo.CADENA
    

class Tangente(Funcion):
    def __init__(self,id,params,instrs, fila, columna):
        self.id = id
        self.parametros = params
        self.instrucciones = instrs
        self.fila = fila
        self.columna = columna
        self.tipo = Tipo.NULO
        self.struct = False
        self.mutable = False
    
    def ejecutar(self, arbol, tabla):
        simbolo = tabla.getSimboloEnTs("tan_#_#_#_parameter")
        if simbolo == None:return Error("SEMANTICO","NO SE ENCONTRO PARAMETRO PARA tan",self.fila,self.columna)

        try:
            ret=math.tan(simbolo.getValor())   
            self.tipo = self.getTipo(ret)     
            return ret
        except:
            return Error("SEMANTICO","FUNCION TAN() UNICAMENTE RECIBE EXPRESION DE TIPO NUMERICO",self.fila,self.columna)
        
    def getTipo(self, val):
        if isinstance(val,int):
            return Tipo.ENTERO
        elif isinstance(val,float):
            return Tipo.DECIMAL
        elif isinstance(val,bool):
            return Tipo.BOOLEANO
        return Tipo.CADENA
