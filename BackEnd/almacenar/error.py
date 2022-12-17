class Error:
    def __init__(self,tipo, descripcion, fila, columna):
        self.tipo = tipo
        self.descripcion =descripcion
        self.fila = fila
        self.columna = columna

    def toString(self):
        return "\n"+self.tipo + " -> " + self.descripcion + " en: ["+str(self.fila)+","+str(self.columna)+"]\n"
    
    def getTipo(self):
        return self.tipo
    
    def getDescripcion(self):
        return self.descripcion
    
    def getFila(self):
        return self.fila
    
    def getCol(self):
        return self.columna