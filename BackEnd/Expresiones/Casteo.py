from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import tipo, operador_logico



class Casteo(instruccion):
    def __init__(self, tipo,expresion,fila,columna):
        self.tipo =tipo
        self.expresion=expresion
        self.fila=fila
        self.columna=columna
        


    def interpretar(self, tree, table):
        val = self.expresion.interpretar(tree,table)         #interpretar la expresion
        if isinstance(val,Excepcion):return val#verificamos si es error

    #DESTINO DECIMAL
    #STRING -> DECIMAL
        if self.tipo==tipo.DECIMAL  : #tipo q nos piden a pasarlo

          if self.expresion.tipo ==tipo.CADENA:#si es una cadena
                try:
                    return float(self.obtenerVal(self.expresion.tipo,val))
                except:
                    return Excepcion("Semantico","No se puede castear para Float64: "+str(val)+" ",self.fila,self.columna)
          #si no entra en nada F es error
          return Excepcion("Semantico","Tipo erroneo de casteo para Float64, se espera una cadena!",self.fila,self.columna)
        


    #DESTINO ENTERO
    #STRING -> ENTERO
        if self.tipo==tipo.ENTERO  : #tipo q nos piden a pasarlo

          if self.expresion.tipo ==tipo.CADENA:#si es una cadena
                try:
                    return int(self.obtenerVal(self.expresion.tipo,val))
                except:
                    return Excepcion("Semantico","No se puede castear para Int64: "+str(val)+" ",self.fila,self.columna)
          #si no entra en nada F es error
          return Excepcion("Semantico","Tipo erroneo de casteo para Int64, se espera una cadena!",self.fila,self.columna)
        



        return Excepcion("Semantico","Tipo destino erroneo de casteo:  parser(destino,cadena)",self.fila,self.columna)








    def obtenerVal(self,tipo,val):
        if tipo ==tipo.ENTERO:
            return int(val)
        if tipo ==tipo.DECIMAL:
            return float(val)
        if tipo ==tipo.BOOLEANO:#bool estaba comentado
            return bool(val)

        return str(val)# OJO POSIBLE ERROR!



    def getNodo(self):
        nodo = NodoAST("PARSER")
        nodo.agregarHijo(str(self.tipo))
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo












        '''
        
            #DESTINO DECIMAL
    #   ENTERO | STRING -> DECIMAL
        if self.tipo==tipo.DECIMAL  : #tipo q nos piden a pasarlo

          if self.expresion.tipo ==tipo.ENTERO:#si es de tipo entero entonces lo pasamos a decimal
                try:
                    return float(self.obtenerVal(self.expresion.tipo,val))
                except:
                    return Excepcion("Semantico","No se puede castear para Float64: "+str(val),self.fila,self.columna)
        
          elif self.expresion.tipo ==tipo.CADENA:#si es de tipo cadena entonces lo pasamos a decimal
                try:
                    return float(self.obtenerVal(self.expresion.tipo,val))
                except:
                    return Excepcion("Semantico","No se puede castear para Float64: "+str(val),self.fila,self.columna)
        
          #si no entra en nada F es error
          return Excepcion("Semantico","Tipo erroneo de casteo para Float64",self.fila,self.columna)
        
        '''