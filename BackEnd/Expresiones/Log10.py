from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import tipo, operador_logico
import math


class Log10(instruccion):
    def __init__(self, expresion,fila,columna):
  
        self.tipo = None
        self.expresion=expresion
        self.fila=fila
        self.columna=columna
        


    def interpretar(self, tree, table):
                val = self.expresion.interpretar(tree,table)#interpretar la expresion
                if isinstance(val,Excepcion):return val#verificamos si es error
                
                if ( self.expresion.tipo == tipo.DECIMAL ) or ( self.expresion.tipo == tipo.ENTERO ):
                    self.tipo = self.expresion.tipo
                    return self.log10(self.obtenerVal(self.expresion.tipo,val)  )

            
                return Excepcion("Semantico","Tipo valor erroneo para log10(valor)",self.fila,self.columna)




    def log10(self,expresion):#METODO PARA SACAR LOG10
        #en py 1ero es num 
        return math.log10(expresion)


    def obtenerVal(self,tipo,val):
        if tipo ==tipo.ENTERO:
            return int(val)
        if tipo ==tipo.DECIMAL:
            return float(val)
        if tipo ==tipo.BOOLEANO:#bool estaba comentado
            return bool(val)

        return str(val)# OJO POSIBLE ERROR!



    def getNodo(self):
        nodo = NodoAST("LOG10")
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo