from TS.Simbolo import *#importo todo lo de simbolos
#para ahorrarme procesos respecto a la fase anterior optimizare

class TablaSimbolosV2:
    
    def __init__(self, anterior):
        self.anterior = anterior
        
        # NUEVO
        self.size = 0
        self.breakLbl = ''
        self.continueLbl = ''
        self.returnLbl = ''

        if(anterior != None):
            self.size = self.anterior.size
            self.breakLbl = self.anterior.breakLbl
            self.continueLbl = self.anterior.continueLbl
            self.returnLbl = self.anterior.returnLbl
        
        self.variables = {}
        self.functions = {}
        self.structs = {}



    def saveVar(self, idVar, symType, inHeap, structType = ""):
        if idVar in self.variables.keys():
            print("Variable ya existe")
        else:
            newSymbol = Simbolo(idVar, symType, self.size, self.anterior == None, inHeap, structType)
            self.size += 1
            self.variables[idVar] = newSymbol
        return self.variables[idVar]



    def saveFunc(self, idFunc, function):
        if idFunc in self.functions.keys():
            print("Función repetida")
        else:
            self.functions[idFunc] = function



    
    def saveStruct(self, idStruct, attr):
        if idStruct in self.structs.keys():
            print("Struct repetido")
        else:
            self.structs[idStruct] = attr




    def getVar(self, idVar):
        env = self
        while env != None:
            if idVar in env.variables.keys():
                return env.variables[idVar]
            env = env.anterior
        return None



    
    def getFunc(self, idFunc):
        env = self
        while env != None:
            if idFunc in env.functions.keys():
                return env.functions[idFunc]
        return None


        
    def getStruct(self, idStruct):
        env = self
        while env != None:
            if idStruct in env.structs.keys():
                return env.structs[idStruct]
            end = end.anterior
        return None

        

    def getGlobal(self):
        env = self
        while env.anterior != None:
            env = env.anterior
        return env