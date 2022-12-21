from Optimizador.InstruccionC3D import *

class Return(C3DInstruction):

    def __init__(self, line, column):
        C3DInstruction.__init__(self, line, column)
    
    def getCode(self):
        return 'return;'