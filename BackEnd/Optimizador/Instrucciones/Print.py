from Optimizador.InstruccionC3D import *
class Print(C3DInstruction):
    
    def __init__(self, strTo, exp, line, column):
        C3DInstruction.__init__(self, line, column)
        self.strTo = strTo
        self.exp = exp
    
    def getCode(self):
        if self.strTo=="%d" or self.strTo=="%c":
            return f'fmt.Printf(\"{self.strTo}\", int({self.exp.getCode()}));'

        else:
            return f'fmt.Printf(\"{self.strTo}\", {self.exp.getCode()});'