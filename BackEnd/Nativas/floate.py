from almacenar.generador import Generador
from instrucciones.funcs import Funcion
from almacenar.tipo import Return, Tipo
from almacenar.error import Error
from padres.Nodo import NodoArbol
from padres.expresion import Expresion
from padres.instruccion import Instruccion

#from instrucciones.funcs import Funcion
#from almacenar.tipo import Tipo
#from almacenar.error import Error
class Flooaat(Instruccion):
    def __init__(self,tipo,exp,fila, columna):
        self.tipo = tipo
        self.expresion = exp
        self.fila = fila
        self.columna = columna 
        self.struct = False
        self.mutable = False
    
    def compilar(self, arbol, tabla):
        resultadoExp = self.expresion.compilar(arbol,tabla)
        if isinstance(resultadoExp,Error):return resultadoExp
        
        genAux = Generador()
        generador = genAux.getInstance()
        self.tipo = Tipo.DECIMAL
        
        if self.expresion.tipo == Tipo.DECIMAL or self.expresion.tipo == Tipo.ENTERO:
            generador.agregarComentario("--FLOAT--")
            
            try:
                prueba = float(resultadoExp.getValor())
                num=generador.agregarTemporal();generador.liberarTemporal(num)
                generador.addExp(num,prueba,'','')
                return Return(num,self.tipo,True)
            except:
                return Return(resultadoExp.getValor(),self.tipo,True)
        else:
            return Error("SEMANTICO","EXPRESION INVALIDA PARA TRUNC",self.fila,self.columna)
        
        
    def getNode(self):
        nodoTRUNC = NodoArbol("FLOAT") #NOMBRE PADRE
        nodoTRUNC.agregarHijoConNodo(self.expresion.getNode())
        return nodoTRUNC