from almacenar.generador import Generador
from instrucciones.continuar import Continue
from padres.instruccion import Instruccion
from almacenar.error import Error
from almacenar.tipo import Tipo
from almacenar.ts import TablaSimbolos
from padres.Nodo import NodoArbol
from instrucciones.breeak import Break
from instrucciones.retorn import Retorno

#from instrucciones.continuar import Continue
#from padres.instruccion import Instruccion
#from almacenar.error import Error
#from almacenar.tipo import Tipo
#from almacenar.ts import TablaSimbolos
#from padres.Nodo import NodoArbol
#from instrucciones.breeak import Break
#from instrucciones.retorn import Retorno


class Mientras(Instruccion):
    def __init__(self, exp, instrucs,fila, columna):
        self.condicion = exp
        self.instrucciones = instrucs
        self.fila = fila
        self.columna = columna
    
    def compilar(self, arbol, tabla):
        genAux = Generador()
        generador = genAux.getInstance()
        
        continueLbl = generador.agregarLabel()
        generador.agregarComentario('INICIA WHILE')
        generador.colocarLabel(continueLbl)
                       
        #while True:
        condicion = self.condicion.compilar(arbol,tabla)
        if isinstance(condicion,Error): return condicion
        
        if self.condicion.tipo == Tipo.BOOLEANO:
            
            whileTabla  = TablaSimbolos(tabla)
            whileTabla.setTsAnterior(tabla)
            arbol.agregarAListaTablas('WHILE',whileTabla)#aqui agrego la tabla generada 
            
            whileTabla.breakLbl = condicion.falseLbl
            whileTabla.continueLbl = continueLbl
            generador.colocarLabel(condicion.trueLbl)
                    
            for instruccion in self.instrucciones:
                cuerpoWhile=instruccion.compilar(arbol,whileTabla)
                if isinstance(cuerpoWhile, Error):
                    arbol.getListaErrores().append(cuerpoWhile)
                    arbol.actualizarConsola(cuerpoWhile.toString())
                if isinstance(cuerpoWhile,Retorno): return Error("SEMANTICO",'RETURN UNICAMENTE PUEDE ESTAR PRESENTE EN FUNCION',self.fila,self.columna)
                
            generador.agregarGoto(continueLbl)
            generador.colocarLabel(condicion.falseLbl)
            generador.agregarComentario('FINALIZA WHILE')
            #return
                #if isinstance(cuerpoWhile,Break): return None #sale con break dentro de ciclo que venga como instruccion
                #if isinstance(cuerpoWhile,Continue): break
                #if isinstance(cuerpoWhile,Retorno): return cuerpoWhile

        else:
            return Error("SEMANTICO", "EXPRESION NO RETORNA VALOR DE TIPO BOOL EN WHILE", self.fila,self.columna)  
    
    def getNode(self):
        nodowhile = NodoArbol("WHILE") #NOMBRE PADRE
        #PARA IF
        nodowhile.agregarHijoConNodo(self.condicion.getNode())
        instruccsWhile = NodoArbol("CUERPO WHILE")
        for instruccion in self.instrucciones: #este trae todas las instrucciones contenidas en el cuerpo del if
            instruccsWhile.agregarHijoConNodo(instruccion.getNode())
        nodowhile.agregarHijoConNodo(instruccsWhile)                  
        return nodowhile