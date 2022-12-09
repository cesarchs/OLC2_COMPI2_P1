from Optimizador.InstruccionC3D import *
class MathFunc(C3DInstruction):
    
    def __init__(self,opI,opD, line, column):
        C3DInstruction.__init__(self, line, column)
        
        self.left = opI
        self.right= opD

    def getCode(self):
        return f'math.Mod({self.left.value},{self.right.value})'