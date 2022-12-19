from almacenar.error import Error
from almacenar.generador import Generador
from almacenar.tipo import Tipo
from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol

#from almacenar.error import Error
#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol

class Retorno(Instruccion):
    def __init__(self, exp,fila, columna):
        self.expresion= exp
        self.fila = fila
        self.columna = columna
        self.tipo = None
        self.expRetorno=None
        
    def compilar(self, arbol, tabla):
        #if tabla.returnLbl =='':
        #    return Error('SEMANTICO','RETURN NO VALIDO EN AMBITO ACTUAL',self.fila,self.columna)
        
        expRetorno = self.expresion.compilar(arbol,tabla)
        if isinstance(expRetorno,Error): return Error
        simbolfunc= tabla.actualfunc
        
        genAux = Generador()
        generador = genAux.getInstance()
        
        if simbolfunc == None:
            return Error("SEMANTICO","RETORNO FUERA DE AMBITO FUNCION",self.fila,self.columna)
        
        if simbolfunc.tipo == Tipo.BOOLEANO:
            tempLlb = generador.agregarLabel()
            generador.colocarLabel(expRetorno.trueLbl)
            generador.setPila('P','1')
            generador.agregarGoto(tempLlb)
            generador.colocarLabel(expRetorno.falseLbl)
            generador.setPila('P','0')
            generador.colocarLabel(tempLlb)
        
        else:
            generador.setPila('P',expRetorno.getValor())
        
        generador.agregarGoto(tabla.returnLbl)
        #agrego->->->->->->->->->
        tabla.gotoReturn= True
        #->->->->->->->->->->->->
            
    
    def getNode(self):
        nodoBreak = NodoArbol("RETURN")
        nodoBreak.agregarHijoConNodo(self.expresion.getNode())
        return nodoBreak