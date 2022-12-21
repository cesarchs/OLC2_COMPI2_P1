from optimizacion.Expresiones.Literal import Literal
from optimizacion.c3d import *

class Expresion(C3DInstruction):
    def __init__(self, left,right,typeOp,line,column):
        C3DInstruction.__init__(self,line,column)
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
        else:
            return self.deleted
        return self.deleted
    
    def OperandoOperador(self):
        if self.typeOp == '+' or self.typeOp == '-':
            if self.right.getCode()=='0':
                self.typeOp=''
                self.right=Literal('',self.line,self.column)
                #self.deleted=True
                return True
            elif self.left.getCode()=='0':
                if self.typeOp =='+':
                    self.typeOp=''
                    self.left=Literal('',self.line,self.column)
                else:
                    self.typeOp=''
                    self.left=Literal('-',self.line,self.column)
                #self.deleted=True
                return True
            else:
                return False
        elif self.typeOp == '*':
            if self.right.getCode()=='1':
                self.typeOp=''
                self.right=Literal('',self.line,self.column)
                #self.deleted=True
                return True
            elif self.left.getCode()=='1':
                self.typeOp=''
                self.left=Literal('',self.line,self.column)
                #self.deleted=True
                return True
            else:
                return False
        elif self.typeOp == '/':
            if self.right.getCode()=='1':
                self.typeOp=''
                self.right=Literal('',self.line,self.column)
                #self.deleted=True
                return True
            else:
                return False
        else:
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
            print('EXP INCORRECTA')

    def getCode(self):
        return f'{self.left.getCode()}{self.typeOp}{self.right.getCode()}'