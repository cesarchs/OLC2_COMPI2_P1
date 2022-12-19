from almacenar.generador import Generador
from padres.expresion import Expresion
from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol
from almacenar.error import Error
from almacenar.tipo import Return, Tipo

#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol
#from almacenar.error import Error
#from almacenar.tipo import Tipo
import copy
class CambiarArreglo(Instruccion):
    def __init__(self, identificador, expresiones, valor, fila, columna):
        self.identificador = identificador
        self.expresiones = expresiones
        self.valor = valor
        self.fila = fila
        self.columna = columna
    
    def compilar(self, arbol, tabla):
        self.dimensiones = len(self.expresiones)
        arraysimbolo=tabla.getSimboloEnTs(self.identificador)
        genAux = Generador()
        generador = genAux.getInstance()
        
        generador.agregarComentario(" INICIA MODIFICACION DE ARREGLO ")
        
        if arraysimbolo == None:
            return Error("SEMANTICO","ARREGLO: "+self.identificador+ "NO ESTA DECLARADO",self.fila,self.columna)
        
        self.tipo = arraysimbolo.getTipo()
        
        if not arraysimbolo.getArreglo():
            return Error("SEMANTICO", "ETIQUETA: "+self.identificador+" no es un arreglo",self.fila,self.columna)
        
        resExp = self.valor.compilar(arbol,tabla)
        if isinstance(resExp,Error): return resExp
        
        #BUSQUEDA DE POSICION EN ARREGLO
        #obtengo la posicion que se guardo en la pila para acceder a HEAP
        h = generador.agregarTemporal();generador.liberarTemporal(h)
        if not arraysimbolo.esGlobal:
            tempPos = generador.agregarTemporal();generador.liberarTemporal(tempPos)
            generador.addExp(tempPos,'P',arraysimbolo.posicion,'+')
            generador.getPila(h,tempPos)
        else:
            generador.getPila(h,arraysimbolo.posicion)
        #temp = []
        salir=generador.agregarLabel()
        
        
        self.obtenerValorDimension(arbol,tabla,copy.copy(self.expresiones),h,arraysimbolo,salir,resExp,generador)
        generador.colocarLabel(salir)
        
        return None
        
    
    def obtenerValorDimension(self,arbol,tabla,expresiones,h,arreglo,salir,resExp,generador:Generador):
        dimension=expresiones.pop(0)            #obtengo primer dimensión
        valor=generador.agregarTemporal();generador.liberarTemporal(valor)
        tamano=generador.agregarTemporal();generador.liberarTemporal(tamano)
        num = dimension.compilar(arbol,tabla)   #obtengo valor de dimension
        ##->->->->->->->->->->
        if num.tipo != Tipo.ENTERO:return Error("SEMANTICO","EXPRESION A ACCESO DE ARREGLO DEBER SER UN NUMERO",self.fila,self.columna)
        ##->->->->->->->->->->
        #temp.append(valor)
        if arreglo.tipo == Tipo.ENTERO or arreglo.tipo == Tipo.CADENA or arreglo.tipo == Tipo.CARACTER:
            #aqui se agregar el codigo para el la comprobacion de si el  denominador es 0     
            generador.getHeap(tamano,h)
            
            generador.agregarComentario("COMPROBACION QUE INDEX EN ARRAY EXISTA")
            ltrue=generador.agregarLabel()
            lfalse=generador.agregarLabel()
            generador.agregarIf(num.getValor(),'1','<',ltrue)
            generador.agregarIf(num.getValor(),tamano,'>',ltrue)
            generador.agregarGoto(lfalse)
            generador.colocarLabel(ltrue)
            generador.printBoundError()
            generador.agregarGoto(salir)
            
            generador.colocarLabel(lfalse)
            if len(expresiones)>0:
                #temp.pop(0)
                generador.addExp(h,h,num.getValor(),'+') 
                generador.getHeap(valor,h)
                self.obtenerValorDimension(arbol,tabla,copy.copy(expresiones),valor,arreglo,salir,resExp,generador)
            if len(expresiones)==0:
                generador.addExp(h,h,num.getValor(),'+')        
                generador.setHeap(h,resExp.getValor())
                ##->->->->->->->->->->->->->->
            #generador.colocarLabel(salir)
                ##->->->->->->->->->->->->->->
            return 
        
        
    def getNode(self):
        nodoModArr= NodoArbol("MOD_ARRAY")
        nodoModArr.agregarHijoSinNodo(str(self.identificador))
        expsss = NodoArbol("EXPRESION DIMENSION")
        for expron in self.expresiones:
            expsss.agregarHijoConNodo(expron.getNode())
        nodoModArr.agregarHijoConNodo(expsss)
        nodoModArr.agregarHijoConNodo(self.valor.getNode())
        return nodoModArr

    
    def buscarCambiardimension(self,arbol,tabla,expresiones,arreglo,valor):
        if len(expresiones) == 0:
            if isinstance(arreglo,list):
                return Error("SEMANTICO", "MODIFICACION A ARREGLO INCOMPLETO", self.fila, self.columna)
            return valor
        
        if not isinstance(arreglo,list):
            return Error("SEMANTICO", "POSICION A ACCEDER NO EXISTE", self.fila,self.columna)
        dimension=expresiones.pop(0)
        num = dimension.ejecutar(arbol,tabla)
        if isinstance(num, Error): return num
        if num <=0: return Error("SEMANTICO", "POSICION A ACCEDER NO EXISTE", self.fila,self.columna)
        if dimension.tipo != Tipo.ENTERO:
            return Error("SEMANTICO","EXPRESION DEBE DE SER ENTERO PARA POSICION DE ARREGLO",self.fila,self.columna)
        try:
            value = self.buscarCambiardimension(arbol,tabla,copy.copy(expresiones),arreglo[num-1],valor)
        except:
            return Error("SEMANTICO", "POSICION A ACCEDER NO EXISTE", self.fila,self.columna)
        if isinstance(value, Error): return value
        if value != None:
            arreglo[num-1]= value
        return None