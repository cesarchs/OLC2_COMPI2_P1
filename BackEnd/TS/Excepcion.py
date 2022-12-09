class Excepcion:
    def __init__(self,tipo,descripcion,fila,columna):
        self.tipo=tipo
        self.descripcion=descripcion
        self.fila=fila
        self.columna=columna


    def toString(self):
        return self.tipo+" : " +   self.descripcion+"[fila: " +  str(self.fila)+" , columna: " +  str(self.columna)+"]"

    
























