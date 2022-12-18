from instrucciones.funcs import Funcion
from almacenar.tipo import Tipo
from almacenar.error import Error

#from instrucciones.funcs import Funcion
#from almacenar.tipo import Tipo
#from almacenar.error import Error

class Stringgss(Funcion):
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
        pass