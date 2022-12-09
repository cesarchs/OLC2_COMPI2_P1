from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Simbolo import Simbolo
from TS.Tipo import tipo
from TS.TablaSimbolo import TablaSimbolos


class Return(instruccion):# es como un nodo y se arma el arbol con estos nodos

      # expresion,instrucciones,instrucciones else,NODO_IF              
    def __init__(self,expresion,fila,columna ):
        self.expresion=expresion
        self.fila=fila
        self.columna=columna
        self.tipo=None#=tipo.NULO#valor de return por defecto de una funcion sin return; porq con return debe de retornar el tipo correspondiente
        self.result=None


    def interpretar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)
        result = self.expresion.interpretar(tree,table)
        if isinstance(result,Excepcion): return result

        self.tipo= self.expresion.tipo#aqui guardamos el tipo del result
        self.result=result#guardado el result


        return self
        


    def getNodo(self):
        nodo = NodoAST("RETURN")
        nodo.agregarHijoNodo(self.expresion.getNodo())


        return nodo



    def compilar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)
            result = self.expresion.compilar(tree,table)
            if isinstance(result,Excepcion): return result

            #print("aparece||||||||||||||||||| valor:"+str(result.valor)+", tipo:"+str(result.tipo))

            self.tipo= result.tipo#aqui guardamos el tipo del result
            self.result=result#guardado el result

            #print("++++++++++++++++++++++++++++++++++++++++++++"+str(result.tipo)+","+str(result.valor)+"\n")
            
            simbolo = Simbolo("RETURN_VALOR_funcion",result.tipo,None,self.fila,self.columna,result.valor,0,(result.tipo == tipo.CADENA or result.tipo == tipo.ARREGLO))
            resultTablaS,newt = table.actualizarTabla(simbolo)#lo metemos a la tabla simbolos

            #print("en return actualice el return en posicion 0:"+str(newt.valor))
            if isinstance(resultTablaS,Excepcion): return resultTablaS#por si hubo error

            genAux = Generator()
            generator = genAux.getInstance()#obtengo mi static generator
            generator.addCommit("_________INICIO DE GUARDADO RETURN EN STACK_________")
            tempret = generator.addTemporal()#T2
            generator.addExp(tempret, 'P', '0', '+')
            
            #obtener el valor de param_cadena
            if newt.tipo==tipo.BOOLEANO:
                tempLbl = generator.newLabel()
                
                generator.inputLabel(result.trueLbl)
                generator.addExp(tempret, 'P', '0', '+')
                generator.setStack(tempret, "1")
                
                generator.addGoto(tempLbl)

                generator.inputLabel(result.falseLbl)
                generator.addExp(tempret, 'P', '0', '+')
                generator.setStack(tempret, "0")

                generator.inputLabel(tempLbl)

                generator.addCommit("_________AQUI ESCRIBO EL RETURN DE LA FUNCION_________")
            
            #el final de FuncionSimple me escribe return
                generator.addReturn()
            
                return newt


            else:
                generator.setStack(tempret, newt.valor)


            #AQUI ESCRIBO EL RETURN DE LA FUNCION
            generator.addCommit("_________AQUI ESCRIBO EL RETURN DE LA FUNCION_________")
            
            #el final de FuncionSimple me escribe return
            generator.addReturn()
            
            return newt









