#from TIPO import tipo


class Simbolo():
    def __init__(self, identificador, tipo,arreglo, fila, columna, valor,size=None,inHEAP=None,global1=None):
        self.id=identificador
        self.tipo=tipo
        self.fila=fila
        self.columna=columna
        self.valor=valor
        self.arreglo=arreglo


        self.index=None


        self.size=size
        self.inHEAP=inHEAP
        self.global1=global1
        #por si queremos saber el numero de referencia self.ref=0 e irle ++
#--------------------------------
    def getID(self):
        return self.id

    def setID(self,id):    
        self.id=id
#--------------------------------
    def getTipo(self):
        return self.tipo

    def setTipo(self,tipo):    
        self.tipo=tipo   
 #--------------------------------       
    def getFILA(self):
        return self.fila

    def setFILA(self,fila):    
        self.fila=fila       
#--------------------------------
    def getCOLUMNA(self):
        return self.columna

    def setCOLUMNA(self,col):    
        self.columna=col
#--------------------------------
    def getValor(self):
        return self.valor

    def setValor(self,valor):    
        self.valor=valor     
#--------------------------------












