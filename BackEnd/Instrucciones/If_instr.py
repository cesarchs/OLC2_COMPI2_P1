from Instrucciones.Continue import Continue
from Abstract.NodoAST import NodoAST
from Instrucciones.Return import Return
from Instrucciones.Break import Break
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Tipo import tipo
from TS.TablaSimbolo import TablaSimbolos
from TS.Simbolo import Simbolo

class If(instruccion):# es como un nodo y se arma el arbol con estos nodos

      # expresion,instrucciones,instrucciones else,NODO_IF              
    def __init__(self,condicion,instruccionesIf,instruccionesElse, elseIf,fila,columna ):
        self.condicion = condicion
        self.instruccionesIf=instruccionesIf
        self.instruccionesElse=instruccionesElse
        self.elseIf=elseIf
        self.fila=fila
        self.columna=columna


    def interpretar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)
        condicion = self.condicion.interpretar(tree,table) #nos puede traer un suma variable condicio if
        #por si tenemos un error en lo anterior
        if isinstance(condicion, Excepcion): return condicion#retorno la excepcion q me esta trayendo condicion por si tiene, ponerlo siempre


        if self.condicion.tipo ==tipo.BOOLEANO:#ya encontro el bool

            if bool(condicion)==True:#verifica si es verdadera la condicion; bool() posible cague
                #si entra creamos una nueva tabla de simbolos porq es un IF
                nuevaTabla =TablaSimbolos(table) #nueva tabla, porq es un NUEVO AMBITO
                for instruccion in self.instruccionesIf:
                    result =instruccion.interpretar(tree,nuevaTabla)#ejecuta instruccion adentro if, y usa el NUEVO AMBITO del if
                    if isinstance(result, Excepcion): 
                        #hacemos esto de abajo paraq no se nos salga o termine lo del if
                        tree.getExcepciones().append(result)
                        tree.updateConsola(result.toString(),1)


#si detecto un break tonces;se pone return para salir de este for pero no sale del while de arriba
                    if isinstance(result, Break):return result#significa q se realizo correctamente el break
                    if isinstance(result, Continue):return result#significa q se realizo correctamente el continue
                    if isinstance(result, Return):return result#porq al final para q se salga de la funcion

        
            else:#por si viene un else julia
                if self.instruccionesElse!=None:#verifica si es verdadera la condicion
                    #si entra creamos una nueva tabla de simbolos
                    nuevaTabla =TablaSimbolos(table) #nueva tabla, porq es un NUEVO AMBITO
                    for instruccion in self.instruccionesElse:
                        result =instruccion.interpretar(tree,nuevaTabla)#ejecuta instruccion adentro if, y usa el NUEVO AMBITO del if
                        if isinstance(result, Excepcion): 
                            #hacemos esto de abajo paraq no se nos salga o termine lo del if
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString(),1)

#si detecto un break tonces;se pone return para salir de este for pero no sale del while de arriba
                        if isinstance(result, Break):return result#significa q se realizo correctamente el break
                        if isinstance(result, Continue):return result#significa q se realizo correctamente el continue
                        if isinstance(result, Return):return result#porq al final para q se salga de la funcion


                #PARTE DEL ELSEIF DE JULIA
                elif self.elseIf !=None:#solo es un nodo no es una lista
                    result= self.elseIf.interpretar(tree,table)
                    if isinstance(result, Excepcion): return result

#si detecto un break tonces;se pone return para salir de este for pero no sale del while de arriba       
                    if isinstance(result, Break):return result#significa q se realizo correctamente el break
                    if isinstance(result, Continue):return result#significa q se realizo correctamente el continue
                    if isinstance(result, Return):return result#porq al final para q se salga de la funcion

                    

        else:
            return Excepcion("Semantico","Tipo de condicion if no Booleano", self.fila,self.columna)
        
        


#min 44 video 7





    def getNodo(self):
        nodo = NodoAST("IF")

        instruccionesIf = NodoAST("INSTRUCCIONES IF")

        for instr in self.instruccionesIf:
            instruccionesIf.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instruccionesIf)

        if self.instruccionesElse!=None:#verifica si es verdadera la condicion=ELSE
            instruccionesELSE = NodoAST("INSTRUCCIONES ELSE")
            for instr in self.instruccionesElse:
                instruccionesELSE.agregarHijoNodo(instr.getNodo())
            nodo.agregarHijoNodo(instruccionesELSE)
                  

                #PARTE DEL ELSEIF DE JULIA
        elif self.elseIf !=None:#solo es un nodo no es una lista
            nodo.agregarHijoNodo(self.elseIf.getNodo())
        
        return nodo




    def compilar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)
        
        genAux = Generator()
        generator = genAux.getInstance()#obtengo mi static generator
        generator.addCommit("_________INICIO DE IF_________")

        condicion = self.condicion.compilar(tree,table) #nos puede traer un suma variable condicio if
        #por si tenemos un error en lo anterior
        if isinstance(condicion, Excepcion): return condicion#retorno la excepcion q me esta trayendo condicion por si tiene, ponerlo siempre


        if self.condicion.tipo ==tipo.BOOLEANO:#ya encontro el bool
            
            generator.inputLabel(condicion.trueLbl)
            skipElse = generator.newLabel()

            nuevaTabla =TablaSimbolos(table) #nueva tabla, porq es un NUEVO AMBITO
            
            for instruccion in self.instruccionesIf:
                result =instruccion.compilar(tree,nuevaTabla)#ejecuta instruccion adentro if, y usa el NUEVO AMBITO del if
                
                if isinstance(result, Excepcion): 
                    #hacemos esto de abajo paraq no se nos salga o termine lo del if
                    tree.getExcepciones().append(result)
                    #tree.updateConsola(result.toString(),1)
               
                #if isinstance(result, Return):return result#porq al final para q se salga de la funcion




            generator.addGoto(skipElse)
            generator.inputLabel(condicion.falseLbl)

            



   #######################################################################################             


            if self.instruccionesElse!=None:#verifica si es verdadera la condicion
                #si entra creamos una nueva tabla de simbolos
                nuevaTabla =TablaSimbolos(table) #nueva tabla, porq es un NUEVO AMBITO
                for instruccion in self.instruccionesElse:
                    result =instruccion.compilar(tree,nuevaTabla)#ejecuta instruccion adentro if, y usa el NUEVO AMBITO del if
                    if isinstance(result, Excepcion): 
                        #hacemos esto de abajo paraq no se nos salga o termine lo del if
                        tree.getExcepciones().append(result)
                        #tree.updateConsola(result.toString(),1)
                    
                    #if isinstance(result, Return):return result#porq al final para q se salga de la funcion




            #PARTE DEL ELSEIF DE JULIA
            elif self.elseIf !=None:#solo es un nodo no es una lista
                result= self.elseIf.compilar(tree,table)
                if isinstance(result, Excepcion): return result
                
                #if isinstance(result, Return):return result#porq al final para q se salga de la funcion



                    
            generator.inputLabel(skipElse)
        else:

            generator.inputLabel(condicion.trueLbl)#como queda inconcluso hago esto
            generator.inputLabel(condicion.falseLbl)

            return Excepcion("Semantico","Tipo de condicion if no Booleano", self.fila,self.columna)
        





