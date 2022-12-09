#   soy print simple PRACTICAMENTE LA GRAM A CODIGO

from Expresiones.aritmetica import Aritmetica
from Instrucciones.LLamarArray import LLamarArray
from Instrucciones.Struct import Struct
from Expresiones.primitivos import Primitivos
from typing import List
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Tipo import operador_aritmetico, tipo



class Imprimir(instruccion):# es como un nodo y se arma el arbol con estos nodos
    def __init__(self, expresion , fila, columna,tipo ):
        self.expresion=expresion# en un print solo nos importa la expresion a imprimir asi q F por los parentesis
        self.fila=fila
        self.columna=columna
        self.tipo=tipo

        self.arbolPrint=None
        self.tablaPrint=None


        self.LV=""
        self.LF=""


    def interpretar(self, tree, table):

        #asigno arbol como tabla al print para su ambito
        self.arbolPrint=tree
        self.tablaPrint=table

        if isinstance(self.expresion, List):
            #print("ohhhh yeahhhh prints concatenacion!!!!")
            varAprint=""

            for param in self.expresion:

                value = param.interpretar(tree,table)
                if isinstance(value, Excepcion):return value

                if isinstance(value, List):
                    cadenita = self.verArray(value,tree,table)
                    value = cadenita 

                #if isinstance(value, str) or isinstance(value, int) or isinstance(value, float) or isinstance(value, bool) or isinstance(value, None):
                 #   varAprint+=str(value)
                #else:

                if isinstance(value, Aritmetica):

                    #print("JAVIER F"+str(value))
                    
                    value90 = value.interpretar(tree,table)
                    if isinstance(value, Excepcion):return value
                    value = value90


                varAprint+=str(value)
                #print("\n\narray impresion----\n\n"+varAprint)

            if self.tipo==0:
                tree.updateConsola(varAprint,0)#0 si es print
            else:
                tree.updateConsola(varAprint,1)#1 si es printl

            #print(varAprint)
            return None

        #si no viene concatenacion
        #print(str(self.expresion))

        value = self.expresion.interpretar(tree,table) #retorna cualquier valor
        #print("...........................................")
        #print(str(value))

        #por si tenemos un error en lo anterior
        if isinstance(value, Excepcion):
            return value#lo retornamos

        if self.expresion.tipo==tipo.ARREGLO:#debo de crear el value para q me imprima lo del arreglo

            
            cadenita = self.verArray(value,tree,table)
            
            #print(cadenita)  
            if self.tipo==0:
                tree.updateConsola(cadenita,0)#0 si es print
            else:
                tree.updateConsola(cadenita,1)#1 si es println
            return None #aguas puede hacer cagadales xd

            #return Excepcion("Semantico","No se puede imprimir un arreglo completo", self.fila,self.columna)
        

        #si viene un tipo primitivo lo interpretammos
        if isinstance(value, Primitivos):
            value = value.interpretar(tree,table)
            if isinstance(value, Excepcion):return value
            #print("shieeet TONO ENTRE AQUI XD......")


        #si no tiene errores


        if isinstance(value,Struct):
            result = tree.getStruct(value.nombre)
            if isinstance(result, Excepcion):return result
            
            value = result

            #print("TONO ENTRE AQUI XD......")
            #print(str(value))


        if self.tipo==0:
            tree.updateConsola(value,0)#0 si es print
        else:
            tree.updateConsola(value,1)#1 si es println
        
        return None #aguas puede hacer cagadales xd


    
    def getNodo(self):
        nodo = NodoAST("IMPRIMIR")
        try:

            nodo.agregarHijoNodo(self.expresion.getNodo() )#PUEDE COMO NO PUEDE VENIR JAVIER
            return nodo
            
        except :
            parametros = NodoAST("LISTA_IMPRIMIR")
            for param in self.expresion:
                try:
                    value = param.interpretar(self.arbolPrint,self.tablaPrint)
                    if isinstance(value, Excepcion): return value
                    parametros.agregarHijoNodo(NodoAST(str(value)))

                except:
                    parametros.agregarHijoNodo(NodoAST(str(param)))#corregido


            
            nodo.agregarHijoNodo(parametros)
            #nodo.agregarHijoNodo(self.expresion)#PUEDE COMO NO PUEDE VENIR JAVIER
            return nodo
        
 
        
        


    def verArray(self,value,tree,table):
            cadenita=""
            init=False
            #for para ver si detecto en mis elementos del array otro array

            try:    
                cadenita="["
                for expresion in value:#recorro la lista de elementos q posee el array
                        resultExpresion = expresion.interpretar(tree,table)#c\u de los elementos del array interpretar
                        
                        if isinstance(resultExpresion, Excepcion):return resultExpresion#por si me da error
                        if init:
                            cadenita +=","
                        init=True

                        try:
                            if isinstance(resultExpresion, List):
                                #print("[array detected!]") 
                                cadenita += self.verArray(resultExpresion,tree,table)           #pensar para q salgan primitivos
                        except: 
                            print("F (T.T) List en isinstance dio clavo..."+str(resultExpresion))


                        try:
                            if isinstance(resultExpresion, LLamarArray):
                                print("[LLamarArray detected!]")


                            if isinstance(value, Aritmetica):

                                #print("JAVIER F" + str(value))

                                value90 = value.interpretar(tree, table)
                                if isinstance(value, Excepcion): return value
                                value = value90
                                
                        except: 
                            print("F (T.T) List en isinstance dio clavo..."+str(resultExpresion))

                        if isinstance(resultExpresion, List):
                            pass
                        else:
                            cadenita += str(resultExpresion)

                cadenita += "]"

            except:
                cadenita += str(value) 
                
            return cadenita





    def compilar(self, tree, table):
        #asigno arbol como tabla al print para su ambito
        self.arbolPrint=tree
        self.tablaPrint=table

        if isinstance(self.expresion, List):
            #print("ohhhh yeahhhh prints concatenacion!!!!")
            varAprint=""
            

            for param in self.expresion:

                val = param.compilar(tree,table)
                if isinstance(val, Excepcion):return val
                #si no tiene errores-------------------------------------------------------------------------------------------------------
                genAux = Generator()#hace la magia de todo si lo implemento me ahorre un monton crea todo por asi decirlo
                generator = genAux.getInstance()

                if isinstance(val, List):
                    #NO SE QUE HACER EN VERSION C3D XD
                    cadenita = self.verArray(val,tree,table)
                    val = cadenita 

                

                if isinstance(val, Aritmetica):

                    #NO SE QUE HACER EN VERSION C3D XD
                    
                    value90 = val.compilar(tree,table)
                    if isinstance(value90, Excepcion):return value90
                    val = value90

                #print(">>>AQUI SE CAGA::::"+str(val))

                if val==None:
                    return


                if(val.tipo == tipo.ENTERO):
                    generator.addCommit("--------print entero---------")
                    generator.addPrint("d", val.valor)

                elif(val.tipo == tipo.DECIMAL):
                    generator.addCommit("--------print decimal--------")
                    generator.addPrint("f", val.valor)

                elif(val.tipo == tipo.NULO):
                    generator.addCommit("--------print Nothing--------")
                    tempLbl = generator.newLabel()#genero label para salir
            
                    generator.inputLabel(val.trueLbl)
                    
                    generator.addPrint("c", 110,"//N")#N
                    generator.addPrint("c", 111,"//o")#o
                    generator.addPrint("c", 116,"//t")#t
                    generator.addPrint("c", 104,"//h")#i
                    generator.addPrint("c", 105,"//i")#i
                    generator.addPrint("c", 110,"//n")#n
                    generator.addPrint("c", 103,"//g")#g
                    
                    generator.addGoto(tempLbl)#se lo meto al c3d, etiqueta de escape o salida
                    
                    generator.inputLabel(val.falseLbl)
                    
                    generator.addPrint("f", val.valor)#si no fuera nothing entonces imprimo en num -1997.0509
                    

                    generator.inputLabel(tempLbl)#se lo meto al c3d, etiqueta de escape o salida

                elif val.tipo == tipo.BOOLEANO:
                    generator.addCommit("---------print bool-----------")
                    tempLbl = generator.newLabel()#genero label
                    
                    generator.inputLabel(val.trueLbl)
                    generator.printTrue()
                    
                    generator.addGoto(tempLbl)#se lo meto al c3d
                    
                    generator.inputLabel(val.falseLbl)
                    generator.printFalse()

                    generator.inputLabel(tempLbl)

                elif val.tipo == tipo.CADENA:
                    generator.addCommit("-------------print cadena-------------")
                    generator.fPrintString()

                    paramTemp = generator.addTemporal()
                    
                    generator.addExp(paramTemp, 'P', table.size, '+')#table.size seria el ambito cuando guarde ya en pila le tengo que aumentar
                    generator.addExp(paramTemp, paramTemp, '1', '+')
                    generator.setStack(paramTemp, val.valor)
                    
                    generator.newEnv(table.size)
                    generator.callFuncion('printString')

                    temp = generator.addTemporal()
                    generator.getStack(temp, 'P')
                    generator.retEnv(table.size)

                elif val.tipo == tipo.CHARACTER:
                    generator.addCommit("-------------------print char---------------")
                    generator.fPrintArray()

                    paramTemp = generator.addTemporal()
                    
                    generator.addExp(paramTemp, 'P', table.size, '+')
                    generator.addExp(paramTemp, paramTemp, '1', '+')
                    generator.setStack(paramTemp, val.valor)
                    
                    generator.newEnv(table.size)
                    generator.callFuncion('printArray')

                    temp = generator.addTemporal()
                    generator.getStack(temp, 'P')
                    generator.retEnv(table.size)


                elif val.tipo == tipo.ARREGLO:
                    self.imprimirArreglo(val,generator,tree,table)



                else:#creo q seria para struct nada mas
                    print("print etc. adaptar de lo q hice en proyecto 1")
                

            if self.tipo==1:
                    generator.addPrint("c", 10)

                    #print(">>>>>>>><<<<<<<<<<<"+generator.getCodigo())

                    #print(varAprint)
                    return None

        #si no viene concatenacion
        #print(str(self.expresion))
        #######################################################################################################
        else:
            val = self.expresion.compilar(tree, table)

        if isinstance(val, Excepcion):
            return val#lo retornamos

        '''if self.expresion.tipo==tipo.ARREGLO:#debo de crear el value para q me imprima lo del arreglo
            #IN WORK
            cadenita = self.verArray(val,tree,table)
            if self.tipo==0:
                tree.updateConsola(cadenita,0)#0 si es print
            else:
                tree.updateConsola(cadenita,1)#1 si es println
            return None #aguas puede hacer cagadales xd'''
        
        #si viene un tipo primitivo lo interpretammos
        if isinstance(val, Primitivos):
            val = val.interpretar(tree,table)
            if isinstance(val, Excepcion):return val
            #IN WORK
            
        

        if isinstance(val,Struct):
            result = tree.getStruct(val.nombre)
            if isinstance(result, Excepcion):return result
            value = result
            #IN WORK


