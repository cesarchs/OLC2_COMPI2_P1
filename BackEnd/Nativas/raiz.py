from instrucciones.funcs import Funcion
from almacenar.tipo import Tipo
from almacenar.error import Error

#from instrucciones.funcs import Funcion
#from almacenar.tipo import Tipo
#from almacenar.error import Error
import math

class Raiz(Funcion):
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
        simbolo = tabla.getSimboloEnTs("raizsqrt_#_#_#_parameter")
        if simbolo == None:return Error("SEMANTICO","NO SE ENCONTRO PARAMETRO PARA sqrt()",self.fila,self.columna)

        try:
            self.tipo= simbolo.getTipo()         
            return math.sqrt(simbolo.getValor())
        except:
            return Error("SEMANTICO","FUNCION SQRT() UNICAMENTE RECIBE EXPRESION DE TIPO NUMERICO",self.fila,self.columna)