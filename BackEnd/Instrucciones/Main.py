from Abstract.NodoAST import NodoAST
from Instrucciones.Break import Break
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import tipo
from TS.TablaSimbolo import TablaSimbolos
from TS.Simbolo import Simbolo

class Main(instruccion):
            
    def __init__(self,instrucciones,fila,columna ):
        self.instrucciones=instrucciones
        self.fila=fila
        self.columna=columna


    def interpretar(self, tree, table):

        nuevaTabla =TablaSimbolos(table)#creamos un nueva tabla de simbolos para este ambito creo

        for instruccion in self.instrucciones:#recorre sus instrucciones

                value=instruccion.interpretar(tree,nuevaTabla)#si hay errores los guardamos
                if isinstance(value, Excepcion):
                    tree.getExcepciones().append(value)
                    tree.updateConsola(value.toString())

                if isinstance(value, Break):#en main no se pueden poner breaks asiq aqui los detectamos como error
                    error = Excepcion("Semantico","Error semantico break fuera de ciclo",instruccion.fila,instruccion.columna)
                    tree.getExcepciones().append(error)
                    tree.updateConsola(error.toString())
            

        #en JULIA NO EXISTE XD    

    def getNodo(self):
        nodo = NodoAST("MAIN")

        instrucciones = NodoAST("INSTRUCCIONES")

        for instr in self.instrucciones:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)
    
        return nodo

        
