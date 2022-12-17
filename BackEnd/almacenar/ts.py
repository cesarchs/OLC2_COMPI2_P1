from almacenar.error import Error
from almacenar.funcsimbolo import SimboloFun
from almacenar.simbolo import Simbolo
from almacenar.tipo import Ambito, Tipo

#from almacenar.error import Error
#from almacenar.tipo import Ambito

class TablaSimbolos:
    def __init__(self,prev):
        self.prev = prev
        #nuevo
        self.size = 0
        self.breakLbl = ''
        self.continueLbl = ''
        self.returnLbl = ''
        #->->->->->-->->->->->
        self.gotoReturn = False
        #->->->->->-->->->->->
        if prev != None:
            self.size = self.prev.size
            self.breakLbl = self.prev.breakLbl
            self.continueLbl = self.prev.continueLbl
            self.returnLbl = self.prev.returnLbl
        
        self.tsimbolos={} # ->->->->->->->->-> esta lista es posible que se elimene ->->->->->->->->->->->->->->->->
        self.tsfunciones={} # TS de funciones -->->->->->->->
        self.anterior = None
        self.listadoGlobales = []
        self.listadoLocales = []
        self.prop  = 'main' #->->->->->->->->->->->->->->->->->->->->
        self.actualfunc = self.prev.actualfunc if prev != None else None
        
    #obtengo simbolos en tabla
    def getSimbolos(self):
        return self.tsimbolos
    
    #buscar simbolo solo en tabla actual
    def existeVariableLocalTsActual(self,id):
        if id in self.tsimbolos: #que busque en su atributo simbolos(diccionario de simbolos)
            return True
    
    def getTablaAnterior(self):
        return self.anterior
    
    #para crear enlace a tabla anterior
    def setTsAnterior(self, tabla):
        self.anterior = tabla
    
    def setSimboloEnTs(self, simbolo): #agrega una nueva definicion
        if simbolo.id in self.tsimbolos:
            return Error('SEMANTICO',"etiqueta "+simbolo.id+" ya existe",simbolo.fil,simbolo.col)
        else:
            self.tsimbolos[simbolo.id] = simbolo
            self.actualizarSize()
            return None
    #guardo variables directamente en ts
    def agregarVar(self,id,tipo,fil,col):
        nuevaVariable = Simbolo(id,tipo,'',fil,col,self.size,False,(tipo == Tipo.CADENA or tipo == Tipo.STRUCT),Ambito.LOCAL,False,False,False)
        self.tsimbolos[nuevaVariable.id]=nuevaVariable
        self.actualizarSize()
        return None

    #guardo variables directamente en ts
    def agregarVec(self,id,tipo,esvector,dimensiones,fil,col):
        nuevaVariable = Simbolo(id,tipo,'',fil,col,self.size,False,(tipo == Tipo.CADENA or tipo == Tipo.STRUCT),Ambito.LOCAL,False,False,False)
        nuevaVariable.arreglo = esvector
        nuevaVariable.dimensiones=dimensiones
        self.tsimbolos[nuevaVariable.id]=nuevaVariable
        self.actualizarSize()
        return None
    
    #guardar funcion en ts de funciones
    def setSimboloEnTsFunc(self,func,idUnico,esNativa=False):
        if func.id in self.tsfunciones:
            return Error('SEMANTICO',"etiqueta "+func.id+" ya existe",func.fil,func.col)
        else:
            self.tsfunciones[func.id] = SimboloFun(func,idUnico,esNativa)
            #->->->->->->->->->->->->-> VALIDAR QUE FUNCIONE SIN ESTO
            #self.actualizarSize()
            #->->->->->->->->->->->->->->>-
            return None
    
    def getFuncion(self,id):
        tsactual = self
        while tsactual != None:
            if id in tsactual.tsfunciones:
                return tsactual.tsfunciones[id]
            else:
                tsactual = tsactual.anterior
        return None
        
    def getSimboloEnTs(self,id):
        tsActual = self #obtengo referencia de la tabla actual
        while tsActual != None: #si la tabla actual tiene elementos
            if id in tsActual.tsimbolos: #que busque en su atributo simbolos(diccionario de simbolos)
                return tsActual.tsimbolos[id] #la clave que se solocita*
            else:#sino que busque en la tabla anterior(en otro ambito )
                tsActual = tsActual.anterior
        return None

    def actualizarTs(self,simbolo):
        tsActual = self #obtengo referencia de la tabla actual
        while tsActual != None: #si la tabla actual tiene elementos
            if simbolo.id in tsActual.tsimbolos: #que busque en su atributo simbolos(diccionario de simbolos)
                tsActual.tsimbolos[simbolo.id]=simbolo #la clave que se solocita*
                #self.tsimbolos[simbolo.id].setTipo(simbolo.getTipo())
                return "etiqueta actualizada" 
            else:#sino que busque en la tabla anterior(en otro ambito)
                tsActual = tsActual.anterior
        return None
    
    def tablaAnterior(self):
        if self.anterior != None:
            return True
            
    
    def actualizarTsLocal(self,simbolo):
        tsActual = self
        simbolos = tsActual.getSimbolos()
        if simbolo.id in simbolos: #que busque en su atributo simbolos(diccionario de simbolos)
            self.tsimbolos[simbolo.id]=simbolo #la clave que se solocita*
            #self.tsimbolos[simbolo.id].setTipo(simbolo.getTipo())
            return "etiqueta actualizada" 
        #else:#sino que busque en la tabla anterior(en otro ambito)
        #    tsActual = tsActual.anterior
        return None
    
    def getTsLocal(self,id):
        tsActual = self
        simbolos = tsActual.getSimbolos()
        if id in simbolos: #que busque en su atributo simbolos(diccionario de simbolos)
            #self.tsimbolos[simbolo.id]=simbolo #la clave que se solocita*
            #self.tsimbolos[simbolo.id].setTipo(simbolo.getTipo())
            return "etiqueta encontrada" 
        #else:#sino que busque en la tabla anterior(en otro ambito)
        #    tsActual = tsActual.anterior
        return None
    
    def setEstadoLocal(self):
        'esta funcion ayuda a regresar todas las variales a local en caso en una instruccion venga un global'
        tsActual = self
        simbolos = tsActual.getSimbolos()
        for simbolo in simbolos:
            simbolos[simbolo].setAmbito(Ambito.LOCAL)
            
    def setEtiquetaGlobal(self,id):
        self.listadoGlobales.append(id)
    
    def buscarEtiquetaGlobal(self,id):
        if id in self.listadoGlobales:
            return True
        return False
    
    def setEtiquetaLocal(self,id):
        self.listadoLocales.append(id)
    
    def buscarEtiquetaLocal(self,id):
        if id in self.listadoLocales:
            return True
        return False
        
        
    def actualizarTsSinGLobal(self,simbolo,tsgloba):
        tsActual = self #obtengo referencia de la tabla actual
        while tsActual != None: #si la tabla actual tiene elementos
            if simbolo.id in tsActual.tsimbolos: #que busque en su atributo simbolos(diccionario de simbolos)
                tsActual.tsimbolos[simbolo.id]=simbolo #la clave que se solocita*
                #self.tsimbolos[simbolo.id].setTipo(simbolo.getTipo())
                return "etiqueta actualizada" 
            else:#sino que busque en la tabla anterior(en otro ambito)
                if tsActual.anterior!=tsgloba:
                    tsActual = tsActual.anterior
                else:
                    return None
        return None
    
    def getTsSinGLobal(self,id,tsgloba):
        tsActual = self #obtengo referencia de la tabla actual
        while tsActual != None: #si la tabla actual tiene elementos
            if id in tsActual.tsimbolos: #que busque en su atributo simbolos(diccionario de simbolos)
                return tsActual.tsimbolos[id] #la clave que se solocita*
                #self.tsimbolos[simbolo.id].setTipo(simbolo.getTipo()) 
            else:#sino que busque en la tabla anterior(en otro ambito)
                if tsActual.anterior!=tsgloba:
                    tsActual = tsActual.anterior
                else:
                    return None
        return None
    
    def actualizarSize(self):
        self.size += 1
        
            