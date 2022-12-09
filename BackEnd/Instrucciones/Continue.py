from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Tipo import tipo
from TS.TablaSimbolo import TablaSimbolos


class Continue(instruccion):# es como un nodo y se arma el arbol con estos nodos

      # expresion,instrucciones,instrucciones else,NODO_IF              
    def __init__(self,fila,columna ):
        self.fila=fila
        self.columna=columna
        


    def interpretar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)

        return self
        

    def getNodo(self):
        nodo = NodoAST("CONTINUE")
        return nodo


    def compilar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)
        genAux = Generator()
        generator = genAux.getInstance()#obtengo mi static generator
        generator.addCommit("_________CONTINUE_________")

        breakLabel = table.continueLbl

        if table.continueString==True:
            generator.addCommit("incremento el indice de heap")
            generator.addExp(table.tempLblPlusOne,table.tempLblPlusOne,'1','+')
            generator.addCommit("obtengo el ascci ++")
            generator.getHeap(table.temp2Lbl,table.tempLblPlusOne)

            generator.addExp(table.retTemp, 'H', '', '')
            generator.addCommit("asigno el ascii ++")
            generator.setHeap('H', table.temp2Lbl)   # heap[H] = ascii de c/u de los caracter de la cadena;
            generator.nextHeap()
            generator.setHeap('H', '-1')            # FIN DE CADENA q es -1
            generator.nextHeap()  
            generator.addCommit("al stack le meto el puntero de la nueva cadena")
            generator.setStack(table.simboloSize,table.retTemp)


        if table.continueInt==True:
            generator.addCommit("agrego el ++ para indice de for")     
            generator.addCommit(" saco el indice y le hago ++")
            generator.getStack(table.t0,table.intSimboloSize)
            generator.addExp(table.t0,table.t0,'1','+')
            generator.setStack(table.intSimboloSize,table.t0)

            

        if breakLabel !="":
            generator.addGoto(breakLabel)
            generator.addCommit("_________FIN CONTINUE_________")



        
        return self