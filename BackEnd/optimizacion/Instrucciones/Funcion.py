from optimizacion.c3d import *

class Function(C3DInstruction):

    def __init__(self, instr, id, line, column):
        C3DInstruction.__init__(self, line, column)
        self.instr = instr
        self.id = id
    
    def getCode(self):
        ret = f'func {self.id}(){{\n'
        for ins in self.instr:
            auxText = ins.getCode()
            if(auxText == ''):
                continue
            #ret = ret + f'\t{auxText}'
            
            if ins.esLider:
                ret = ret + f'\n\t{auxText} //----Lider----'
            else:
                ret = ret + f'\t{auxText}'
            ret = ret + '\n'
            
        ret = ret + '}'
        return ret