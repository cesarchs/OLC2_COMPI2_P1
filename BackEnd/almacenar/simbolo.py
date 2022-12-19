class Simbolo:
    'ESTA CLASE SIRVE PARA DEFINIR UN SIMBOLO EN LA TS'
    def __init__(self,id,tipo,valor,fil,col,posicion,globalvar,enHeap,ambito,arreglo,struc,muta):
        self.id = id
        self.tipo= tipo
        self.valor = valor
        self.fil = fil
        self.col = col
        self.posicion = posicion
        self.esGlobal = globalvar
        self.enHeap = enHeap
        self.ambito = ambito
        self.arreglo = arreglo
        self.struct = struc
        self.mutable = muta
        self.dimensiones=None
        self.array = None
        #self.ref 
    
    #SETs:
    def setId(self,id):
        self.id = id

    def setTipo(self,tipo):
        self.tipo = tipo
        
    def setValor(self,valor):
        self.id = valor
        
    def setAmbito(self,ambito):
        self.ambito = ambito

    #GETs:
    def getId(self):
        return self.id

    def getTipo(self):
        return self.tipo
    
    def getValor(self):
        return self.valor
    
    def getPosicion(self):
        return self.posicion
    
    def getFil(self):
        return self.fil
    
    def getCol(self):
        return self.col
    
    def getAmbito(self):
        return self.ambito

    def getArreglo(self):
        return self.arreglo
    
    def getStruct(self):
        return self.struct
    
    def getMuta(self):
        return self.mutable

    def verenHeap(self):
        return self.enHeap
    
    def getEsGlobal(self):
        return self.esGlobal
    
    def getDimensiones(self):
        return self.dimensiones
    
    def setDimensiones(self,dimensiones):
        self.dimensiones=dimensiones
        
    def getArray(self):
        return self.array
    
    def setArray(self,array):
        self.array = array
