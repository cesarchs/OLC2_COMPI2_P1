
from typing import List
from Expresiones.primitivos import Primitivos
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import tipo
from TS.Simbolo import Simbolo

class Push(instruccion):# es como un nodo y se arma el arbol con estos nodos

                    
    def __init__(self,identificador , expresion, fila, columna ):
        self.identificador=identificador
        self.expresion=expresion
        self.fila=fila
        self.columna=columna


        self.arreglo=True
        self.cuerpoSiesArray=None


    def interpretar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)
        value = self.expresion.interpretar(tree,table) #retorna cualquier valor

        #por si tenemos un error en lo anterior
        if isinstance(value, Excepcion):
            return value#lo retornamos

        try:
            #print("99999999999999999999999999999999999999999")
            #print(str(value))
            #print(str(len(value)))         tipo lo converti en el nodo XD SINO NO SALE
            simbolo = Simbolo(self.identificador,self.expresion, self.arreglo, self.fila,self.columna,value)#buscar si esta en la tabla y se modifica ahi, sino entra en if isinstance(result,Excepcion): 
            table.actualizarTablaARRAY(simbolo)#lo modifico o no lo hizo 
            return None
        except:
            return Excepcion("Semantico","Tipo erroneo para push, SOLO ES VALIDO PARA ARREGLOS!",self.fila,self.columna)


      
        

    def getNodo(self):
            nodo = NodoAST("ARRAY_PUSH")
            nodo.agregarHijo(str(self.identificador))
            nodo.agregarHijoNodo(self.expresion.getNodo())
            return nodo


