from optimizacion.c3d import C3DInstruction

class FuncionMath(C3DInstruction):
    def __init__(self,opi,opd, line, column):
        C3DInstruction.__init__(self,line,column)
        
        self.OpI = opi
        self.OpD = opd
    
    def getCode(self):
        return f'math.Mod({self.OpI},{self.OpD});'