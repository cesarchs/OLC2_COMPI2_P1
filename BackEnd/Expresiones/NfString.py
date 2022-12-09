from typing import List
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import tipo, operador_logico
import math


#NO PARSEA ARRAYS AUN :(

class nfString(instruccion):
    def __init__(self, expresion,fila,columna):
  
        self.tipo = None
        self.expresion=expresion
        self.fila=fila
        self.columna=columna
        


    def interpretar(self, tree, table):
                val = self.expresion.interpretar(tree,table)#interpretar la expresion
                if isinstance(val,Excepcion):return val#verificamos si es error
                
                if ( self.expresion.tipo != None ):
                    self.tipo = tipo.CADENA
                    return self.Trunc(self.obtenerVal(self.expresion.tipo,val,tree,table   )  )

            
                return Excepcion("Semantico","Tipo valor erroneo para string(valor)",self.fila,self.columna)




    def Trunc(self,expresion):#METODO PARA SACAR trunc
        #en py 1ero es num 
        return str(expresion)


    def obtenerVal(self,tipo,val,tree,table):
        if tipo ==tipo.ENTERO:
            return int(val)
        if tipo ==tipo.DECIMAL:
            return float(val)
        if tipo ==tipo.BOOLEANO:#bool estaba comentado
            return bool(val)

        if tipo ==tipo.ARREGLO:
            return self.verArray(val,tree,table)


        return str(val)# OJO POSIBLE ERROR!



    def getNodo(self):
        nodo = NodoAST("STRING")
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo



    def verArray(self,value,tree,table):
            cadenita="["
            init=False
            #for para ver si detecto en mis elementos del array otro array

            try:    
                
                for expresion in value:#recorro la lista de elementos q posee el array
                        resultExpresion = expresion.interpretar(tree,table)#c\u de los elementos del array interpretar 
                        
                        if isinstance(resultExpresion, Excepcion):return resultExpresion#por si me da error
                        if init:
                            cadenita +=","
                        init=True

                        try:
                            if isinstance(resultExpresion, List):
                                #print("[array detected!]") 
                                cadenita += self.verArray(resultExpresion,tree,table)
                        except: 
                            print("F (T.T) List en isinstance dio clavo..."+str(resultExpresion))

                        if isinstance(resultExpresion, List):
                            pass
                        else:
                            cadenita += str(resultExpresion)

                cadenita += "]"

            except:
                cadenita += str(value) 
                
            return cadenita