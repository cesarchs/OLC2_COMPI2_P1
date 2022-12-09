from Expresiones.primitivos import Primitivos
from typing import List
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Return2 import ReturnC3D
from TS.Tipo import tipo
from TS.Simbolo import Simbolo

class LLamarArray(instruccion):# es como un nodo y se arma el arbol con estos nodos                            PARA ARRAYS TIPO ID[][]=NEW[N][N]
#los commits son de declaracion.py
                    
    def __init__(self,id,dimension, fila, columna):
        self.id=id
        self.dimension=dimension
   
        self.fila=fila
        self.columna=columna


        self.cuerpoSiesArray=None
        self.tipo=None
        #self.mafuba=None

        self.LV =""
        self.LF =""


    def interpretar(self, tree, table):

        #print("-------------------CAMBIANDO VALOR A ARRAYS--------------------")
        #print(str(self.id))

        array2 = table.getTabla(self.id)
        array = array2.valor
        if isinstance(array, Excepcion): return array#lo retornamos

        #print(str(array))

        if isinstance(array, List):
            self.cuerpoSiesArray=array
            #self.arreglo=True


            posicionActual=None
            for item in self.dimension:
                if posicionActual!=None:
                    #print(":::::N dimension:::::")
                    aguas = item.interpretar(tree,table)
                    if isinstance(aguas, Excepcion): return aguas#lo retornamos  
                    #print(str(aguas))

                    #print("posicion en array n dimension")
                    vara = posicionActual.interpretar(tree,table)#error
                    if isinstance(vara, Excepcion): return vara#lo retornamos  

                    try:
                        posicionActual = vara[aguas-1]
                    except :
                        #print("no es array el valor en esta posicion"+str(aguas-1))
                        return Excepcion("Semantico","posicion en array no es otro array, no pudo ser accedido para imprimirse", self.fila,self.columna)

                    #print(str(posicionActual))

                else:

                    #print(":::::primera dimension:::::")
                    aguas = item.interpretar(tree,table)
                    if isinstance(aguas, Excepcion): return aguas#lo retornamos  
                    #print(str(aguas))

                    #print("posicionActual en array 1era dimension, cambiamos")
                    #print("~~ array: "+str(array))
                    posicionActual=array[aguas-1]
                    #print(str(posicionActual))
                    #print("_________________________________________________")

                    #if isinstance(posicionActual, LLamarArray):
                     #   mierd = LLamarArray.interpretar(tree,LLamarArray.table)

                      #  return mierd


                    

            # saliendo del for por aqui modifico el valor porq posicionActual esta posicionado en el lugar correcto
            #print("----ya accedi a la posicion del array ahora toca modificar----")
            #print("soy valor saliendo de for:"+str(posicionActual))                        #YA TENGO ARRA[][] Q RETORNA EL VALOR EN ESA POSICION
            #print("~~~~IZANAMI~~~~")
            af = posicionActual

            if not (isinstance(af,int) or isinstance(af,str) or isinstance(af,bool) or isinstance(af,float)):
                af = posicionActual.interpretar(tree,table)
                self.tipo = posicionActual.tipo


            
            #print("~~~~ FIN IZANAMI~~~~")
            if isinstance(af, Excepcion): return af#lo retornamos    
            #print("valor de la posicion a modificar, este se ira :'(   :"+str(af))


            if  isinstance(af,int):
                self.tipo =tipo.ENTERO

            elif isinstance(af,str):
                self.tipo =tipo.CADENA

            elif isinstance(af,bool):
                self.tipo =tipo.BOOLEANO

            elif isinstance(af,float):
                self.tipo =tipo.DECIMAL



            #print("maaaaaaaayyyyyyyy")
            #print(str(self.tipo))


    


                    
    
            may = Primitivos(self.tipo,af,self.fila,self.columna)
            #print("**********************pua may")
            #print(self.id)
            #print(str(may.valor))
            #print(str(may.tipo))
            #print("**********************pua may")


            #self.mafuba = may
            return may

        return Excepcion("Semantico","Tipo de dato no es array para ser impreso como un array", self.fila,self.columna)



        
    

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

        if isinstance(array, ReturnC3D):

            #print("esto es dimension:"+str(self.dimension))

            if len(self.dimension)==1:
                #print("* ACCESO DE 1 DIMENSION")
                for item in self.dimension:
                    valor = item.compilar(tree,table)
                    value = ''#item.interpretar(tree,table)
                    if isinstance(valor, Excepcion): return valor#lo retornamos
                    #print("** indice de array:"+str(valor.valor))
                #print("*** posiciones de acceso del array validas (1-"+str(len(array.Array))+") | inferior del array:"+str(array.Array[0].valor)+" tipo de inf:"+str(array.Array[0].tipo)+" | superior del array:"+str(array.Array[-1].valor)+" tipo de sup:"+str(array.Array[-1].tipo))
                
                self.ErrorArray(valor.valor,str(len(array.Array)))
                
                try:
                    genAux = Generator()
                    generator = genAux.getInstance()#el q me hara el paro en todo
                    if array.Array[int(valor.valor)-1].tipo == tipo.BOOLEANO:
                        #si ya es bool entonces
                        if self.LV == '':
                            self.LV = generator.newLabel()
                        if self.LF == '':
                            self.LF = generator.newLabel()

                        t1 = generator.addTemporal()
                        generator.getHeap(t1,array.Array[int(valor.valor)-1].posicion)
                        generator.addIf(t1, '1', '==', self.LV)
                        generator.addGoto(self.LF)

                        generator.addCommit("Fin compilacion acceso")
                        generator.addSaltoLinea()

                        ret = ReturnC3D(None, tipo.BOOLEANO, False)
                        ret.trueLbl = self.LV
                        ret.falseLbl = self.LF
                        return ret

                    
                    if array.Array[int(valor.valor)-1].posicion!=-1:
                        t1 = generator.addTemporal()
                        generator.addCommit("accediendo a array 1 dimension")
                        generator.getHeap(t1,array.Array[int(valor.valor)-1].posicion)
                        ret = ReturnC3D(t1, array.Array[int(valor.valor)-1].tipo, True)
                        return ret
                    return array.Array[int(valor.valor)-1]  #AQUI HAY UN C3D Q TIENE VALOR,TIPO,ESTEMP y Array[]
                except :
                    #self.ErrorArray(valor.valor)
                    try:
                        return array.Array[int(valor.index)-1]  #AQUI HAY UN C3D Q TIENE VALOR,TIPO,ESTEMP y Array[]
                    except:
                        return Excepcion("Semantico","Error semantico, index in array out of range!"+str(value),self.fila,self.columna)

                

            elif len(self.dimension)==2:
                #print("ACCESO DE 2 DIMENSIONES")
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
                self.ErrorArray(listaIndices[1],str(len(array.Array[int(listaIndices[0])-1].Array)))

                try:
                    genAux = Generator()
                    generator = genAux.getInstance()#el q me hara el paro en todo
                    if posicion.Array[int(listaIndices[1])-1].tipo == tipo.BOOLEANO:
                        #si ya es bool entonces
                        if self.LV == '':
                            self.LV = generator.newLabel()
                        if self.LF == '':
                            self.LF = generator.newLabel()
                        t1 = generator.addTemporal()
                        generator.getHeap(t1,posicion.Array[int(listaIndices[1])-1].posicion)                       
                        generator.addIf(t1, '1', '==', self.LV)
                        generator.addGoto(self.LF)
                        generator.addCommit("Fin compilacion acceso")
                        generator.addSaltoLinea()

                        ret = ReturnC3D(None, tipo.BOOLEANO, False)
                        ret.trueLbl = self.LV
                        ret.falseLbl = self.LF
                        return ret

                    t1 = generator.addTemporal()
                    generator.addCommit("accediendo a array 2 dimension")
                    generator.getHeap(t1,posicion.Array[int(listaIndices[1])-1].posicion)
                    ret = ReturnC3D(t1, posicion.Array[int(listaIndices[1])-1].tipo, True)
                    return ret
                    #return posicion.Array[int(listaIndices[1])-1]#AQUI HAY UN C3D Q TIENE VALOR,TIPO,ESTEMP y Array[]
                except :
                    #self.ErrorArray(valor.valor)
                    return Excepcion("Semantico","Error semantico, index in array out of range!",self.fila,self.columna)



            elif len(self.dimension)>=3:
                #print("ACCESO DE N DIMENSIONES\naun en proceso!")
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
                #posicion=array.Array[int(listaIndices[0])-1]#obtengo la 1er dimension de las n
                condador=0

                indice2=0

                try:
                    genAux = Generator()
                    generator = genAux.getInstance()#el q me hara el paro en todo

                    for indices in listaIndices:
                        #print("**** "+str(indices))
                        if condador==0:
                            condador+=1
                        else:
                            indice2=indices
                            generator.addCommit("jsjsjjss")
                            self.ErrorArray(indice2,str(len(array.Array)))
                            posicion = posicion.Array[int(indices)-1]
                        #return posicion.Array[int(listaIndices[1])-1]#AQUI HAY UN C3D Q TIENE VALOR,TIPO,ESTEMP y Array[]

                     


                    if posicion.tipo == tipo.BOOLEANO:
                        #si ya es bool entonces                        
                        if self.LV == '':
                            self.LV = generator.newLabel()
                        if self.LF == '':
                            self.LF = generator.newLabel()
                        t1 = generator.addTemporal()
                        generator.getHeap(t1,posicion.posicion)                   
                        generator.addIf(t1, '1', '==', self.LV)
                        generator.addGoto(self.LF)
                        generator.addCommit("Fin compilacion acceso")
                        generator.addSaltoLinea()

                        ret = ReturnC3D(None, tipo.BOOLEANO, False)
                        ret.trueLbl = self.LV
                        ret.falseLbl = self.LF
                        return ret

                    t1 = generator.addTemporal()
                    generator.addCommit("accediendo a array 2 dimension")
                    generator.getHeap(t1,posicion.posicion)
                    ret = ReturnC3D(t1, posicion.tipo, True)
                    return ret

                    #return posicion
                
                except :
                    self.ErrorArray(indice2,str(len(array.Array)))   
                    return Excepcion("Semantico","Error semantico, index in array out of range!",self.fila,self.columna)

                
                

            '''for item in self.dimension:
                
                valor = item.compilar(tree,table)
                if isinstance(valor, Excepcion): return valor#lo retornamos

                print(str(valor.valor))

            print("*** posiciones de acceso del array validas (1-"+str(len(array.Array))+") | inferior del array:"+str(array.Array[0].valor)+" tipo de inf:"+str(array.Array[0].tipo)+" | superior del array:"+str(array.Array[-1].valor)+" tipo de sup:"+str(array.Array[-1].tipo))
            

            return array.Array[int(valor.valor)-1] #array.Array[self.dimension]'''
            return None

        return Excepcion("Semantico","Tipo de dato no es array, no puede ser tratado como un array", self.fila,self.columna)

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

            