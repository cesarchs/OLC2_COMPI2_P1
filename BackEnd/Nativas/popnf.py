from instrucciones.funcs import Funcion
from almacenar.tipo import Tipo
from almacenar.error import Error
#from instrucciones.funcs import Funcion
#from almacenar.tipo import Tipo
#from almacenar.error import Error
#
class PopArr(Funcion):
    def __init__(self,id,params, instrs,fila, columna):
        self.id = id
        self.parametros = params
        self.instrucciones = instrs
        self.fila = fila
        self.columna = columna
        self.tipo = Tipo.NULO
        self.struct = False
        self.mutable = False
    
    def compilar(self, arbol, tabla):
        simbolo = tabla.getSimboloEnTs("popsarray_#_#_#_parameter")
        if simbolo == None:return Error("SEMANTICO","NO SE ENCONTRO PARAMETRO PARA POP!",self.fila,self.columna)
        try:
            valpop=simbolo.getValor().pop()
            tipo = self.getTipo(valpop)
            self.tipo= tipo
            return valpop 
        except:
            return Error("SEMANTICO","NO SE PUEDE HACER POP! EN ARREGLO: "+str(self.id),self.fila,self.columna)
    
    def getTipo(self, val):
        if isinstance(val,int):
            return Tipo.ENTERO
        elif isinstance(val,float):
            return Tipo.DECIMAL
        elif isinstance(val,bool):
            return Tipo.BOOLEANO
        elif isinstance(val,list):
            return Tipo.ARREGLO
        return Tipo.CADENA