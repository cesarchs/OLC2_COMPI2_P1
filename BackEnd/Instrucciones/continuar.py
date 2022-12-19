from almacenar.error import Error
from almacenar.generador import Generador
from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol

#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol

class Continue(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        
    def compilar(self, arbol, tabla):
        if tabla.continueLbl=='':
            return Error('SEMANTICO','CONTINUE NO VALIDO EN AMBITO ACTUAL',self.fila,self.columna)
        genAux = Generador()
        generador = genAux.getInstance()
        generador.agregarComentario("GOTO CONTINUE")
        generador.agregarGoto(tabla.continueLbl)
        generador.agregarComentario("GOTO FIN CONTINUE")
    
    def getNode(self):
        nodoBreak = NodoArbol("CONTINUE")
        return nodoBreak