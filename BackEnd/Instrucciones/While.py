from Instrucciones.Continue import Continue
from Abstract.NodoAST import NodoAST
from Instrucciones.Return import Return
from Instrucciones.Break import Break
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Tipo import tipo
from TS.TablaSimbolo import TablaSimbolos



#--------------------------------------------------------------------------
#VIDEO 8 
# MIN 47 CICLO FOR 
#--------------------------------------------------------------------------



class While(instruccion):# es como un nodo y se arma el arbol con estos nodos

      # expresion,instrucciones,instrucciones else,NODO_IF              
    def __init__(self,condicion,instrucciones,fila,columna ):
        self.condicion = condicion
        self.instrucciones=instrucciones
        self.fila=fila
        self.columna=columna
        # SELF.DECLARACION
        # SELF.ASIGNACION
        #


    def interpretar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)
        
        #condicion = self.condicion.interpretar(tree,table) #nos puede traer un suma variable condicio if
            
        #PARA FOR:: VIENE AQUI UNA ASIGNACION O DECLARACION DE AHI TODO ES IGUAL
        while True:#si el while va aqui si se actualizan las variables
        
            condicion = self.condicion.interpretar(tree,table) #nos puede traer un suma variable condicio if
            #por si tenemos un error en lo anterior
            if isinstance(condicion, Excepcion): return condicion#retorno la excepcion q me esta trayendo condicion por si tiene, ponerlo siempre

            if self.condicion.tipo ==tipo.BOOLEANO:#ya encontro el bool
                
                if bool(condicion)==True:#verifica si es verdadera la condicion; bool() posible cague
                    #si entra creamos una nueva tabla de simbolos porq es un IF
                    nuevaTabla =TablaSimbolos(table) #nueva tabla, porq es un NUEVO AMBITO
                    for instruccion in self.instrucciones:
                        result =instruccion.interpretar(tree,nuevaTabla)#ejecuta instruccion adentro if, y usa el NUEVO AMBITO del if
                        if isinstance(result, Excepcion): 
                            #hacemos esto de abajo paraq no se nos salga o termine lo del if
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString(),1)

                        if isinstance(result, Break): 
                            #si detecto un break tonces
                            #se pone return para salir de este for pero no sale del while de arriba

                            return None#significa q se realizo correctamente el break
                            #se saldria de interpretar


                        if isinstance(result, Return):
                            return result#porq al final para q se salga de la funcion


                        if isinstance(result, Continue): 
                            #si detecto un continue tonces
                            break

                    #PARA FOR:: ACTUALIZACION DEL DATO (ASIGNACION|INCREMENTO DECREMENTO)

                    
                else:
                    break    #escape hasta q la condicion sea falsa     
            
            else:
                return Excepcion("Semantico","Tipo de condicion while no Booleano", self.fila,self.columna)
            
        


        #video 12 switch case(teoria) y return min 21:00 





    def getNodo(self):
        nodo = NodoAST("WHILE")

        instrucciones = NodoAST("INSTRUCCIONES")

        for instr in self.instrucciones:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)

        return nodo




    def compilar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)
        genAux = Generator()
        generator = genAux.getInstance()#obtengo mi static generator
        generator.addCommit("_________INICIO DE WHILE_________")


        Recursividad = generator.newLabel()
        generator.inputLabel(Recursividad)

        condicion = self.condicion.compilar(tree,table) #nos puede traer un suma variable condicio if
        #por si tenemos un error en lo anterior
        if isinstance(condicion, Excepcion): return condicion#retorno la excepcion q me esta trayendo condicion por si tiene, ponerlo siempre

        if self.condicion.tipo ==tipo.BOOLEANO:#ya encontro el bool

            generator.inputLabel(condicion.trueLbl)
            
            
            nuevaTabla =TablaSimbolos(table) #nueva tabla, porq es un NUEVO AMBITO

            nuevaTabla.breakLbl=condicion.falseLbl
            nuevaTabla.continueLbl=Recursividad

            for instruccion in self.instrucciones:
                result =instruccion.compilar(tree,nuevaTabla)#ejecuta instruccion adentro if, y usa el NUEVO AMBITO del if
                
                if isinstance(result, Excepcion): 
                    tree.getExcepciones().append(result)


            generator.addGoto(Recursividad)
            generator.inputLabel(condicion.falseLbl)
            return None   
        
        else:
            generator.inputLabel(condicion.trueLbl)#como queda inconcluso hago esto
            generator.inputLabel(condicion.falseLbl)

            return Excepcion("Semantico","Tipo de condicion while no Booleano", self.fila,self.columna)
        
        