from Optimizador.InstruccionC3D import *

class Goto(C3DInstruction):
    
    def __init__(self, label, line, column):
        C3DInstruction.__init__(self, line, column)
        self.label = label
        self.banderaGo = False
        self.labelAux = ''
        
    def getCode(self):
        if self.deleted:
            return ''
        return f'goto {self.label}; {self.evitarErrorGotoEnGo()}'
    
    def evitarErrorGotoEnGo(self):
        if self.banderaGo == True:
            return f'\n\tgoto {self.labelAux};'
        else:
            return ''