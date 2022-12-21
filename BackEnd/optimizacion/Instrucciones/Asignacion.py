from typing import Literal

from flask.scaffold import F
from optimizacion.Expresiones.Expresiones import Expresion
from optimizacion.c3d import *
from optimizacion.Expresiones.Literal import *

class Asignacion(C3DInstruction):
    def __init__(self, place, exp, line, column):
        C3DInstruction.__init__(self, line, column)
        self.place = place                              # esto es lo que esta antes del igual t0=; stack[int(t0)] = 
        self.exp = exp                                  #esto es lo que esta al 

    def selfAssignment(self):
        if type(self.exp) is Literal:                   # si es literal es una asingacion de este tipo: t0=1; t0=2.5,t0=t1,t0=-4
            aux = self.place.getCode() == self.exp.getCode()
        else:                                           #sino es t0=t0 + t1 
                                                        #lado antes de igual  ==  lado drecho despues del igual ó lado antes de igual  ==  lado izquierdo despues del igual
            aux = self.place.getCode() == self.exp.right.getCode() or self.place.getCode() == self.exp.left.getCode()
        return aux
    
    def validarRegla7(self):
        if type(self.exp.left) is Literal or type(self.exp.right) is Literal:
            aux = (self.place.getCode() != self.exp.left.getCode() and (self.exp.right.getCode() == '0' or self.exp.right.getCode() == '1')) or (self.place.getCode() != self.exp.right.getCode() and (self.exp.left.getCode() == '0' or self.exp.left.getCode() == '1'))
            return aux
        return False
    
    #def validarReglao8(self):
    #    if type(self.exp.left) is Literal and self.exp.right.getCode()   or type(self.exp.right) is Literal:
    #        return True
    #    return False
    
    def getCode(self):
        if self.deleted:
            return ''
        return f'{self.place.getCode()} = {self.exp.getCode()};'
    
    #def validarRegla1(self):
        