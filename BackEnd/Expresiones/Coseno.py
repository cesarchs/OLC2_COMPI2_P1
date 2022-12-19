from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import tipo, operador_logico
import math


class Coseno(instruccion):
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
                    return self.Coseno(self.obtenerVal(self.expresion.tipo,val)  )

            
                return Excepcion("Semantico","Tipo valor erroneo para cos(valor)",self.fila,self.columna)




    def Coseno(self,expresion):#METODO PARA SACAR coseno
        #en py 1ero es num 
        
        return math.cos(math.radians(expresion))


    def obtenerVal(self,tipo,val):
        if tipo ==tipo.ENTERO:
            return int(val)
        if tipo ==tipo.DECIMAL:
            return float(val)
        if tipo ==tipo.BOOLEANO:#bool estaba comentado
            return bool(val)

        return str(val)# OJO POSIBLE ERROR!



    def getNodo(self):
        nodo = NodoAST("COSENO")
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo