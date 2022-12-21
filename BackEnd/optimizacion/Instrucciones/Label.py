from Optimizador.InstruccionC3D import *
class Label(C3DInstruction):
    
    def __init__(self, id, line, column):
        C3DInstruction.__init__(self, line, column)
        self.id = id
        self.R5=''
    
    def getCode(self):
        if self.deleted:
            return ''
        return f'{self.R5}{self.id}:'