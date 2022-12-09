from typing import List
from TS.Excepcion import Excepcion
from TS.Tipo import tipo
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Generador import Generator
from TS.Return2 import ReturnC3D



######################################
# FALTA PARA EL NOTHING
######################################

class Primitivos(instruccion):# es como un nodo y se arma el arbol con estos nodos; hasta ahorita usados para enteros, decimal
    def __init__(self, tipoq, valor, fila, columna ):
        self.tipo=tipoq
        self.valor=valor
        self.fila=fila
        self.columna=columna
        self.TMP=""
        self.C3D=""
        self.arrays=[]#aqui guardare c/u de los caracteres de una cadena|string
        self.LV=""
        self.LF=""

       # if self.tipo == tipo.ENTERO or self.tipo==tipo.DECIMAL:
        #    self.TMP=str(valor)

        #elif self.tipo == tipo.CADENA or self.tipo==tipo.CHARACTER:
         #   print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
          #  for ch in self.valor:
                
           #     print(ch + ' = ' + str(ord(ch)))#asi saco el ascii de una cadena
            #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")



    def interpretar(self, tree, table):
        if (self.tipo==tipo.ARREGLO):
            #print("aaa")
            return self.valor
        return self.valor

    


    def compilar(self, tree, table):
        genAux = Generator()
        generator = genAux.getInstance()#el q me hara el paro en todo

        if self.tipo == tipo.ENTERO or self.tipo==tipo.DECIMAL:
            return ReturnC3D(str(self.valor), self.tipo, False)

        elif self.tipo == tipo.BOOLEANO:
            generator.addCommit("-------------BOOL-----------------")
            if self.LV == '':
                self.LV = generator.newLabel()
            if self.LF == '':
                self.LF = generator.newLabel()
            
            if(self.valor):
                generator.addGoto(self.LV)
                generator.addCommit("GOTO PARA EVITAR ERROR DE GO")
                generator.addGoto(self.LF)
            else:
                generator.addGoto(self.LF)
                generator.addCommit("GOTO PARA EVITAR ERROR DE GO")
                generator.addGoto(self.LV)


            ret = ReturnC3D(self.valor, self.tipo, False)
            ret.trueLbl = self.LV
            ret.falseLbl = self.LF

            return ret

        elif self.tipo == tipo.CADENA:
            retTemp = generator.addTemporal()
            generator.addCommit("-------------CADENA-----------------")
            generator.addExp(retTemp, 'H', '', '')
            

            for char in str(self.valor):
                generator.setHeap('H', ord(char))   # heap[H] = ascii de c/u de los caracter de la cadena;
                generator.nextHeap()                # H = H + 1;
                

                


            generator.setHeap('H', '-1')            # FIN DE CADENA q es -1
            generator.nextHeap()                    # H = H + 1;
            


            return ReturnC3D(retTemp, tipo.CADENA, True)

        elif self.tipo == tipo.CHARACTER:
            generator.addCommit("-------------CHAR-----------------")
            retTemp = generator.addTemporal()
            generator.addExp(retTemp, 'H', '', '')

            for char in str(self.valor):
                generator.setHeap('H', ord(char))   # heap[H] = ascii de c/u de los caracter de la cadena;
                generator.nextHeap()                # H = H + 1;
                


            generator.setHeap('H', '-1')            # FIN DE CADENA q es -1
            generator.nextHeap()                    # H = H + 1;
            


            return ReturnC3D(retTemp, tipo.CADENA, True)

        elif self.tipo == tipo.ARREGLO:
            retTemp = generator.addTemporal()
            generator.addCommit("-------------ARREGLOS-----------------")
            generator.addExp(retTemp, 'H', '', '')#T0=H

            tam=False
            arr=None

            for char in self.valor:

                if not tam:#para meter el tam 1 vez por cada array
                    generator.addCommit("~~~ TAM DEL ARRAY:"+str(len(self.valor)))
                    generator.setHeap('H', len(self.valor))   # meto de primero el tam del array en la posicion 0
                    generator.nextHeap() # H = H + 1;
                    

                    generator.addCommit("~~~ FIN DEL TAM ARRAY:"+str(len(self.valor)))
                    tam=True 

                value = char.compilar(tree,table)
                if isinstance(value, Excepcion): return value#lo retornamos



                if value.tipo==tipo.BOOLEANO:#si es tipo bool el item de mi array entonces....
                    tempLbl = generator.newLabel()

                    generator.addCommit("---item del array:"+str(value.valor)+" tipo:"+str(value.tipo))
                    
                    #####################################################
                    heap = generator.addTemporal()
                    
                    #####################################################

                    
                
                    generator.inputLabel(value.trueLbl)
                    generator.setHeap('H', 1)  # heap[H] = elemento del array
                    generator.addCommit("creo un apuntador a bool en HEAP")
                    generator.addExp(heap,'H','','')
                    value.posicion = heap
                    generator.nextHeap()                # H = H + 1;
                    
                    generator.addGoto(tempLbl)

                    generator.inputLabel(value.falseLbl)
                    generator.setHeap('H', 0)  # heap[H] = elemento del array
                    generator.addCommit("creo un apuntador a bool en HEAP")
                    generator.addExp(heap,'H','','')
                    value.posicion = heap
                    generator.nextHeap()                # H = H + 1;

                    generator.inputLabel(tempLbl)


                    self.arrays.append(value)#AQUI GUARDO EL ITEM DEL ARRAY EN SELF.ARRAYS PARA Q SEPA Q ES CADA COSA
                    #(AUN NO SE EN Q SACARLE PROVECHO)


                    


                else:
                
        #creo q deberia tener una Lista y aqui este value.valor meter los apuntadores en ella
        #debido a que representan las localizaciones de las partes de un array compuesto no solo de int


                    generator.addCommit("---item del array:"+str(value.valor)+" tipo:"+str(value.tipo))
                    #####################################################
                    heap = generator.addTemporal()
                    generator.addCommit("creo un apuntador a int,float,string,char,array en HEAP")

                    #solo q para string y char no tomare en cuenta el atributo posicion porq no son la posicion tal cual
                    #sino el atributo valor

                    generator.addExp(heap,'H','','')
                    value.posicion = heap
                    #####################################################
                    self.arrays.append(value)#AQUI GUARDO EL ITEM DEL ARRAY EN SELF.ARRAYS PARA Q SEPA Q ES CADA COSA
                    #(AUN NO SE EN Q SACARLE PROVECHO)

                    generator.setHeap('H', value.valor)  # heap[H] = elemento del array
                    generator.nextHeap()                # H = H + 1;
                    


            #generator.setHeap('H', '-1997.0905')    # FIN DE array q es -1
            #generator.nextHeap()                    # H = H + 1;

            return ReturnC3D(retTemp, tipo.ARREGLO, True,self.arrays)


        elif self.tipo == tipo.NULO:
            return ReturnC3D(str("00000000"), tipo.NULO, False)



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

    def getNodo(self):
        if self.tipo==tipo.ARREGLO:
            nodo = NodoAST(str(self.tipeof(str(self.tipo))))
            #nodo.agregarHijo(str(self.valor)+"PUA JAVIER XD")
            parametros = NodoAST("LISTA ELEMENTOS")
            for param in self.valor:
                parametros.agregarHijoNodo(param.getNodo())
            nodo.agregarHijoNodo(parametros)
            return nodo
            
        else:
            nodo = NodoAST(str(self.tipeof(str(self.tipo))))
            nodo.agregarHijo(str(self.valor))
            return nodo

        
        



























