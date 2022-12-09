
from Instrucciones.FuncionSimple import FuncionSP
from typing import List
from Expresiones.primitivos import Primitivos
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import tipo
from TS.Simbolo import Simbolo

class Pop(instruccion):# es como un nodo y se arma el arbol con estos nodos

                    
    def __init__(self,identificador , expresion, fila, columna ):
        self.identificador=identificador
        self.expresion=expresion
        self.fila=fila
        self.columna=columna

        self.tipo=tipo.NULO#valor de return de una funcion
        
        self.arreglo=True
        self.cuerpoSiesArray=None


    def interpretar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)


        try:
            #print("99999999999999999999999999999999999999999")
            #print(str(self.identificador))
            #print(str(len(value)))         tipo lo converti en el nodo XD SINO NO SALE
            simbolo = Simbolo(self.identificador,self.expresion, self.arreglo, self.fila,self.columna,"")#buscar si esta en la tabla y se modifica ahi, sino entra en if isinstance(result,Excepcion): 
            ash = table.actualizarTablaARRAY2(simbolo)#lo modifico o no lo hizo 


            #print("////////////////////////////////////////////////////////\n"+str(ash.tipo))
            self.tipo = ash.tipo
           # print(str(ash.valor))
           # print(str(ash))
            

            

            return ash.valor

        except:
            return Excepcion("Semantico","Tipo erroneo para pop, SOLO ES VALIDO PARA ARREGLOS!",self.fila,self.columna)


      
        

    def getNodo(self):
            nodo = NodoAST("ARRAY_POP")
            nodo.agregarHijo(str(self.identificador))
            nodo.agregarHijo(str(self.expresion))
            return nodo


