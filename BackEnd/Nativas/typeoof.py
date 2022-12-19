from instrucciones.funcs import Funcion
from almacenar.tipo import Tipo
from almacenar.error import Error

#from instrucciones.funcs import Funcion
#from almacenar.tipo import Tipo
#from almacenar.error import Error

class Typeoff(Funcion):
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
        simbolo = tabla.getSimboloEnTs("typeof_#_#_#_parameter")
        if simbolo == None:return Error("SEMANTICO","NO SE ENCONTRO PARAMETRO PARA typeof",self.fila,self.columna)
        
        self.tipo=Tipo.CADENA

        try:
            return self.getValor(simbolo.getTipo())
        except:
            return Error("SEMANTICO","NO SE LOGRO OBTENER EL TIPO",self.fila,self.columna)


    def getValor(self, tipo):
        if tipo == Tipo.ENTERO:
            return "Int64"
        elif tipo == Tipo.DECIMAL:
            return "Float64"
        elif tipo == Tipo.BOOLEANO:
            return "Bool"
        elif tipo == Tipo.CARACTER:
            return "Char"
        elif tipo == Tipo.CADENA:
            return "String"
        elif tipo == Tipo.NULO:
            return "Nulo"