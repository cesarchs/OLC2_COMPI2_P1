from typing import List
from Expresiones.identificador import Identificador
from Expresiones.primitivos import Primitivos
from Expresiones.relacional import Relacional
from Instrucciones.If_instr import If
from Instrucciones.asignacion import Asignacion
from TS.Generador import Generator
from TS.Simbolo import Simbolo
from Instrucciones.Continue import Continue
from Abstract.NodoAST import NodoAST
from Instrucciones.Return import Return
from Instrucciones.Break import Break
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import operador_relacional, tipo
from TS.TablaSimbolo import TablaSimbolos



#--------------------------------------------------------------------------
#VIDEO 8 
# MIN 47 CICLO FOR 
#--------------------------------------------------------------------------



class For(instruccion):# es como un nodo y se arma el arbol con estos nodos
             
      # expresion,instrucciones,instrucciones else,NODO_IF              
    def __init__(self,condicion,condicion2,instrucciones,fila,columna ):
        self.condicion = condicion
        self.condicion2 = condicion2
        self.instrucciones=instrucciones
        self.fila=fila
        self.columna=columna

        
        
        #ForPython ={'tipo':'for1','variable_for':t[2],'inicio_for':t[4],'fin_for':t[6] }
    


    def interpretar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)
        #print("mierdaaaaaaaaaaaaaa")
        #print(str(self.condicion))
        #print(str(self.condicion.tipo))

        #try:
        if self.condicion.tipo ==None and self.condicion.identificador!="":
            
            if self.condicion2['inicio_for']==None and self.condicion2['fin_for']==None and self.condicion2['forString']!=None:


                num1 = self.condicion2['forString'].interpretar(tree,table)
                if isinstance(num1, Excepcion): return num1
                #print("--- condicion2 ---")
                #print(str(num1))

                if isinstance(num1, str):#si es una cadena:#si es una cadena            qqqqqqqqqqqqqqq
                    cosa = self.condicion

                    #print("for letra in \"hello\"    ")
                    
                    nuevaTabla =TablaSimbolos(table) #nueva tabla, porq es un NUEVO AMBITO

                    # declaro la variable declarativa en el ambito del for
                    simbolo = Simbolo(cosa.identificador,cosa.tipo, False, cosa.fila,cosa.columna,"")
                    nuevaTabla.setTabla(simbolo)

                    
                    for cosa in num1: 
                        #print("dentro for-----------------------")  
                        #print(cosa)

                        # actualizo el valor la variable declarativa en el ambito del for
                        simbolo = Simbolo(self.condicion.identificador,self.condicion.tipo, False, self.condicion.fila,self.condicion.columna,cosa)#buscar si esta en la tabla y se modifica ahi, sino entra en if isinstance(result,Excepcion): 
                        nuevaTabla.actualizarTabla(simbolo)#lo modifico o no lo hizo                    

                        
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

                        if isinstance(num1, List):
                            
                            #print("array detected in for")

                            #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                            cosa = self.condicion

                            #print("for letra in [1,2,3,4,5,6,7]    ")
                            
                            nuevaTabla =TablaSimbolos(table) #nueva tabla, porq es un NUEVO AMBITO

                            # declaro la variable declarativa en el ambito del for
                            simbolo = Simbolo(cosa.identificador,cosa.tipo, False, cosa.fila,cosa.columna,"")
                            nuevaTabla.setTabla(simbolo)

                            
                            for cosa in num1: 
                                #print("dentro for-----------------------")  
                                #print(cosa)

                                # actualizo el valor la variable declarativa en el ambito del for
                                simbolo = Simbolo(self.condicion.identificador,cosa.tipo, False, self.condicion.fila,self.condicion.columna,cosa)#buscar si esta en la tabla y se modifica ahi, sino entra en if isinstance(result,Excepcion): 
                                nuevaTabla.actualizarTabla(simbolo)#lo modifico o no lo hizo                    

                                
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
                            #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                        
                        
                        
                        
                        
                        else:return Excepcion("Semantico","tipo rango de for no es una cadena", self.fila,self.columna)





                                                    
            elif self.condicion2['inicio_for']!=None and self.condicion2['fin_for']!=None and self.condicion2['forString']==None:
                #print("for var in 1:5")

                num1 = self.condicion2['inicio_for'].interpretar(tree,table)
                if isinstance(num1, Excepcion): return num1
                #print("--- init ---")
                #print(str(num1))


                num2 = self.condicion2['fin_for'].interpretar(tree,table)
                if isinstance(num2, Excepcion): return num2
                #print("--- finit ---")
                #print(str(num2))



                if isinstance(num1, int) and isinstance(num2, int):#si tanto el init como el finit son enteros
                    cosa = self.condicion

                    #print("entre a for letra in 1:5")
                    
                    nuevaTabla =TablaSimbolos(table) #nueva tabla, porq es un NUEVO AMBITO

                    # declaro la variable declarativa en el ambito del for
                    simbolo = Simbolo(cosa.identificador,cosa.tipo, False, cosa.fila,cosa.columna,"")
                    #print("asasasas")
                    #print(str(cosa))
                    nuevaTabla.setTabla(simbolo)

                    
                    for cosa in range(num1, num2+1): 
                        #print("dentro for-----------------------")  
                        #print(cosa)

                        # actualizo el valor la variable declarativa en el ambito del for
                        simbolo = Simbolo(self.condicion.identificador,tipo.ENTERO, False, self.condicion.fila,self.condicion.columna,cosa)#buscar si esta en la tabla y se modifica ahi, sino entra en if isinstance(result,Excepcion): 
                        nuevaTabla.actualizarTabla(simbolo)#lo modifico o no lo hizo                    

                        
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
                else: return Excepcion("Semantico","tipo rango de for no es entero", self.fila,self.columna)

             
    
        #except:
        else: return Excepcion("Semantico","variable de control no es correcta en for", self.fila,self.columna)


        #video 12 switch case(teoria) y return min 21:00 

    



    def getNodo(self):
        nodo = NodoAST("FOR")

        instrucciones = NodoAST("INSTRUCCIONES")

        for instr in self.instrucciones:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)

        return nodo

    


    #########################################################
    #########################################################
    
    #aun no esta listo

    #########################################################
    #########################################################
    def compilar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)
        genAux = Generator()
        generator = genAux.getInstance()

        generator.addCommit("------------FOR-------------")
        

        #try:
        if self.condicion.tipo ==None and self.condicion.identificador!="":
            
            if self.condicion2['inicio_for']==None and self.condicion2['fin_for']==None and self.condicion2['forString']!=None:
                
                genAux = Generator()
                generator = genAux.getInstance()#obtengo mi static generator
                generator.addCommit("_________INICIO DE FOR INDICE IN \"cadena\"_________")

                if self.condicion2['forString'].tipo==tipo.ARREGLO:
                    polo = Asignacion(self.condicion.identificador,self.condicion2['forString'], self.fila, self.columna)
                    polo.compilar(tree,table)


                    simbolo2 = table.getTabla(self.condicion.identificador)
                    if simbolo2==None:return Excepcion("Semantico","Variable "+self.identificador+"  no encontrada en TablaSimbolos", self.fila,self.columna)
                    final = Primitivos(tipo.ENTERO,len(simbolo2.valor.Array), self.fila, self.columna)#creo el fin de cadena


                    ARRAYs = simbolo2.valor.Array


                    inicial = Primitivos(tipo.ENTERO, 1 , self.fila, self.columna)#creo el fin de cadena
                    polo2 = Asignacion('Veces',inicial, self.fila, self.columna)
                    polo2.compilar(tree,table)


                    ider = Identificador('Veces',self.fila, self.columna)

                    condicion0 = Relacional(operador_relacional.MENORQUE,ider,final,self.fila,self.columna)
                    Recursividad = generator.newLabel()


                    '''
                    	T0=T0+1;
                        T10001 = heap[int(T0)]
                        stack[int(0)]=T10001;
                    '''

                    generator.addCommit("agrego el ++ para indice de for")
                    simbolo = table.getTabla(self.condicion.identificador)
                    if simbolo==None:return Excepcion("Semantico","Variable "+self.identificador+"  no encontrada en TablaSimbolos", self.fila,self.columna)


                    generator.addCommit(">>>>>al stack le meto el puntero del item del array")
                    generator.addExp(simbolo2.valor.valor,simbolo2.valor.valor,'1','+')
                    t10001 = generator.addTemporal()
                    generator.getHeap(t10001,simbolo2.valor.valor)
                    generator.setStack(simbolo.size,t10001)

                    onix = str(simbolo2.valor.valor)
                    
                    simbolo2.tipo= simbolo2.valor.Array[0].tipo
                    simbolo2.valor = ARRAYs[0]

                    

                    result,newVar = table.actualizarTabla(simbolo2)#lo modifico o no lo hizo 
                    if isinstance(result,Excepcion):return result
                    
                    generator.inputLabel(Recursividad)

                    condicion = condicion0.compilar(tree,table) #nos puede traer un suma variable condicio if
                    #por si tenemos un error en lo anterior
                    if isinstance(condicion, Excepcion): return condicion#retorno la excepcion q me esta trayendo condicion por si tiene, ponerlo siempre

                    if condicion.tipo ==tipo.BOOLEANO:#ya encontro el bool
                        generator.addCommit("bueno entre aqui xd")
                        generator.inputLabel(condicion.trueLbl)
                        nuevaTabla =TablaSimbolos(table) #nueva tabla, porq es un NUEVO AMBITO
                        nuevaTabla.breakLbl=condicion.falseLbl
                        nuevaTabla.continueLbl=Recursividad
                        #--------------------------------------------
                        nuevaTabla.continueString=True
                        nuevaTabla.tempLblPlusOne=simbolo2.valor
                        t2 = generator.addTemporal()
                        nuevaTabla.temp2Lbl=t2
                        retTemp = generator.addTemporal()
                        nuevaTabla.retTemp=retTemp
                        nuevaTabla.simboloSize=simbolo.size
                        #--------------------------------------------

                        for instruccion in self.instrucciones:
                            #print("--PED43AZO D434E M4IE343RD4343AA"+str(instruccion))
                            result =instruccion.compilar(tree,nuevaTabla)#ejecuta instruccion adentro if, y usa el NUEVO AMBITO del if

                            if isinstance(result, Excepcion): 
                                tree.getExcepciones().append(result)



                        simbolo3 = table.getTabla(ider.identificador)
                        if simbolo3==None:return Excepcion("Semantico","Variable "+self.identificador+"  no encontrada en TablaSimbolos", self.fila,self.columna)

                        t5 = generator.addTemporal()
                        generator.getStack(t5,simbolo3.size)

                        t6 = generator.addTemporal()
                        generator.addExp(t6,t5,'1','+')
                        generator.setStack(simbolo3.size,t6)


                        #aqui el ++ del item del for a.k.a ID
                        generator.addCommit("========= el ++ para el id del array =========")
                        generator.addCommit(">>>>>al stack le meto el puntero del item del array")
                        generator.addExp(onix,onix,'1','+')
                        t10001 = generator.addTemporal()
                        generator.getHeap(t10001,onix)
                        generator.setStack(simbolo.size,t10001)



                        generator.addIf(t6,len(ARRAYs),'<=',Recursividad)
                        generator.addGoto(condicion.falseLbl)
                        generator.inputLabel(condicion.falseLbl)


                        #generator.setStack(simbolo.size,ARRAYs[0].valor)

                        return None
                    else:
                        generator.inputLabel(condicion.trueLbl)#como queda inconcluso hago esto
                        generator.inputLabel(condicion.falseLbl)

                        return Excepcion("Semantico","Tipo de condicion for no Booleano", self.fila,self.columna)


                



                inicio = self.condicion2['forString'].compilar(tree,table)
                if isinstance(inicio, Excepcion): return inicio
                
                if inicio.tipo==tipo.CADENA:

                    #print("/////////////////////////")
                    #print(str(inicio))
                    #print("/////////////////////////")


                    polo = Asignacion(self.condicion.identificador,self.condicion2['forString'], self.fila, self.columna)
                    polo.compilar(tree,table)

                    final = Primitivos(tipo.CADENA, '', self.fila, self.columna)#creo el fin de cadena

                    condicion0 = Relacional(operador_relacional.DIFERENTE,self.condicion,final,self.fila,self.columna)
                    Recursividad = generator.newLabel()


                    #t10 = generator.addTemporal()
                    generator.addCommit("contador de la cadena a recorrer")
                    #generator.addExp(t10,inicio.valor,'','')


                    generator.addCommit("agrego el ++ para indice de for")
                    simbolo = table.getTabla(self.condicion.identificador)
                    if simbolo==None:return Excepcion("Semantico","Variable "+self.identificador+"  no encontrada en TablaSimbolos", self.fila,self.columna)
                    t0 = generator.addTemporal()
                    generator.addCommit(" saco el indice y le hago ++")
                    generator.getStack(t0,simbolo.size)
                    
                    #creo la letra
                    generator.addCommit("incremento el indice de heap")
                    generator.addExp(t0,t0,'0','+')

                    t2 = generator.addTemporal()
                    generator.addCommit("obtengo el ascci ++")
                    generator.getHeap(t2,t0)

                    retTemp = generator.addTemporal()
                    generator.addExp(retTemp, 'H', '', '')
                    generator.addCommit("asigno el ascii ++")
                    generator.setHeap('H', t2)   # heap[H] = ascii de c/u de los caracter de la cadena;
                    generator.nextHeap()
                    generator.setHeap('H', '-1')            # FIN DE CADENA q es -1
                    generator.nextHeap()  

                    generator.addCommit("al stack le meto el puntero de la nueva cadena")
                    generator.setStack(simbolo.size,retTemp)
                    
                    
                    generator.inputLabel(Recursividad)

                    condicion = condicion0.compilar(tree,table) #nos puede traer un suma variable condicio if
                    #por si tenemos un error en lo anterior
                    if isinstance(condicion, Excepcion): return condicion#retorno la excepcion q me esta trayendo condicion por si tiene, ponerlo siempre

                    if condicion.tipo ==tipo.BOOLEANO:#ya encontro el bool

                        generator.inputLabel(condicion.trueLbl)
                        nuevaTabla =TablaSimbolos(table) #nueva tabla, porq es un NUEVO AMBITO
                        nuevaTabla.breakLbl=condicion.falseLbl
                        nuevaTabla.continueLbl=Recursividad
                        #--------------------------------------------
                        nuevaTabla.continueString=True
                        nuevaTabla.tempLblPlusOne=inicio.valor
                        t2 = generator.addTemporal()
                        nuevaTabla.temp2Lbl=t2
                        retTemp = generator.addTemporal()
                        nuevaTabla.retTemp=retTemp
                        nuevaTabla.simboloSize=simbolo.size
                        #--------------------------------------------

                        for instruccion in self.instrucciones:

                            '''if isinstance(instruccion,If):

                                for if_inst in instruccion.instruccionesIf:
                                    if isinstance(if_inst,Continue):
                                        
                                        generator.addCommit("incremento el indice de heap")
                                        generator.addExp(t10,t10,'1','+')

                                        t2 = generator.addTemporal()
                                        generator.addCommit("obtengo el ascci ++")
                                        generator.getHeap(t2,t10)

                                        retTemp = generator.addTemporal()
                                        generator.addExp(retTemp, 'H', '', '')
                                        generator.addCommit("asigno el ascii ++")
                                        generator.setHeap('H', t2)   # heap[H] = ascii de c/u de los caracter de la cadena;
                                        generator.nextHeap()
                                        generator.setHeap('H', '-1')            # FIN DE CADENA q es -1
                                        generator.nextHeap()  
                                        generator.addCommit("al stack le meto el puntero de la nueva cadena")
                                        generator.setStack(simbolo.size,retTemp)'''


                                

                            #print("--PED43AZO D434E M4IE343RD4343AA"+str(instruccion))
                            result =instruccion.compilar(tree,nuevaTabla)#ejecuta instruccion adentro if, y usa el NUEVO AMBITO del if
                            
                            if isinstance(result, Excepcion): 
                                tree.getExcepciones().append(result)


                        


                        #creo la letra++
                        generator.addCommit("incremento el indice de heap")
                        generator.addExp(inicio.valor,inicio.valor,'1','+')

                        
                        generator.addCommit("obtengo el ascci ++")
                        generator.getHeap(t2,inicio.valor)

                        
                        generator.addExp(retTemp, 'H', '', '')
                        generator.addCommit("asigno el ascii ++")
                        generator.setHeap('H', t2)   # heap[H] = ascii de c/u de los caracter de la cadena;
                        generator.nextHeap()
                        generator.setHeap('H', '-1')            # FIN DE CADENA q es -1
                        generator.nextHeap()  

                        generator.addCommit("al stack le meto el puntero de la nueva cadena")
                        generator.setStack(simbolo.size,retTemp)


                        generator.addCommit("para q se cague diria xd")
                        ##############para q no se encicle infinitamente
                        t1 = generator.addTemporal()
                        generator.getHeap(t1,inicio.valor)
                        generator.addIf(t1,'-1','==',condicion.falseLbl)
                        #######################################continuidad
                        generator.addGoto(Recursividad)
                        generator.inputLabel(condicion.falseLbl)
                        return None   
                    
                    else:
                        generator.inputLabel(condicion.trueLbl)#como queda inconcluso hago esto
                        generator.inputLabel(condicion.falseLbl)

                        return Excepcion("Semantico","Tipo de condicion for no Booleano", self.fila,self.columna)

                elif inicio.tipo==tipo.ARREGLO:
                   
                    generator.addCommit("EXECUTE ORDER 66 ")
                    polo = Asignacion(self.condicion.identificador,self.condicion2['forString'], self.fila, self.columna)
                    polo.compilar(tree,table)


                    simbolo2 = table.getTabla(self.condicion.identificador)
                    if simbolo2==None:return Excepcion("Semantico","Variable "+self.identificador+"  no encontrada en TablaSimbolos", self.fila,self.columna)
                    final = Primitivos(tipo.ENTERO,len(simbolo2.valor.Array), self.fila, self.columna)#creo el fin de cadena


                    ARRAYs = simbolo2.valor.Array


                    inicial = Primitivos(tipo.ENTERO, 1 , self.fila, self.columna)#creo el fin de cadena
                    polo2 = Asignacion('Veces',inicial, self.fila, self.columna)
                    polo2.compilar(tree,table)


                    ider = Identificador('Veces',self.fila, self.columna)

                    condicion0 = Relacional(operador_relacional.MENORQUE,ider,final,self.fila,self.columna)
                    Recursividad = generator.newLabel()


                    '''
                    	T0=T0+1;
                        T10001 = heap[int(T0)]
                        stack[int(0)]=T10001;
                    '''

                    generator.addCommit("agrego el ++ para indice de for")
                    simbolo = table.getTabla(self.condicion.identificador)
                    if simbolo==None:return Excepcion("Semantico","Variable "+self.identificador+"  no encontrada en TablaSimbolos", self.fila,self.columna)


                    generator.addCommit(">>>>>al stack le meto el puntero del item del array")
                    generator.addExp(simbolo2.valor.valor,simbolo2.valor.valor,'1','+')
                    t10001 = generator.addTemporal()
                    generator.getHeap(t10001,simbolo2.valor.valor)
                    generator.setStack(simbolo.size,t10001)

                    onix = str(simbolo2.valor.valor)
                    
                    simbolo2.tipo= simbolo2.valor.Array[0].tipo
                    simbolo2.valor = ARRAYs[0]

                    

                    result,newVar = table.actualizarTabla(simbolo2)#lo modifico o no lo hizo 
                    if isinstance(result,Excepcion):return result
                    
                    generator.inputLabel(Recursividad)

                    condicion = condicion0.compilar(tree,table) #nos puede traer un suma variable condicio if
                    #por si tenemos un error en lo anterior
                    if isinstance(condicion, Excepcion): return condicion#retorno la excepcion q me esta trayendo condicion por si tiene, ponerlo siempre

                    if condicion.tipo ==tipo.BOOLEANO:#ya encontro el bool
                        generator.addCommit("bueno entre aqui xd")
                        generator.inputLabel(condicion.trueLbl)
                        nuevaTabla =TablaSimbolos(table) #nueva tabla, porq es un NUEVO AMBITO
                        nuevaTabla.breakLbl=condicion.falseLbl
                        nuevaTabla.continueLbl=Recursividad
                        #--------------------------------------------
                        nuevaTabla.continueString=True
                        nuevaTabla.tempLblPlusOne=simbolo2.valor
                        t2 = generator.addTemporal()
                        nuevaTabla.temp2Lbl=t2
                        retTemp = generator.addTemporal()
                        nuevaTabla.retTemp=retTemp
                        nuevaTabla.simboloSize=simbolo.size
                        #--------------------------------------------

                        for instruccion in self.instrucciones:
                            #print("--PED43AZO D434E M4IE343RD4343AA"+str(instruccion))
                            result =instruccion.compilar(tree,nuevaTabla)#ejecuta instruccion adentro if, y usa el NUEVO AMBITO del if

                            if isinstance(result, Excepcion): 
                                tree.getExcepciones().append(result)



                        simbolo3 = table.getTabla(ider.identificador)
                        if simbolo3==None:return Excepcion("Semantico","Variable "+self.identificador+"  no encontrada en TablaSimbolos", self.fila,self.columna)

                        t5 = generator.addTemporal()
                        generator.getStack(t5,simbolo3.size)

                        t6 = generator.addTemporal()
                        generator.addExp(t6,t5,'1','+')
                        generator.setStack(simbolo3.size,t6)


                        #aqui el ++ del item del for a.k.a ID
                        generator.addCommit("========= el ++ para el id del array =========")
                        generator.addCommit(">>>>>al stack le meto el puntero del item del array")
                        generator.addExp(onix,onix,'1','+')
                        t10001 = generator.addTemporal()
                        generator.getHeap(t10001,onix)
                        generator.setStack(simbolo.size,t10001)



                        generator.addIf(t6,len(ARRAYs),'<=',Recursividad)
                        generator.addGoto(condicion.falseLbl)
                        generator.inputLabel(condicion.falseLbl)


                        #generator.setStack(simbolo.size,ARRAYs[0].valor)

                        return None
                    else:
                        generator.inputLabel(condicion.trueLbl)#como queda inconcluso hago esto
                        generator.inputLabel(condicion.falseLbl)

                        return Excepcion("Semantico","Tipo de condicion for no Booleano", self.fila,self.columna)

                    #return None
                  

                        
                return Excepcion("Semantico","Tipo de dominio no de tipo cadena en for", self.fila,self.columna)
                
                
                    
                    
    



            #for array xd       
                    
                    
                                

                            








