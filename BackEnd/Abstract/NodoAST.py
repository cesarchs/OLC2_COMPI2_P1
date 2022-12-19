
class NodoAST():
    def __init__(self,valor):
        self.valor=valor
        self.hijos = []
        

    def setHijos(self,hijos):#array=array
        self.hijos = hijos

    def agregarHijo(self,valorHijo):#el nodo NO esta hecho
        self.hijos.append(NodoAST(valorHijo))

    def agregarHijos(self,hijos):#hijos in array append self.hijos
        for hijo in hijos:
            self.hijos.append(hijo)
            
    def agregarHijoNodo(self,hijo):#ya el nodo esta hecho
        self.hijos.append(hijo)


    def agregarPrimerHijo(self,valorHijo):#el nodo NO esta hecho e insertamos al inicio
        self.hijos.insert(0,NodoAST(valorHijo))


    def agregarPrimerHijoNodo(self,hijo):#el nodo YA esta hecho e insertamos al inicio
        self.hijos.insert(0,hijo)




    def getValor(self):
        return str(self.valor)

    def setValor(self,valor):
        self.valor=valor

    def getHijos(self):
        return self.hijos
