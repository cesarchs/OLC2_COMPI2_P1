class Informacion:
    def __init__(self, consola,c3d ,arbol):
        self.consola = consola
        self.c3d = c3d
        self.arbol = arbol
        self.tablaSimbolos=[{'no':'0', 'id':'-','tipo':'-','ambito':'-','valor':'-','fil':'-','col':'-'}]
        self.errores =     [{'no':'-','des':'-', 'fil':'-',   'col':'-','fecha':''}]
    
    def setTs(self,listaTs):
        self.tablaSimbolos=listaTs
    
    def setlError(self,listaError):
        self.errores=listaError
    
    def getConsola(self):
        if self.consola == '':
            return ''
        return self.consola
    
    def getC3D(self):
        return self.c3d

    def getArbol(self):
        return self.arbol
    
    def getTs(self):
        return self.tablaSimbolos
    
    def getErrores(self):
        return self.errores
    
    