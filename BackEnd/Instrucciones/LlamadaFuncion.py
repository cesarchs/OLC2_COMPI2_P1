

from Abstract.NodoAST import NodoAST
from Expresiones.identificador import Identificador
from Expresiones.primitivos import Primitivos
from Instrucciones.FuncionSimple import FuncionSP
from posixpath import normcase
from Instrucciones.Break import Break
from Abstract.instruccion import instruccion
from Instrucciones.asignacion import Asignacion
from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Return2 import ReturnC3D
from TS.Tipo import tipo
from TS.TablaSimbolo import TablaSimbolos
from TS.Simbolo import Simbolo

class LlamadaFuncion(instruccion):
            
    def __init__(self,nombre,parametros,fila,columna ):
        self.nombre=nombre
        self.parametros = parametros #expresiones
        self.fila=fila
        self.columna=columna
        self.arreglo =False
        self.isStruct=0
        self.LV = ''
        self.LF = ''


    def interpretar(self, tree, table):
        #obtener la funcion en el ast
        result = tree.getFuncion(self.nombre)#self.nombre.lower()

        if result ==None:#no se encontro la funcion
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                    #obtener la funcion en el ast
            result = tree.getStruct(self.nombre)

            if result ==None:#no se encontro struct
                return Excepcion("Semantico","Error semantico, no es llamada de funcion ni struct como creacion [ "+str(self.nombre)+" ] no exite! ",self.fila,self.columna)

            nuevaTabla =TablaSimbolos(tree.getTablaSimbolosGlobal())#creamos un nueva tabla de simbolos para este ambito creo
            #pero debe de ser la de la tabla de simbolos y obtenerla de la llamada de funcion
            #pasamos en la tabla a pasar lo de la anterior para q no se pierda nada;ya q con ackermann se perdia info y no se pasaba

            

            #OBTENER PARAMS: hay q modificarla TuT pero valera la pena :D
            #comprobamos si el tam de params es igual al de la funcion
            if len(result.instrucciones)==len(self.parametros):



                #tengo q validar sino esta en la blackList de atributos del struct



                contador=0#para validar q sean del mismo tipo
                for expresion in self.parametros:#se obtiene el valor de param en la llamada

                    resultExpresion = expresion.interpretar(tree,table)#obtener los params de la tabla que nos trae el metodo interpretar 
                    #porq estamos en el abito de la llamada pero los nuevos valores se van a meter en la tabla simbolos global ;para q no se pierdan nuestras variables
                    
                    
                    
                    if isinstance(resultExpresion, Excepcion):return resultExpresion
                    

                    #validar q sean del mismo tipo
                    #JULIA ['tipo'] DEBO DE CAMBIARLO JAVIER PORQ NO LO LLEVA
                    if result.instrucciones[contador].tipo==expresion.tipo or result.instrucciones[contador].tipo==tipo.NULO :
                        #creacion de simbolo e ingresarlo a la tabla de simbolos

                        TypeNull=False#me va aservir si viene un param con atributo nothing, debido a que asi se concibio en los params de la funcion

                        if result.instrucciones[contador].tipo==tipo.NULO:
                            TypeNull=True


                            #print("\n\nKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK\n\n")
                            #print("en mis params de STRUCT->  "+str(result.instrucciones[contador].tipo))
                            #print("en mis params de CREACION->  "+str(self.parametros[contador].tipo))

                            simbolo = Simbolo(str(result.instrucciones[contador].identificador),self.parametros[contador].tipo,self.arreglo ,self.fila,self.columna,resultExpresion)
                            resultTablaS = nuevaTabla.setTabla(simbolo)#lo metemos a la tabla simbolos
                            if isinstance(resultTablaS,Excepcion): return resultTablaS#por si hubo error

                            #print("\n\nKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")


                        if TypeNull==False:

                            simbolo = Simbolo(str(result.instrucciones[contador].identificador),result.instrucciones[contador].tipo,self.arreglo  ,self.fila,self.columna,resultExpresion)
                            resultTablaS = nuevaTabla.setTabla(simbolo)#lo metemos a la tabla simbolos
                            if isinstance(resultTablaS,Excepcion): return resultTablaS#por si hubo error

                    else:
                        return Excepcion("Semantico","tipo de datos diferente en Parametros de CREACION STRUCT", self.fila,self.columna)
                    
                    
                    contador+=1


            else: 
                return Excepcion("Semantico","Error semantico, STRUCT [ "+str(self.nombre)+" ] tiene un numero de PARAMETROS incorrectos! ",self.fila,self.columna)

            #como si encontro la funcion entonces tenemos q interpretar
            value = result.interpretar(tree, nuevaTabla)#ejecutar la funcion; enviamos la nueva tabla a la funcion para q no se pierdan los datos
            if isinstance(value, Excepcion):return value
            #si no es error tonces lo q podemos pasar en la llamada venga como expresion tmabien le tenemos q asignar tipo

            self.tipo = result.tipoS        #sacrificio para obtener la funciones expresion de una           0=mutable    1=inmutable

            self.isStruct=1

            value.tablaSimbolosFuncion = nuevaTabla
            
            return value#sacrificio para obtener la funciones y expresion de una
            #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            #return Excepcion("Semantico","Error semantico, funcion [ "+str(self.nombre)+" ] llamada no exite! ",self.fila,self.columna)

        nuevaTabla =TablaSimbolos(tree.getTablaSimbolosGlobal())#creamos un nueva tabla de simbolos para este ambito creo
        #pero debe de ser la de la tabla de simbolos y obtenerla de la llamada de funcion
        #pasamos en la tabla a pasar lo de la anterior para q no se pierda nada;ya q con ackermann se perdia info y no se pasaba



        #OBTENER PARAMS: hay q modificarla TuT pero valera la pena :D
        #comprobamos si el tam de params es igual al de la funcion
        if len(result.parametros)==len(self.parametros):

            contador=0#para validar q sean del mismo tipo
            for expresion in self.parametros:#se obtiene el valor de param en la llamada

                resultExpresion = expresion.interpretar(tree,table)#obtener los params de la tabla que nos trae el metodo interpretar 
                #porq estamos en el abito de la llamada pero los nuevos valores se van a meter en la tabla simbolos global ;para q no se pierdan nuestras variables
                
                
                
                if isinstance(resultExpresion, Excepcion):return resultExpresion
                

                #validar q sean del mismo tipo
                #JULIA ['tipo'] DEBO DE CAMBIARLO JAVIER PORQ NO LO LLEVA
                if result.parametros[contador]['tipo']==expresion.tipo or result.parametros[contador]['tipo']==tipo.NULO :
                    #creacion de simbolo e ingresarlo a la tabla de simbolos

                    TypeNull=False#me va aservir si viene un param con atributo nothing, debido a que asi se concibio en los params de la funcion

                    if result.parametros[contador]['tipo']==tipo.NULO:
                        TypeNull=True


                        #print("\n\nKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK\n\n")
                        #print("en mis params de la funcion->  "+str(result.parametros[contador]['tipo']))
                        #print("en mis params de llamada->  "+str(self.parametros[contador].tipo))

                        simbolo = Simbolo(str(result.parametros[contador]['identificador']),self.parametros[contador].tipo,self.arreglo ,self.fila,self.columna,resultExpresion)
                        resultTablaS = nuevaTabla.setTabla(simbolo)#lo metemos a la tabla simbolos
                        if isinstance(resultTablaS,Excepcion): return resultTablaS#por si hubo error

                        #print("\n\nKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")


                    if TypeNull==False:

                        simbolo = Simbolo(str(result.parametros[contador]['identificador']),result.parametros[contador]['tipo'],self.arreglo  ,self.fila,self.columna,resultExpresion)
                        resultTablaS = nuevaTabla.setTabla(simbolo)#lo metemos a la tabla simbolos
                        if isinstance(resultTablaS,Excepcion): return resultTablaS#por si hubo error

                else:
                    return Excepcion("Semantico","tipo de datos diferente en Parametros de la llamada", self.fila,self.columna)
                
                
                contador+=1


        else: 
            return Excepcion("Semantico","Error semantico, funcion [ "+str(self.nombre)+" ] tiene un numero de PARAMETROS incorrectos! ",self.fila,self.columna)

        #como si encontro la funcion entonces tenemos q interpretar
        value = result.interpretar(tree, nuevaTabla)#ejecutar la funcion; enviamos la nueva tabla a la funcion para q no se pierdan los datos
        if isinstance(value, Excepcion):return value
        #si no es error tonces lo q podemos pasar en la llamada venga como expresion tmabien le tenemos q asignar tipo
        self.tipo = result.tipo#sacrificio para obtener la funciones expresion de una


        return value#sacrificio para obtener la funciones y expresion de una


