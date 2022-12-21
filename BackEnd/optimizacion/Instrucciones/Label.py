from optimizacion.c3d import *

class Label(C3DInstruction):

    def __init__(self, id, line, column):
        C3DInstruction.__init__(self, line, column)
        self.id = id
        #atributo para bloques: todo destino de un salto es lider
        self.esLider=True
    
    def getCode(self):
        if self.deleted:
            return ''
        return f'{self.id}:'