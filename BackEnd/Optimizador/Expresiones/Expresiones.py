from Optimizador.InstruccionC3D import *

class Expression(C3DInstruction):
    
    def __init__(self, left, right, typeOp, line, column):
        C3DInstruction.__init__(self, line, column)
        self.left = left
        self.right = right
        self.typeOp = typeOp
        self.constant = left.constant or right.constant

    def neutralOps(self):
        if self.typeOp == '+' or self.typeOp == '-':
            self.deleted = self.right.getCode() == '0' or self.left.getCode() == '0'
        elif self.typeOp == '*':
            self.deleted = self.right.getCode() == '1' or self.left.getCode() == '1'
        elif self.typeOp == '/':
            self.deleted = self.right.getCode() == '1'
        elif self.typeOp == '':
            self.deleted = self.right.getCode() == '1'
        return self.deleted

    def neutralOps2(self):
            if self.typeOp == '+' or self.typeOp == '-':
                self.deleted = self.right.getCode() == '0'
            elif self.typeOp == '*':
                self.deleted = self.right.getCode() == '1'
            elif self.typeOp == '/':
                self.deleted = self.right.getCode() == '1'
            elif self.typeOp == '':
                self.deleted = self.right.getCode() == '1'
            return self.deleted


    def Rule8(self):
        if self.typeOp == '*':
            return self.right.getCode() == '0' or self.right.getCode() == '2'
        elif self.typeOp == '/':
            return self.left.getCode() == '0'
        elif self.typeOp == '':
            return False
        return False

    def getContrary(self):
        if self.typeOp == '>':
            self.typeOp = '<='
        elif self.typeOp == '<':
            self.typeOp = '>='
        elif self.typeOp == '>=':
            self.typeOp = '<'
        elif self.typeOp == '<=':
            self.typeOp = '>'
        elif self.typeOp == '==':
            self.typeOp = '!='
        elif self.typeOp == '!=':
            self.typeOp = '=='
        else:
            print('QUE ANDAS GENERANDO AHI >:v')

    def getCode(self):
        return f'{self.left.getCode()}{self.typeOp}{self.right.getCode()}'