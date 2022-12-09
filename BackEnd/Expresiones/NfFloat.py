from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Return2 import ReturnC3D
from TS.Tipo import tipo, operador_logico
import math


class nfFloat(instruccion):
    def __init__(self, expresion,fila,columna):
  
        self.tipo = None
        self.expresion=expresion
        self.fila=fila
        self.columna=columna
        


    def interpretar(self, tree, table):
                val = self.expresion.interpretar(tree,table)#interpretar la expresion
                if isinstance(val,Excepcion):return val#verificamos si es error
                
                if ( self.expresion.tipo == tipo.ENTERO ):
                    self.tipo = tipo.DECIMAL
                    return self.Trunc(self.obtenerVal(self.expresion.tipo,val)  )

            
                return Excepcion("Semantico","Tipo valor erroneo para float(valor)",self.fila,self.columna)




    def Trunc(self,expresion):#METODO PARA SACAR trunc
        #en py 1ero es num 
        
        return float(expresion)


    def obtenerVal(self,tipo,val):
        if tipo ==tipo.ENTERO:
            return int(val)
        if tipo ==tipo.DECIMAL:
            return float(val)
        if tipo ==tipo.BOOLEANO:#bool estaba comentado
            return bool(val)

        return str(val)# OJO POSIBLE ERROR!



    def getNodo(self):
        nodo = NodoAST("FLOAT")
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo



    def compilar(self, tree, table):
        val = self.expresion.compilar(tree,table)#interpretar la expresion
        if isinstance(val,Excepcion):return val#verificamos si es error
        
        if (val.tipo == tipo.ENTERO ):
            self.tipo = tipo.DECIMAL
            genAux = Generator()
            generator = genAux.getInstance()
            generator.addCommit("-------------NATIVAS FLOAT -------------")

            try:
                #si es un valor entonces lo paso a float desde aqui sino pues es una variable y entre en except
                return ReturnC3D(self.Trunc(val.valor),tipo.DECIMAL,True) 
            except :
                return ReturnC3D(val.valor,tipo.DECIMAL,True) 
            
               #self.Trunc(self.obtenerVal(self.expresion.tipo,val)  )

    
        return Excepcion("Semantico","Tipo valor erroneo para float(valor)",self.fila,self.columna)