#video 11 modifico la llamada debido aque aqui si los params alteran la cosa no como en la funcion q ahi solo se definen





    def getNodo(self):

        if self.isStruct==0:
            nodo = NodoAST("LLAMADA FUNCION")

        else:
            nodo = NodoAST("ACCESO/CREACION STRUCT")


        nodo.agregarHijo(str(self.nombre))#PUEDE COMO NO PUEDE VENIR JAVIER
        parametros = NodoAST("PARAMETROS")
        #VIDEO 15 MIN 51:40
        for param in self.parametros:
            parametros.agregarHijoNodo(param.getNodo())
        nodo.agregarHijoNodo(parametros)
        
        return nodo



    





    def compilar(self, tree, table):
        #obtener la funcion en el ast
        result = tree.getFuncion(self.nombre)#self.nombre.lower()

        #LLAMAR A FUNCION CON GENERATOR
        genAux = Generator()#hace la magia de todo si lo implemento me ahorre un monton crea todo por asi decirlo
        generator = genAux.getInstance()

        
        if result ==None:#no se encontro la funcion
            print('debo de hacer para struct q entra aqui >:v')
            return None


        nuevaTabla =TablaSimbolos(tree.getTablaSimbolosGlobal())#creamos un nueva tabla de simbolos para este ambito creo
        #pero debe de ser la de la tabla de simbolos y obtenerla de la llamada de funcion
        #pasamos en la tabla a pasar lo de la anterior para q no se pierda nada;ya q con ackermann se perdia info y no se pasaba



        #OBTENER PARAMS: hay q modificarla TuT pero valera la pena :D
        #comprobamos si el tam de params es igual al de la funcion
        if len(result.parametros)==len(self.parametros):

            generator.addCommit("SI TENGO EL #PARAMS CORRECTO :V")

            #por defecto en la funcion meto el return como atributo 0
            simbolo = Simbolo("RETURN_VALOR_funcion",result.tipo,None,self.fila,self.columna,-1,0,(result.tipo == tipo.CADENA or result.tipo == tipo.ARREGLO))
            resultTablaS = nuevaTabla.setTabla(simbolo)#lo metemos a la tabla simbolos
            if isinstance(resultTablaS,Excepcion): return resultTablaS#por si hubo error



            unavez=True
           

            contador=0#para validar q sean del mismo tipo
            for expresion in self.parametros:#se obtiene el valor de param en la llamada

                #generator.addCommit(">>>COMPILO C/U DE LOS PARAMS:"+str(expresion.valor))
                resultExpresion = expresion.compilar(tree,table)#obtener los params de la tabla que nos trae el metodo interpretar 
                #porq estamos en el abito de la llamada pero los nuevos valores se van a meter en la tabla simbolos global ;para q no se pierdan nuestras variables
                
                if isinstance(resultExpresion, Excepcion):return resultExpresion
                
                #generator.addCommit(">>>FIN DE COMPILO C/U DE LOS PARAMS:"+str(resultExpresion.valor))
                
                

                #validar q sean del mismo tipo
                #JULIA ['tipo'] DEBO DE CAMBIARLO JAVIER PORQ NO LO LLEVA
                if result.parametros[contador]['tipo']==resultExpresion.tipo or result.parametros[contador]['tipo']==tipo.NULO:
                    #creacion de simbolo e ingresarlo a la tabla de simbolos

                    TypeNull=False#me va aservir si viene un param con atributo nothing, debido a que asi se concibio en los params de la funcion

                    if result.parametros[contador]['tipo']==tipo.NULO:
                        TypeNull=True


                        return Excepcion("Semantico","tipo de dato sin especificar { "+str(resultExpresion.tipo)+"| "+str(resultExpresion)+" }, en Parametro: "+str(result.parametros[contador]['identificador'])+"", self.fila,self.columna)
                


                    else:


                        if unavez==True and generator.inFunc == True:
                            generator.addCommit("JAVIER PIENSA.............")
                            unavez=False
                            a1 = generator.funcsB
                            a2 = a1.split(self.nombre+"();")
                            a3=a2[0]
                            
                            #print("javierPiensa------------------------------------\n\n\n"+a3)
                            a=a3
                            generator.temps_backUp=[]
                            #print("\n\n==================================")
                            for temp in generator.temps:
                                #print(temp)
                                b = temp
                                if a.count(b) >=2:            # find return position of string if found else -1
                                    #print(b)
                                    pass
                                else:

                                    if b in generator.tempsNO:
                                        #print(b+" este nel")
                                        break
                                    else:
                                        #print(b+"   bingo...")
                                        generator.addCommit("meto bckup------------------------------")
                                        #id = Identificador(temp,self.fila,self.columna)
                                        #polo = Asignacion(id,Primitivos(tipo.ENTERO,b,self.fila,self.columna), self.fila, self.columna)
                                        
                                        simbolo = Simbolo(temp,tipo.ENTERO,self.arreglo  ,self.fila,self.columna,b,0,(result.parametros[contador]['tipo'] == tipo.CADENA or result.parametros[contador]['tipo'] == tipo.ARREGLO))
                                        fail,resultTablaS = table.setTabla(simbolo)#lo metemos a la tabla simbolos
                                        if isinstance(resultTablaS,Excepcion): return resultTablaS#por si hubo error
                                        #print(str(resultTablaS))
                                        paramTemp = generator.addTemporal2()
                                        
                                        generator.addExp(paramTemp, 'P', table.size, '+')#table.size seria el ambito cuando guarde ya en pila le tengo que aumentar
                                        
                                        generator.setStack(paramTemp, b)

                                        simbolo.size=table.size
                                        table.actualizarTabla(simbolo)
                                        generator.temps_backUp.append(b)
                            #print("==================================\n\ntemps:::"+str(generator.temps_backUp)+"\n\n")
                            nuevaTabla.size = table.size

                        simbolo = Simbolo(str(result.parametros[contador]['identificador']),result.parametros[contador]['tipo'],self.arreglo  ,self.fila,self.columna,resultExpresion,0,(result.parametros[contador]['tipo'] == tipo.CADENA or result.parametros[contador]['tipo'] == tipo.ARREGLO))
                        resultTablaS = nuevaTabla.setTabla(simbolo)#lo metemos a la tabla simbolos
                        if isinstance(resultTablaS,Excepcion): return resultTablaS#por si hubo error


                        

                        #vamos bien OK
                        paramTemp = generator.addTemporal2()
                        generator.addCommit("******************************************** PASO DE PARAM "+self.nombre)
                        generator.addExp(paramTemp, 'P', table.size, '+')#table.size seria el ambito cuando guarde ya en pila le tengo que aumentar
                        generator.addExp(paramTemp, paramTemp, contador+1, '+')
                        generator.setStack(paramTemp, resultExpresion.valor)

                        simbolo.size=contador+1
                        nuevaTabla.actualizarTabla(simbolo)

                else:
                    return Excepcion("Semantico","tipo de datos diferente en Parametros de la llamada", self.fila,self.columna)
                
                
                contador+=1


        else: 
            return Excepcion("Semantico","Error semantico, funcion [ "+str(self.nombre)+" ] tiene un numero de PARAMETROS incorrectos! ",self.fila,self.columna)

        #como si encontro la funcion entonces tenemos q interpretar
        if generator.inFunc==True:
            #print(":/ me pise xd "+self.nombre+"  "+generator.ambito)
             #DEBO DE LLAMAR A LA FUNCION EN EL MAIN
            generator.addCommit("-------------LLAMADA A FUNCION desde la class-------------")
            #generator.temps.append(self.nombre+"_init")


            generator.newEnv(table.size)#cambio de entorno
            generator.callFuncion(self.nombre)#llamo a esta funcion

            temp = generator.addTemporal2()#genero temp por si retorna algo o no
            generator.getStack(temp, 'P')#obtengo return si tiene
            generator.retEnv(table.size)#regreso a mi ambito global (me salgo ya de la funcion)
            #generator.temps.append(self.nombre+"_finit")

            if  generator.inFunc == True:
                for temp in generator.temps_backUp:
                    b = temp
                    resultTablaS = table.getTabla(b)

                    generator.addCommit("saco bckup------------------------------"+str(resultTablaS.size))
                    paramTemp = generator.addTemporal2()
                    generator.addExp(paramTemp, 'P', resultTablaS.size, '+')#table.size seria el ambito cuando guarde ya en pila le tengo que aumentar
                    generator.getStack(b,paramTemp)

                generator.addCommit("********************************************"+self.nombre)
                            
            self.tipo = result.tipo#sacrificio para obtener la funciones expresion de una

           
            #a menos q devuelva de funcionSimple una tupla de valores q tenga si es o no return y el tipo de este
            tree.returnLbl[self.nombre] = ReturnC3D(temp,self.tipo,True)

            generator.parImpar=True
            generator.ambito2=result
            return tree.returnLbl[self.nombre]



        else:
            #print("? "+self.nombre+"  "+generator.ambito)
            pass


        value = result.compilar(tree, nuevaTabla)#ejecutar la funcion; enviamos la nueva tabla a la funcion para q no se pierdan los datos
        if isinstance(value, Excepcion):return value
        #si no es error tonces lo q podemos pasar en la llamada venga como expresion tmabien le tenemos q asignar tipo
        self.tipo = result.tipo#sacrificio para obtener la funciones expresion de una


        #print("SAS SAS SAS es el RET de funcion q me indica si hay return o no en ella, entonces hay return? :"+str(value))

        #DEBO DE LLAMAR A LA FUNCION EN EL MAIN
        generator.addCommit("-------------LLAMADA A FUNCION desde la class-------------")
        #generator.temps.append(self.nombre+"_init")


        generator.newEnv(table.size)#cambio de entorno
        generator.callFuncion(self.nombre)#llamo a esta funcion

        temp = generator.addTemporal2()#genero temp por si retorna algo o no
        generator.getStack(temp, 'P')#obtengo return si tiene
        generator.retEnv(table.size)#regreso a mi ambito global (me salgo ya de la funcion)
        #generator.temps.append(self.nombre+"_finit")





        if  generator.inFunc == True:
            for temp in generator.temps_backUp:
                b = temp
                resultTablaS = table.getTabla(b)

                generator.addCommit("saco bckup------------------------------"+str(resultTablaS.size))
                paramTemp = generator.addTemporal2()
                generator.addExp(paramTemp, 'P', resultTablaS.size, '+')#table.size seria el ambito cuando guarde ya en pila le tengo que aumentar
                generator.getStack(b,paramTemp)

            generator.addCommit("********************************************"+self.nombre)
                        
            

        if value==True:
            #a menos q devuelva de funcionSimple una tupla de valores q tenga si es o no return y el tipo de este
            if self.tipo==tipo.BOOLEANO:
                alfa = ReturnC3D(temp,self.tipo,False)
                self.checkLabels()
                alfa.trueLbl = self.LV
                alfa.falseLbl= self.LF

                tree.returnLbl[self.nombre] = alfa
                generator.addCommit("---retorna boleano---")
                generator.addIf(temp, '1', '==', self.LV)# if Tn (>|<.....) Tm {goto L1}
                generator.addGoto(self.LF)#else goto L0
                
            else:
                tree.returnLbl[self.nombre] = ReturnC3D(temp,self.tipo,True)

        elif value==None:#ya la compile 1vez
            try:
                tree.returnLbl[self.nombre].valor = temp

            except:#recursividad
                #guardo el ret de la funcion tenga o no tenga
                tree.returnLbl[self.nombre] = ReturnC3D(temp,self.tipo,True)#

            

        else:#no tiene return la funcion implicitamente, pero pueden venir lower o upper

            #print("[FUNCION SIN RETURN nombre] "+self.nombre)

            if self.nombre=='lowercase' or self.nombre=='uppercase':
                tree.returnLbl[self.nombre] = ReturnC3D(temp,tipo.CADENA,True)
                return tree.returnLbl[self.nombre]

            elif self.nombre=="length":
                tree.returnLbl[self.nombre] = ReturnC3D(temp,tipo.ENTERO,True)
                return tree.returnLbl[self.nombre]

            else:#caso para las demas funciones sin return leidas
                
                return ReturnC3D(temp,self.tipo,True)



        return tree.returnLbl[self.nombre]
        


    def checkLabels(self):#si no hay labels true o false las creo para mis expresiones relacionales
            genAux = Generator()
            generator = genAux.getInstance()
            if self.LV == '':
                  self.LV = generator.newLabel()
            if self.LF == '':
                  self.LF = generator.newLabel()