#si no tiene errores-------------------------------------------------------------------------------------------------------
        genAux = Generator()#hace la magia de todo si lo implemento me ahorre un monton crea todo por asi decirlo
        generator = genAux.getInstance()

        #print(">>>AQUI SE CAGA::::"+str(val))

        if val==None:
            return

        if(val.tipo == tipo.ENTERO):
            generator.addCommit("--------print entero---------")
            generator.addPrint("d", val.valor)

        elif(val.tipo == tipo.DECIMAL):
            generator.addCommit("--------print decimal--------")
            generator.addPrint("f", val.valor)

        elif(val.tipo == tipo.NULO):
                    
                    generator.addCommit("--------print Nothing--------")
                    tempLbl = generator.newLabel()#genero label para salir
            
                    generator.inputLabel(val.trueLbl)
                    
                    generator.addPrint("c", 110,"//N")#N
                    generator.addPrint("c", 111,"//o")#o
                    generator.addPrint("c", 116,"//t")#t
                    generator.addPrint("c", 104,"//h")#i
                    generator.addPrint("c", 105,"//i")#i
                    generator.addPrint("c", 110,"//n")#n
                    generator.addPrint("c", 103,"//g")#g
                    
                    generator.addGoto(tempLbl)#se lo meto al c3d, etiqueta de escape o salida
                    
                    generator.inputLabel(val.falseLbl)
                    
                    generator.addPrint("f", val.valor)#si no fuera nothing entonces imprimo en num -1997.0509
                    

                    generator.inputLabel(tempLbl)#se lo meto al c3d, etiqueta de escape o salida
                    

        elif val.tipo == tipo.BOOLEANO:
            generator.addCommit("---------print bool-----------")
            tempLbl = generator.newLabel()#genero label para salir

            
            generator.inputLabel(val.trueLbl)
            generator.printTrue()
            
            generator.addGoto(tempLbl)#se lo meto al c3d, etiqueta de escape o salida
            
            generator.inputLabel(val.falseLbl)
            generator.printFalse()

            generator.inputLabel(tempLbl)#se lo meto al c3d, etiqueta de escape o salida

        elif val.tipo == tipo.CADENA:
            generator.addCommit("-------------print cadena-------------")
            generator.fPrintString()

            paramTemp = generator.addTemporal()
            
            generator.addExp(paramTemp, 'P', table.size, '+')#table.size seria el ambito cuando guarde ya en pila le tengo que aumentar
            generator.addExp(paramTemp, paramTemp, '1', '+')
            generator.setStack(paramTemp, val.valor)
            
            generator.newEnv(table.size)
            generator.callFuncion('printString')

            temp = generator.addTemporal()
            generator.getStack(temp, 'P')
            generator.retEnv(table.size)

        elif val.tipo == tipo.CHARACTER:
            generator.addCommit("-------------------print char---------------")
            generator.fPrintString()

            paramTemp = generator.addTemporal()
            
            generator.addExp(paramTemp, 'P', table.size, '+')
            generator.addExp(paramTemp, paramTemp, '1', '+')
            generator.setStack(paramTemp, val.valor)
            
            generator.newEnv(table.size)
            generator.callFuncion('printString')

            temp = generator.addTemporal()
            generator.getStack(temp, 'P')
            generator.retEnv(table.size)

        elif val.tipo == tipo.ARREGLO:
            '''generator.addCommit("-------------------print array---------------")
            generator.fPrintArray()

            paramTemp = generator.addTemporal()
            
            generator.addExp(paramTemp, 'P', table.size, '+')
            generator.addExp(paramTemp, paramTemp, '1', '+')
            generator.setStack(paramTemp, val.valor)
            
            generator.newEnv(table.size)
            generator.callFuncion('printArray')

            temp = generator.addTemporal()
            generator.getStack(temp, 'P')
            generator.retEnv(table.size)'''

            self.imprimirArreglo(val,generator,tree,table)


        else:#creo q seria para struct nada mas
            print("array etc. adaptar de lo q hice en proyecto 1")
        

        if self.tipo==1:
            generator.addPrint("c", 10)

            #print(">>>>>>>><<<<<<<<<<<"+generator.getCodigo())
            
        
        return None #aguas puede hacer cagadales xd

























    def imprimirArreglo(self,val,generator,tree,table):
        generator.addCommit("-------------------print array--------------- longitud:"+str(val.Array))
        if len(val.Array)>=1:
            contador=0
            generator.addPrint('c', 91,"//[")#[
            for item in val.Array:

                if item.tipo ==tipo.ARREGLO:
                    #generator.addPrint('c', 91)#[
                    self.imprimirArreglo(item,generator,tree,table)
                    #generator.addPrint('c', 93)# ]
                else:
                    if(item.tipo == tipo.ENTERO):
                        generator.addCommit("--------print entero---------")
                        if item.posicion==-1:
                            generator.addPrint("d", item.valor)

                        else:
                            temp = generator.addTemporal()
                            generator.getHeap(temp,item.posicion)
                            generator.addPrint("d", temp)

                    elif(item.tipo == tipo.DECIMAL):
                        generator.addCommit("--------print decimal--------")
                        if item.posicion==-1:
                            generator.addPrint("f", item.valor)

                        else:
                            temp = generator.addTemporal()
                            generator.getHeap(temp,item.posicion)
                            generator.addPrint("f", temp)

                    elif(item.tipo == tipo.NULO):
                                
                                generator.addCommit("--------print Nothing--------")
                                tempLbl = generator.newLabel()#genero label para salir
                        
                                generator.inputLabel(item.trueLbl)
                                
                                generator.addPrint("c", 110,"//N")#N
                                generator.addPrint("c", 111,"//o")#o
                                generator.addPrint("c", 116,"//t")#t
                                generator.addPrint("c", 104,"//h")#i
                                generator.addPrint("c", 105,"//i")#i
                                generator.addPrint("c", 110,"//n")#n
                                generator.addPrint("c", 103,"//g")#g
                                
                                generator.addGoto(tempLbl)#se lo meto al c3d, etiqueta de escape o salida
                                
                                generator.inputLabel(item.falseLbl)
                                
                                generator.addPrint("f", item.valor)#si no fuera nothing entonces imprimo en num -1997.0509
                                

                                generator.inputLabel(tempLbl)#se lo meto al c3d, etiqueta de escape o salida
                                

                    elif item.tipo == tipo.BOOLEANO:
                        generator.addCommit("---------print bool-----------")

                        # Temporal para guardar variable
                        temp = generator.addTemporal()

                        
                        self.LV = generator.newLabel()
                        
                        self.LF = generator.newLabel()

                        if item.valor == True:
                            #generator.addExp(temp,1,'','')
                            generator.getHeap(temp,item.posicion)
                        else:
                            #generator.addExp(temp,0,'','')
                            generator.getHeap(temp,item.posicion)
                        
                        #generator.getHeap(temp,)
                        
                        generator.addIf(temp, '1', '==', self.LV)
                        generator.addGoto(self.LF)

                        generator.addCommit("Fin compilacion acceso")
                        generator.addSaltoLinea()

                        item.trueLbl = self.LV
                        item.falseLbl = self.LF


                        tempLbl = generator.newLabel()#genero label para salir
                        
                        generator.inputLabel(item.trueLbl)
                        generator.printTrue()
                        
                        generator.addGoto(tempLbl)#se lo meto al c3d, etiqueta de escape o salida
                        
                        generator.inputLabel(item.falseLbl)
                        generator.printFalse()

                        generator.inputLabel(tempLbl)#se lo meto al c3d, etiqueta de escape o salida

                    elif item.tipo == tipo.CADENA:
                        generator.addCommit("-------------print cadena-------------")
                        generator.fPrintString()

                        paramTemp = generator.addTemporal()
                        
                        generator.addExp(paramTemp, 'P', table.size, '+')#table.size seria el ambito cuando guarde ya en pila le tengo que aumentar
                        generator.addExp(paramTemp, paramTemp, '1', '+')
                        generator.setStack(paramTemp, item.valor)
                        
                        generator.newEnv(table.size)
                        generator.callFuncion('printString')

                        temp = generator.addTemporal()
                        generator.getStack(temp, 'P')
                        generator.retEnv(table.size)

                    elif item.tipo == tipo.CHARACTER:
                        generator.addCommit("-------------------print char---------------")
                        generator.fPrintString()

                        paramTemp = generator.addTemporal()
                        
                        generator.addExp(paramTemp, 'P', table.size, '+')
                        generator.addExp(paramTemp, paramTemp, '1', '+')
                        generator.setStack(paramTemp, item.valor)
                        
                        generator.newEnv(table.size)
                        generator.callFuncion('printString')

                        temp = generator.addTemporal()
                        generator.getStack(temp, 'P')
                        generator.retEnv(table.size)


                contador+=1
                if contador!= len(val.Array):
                    generator.addPrint('c', 44,"//,")#,
                    

            generator.addPrint('c', 93,"//]")# ]


            
        else:#seria para arreglos vacios :( una troleada la verdad
            '''generator.fPrintArray()

            paramTemp = generator.addTemporal()
            
            generator.addExp(paramTemp, 'P', table.size, '+')
            generator.addExp(paramTemp, paramTemp, '1', '+')
            generator.setStack(paramTemp, val.valor)
            
            generator.newEnv(table.size)
            # generator.addCommit("PUTA HARRY")
            generator.callFuncion('printArray')

            temp = generator.addTemporal()
            generator.getStack(temp, 'P')
            generator.retEnv(table.size)'''

            generator.addPrint('c', 91)#[
            generator.addPrint('c', 93)# ]




    def imprimirC3DPrimi(self,value, tree, table):
                                                                                                                                                                                                                                                                                                                                                         
        tree.contador=tree.contador+1

        if value.tipo == tipo.CADENA:

            cadena = "T"+str(tree.contador)+" = "+ value.TMP+";\nfmt.Printf(\"%c\", ASCII);\n"#valor del primitivo a mostrar

        elif value.tipo == tipo.ENTERO:
    
            cadena = "T"+str(tree.contador)+" = "+ value.TMP+";\nfmt.Printf(\"%d\", int("+ "T"+str(tree.contador)+"));\n"#valor del primitivo a mostrar

        elif value.tipo == tipo.DECIMAL:
        
            cadena = "T"+str(tree.contador)+" = "+ value.TMP+";\nfmt.Printf(\"%f\", "+ "T"+str(tree.contador)+");\n"#valor del primitivo a mostrar

        elif value.tipo == tipo.CHARACTER:#char
        
            cadena = "T"+str(tree.contador)+" = "+ value.TMP+";\nfmt.Printf(\"%c\", ASCII);\n"#valor del primitivo a mostrar

        elif value.tipo == tipo.BOOLEANO:# van a ser 0,1
        
            cadena = "T"+str(tree.contador)+" = "+ value.TMP+";\nfmt.Printf(\"%d\", int("+ "T"+str(tree.contador)+"));\n"#valor del primitivo a mostrar


        return cadena



    def imprimirC3DArit(self,value, tree, table):
                                                                                                                                                                                                                                                                                                                                                         
        #tree.contador=tree.contador+1

        if value.tipo == tipo.CADENA:

            cadena = "fmt.Printf(\"%c\", ASCII);\n"#valor del primitivo a mostrar

        elif value.tipo == tipo.ENTERO:
    
            cadena = "fmt.Printf(\"%d\", int("+ ""+str(value.TMP)+"));\n"#valor del primitivo a mostrar

        elif value.tipo == tipo.DECIMAL:
        
            cadena = "fmt.Printf(\"%f\", "+ str(value.TMP)+");\n"#valor del primitivo a mostrar

        elif value.tipo == tipo.CHARACTER:#char
        
            cadena = "fmt.Printf(\"%c\", ASCII);\n"#valor del primitivo a mostrar

        elif value.tipo == tipo.BOOLEANO:# van a ser 0,1
        
            cadena = "fmt.Printf(\"%d\", int("+ ""+str(value.TMP)+"));\n"#valor del primitivo a mostrar


        return value.C3D+cadena