
from padres.Nodo import NodoArbol
from padres.instruccion import Instruccion
from almacenar.error import Error
from almacenar.tipo import Tipo

#from padres.Nodo import NodoArbol
#from padres.instruccion import Instruccion
#from almacenar.error import Error
#from almacenar.tipo import Tipo


class Listarray(Instruccion):
    def __init__(self, exps, fila, columna):
        self.lexps=exps
        self.fila = fila
        self.tipo = Tipo.NULO #ya que las exps traen su propio tipo
        self.columna = columna
        self.struct = False
        self.mutable = False
        
    def compilar(self, arbol, tabla):
        return self.lexps
        
    def getNode(self):
        nodoRelacional = NodoArbol("ListaArray") #NOMBRE PADRE
        
        return nodoRelacional
            