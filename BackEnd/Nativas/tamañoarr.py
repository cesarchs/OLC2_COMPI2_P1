from almacenar.generador import Generador
from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol
from almacenar.error import Error
from almacenar.tipo import Return, Tipo

#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol
#from almacenar.error import Error
#from almacenar.tipo import Tipo
import copy

class TamanoArreglo(Instruccion):
    def __init__(self, identificador, expresiones,  fila, columna):
        self.identificador = identificador
        self.expresiones = expresiones
        self.fila = fila
        self.columna = columna
        self.struct = False
        self.mutable = False

    def compilar(self, arbol, tabla):
        arraysimbolo=tabla.getSimboloEnTs(self.identificador)
        
        if arraysimbolo == None:
            return Error("SEMANTICO","ARREGLO: "+self.identificador+ "NO ESTA DECLARADO",self.fila,self.columna)
        
        self.tipo = arraysimbolo.getTipo()
        
        if not arraysimbolo.getArreglo():
            return Error("SEMANTICO", "ETIQUETA: "+self.identificador+" no es un arreglo",self.fila,self.columna)
        
        #BUSQUEDA DE POSICION EN ARREGLO
        valorasig = self.buscarCambiardimension(arbol,tabla,copy.copy(self.expresiones),arraysimbolo.getValor())
        if isinstance(valorasig,Error):return valorasig
        try:
            tamanoo=self.getTamano(valorasig)
            self.tipo = Tipo.ENTERO
        except:
            return Error("SEMANTICO","No se puebe obtener el tamaño de la expresion en Arreglo",self.fila,self.columna)
        return tamanoo
        
    def getNode(self):
        nodoModArr= NodoArbol("LENGTH()")
        nodoModArr.agregarHijoSinNodo(str(self.identificador))
        expredim = NodoArbol("EXPRESIONES DIMENSIONES")
        for expssss in self.expresiones:
            expredim.agregarHijoConNodo(expssss.getNode())
        nodoModArr.agregarHijoConNodo(expredim)
        return nodoModArr
    

    
    def buscarCambiardimension(self,arbol,tabla,expresiones,arreglo):
        valor = None
        if len(expresiones) == 0:
            return arreglo
        
        if not isinstance(arreglo,list):
            return Error("SEMANTICO", "POSICION A ACCEDER EN: "+self.identificador +" NO EXISTE", self.fila,self.columna)
        dimension=expresiones.pop(0)
        num = dimension.ejecutar(arbol,tabla)
        if isinstance(num, Error): return num
        if dimension.tipo != Tipo.ENTERO:
            return Error("SEMANTICO","EXPRESION DEBE DE SER ENTERO PARA POSICION DE ARREGLO",self.fila,self.columna)
        try:
            valor = self.buscarCambiardimension(arbol,tabla,copy.copy(expresiones),arreglo[num-1])
        except:
            return Error("SEMANTICO", "POSICION A ACCEDER EN: "+self.identificador +" NO EXISTE", self.fila,self.columna)
        if isinstance(valor, Error): return valor
        return valor
    
    
    def getTamano(self,val):
        if isinstance(val,int):
            n=1
            return n
        elif isinstance(val,float):
            n=1
            return n
        return len(val)
    
    

class TamanoArregloS(Instruccion):
    def __init__(self, identificador, fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna
        self.struct = False
        self.mutable = False

    def compilar(self, arbol, tabla):
        genAux = Generador()
        generador = genAux.getInstance()
        
        generador.agregarComentario("INICIO NATIVA LENGHT")
    
        simbolo = tabla.getSimboloEnTs(self.identificador)
        if simbolo == None:
            return Error('SEMANTICO','Identificador: '+self.identificador+' no ah sido declarado',self.fila,self.columna) 
        
        #COMO AQUI SOLO ES UNA DIMENSION LA QUE SE PIDE ENTONCES SOLO SE OBTIENE EL TAMAÑO DE LA PRIMER DIMENSION
        h=generador.agregarTemporal();generador.liberarTemporal(h)
        if not simbolo.esGlobal:
            tempPos = generador.agregarTemporal();generador.liberarTemporal(tempPos)
            generador.addExp(tempPos,'P',simbolo.posicion,'+')
            generador.getPila(h,tempPos)
        else:
            generador.getPila(h,simbolo.posicion)#hay que validar entorno si esta en funcion o global****************************************
        valor = generador.agregarTemporal()
        generador.getHeap(valor,h)
        self.tipo = Tipo.ENTERO
        return Return(valor,Tipo.ENTERO,True)
        #return valor
    
    def getTamano(self,val):
        if isinstance(val,int):
            n=1
            return n
        elif isinstance(val,float):
            n=1
            return n
        return len(val)
    
    def getNode(self):
        nodoModArr= NodoArbol("LENGTH(")
        nodoModArr.agregarHijoSinNodo(str(self.identificador)+")")
        return nodoModArr