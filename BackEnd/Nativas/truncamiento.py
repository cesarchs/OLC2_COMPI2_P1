from types import FunctionType
from almacenar.generador import Generador
from almacenar.tipo import Return, Tipo
from almacenar.error import Error
from instrucciones.funcs import Funcion
from padres.expresion import Expresion
from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol

#from almacenar.tipo import Tipo
#from almacenar.error import Error
#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol

class Trunc(Instruccion):
    def __init__(self,tipo,exp, fila, columna):
        self.tipo = tipo
        self.expresion = exp
        self.fila = fila
        self.columna = columna
        self.struct = False
        self.mutable = False
    
    def compilar(self, arbol, tabla):
        
        resultadoExp = self.expresion.compilar(arbol,tabla)#veo que es la exp
        if isinstance(resultadoExp,Error): return resultadoExp
        genAux = Generador()
        generador = genAux.getInstance()
        self.tipo=Tipo.ENTERO
        if self.expresion.tipo == Tipo.DECIMAL or self.expresion.tipo == Tipo.ENTERO:
            generador.agregarComentario("--TRUNC--")
            
            try:
                prueba = float(resultadoExp.getValor())
                num=generador.agregarTemporal()
                generador.addExp(num,prueba,'','')
                return Return(num,self.tipo,True)
            except:
                return Return(resultadoExp.getValor(),self.tipo,True)
        else:
            return Error("SEMANTICO","EXPRESION INVALIDA PARA TRUNC",self.fila,self.columna)
    
    def getValor(self, tipo, val):
        if tipo == Tipo.ENTERO:
            return int(val)
        elif tipo == Tipo.DECIMAL:
            return float(val)
        elif tipo == Tipo.BOOLEANO:
            return bool(val)
        return str(val)
    
    def getNode(self):
        nodoTRUNC = NodoArbol("TRUNC") #NOMBRE PADRE
        nodoTRUNC.agregarHijoConNodo(self.expresion.getNode())
        return nodoTRUNC