#for num:num





                                                    
            elif self.condicion2['inicio_for']!=None and self.condicion2['fin_for']!=None and self.condicion2['forString']==None:
                genAux = Generator()
                generator = genAux.getInstance()#obtengo mi static generator
                generator.addCommit("_________INICIO DE FOR INDICE IN 1:5_________")

                inicio = self.condicion2['inicio_for'].compilar(tree,table)
                if isinstance(inicio, Excepcion): return inicio
                final = self.condicion2['fin_for'].compilar(tree,table)
                if isinstance(final, Excepcion): return final


                if inicio.tipo==tipo.ENTERO and final.tipo==tipo.ENTERO:

                    #print("/////////////////////////")
                    #print(str(inicio))
                    #print(str(final))
                    #print("/////////////////////////")


                    polo = Asignacion(self.condicion.identificador,self.condicion2['inicio_for'], self.fila, self.columna)
                    polo.compilar(tree,table)
                    generator.addCommit("fin de asingacion a condicion con inicio_for")

                    condicion0 = Relacional(operador_relacional.MENORQUE,self.condicion,self.condicion2['fin_for'],self.fila,self.columna)
                    Recursividad = generator.newLabel()
                    generator.inputLabel(Recursividad)

                    condicion = condicion0.compilar(tree,table) #nos puede traer un suma variable condicio if
                    #por si tenemos un error en lo anterior
                    if isinstance(condicion, Excepcion): return condicion#retorno la excepcion q me esta trayendo condicion por si tiene, ponerlo siempre

                    if condicion.tipo ==tipo.BOOLEANO:#ya encontro el bool

                        generator.inputLabel(condicion.trueLbl)
                        nuevaTabla =TablaSimbolos(table) #nueva tabla, porq es un NUEVO AMBITO
                        nuevaTabla.breakLbl=condicion.falseLbl
                        nuevaTabla.continueLbl=Recursividad
                        #--------------------------------------------
                        nuevaTabla.continueInt=True
                        simbolo = table.getTabla(self.condicion.identificador)
                        if simbolo==None:return Excepcion("Semantico","Variable "+self.identificador+"  no encontrada en TablaSimbolos", self.fila,self.columna)
                        t0 = generator.addTemporal()
                        nuevaTabla.t0=t0
                        nuevaTabla.intSimboloSize=simbolo.size
                        
                        #--------------------------------------------

                        for instruccion in self.instrucciones:
                            result =instruccion.compilar(tree,nuevaTabla)#ejecuta instruccion adentro if, y usa el NUEVO AMBITO del if
                            
                            if isinstance(result, Excepcion): 
                                tree.getExcepciones().append(result)


                        generator.addCommit("agrego el ++ para indice de for")
                        if(not simbolo.global1):#ME DA MIEDO LO DE GLOBAL1 QUE LO IMPLEMENTO EL AUX A COMPARACION DE QUE YO MUEVO Y MUEVO EN TS HASTA HALLAR LA VARIABLE "GLOBAL"
                            tempPos = generator.addTemporal()
                            generator.addExp(tempPos, 'P', simbolo.size, "+")
                        
                            generator.addCommit(" saco el indice y le hago ++")
                            generator.getStack(t0,tempPos)
                            generator.addExp(t0,t0,'1','+')
                            generator.setStack(tempPos,t0)

                        else:
                            generator.addCommit(" saco el indice y le hago ++")
                            generator.getStack(t0,simbolo.size)
                            generator.addExp(t0,t0,'1','+')
                            generator.setStack(simbolo.size,t0)
                        #######################################continuidad
                        generator.addGoto(Recursividad)
                        generator.inputLabel(condicion.falseLbl)
                        return None   
                    
                    else:
                        generator.inputLabel(condicion.trueLbl)#como queda inconcluso hago esto
                        generator.inputLabel(condicion.falseLbl)

                        return Excepcion("Semantico","Tipo de condicion for no Booleano", self.fila,self.columna)

               
                return Excepcion("Semantico","Tipo de dominio no de tipo numerico en for", self.fila,self.columna)
                
                
        
            
                




        