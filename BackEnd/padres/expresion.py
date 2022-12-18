from abc import ABC, abstractmethod

class Expresion(ABC):#con esta clase se identicara a los posibles hijos 

    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.trueLbl = ''
        self.falseLbl = ''
        super().__init__() #llama al construcctor de esta clase abs

    @abstractmethod
    def compilar(self,arbol,tabla): #cambia nonbre a compilar
        pass
    
    @abstractmethod
    def getNode(self):
        pass
        