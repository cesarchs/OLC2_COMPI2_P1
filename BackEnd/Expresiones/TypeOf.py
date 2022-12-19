from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import tipo, operador_logico
import math


class nfTypeof(instruccion):
    def __init__(self, expresion,fila,columna):
  
        self.tipo = None
        self.expresion=expresion
        self.fila=fila
        self.columna=columna
        


    def interpretar(self, tree, table):
                val = self.expresion.interpretar(tree,table)#interpretar la expresion
                if isinstance(val,Excepcion):return val#verificamos si es error
                
                
                self.tipo = self.expresion.tipo
                #print(">>>>>"+str(self.tipo))
                return self.tipeof(str(self.tipo))  #tipo.ENTERO

    def tipeof(self,num):

        switch={

        "tipo.ENTERO":'Int64',
        "tipo.DECIMAL":'Float64',
        "tipo.BOOLEANO":'Bool',
        "tipo.CHARACTER":'Char',
        "tipo.CADENA":'String',
        "tipo.NULO":'Nothing',
        "tipo.ARREGLO":'Arreglo'

        }

        return switch.get(num,"Invalid input")



    def obtenerVal(self,tipo,val):
        if tipo ==tipo.ENTERO:
            return int(val)
        if tipo ==tipo.DECIMAL:
            return float(val)
        if tipo ==tipo.BOOLEANO:#bool estaba comentado
            return bool(val)

        return str(val)# OJO POSIBLE ERROR!



    def getNodo(self):
        nodo = NodoAST("TYPEOF")
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo