from almacenar.error import Error
from almacenar.generador import Generador
from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol

#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol

class Break(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        
    def compilar(self, arbol, tabla):
        if tabla.breakLbl =='':
            return Error('SEMANTICO','BREAK NO VALIDO EN AMBITO ACTUAL',self.fila,self.columna)
        genAux = Generador()
        generador = genAux.getInstance()
        generador.agregarComentario("GOTO INICIO BREAK")
        
        generador.agregarGoto(tabla.breakLbl)
        
        generador.agregarComentario("GOTO FIN BREAK")
    def getNode(self):
        nodoBreak = NodoArbol("BREAK")
        return nodoBreak