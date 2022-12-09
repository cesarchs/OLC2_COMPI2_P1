from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Tipo import tipo
from TS.TablaSimbolo import TablaSimbolos


class Break(instruccion):# es como un nodo y se arma el arbol con estos nodos

      # expresion,instrucciones,instrucciones else,NODO_IF              
    def __init__(self,fila,columna ):
        self.fila=fila
        self.columna=columna


    def interpretar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)
        
        return self
        

    def getNodo(self):
        nodo = NodoAST("BREAK")
        return nodo

    def compilar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)
        genAux = Generator()
        generator = genAux.getInstance()#obtengo mi static generator
        generator.addCommit("_________BREAK_________")

        breakLabel = table.breakLbl
        if breakLabel !="":
            generator.addGoto(breakLabel)
            generator.addCommit("_________FIN BREAK_________")
        



        
        return self