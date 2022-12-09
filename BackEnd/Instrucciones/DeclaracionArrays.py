from Expresiones import identificador
from Expresiones.identificador import Identificador
from Instrucciones.LLamarArray import LLamarArray
from Expresiones.primitivos import Primitivos
from typing import Collection, List
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Return2 import ReturnC3D
from TS.Tipo import tipo
from TS.Simbolo import Simbolo
import collections



class DeclaracionArray(instruccion):# es como un nodo y se arma el arbol con estos nodos                            PARA ARRAYS TIPO ID[][]=NEW[N][N]
#los commits son de declaracion.py
                    
    def __init__(self,id,dimension,expresion, fila, columna):
        self.id=id
        self.dimension=dimension
        self.expresion=expresion
        self.fila=fila
        self.columna=columna


        self.cuerpoSiesArray=None
        self.isArray=1
        self.tipo=None


    def interpretar(self, tree, table):

        #print("-------------------CAMBIANDO VALOR A ARRAYS2 declaracion--------------------")
        #print(str(self.id))


        #array = self.id.interpretar(tree,table)
        array2 = table.getTabla(self.id)
        array = array2.valor
        if isinstance(array, Excepcion): return array#lo retornamos

        #print(str(array))

        if isinstance(array, List):
            self.cuerpoSiesArray=array
            #self.arreglo=True


            posicionActual=None
            iterando=0
            puntero=None
            for item in self.dimension:

                if iterando >=2:
                    return Excepcion("Semantico","array accedido como de +2 dimensiones", self.fila,self.columna)

                
                if posicionActual!=None:
                    #print(":::::N dimension:::::")
                    aguas = item.interpretar(tree,table)
                    if isinstance(aguas, Excepcion): return aguas#lo retornamos  
                    #print("indice: "+str(aguas))

                    #print("posicion en array n dimension")

                    
                    wakamole = posicionActual[puntero]
                    #print("tengo q ser otro array o valor")
                    #print(str(wakamole))
                    vara = wakamole.interpretar(tree,table)#error
                    if isinstance(vara, Excepcion): return vara#lo retornamos  

                    if iterando ==len(self.dimension)-1:

                        try:
                        #posicionActual = vara[aguas-1]

                                nxt=self.expresion
                        
                                #interpreto el valor a asignar
                                if isinstance(self.expresion,LLamarArray):
                                    nxt = self.expresion.interpretar(tree,table)
                                    if isinstance(nxt, Excepcion): return nxt#lo retornamos el de un id no lo tengo FFF
                        
                                if isinstance(self.expresion,Identificador):
                                    nxt = self.expresion.interpretar(tree,table)
                                    if isinstance(nxt, Excepcion): return nxt#lo retornamos el de un id no lo tengo FFF



                                #interpreto el valor a asignar
                                
                                vara[aguas-1]=nxt

                                
                                #print("merderrrrrrrrrrrrrr")
                                #print(str(wakamole.valor))
                                if isinstance(wakamole,Primitivos):
                                    pass

                                else:
                                    simbolo = Simbolo(wakamole.identificador,wakamole.tipo,True, self.fila,self.columna,vara)#buscar si esta en la tabla y se modifica ahi, sino entra en if isinstance(result,Excepcion): 
                                    table.actualizarTabla(simbolo)#lo modifico o no lo hizo 

                                #array[puntero]=wakamole

                                #print("dude2 wtf")
                                #print(str(array[puntero]))

                                #print("puuuuuuuuuuaa")
                                #print(str(vara))
                                #print(str(posicionActual))

                                anterior = posicionActual#array anterior
                                posicionActual=vara#me muevo de array
                                puntero = aguas-1#actualizo  a la nueva direccion [][]


                                #print("puuuuuuuuuuaaa222")
                                #print(str(vara))
                                #print(str(posicionActual))

                                if collections.Counter(anterior)==collections.Counter(posicionActual):#poner aqui enfasis si lo hago la hice
                                    return Excepcion("Semantico","array accedido como de +2 dimensiones", self.fila,self.columna)


                        

                    
                        except :
                            #print("no es array el valor en esta posicion"+str(aguas-1))
                            return Excepcion("Semantico","posicion en array no es otro array, no pudo ser accedido como multidimensional porq es un valor no un array como tal", self.fila,self.columna)

                    #else: #este seria para mas de 2 dimensiones y continue  #print(str(posicionActual))

                else:

                    #print(":::::primera dimension declaracion:::::")
                    aguas = item.interpretar(tree,table)
                    if isinstance(aguas, Excepcion): return aguas#lo retornamos  
                    #print(str(aguas))

                    #print("posicion en array 1era dimension declaracion")
                    posicionActual=array#[aguas-1]
                    #print(str(posicionActual))

                    
                    if iterando ==len(self.dimension)-1:

                        nxt=self.expresion
                        
                        #interpreto el valor a asignar
                        if isinstance(self.expresion,LLamarArray):
                            nxt = self.expresion.interpretar(tree,table)
                            if isinstance(nxt, Excepcion): return nxt#lo retornamos
                            array[aguas - 1] = nxt
                            #print("MODIFIQUE ARRAY 1 DIMENSION!!!!!!!")
                            #print(str(array[aguas - 1]))
                            return None



                        if isinstance(self.expresion,Identificador):
                            nxt = self.expresion.interpretar(tree,table)
                            if isinstance(nxt, Excepcion): return nxt#lo retornamos
                            array[aguas - 1] = nxt
                            #print("MODIFIQUE ARRAY 1 DIMENSION!!!!!!!")
                            #print(str(array[aguas - 1]))
                            return None



                        array[aguas-1]=nxt
                        #print("MODIFIQUE ARRAY 1 DIMENSION!!!!!!!")
                        #print(str(array[aguas-1]))

                        return None

                    else:
                        puntero = aguas-1


                iterando+=1




            return None

        return Excepcion("Semantico","Tipo de dato no es array para ser modificado como un array", self.fila,self.columna)

        

    def getNodo(self):

        nodo = NodoAST("ACCESO A ARREGLO")
        #nodo.agregarHijo(str(self.tipo))#PUEDE COMO NO PUEDE VENIR JAVIER
        #nodo.agregarHijo(str(self.identificador))
       
        '''exp = NodoAST("EXPRESIONES")
        for expresion in self.expresion:
            exp.agregarHijoNodo(expresion.getNodo())
        nodo.agregarHijoNodo(exp)'''

        return nodo


    def crearDimension(self,tree,table,expresiones):
        arr =[]
        if len(expresiones)==0:
            return None

        dimension = expresiones.pop(0)
        num = dimension.interpretar(tree,table)
        if isinstance(num, Excepcion): return num

        contador=0
        while contador<num:
            arr.append(self.crearDimension(tree,table,expresiones))
            contador+=1

        return arr#1hr 6min
        #1hr 15 min dice q de lugar de None va simbolo con el tipo. para arrays multi-tipo
        #no olvidar las pasadas para esto aunq en julia creo q ya esta sin hacer nada





    def compilar(self, tree, table):
    
        array2 = table.getTabla(self.id)
        array = array2.valor
        if isinstance(array, Excepcion): return array#lo retornamos

        dato = self.expresion.compilar(tree,table)
        if isinstance(dato, Excepcion): return dato#lo retornamos

        

        if isinstance(array, ReturnC3D) and isinstance(dato, ReturnC3D):
            genAux = Generator()
            generator = genAux.getInstance()#el q me hara el paro en todo

            if dato.tipo==tipo.BOOLEANO:
                genAux = Generator()
                generator = genAux.getInstance()#el q me hara el paro en todo
                generator.addCommit("---------asignando bool a array javier-----------")
                tempLbl = generator.newLabel()

                #####################################################
                heap = generator.addTemporal()
                
                #####################################################

                generator.inputLabel(dato.trueLbl)
                generator.setHeap('H', 1)  # heap[H] = elemento del array
                generator.addCommit("creo un apuntador a bool en HEAP")
                generator.addExp(heap,'H','','')
                dato.posicion = heap
                generator.nextHeap()                # H = H + 1;
                
                generator.addGoto(tempLbl)

                generator.inputLabel(dato.falseLbl)
                generator.setHeap('H', 0)  # heap[H] = elemento del array
                generator.addCommit("creo un apuntador a bool en HEAP")
                generator.addExp(heap,'H','','')
                dato.posicion = heap
                generator.nextHeap()                # H = H + 1;

                generator.inputLabel(tempLbl)



            if len(self.dimension)==1:
                #print("* ACCESO DE 1 DIMENSION")
                for item in self.dimension:
                    valor = item.compilar(tree,table)
                    if isinstance(valor, Excepcion): return valor#lo retornamos
                    #print("** indice de array:"+str(valor.valor))
                #print("*** posiciones de acceso del array validas (1-"+str(len(array.Array))+") | inferior del array:"+str(array.Array[0].valor)+" tipo de inf:"+str(array.Array[0].tipo)+" | superior del array:"+str(array.Array[-1].valor)+" tipo de sup:"+str(array.Array[-1].tipo))
                #return #AQUI HAY UN C3D Q TIENE VALOR,TIPO,ESTEMP y Array[]
                
                self.ErrorArray(valor.valor,str(len(array.Array)))
                try:
                    if dato.posicion==-1:#ent,deci,cad,char
                        dato.posicion = array.Array[int(valor.valor)-1].posicion
                    else:
                        print("+=+=+=+=     +=+=+=+=    +=+=+=+="+str(dato.valor))
                        #dato.posicion = array.Array[int(valor.valor)-1].posicion
                    if dato.valor==True or dato.valor==False:
                        if dato.valor==True:
                            dato.valor=1;
                        else:
                            dato.valor=0;
                    generator.addCommit("ASIGNAMOS A HEAP DEL ARRAY 1 dim VALOR")
                    generator.setHeap(array.Array[int(valor.valor)-1].posicion,dato.valor)
                    array.Array[int(valor.valor)-1] = dato
                    return None
                except :
                    #self.ErrorArray(valor.valor)
                    return Excepcion("Semantico","Error semantico, index in array out of range!",self.fila,self.columna)



            elif len(self.dimension)==2:
                #print("ACCESO DE 2 DIMENSIONES")
                listaIndices=[]
                for item in self.dimension:
                    valor = item.compilar(tree,table)
                    if isinstance(valor, Excepcion): return valor#lo retornamos
                    #print("** indice de array:"+str(valor.valor))
                    listaIndices.append(valor.valor)
                #print("*** posiciones de acceso del array validas (1-"+str(len(array.Array))+") | inferior del array:"+str(array.Array[0].valor)+" tipo de inf:"+str(array.Array[0].tipo)+" | superior del array:"+str(array.Array[-1].valor)+" tipo de sup:"+str(array.Array[-1].tipo))
                
                #posicion=array.Array[int(listaIndices[0])-1]
                try:
                    posicion=array.Array[int(listaIndices[0])-1]
                except:
                    self.ErrorArray(listaIndices[0],str(len(array.Array)))
                    return Excepcion("Semantico","Error semantico, index in array out of range!",self.fila,self.columna)

                self.ErrorArray(listaIndices[0],str(len(array.Array)))
                self.ErrorArray(listaIndices[1],str(len(array.Array[int(listaIndices[0])-1].Array)))


                #self.ErrorArray(listaIndices[1],str(len(array.Array)))
                try:
                    if dato.posicion==-1:
                        #print("")
                        dato.posicion=posicion.Array[int(listaIndices[1])-1].posicion
                    else:
                        print("+=+=+=+=     +=+=+=+=    +=+=+=+="+str(dato.valor))
                        #dato.posicion=posicion.Array[int(listaIndices[1])-1].posicion
                    if dato.valor==True or dato.valor==False:
                        if dato.valor==True:
                            dato.valor=1;
                        else:
                            dato.valor=0;
                    generator.addCommit("ASIGNAMOS A HEAP DEL ARRAY 2 dim VALOR")
                    generator.setHeap(posicion.Array[int(listaIndices[1])-1].posicion,dato.valor)
                    posicion.Array[int(listaIndices[1])-1]= dato
                    return None
                except :
                    #self.ErrorArray(valor.valor)
                    return Excepcion("Semantico","Error semantico, index in array out of range!",self.fila,self.columna)

                



            elif len(self.dimension)>=3:
                #print("ACCESO DE N DIMENSIONES\naun en proceso!")

                #GRADO 4 O MAYOR
                listaIndices=[]
                for item in self.dimension:
                    valor = item.compilar(tree,table)
                    if isinstance(valor, Excepcion): return valor#lo retornamos
                    #print("** indice de array:"+str(valor.valor))
                    listaIndices.append(valor.valor)
                #print("*** posiciones de acceso del array validas (1-"+str(len(array.Array))+") | inferior del array:"+str(array.Array[0].valor)+" tipo de inf:"+str(array.Array[0].tipo)+" | superior del array:"+str(array.Array[-1].valor)+" tipo de sup:"+str(array.Array[-1].tipo))
                

                try:
                    posicion=array.Array[int(listaIndices[0])-1]
                except:
                    self.ErrorArray(listaIndices[0],str(len(array.Array)))
                    return Excepcion("Semantico","Error semantico, index in array out of range!",self.fila,self.columna)

                self.ErrorArray(listaIndices[0],str(len(array.Array)))
                
                condador=0
                ind=0
                indice2=0

                try:
                    for indices in listaIndices:
                        #print("**** "+str(indices))
                        if condador==0:
                            posicion=array.Array[int(indices)-1]#obtengo la 1er dimension de las n
                            condador+=1
                        else:
                            indice2=indices
                            if ind == len(listaIndices)-1:
                                self.ErrorArray(indice2,str(len(array.Array)))

                                if dato.posicion==-1:
                                    #print("")
                                    dato.posicion =  posicion.Array[int(indices)-1].posicion
                                else:
                                    print("+=+=+=+=     +=+=+=+=    +=+=+=+="+str(dato.valor))
                                    #dato.posicion =  posicion.Array[int(indices)-1].posicion

                                if dato.valor==True or dato.valor==False:
                                    if dato.valor==True:
                                        dato.valor=1;
                                    else:
                                        dato.valor=0;

                                generator.addCommit("ASIGNAMOS A HEAP DEL ARRAY 3 dim VALOR")
                                generator.setHeap(posicion.Array[int(indices)-1].posicion,dato.valor)
                                posicion.Array[int(indices)-1] = dato
                                return None
                            
                            else:
                                posicion = posicion.Array[int(indices)-1]

                        ind+=1
                except :
                    #self.ErrorArray(indice2)   
                    return Excepcion("Semantico","Error semantico, index in array out of range!",self.fila,self.columna)

                    

            
            return None

        return Excepcion("Semantico","Tipo de dato no es array para ser impreso como un array", self.fila,self.columna)


    def ErrorArray(self,indice,max):
        genAux = Generator()
        generator = genAux.getInstance()#obtengo mi static generator
        generator.addCommit(" Ha ganarse el sueldo :P")
        tmp = generator.addTemporal()
        generator.addCommit("--indice al que se desa acceder--")
        generator.addExp(tmp,str(indice),'','')
        l1 = generator.newLabel()
        l2 = generator.newLabel()
        l3 = generator.newLabel()
        generator.addIf(tmp,'1','<',l1)
        generator.addIf(tmp,max,'>',l1)
        generator.addGoto(l2)
        generator.inputLabel(l1)
        generator.addPrint('c',66,"//B")
        generator.addPrint('c',111,"//o")
        generator.addPrint('c',117,"//u")
        generator.addPrint('c',110,"//n")
        generator.addPrint('c',100,"//d")
        generator.addPrint('c',115,"//s")
        generator.addPrint('c',69,"//E")
        generator.addPrint('c',114,"//r")
        generator.addPrint('c',114,"//r")
        generator.addPrint('c',111,"//o")
        generator.addPrint('c',114,"//r")
        generator.addPrint('c',10,"//salto de linea")
        generator.addCommit("NO CONTINUA CON LA INSTRUCCION")
        generator.addGoto(l3)#cuando esta malo

        generator.inputLabel(l2)#cuando esta bueno
        generator.addCommit("CONTINUA CON LA INSTRUCCION")
        generator.inputLabel(l3)