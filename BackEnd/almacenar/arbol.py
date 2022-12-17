
# ayuda a realizar las instrucciones


from almacenar.error import Error
#from almacenar.error import Error


class Arbol:
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones #LISTADO DE INSTRUCCIONES
        self.lErrores = []                 #LISTADO DE ERROES EN FLUJO 
        self.consola = ""                  #CONSOLA LOCAL
        self.TsGlobal = None               #TABLA GLOBAL DEL ARBOL
        self.A_dot = ""                    #SINTAXIS DOT PARA GRAFICA DE ARBOL
        self.Numero = 0                    #NUMERO DE NODO(CONTADOR)
        self.ListaTablas = []              #LISTA DE TABLAS EN LOS DIVERSOS AMBITOS PARA REPORTE
        self.funcs = {}                    #DICCIONARIO DE FUNCIONES 
        self.structs = {}                  #DICCIONARIO DE STRUCTS
        self.ambitoFuncion = False         #BOOL PARA AMBITO FUNCION  (SI ES TRUE LAS DECLARACIONES QUE SE HAGAN EN LA FUNCION SERAN LOCALES CON EXCEPCION DE GLOBAL)
    #SETs
    def agregarFuncs(self,funcion):
        if funcion.id in self.funcs:
            return Error("SEMANTICO","FUNCION: "+funcion.id+" YA EXISTE",funcion.fila,funcion.columna)
        else:
            self.funcs[funcion.id] = funcion
            return None
    def agregarStruct(self,struct):
        if struct.idStruct in self.structs:
            return Error("SEMANTICO","STRUCT: "+struct.idStruct+" YA EXISTE ", struct.fila,struct.columna)
        else:
            self.structs[struct.idStruct] = struct
            return None
    
    def setInstrucciones(self, instrucciones):
        self.instrucciones = instrucciones

    def setListaErrores(self, errores):
        self.lErrores = errores

    def setConsola(self, consola):
        self.consola = consola
    
    def actualizarConsola(self,cadena):
        self.consola += str(cadena) #+ '\n'

    def setTsGlobal(self, ts):
        self.TsGlobal = ts
    
    def setAdot(self,Adot):
        self.A_dot = Adot
    
    def setNumero(self, numero):
        self.Numero = numero

    def getInstrucciones(self):
        return self.instrucciones
    
    def agregarAListaTablas(self,ambito,tabla):
        self.ListaTablas.append((ambito,tabla))
        
    def setValorAmbitoFuncion(self,valor):
        self.ambitoFuncion=valor
    
    def getValorAmbitoFuncion(self):
        return self.ambitoFuncion
    
    #Gets
    def getListaErrores(self):
        return self.lErrores

    def getConsola(self):
        return self.consola

    def getTsGlobal(self):
        return self.TsGlobal
    
    def getListaTablas(self):
        return self.ListaTablas
    
    def getFuncs(self):
        return self.funcs
    
    def getStructs(self):
        return self.structs
    
    def getFunc(self,id):
        if id in self.funcs:
            return self.funcs[id]
        return None  
    
    def getStuct(self,id):
        if id in self.structs:
            return self.structs[id]
        return None
    
    def tipoStruct(self,id):
        if id in self.structs:
            return True
        return False
    
    def getDot(self,NodoRaiz):
        self.A_dot = ""
        self.A_dot += "digraph G{\n node [shape=record];\n"
        self.A_dot += "n0[label=\""+ NodoRaiz.getValor().replace("\"","\\\"").replace(">","\>")+"\"];\n"
        self.Numero = 1
        self.recorridoArbol("n0",NodoRaiz)
        self.A_dot += "}"
        return self.A_dot
    
    def recorridoArbol(self, etiquetaPadre, nodoPadre):
        for hijo in nodoPadre.getHijos():
            etiquetaHijo = "n"+str(self.Numero)
            self.A_dot += etiquetaHijo + "[label=\""+ hijo.getValor().replace("\"","\\\"").replace(">","\>")+"\"];\n"
            self.A_dot += etiquetaPadre + "->" + etiquetaHijo +";\n"
            self.Numero += 1
            self.recorridoArbol(etiquetaHijo,hijo)    
    
    def getNumero(self):
        return self.Numero
