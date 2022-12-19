from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import tipo, operador_logico
import math


class Log(instruccion):
    def __init__(self, base,expresion,fila,columna):
        self.base =base
        self.tipo = None
        self.expresion=expresion
        self.fila=fila
        self.columna=columna
        


    def interpretar(self, tree, table):
        val = self.expresion.interpretar(tree,table)#interpretar la expresion
        if isinstance(val,Excepcion):return val#verificamos si es error

        val2 =self.base.interpretar(tree,table)#interpretar la expresion
        if isinstance(val2,Excepcion):return val2#verificamos si es error

        if ( self.base.tipo == tipo.DECIMAL ) or ( self.base.tipo == tipo.ENTERO ):
        
            self.tipo = self.base.tipo
            
            if self.base.tipo==tipo.ENTERO  :
                if self.expresion.tipo ==tipo.DECIMAL:
                        return self.log(self.obtenerVal(self.base.tipo,val2)   ,self.obtenerVal(self.expresion.tipo,val)  )
                elif self.expresion.tipo ==tipo.ENTERO:
                        return self.log(self.obtenerVal(self.base.tipo,val2)    ,self.obtenerVal(self.expresion.tipo,val)  )
                #si no entra en nada F es error
                return Excepcion("Semantico","Tipo de valor erroneo para log(base,valor)",self.fila,self.columna)



            elif self.base.tipo==tipo.DECIMAL  :
                if self.expresion.tipo ==tipo.DECIMAL:
                    return self.log(self.obtenerVal(self.base.tipo,val2)   ,self.obtenerVal(self.expresion.tipo,val)  )
                elif self.expresion.tipo ==tipo.ENTERO:
                    return self.log(self.obtenerVal(self.base.tipo,val2)   ,self.obtenerVal(self.expresion.tipo,val)  )
                #si no entra en nada F es error
                return Excepcion("Semantico","Tipo de valor erroneo para log(base,valor)",self.fila,self.columna)
            

        return Excepcion("Semantico","Tipo base erronea para log(base,valor)",self.fila,self.columna)




    def log(self,base,expresion):#METODO PARA SACAR LOG
        #en py 1ero es num y 2ndo es base
        return math.log(expresion,base)


    def obtenerVal(self,tipo,val):
        if tipo ==tipo.ENTERO:
            return int(val)
        if tipo ==tipo.DECIMAL:
            return float(val)
        if tipo ==tipo.BOOLEANO:#bool estaba comentado
            return bool(val)

        return str(val)# OJO POSIBLE ERROR!



    def getNodo(self):
        nodo = NodoAST("LOG")
        nodo.agregarHijoNodo(self.base.getNodo())
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo