
from typing import List
from almacenar.generador import Generador
from instrucciones.declaraciones import Declaracion
from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol
from Expresiones.aritmeticas import Aritmetica
from Expresiones.listaarreglo import Listarray
from almacenar.tipo import OpsAritmetico, Return,Tipo,Ambito
from almacenar.error import Error
from almacenar.simbolo import Simbolo
import copy
#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol
#from Expresiones.aritmeticas import Aritmetica
#from Expresiones.listaarreglo import Listarray
#from almacenar.tipo import OpsAritmetico,Tipo,Ambito
#from almacenar.error import Error
#from almacenar.simbolo import Simbolo



class DeclaracionArreglo(Instruccion):
    def __init__(self,id,exps,tipo, fila, columna):
        self.id = id
        self.Lexpresiones = exps #puede traer: primitivo, id, LARRAY y ARITMETICAS
        self.fila = fila
        self.columna = columna
        self.arreglo = True
        self.struct = False
        self.mutable = False
        self.tipo = tipo
        
    def compilar(self, arbol, tabla):
        self.Dimensiones = 1
        self.getDimension(copy.copy(self.Lexpresiones))
        lista=[]
        if self.tipo != None:
            if isinstance(self.tipo,list):
                self.tipo=self.obtenerTipo(self.tipo,lista)
                    
        #arr = [
        #            [
        #                [1,2,3,4],
        #                [10,56]
        #            ],
        #            [
        #                [6,9,2]
        #            ]
        #      ]::Vector{Vector{Vector{Int64}}};

        
        genAux = Generador()
        generador = genAux.getInstance()
        generador.agregarComentario(" Inicia declaracion Arreglo ")
        
        
        bandera=False
        tamañoLista =0
        array=self.saveArray(copy.copy(self.Lexpresiones),arbol,tabla)
        if self.tipo == Tipo.ENTERO or self.tipo == Tipo.DECIMAL or self.tipo == Tipo.BOOLEANO or self.tipo == Tipo.CARACTER:
            temp=self.obtenerExp(copy.copy(self.Lexpresiones),arbol,tabla,generador,bandera,tamañoLista)
            if isinstance(temp,Error):return temp
        elif self.tipo == Tipo.CADENA:
            temp = self.obtenerExpCadena(copy.copy(self.Lexpresiones),arbol,tabla,generador,bandera,tamañoLista)
            if isinstance(temp,Error):return temp
        
        
        
        simbolodearreglo= Simbolo(self.id,self.tipo,temp,self.fila,self.columna,tabla.size,True,True,Ambito.LOCAL,self.arreglo,self.struct,self.mutable)
        simbolodearreglo.dimensiones=self.Dimensiones
        simbolodearreglo.array = array
        if arbol.getValorAmbitoFuncion()==True:simbolodearreglo.esGlobal=False
        
        #resultadoAsig = tabla.setSimboloEnTs(simbolodearreglo)
        #
        #nuevoarreglo = tabla.getSimboloEnTs(self.id)
        #tempPos=nuevoarreglo.posicion
        #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
        nuevoarreglo = tabla.getSimboloEnTs(self.id)
        if nuevoarreglo == None:
            resultadoAsig = tabla.setSimboloEnTs(simbolodearreglo)
            if isinstance(resultadoAsig,Error): return resultadoAsig
        else:
            try:
                simbolodearreglo.posicion = nuevoarreglo.posicion#simbolodearreglo.posicion-1#posible bug, validar que no se sobre-escriba algo
                tabla.actualizarTs(simbolodearreglo)
            except:
                return Error('SEMANTICO','NO SE PUDO ACTUALIZAR SIMBOLO DE ARRAY',self.fila,self.columna)
        nuevoarreglo = tabla.getSimboloEnTs(self.id)
        tempPos=nuevoarreglo.posicion
        #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
        if not nuevoarreglo.esGlobal:
            tempPos = generador.agregarTemporal();generador.liberarTemporal(tempPos)
            generador.addExp(tempPos,'P',nuevoarreglo.posicion,"+")#validar temppos ya que puede o tiene que ser un temp
        #else:
        generador.setPila(tempPos,temp)#stack[0]=t0
        
        generador.agregarComentario(" Finaliza declaracion Arreglo ")
        
        #if isinstance(resultadoAsig,Error):
        #    tabla.actualizarTs(simbolodearreglo)
        #    return None
        return None

        

        
    
    def getNode(self):
        nodoArray = NodoArbol("DEC_ARRAY") #NOMBRE PADRE
        nodoArray.agregarHijoSinNodo(str(self.id))
        nodoexps = NodoArbol("EXPS_DIMENSIONES")
        #nodoexps.agregarHijoSinNodo(str(self.resul))
        nodoArray.agregarHijoConNodo(nodoexps)
        return nodoArray
    
    def obtenerTipo(self,lista,arr):
        for elem in lista:  
            arr.append(elem)   
            if isinstance(elem,list):
                arr.pop(0)
                self.obtenerTipo(elem,arr)
        return arr[0]
            
    
    def obtenerExp(self,lista,arbol,tabla,generador:Generador,bandera,tamañolista):
        lista_resul = []  # Lista que contendrea los resultados.
        #temp0 = generador.agregarTemporal();generador.liberarTemporal(temp0)
        tempI = generador.agregarTemporal();generador.liberarTemporal(tempI)
        
        for exp in lista:
            if isinstance(exp, list): #verifica instancia de lista
                bandera=False
                tamano=0
                lista_resul.append(self.obtenerExp(exp,arbol,tabla,generador,bandera,tamano))
                tamañolista +=1
                if tamañolista == len(lista):
                    #self.Dimensiones+=1
                    generador.addExp(tempI,'H','','') # t0 = H
                    generador.setHeap('H',len(lista)) # heap[int[H]]=3
                    generador.nextHeap()#h=h+1
                    for temp in lista_resul:
                        generador.setHeap('H',temp)
                        generador.nextHeap()
                    lista_resul=[]
            else:  # El item No es una lista.
                #bandera false
                #GUARDO POS DE H EN DONDE EMPIEZA ARREGLO:
                if not bandera:
                    generador.addExp(tempI,'H','','') # t0 = H
                    generador.setHeap('H',len(lista)) # heap[int[H]]=3
                    generador.nextHeap()#h=h+1
                    #tempsim=SimboloArr(tempI,)
                    bandera=True
                if exp.tipo == Tipo.BOOLEANO:
                    if exp.valor == True:
                        generador.setHeap('H','1')
                    else:
                        generador.setHeap('H','0')      
                else:
                    resExp = exp.compilar(arbol, tabla)
                    if isinstance(resExp, Error):return resExp  # Es error, lo retornas. (Esto no se como funciona.)
                #validacion por si no viene el tipo declarado en array:
                    if self.tipo == None: self.tipo = resExp.tipo
                    generador.setHeap('H',resExp.getValor())#heap[h]=1
                generador.nextHeap()#h=h+1
                
        return tempI  # Retornas la lista actual con todas sus expresiones.
    
    def obtenerExpCadena(self,lista,arbol,tabla,generador:Generador,bandera,tamañolista):
        lista_resul = []  # Lista que contendrea los resultados.
        #temp0 = generador.agregarTemporal();generador.liberarTemporal(temp0)
        tempI = generador.agregarTemporal();generador.liberarTemporal(tempI)
        tamano=0
        for exp in lista:
            if isinstance(exp, list): #verifica instancia de lista
                #bandera=False
                tamano=0
                lista_resul.append(self.obtenerExpCadena(exp,arbol,tabla,generador,bandera,tamano))
                tamañolista +=1
                if tamañolista == len(lista):
                    #self.Dimensiones+=1
                    generador.addExp(tempI,'H','','') # t0 = H
                    generador.setHeap('H',len(lista)) # heap[int[H]]=3
                    generador.nextHeap()#h=h+1
                    for temp in lista_resul:
                        generador.setHeap('H',temp)
                        generador.nextHeap()
                    lista_resul=[]
            else:  # El item No es una lista.
                #bandera false
                #GUARDO POS DE H EN DONDE EMPIEZA ARREGLO:
                resExp = exp.compilar(arbol, tabla)
                if isinstance(resExp, Error):return resExp  # Es error, lo retornas. (Esto no se como funciona.)
                #validacion por si no viene el tipo declarado en array:
                if self.tipo == None: self.tipo = resExp.tipo
                generador.setHeap('H',resExp.getValor())#heap[h]=1
                generador.nextHeap()#h=h+1
                tamañolista +=1
                lista_resul.append(resExp.getValor())
                if tamañolista == len(lista):
                    tamano=0
                    generador.addExp(tempI,'H','','') # t0 = H
                    generador.setHeap('H',len(lista)) # heap[int[H]]=3
                    generador.nextHeap()#h=h+1
                    for temp in lista_resul:
                        generador.setHeap('H',temp)
                        generador.nextHeap()
                    lista_resul=[]
                
        return tempI  # Retornas la lista actual con todas sus expresiones.
    
    def saveArray(self,lista,arbol,tabla):
        lista_resull = []  # Lista que contendrea los resultados.
        for exp in lista:
            if isinstance(exp, list):  # Encontro una lista entre los itemas de la lista.
                lista_resull.append(self.saveArray(exp,arbol,tabla))  # lista_resul.append(otra lista), [5+8, False, True] -> [5+8, False, True, [[9*8, b]]]
                #self.Dimensiones+=1
            else:  # El item No es una lista.
                if exp.tipo == Tipo.BOOLEANO:
                    lista_resull.append(exp.valor)
                    if self.tipo == None: self.tipo = exp.tipo
                else:
                    resExp = exp.compilar(arbol, tabla)  #verificar si se va a usar lo que se guarda aca, sino no hay necesidade compilar
                    if self.tipo == None: self.tipo = resExp.tipo
                    if isinstance(resExp, Error):  # Es error, lo retornas. (Esto no se como funciona.)
                        return resExp
                    else:  # exp, aqui puede ser Id, aritmetica, primitiva bool, etc. Ej: [] -> [5+8] -> [5+8, False] -> [5+8, False, True]; [] -> [9*8, b]
                        lista_resull.append(resExp) # lista_resul.apend(5+8), lista_resul.apend(True), etc.
        return lista_resull  # Retornas la lista actual con todas sus expresiones.
    
    def getDimension(self,lista:list):
        if isinstance(lista[0],list):
            self.Dimensiones+=1
            self.getDimension(copy.copy(lista.pop(0)))
        else:
            return
        

class RetornoDeExpresions():
    def __init__(self,tipo,lexp):
        self.tipo=tipo
        self.lexp=lexp
        
    def getTipo(self):
        return self.tipo
    def getlexp(self):
        return self.lexp