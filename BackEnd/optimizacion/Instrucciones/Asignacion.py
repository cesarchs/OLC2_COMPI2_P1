from Optimizador.Expresiones.Acceso import Access
from Optimizador.Expresiones.Expresiones import Expression
from Optimizador.Expresiones.Literal import Literal
from Optimizador.InstruccionC3D import *
from Optimizador.Instrucciones.MathGo import MathFunc

class Assignment(C3DInstruction):
    
    def __init__(self, place, exp, line, column):
        C3DInstruction.__init__(self, line, column)
        self.place = place
        self.exp = exp
        

    def selfAssignment(self):
        if type(self.exp) is Literal:
            aux = self.place.getCode() == self.exp.getCode()
            #print(self.place.getCode()+"=="+self.exp.getCode()+" "+str(aux))
        else:
            if type(self.exp) is MathFunc or type(self.exp) is Access:
                
                aux = self.place.getCode() == self.exp.getCode()

            else:
                aux = self.place.getCode() == self.exp.right.getCode() or self.place.getCode() == self.exp.left.getCode()
        return aux



    def selfAssignmentR7(self):
        aux=False
        if type(self.exp) is Expression:
                aux = type(self.exp.left)is Literal
        return aux
    
    def getCode(self):
        if self.deleted:
            return ''
        return f'{self.place.getCode()} = {self.exp.getCode()};'