class NodoArbol():#con esta clase se identicara a los posibles hijos 

    def __init__(self, valor): #recibe el id o nombre de TERMINAL O NO TERMINAL
        self.hijos = []
        self.valor = valor #ID DE NODO

    def getValor(self): 
        'RETORNA EL ID DEL NODO'
        return str(self.valor)
    
    def getHijos(self):
        return self.hijos
    
    def setValor(self,valor):
        'ESTABLECE EL NOMBRE DEL NODO'
        self.valor = valor
    
    def setHijos(self,hijos):
        self.hijos = hijos
    
    def agregarHijoSinNodo(self, valor):
        self.hijos.append(NodoArbol(valor))
    
    def agregarHijoConNodo(self, Nodo):
        self.hijos.append(Nodo)
    
    def agregarHijos(self,Hijos):
        for hijo in Hijos:
            self.hijos.append(hijo)
    
    def firstAddHijoSinNodo(self, valor):
        self.hijos.insert(0,NodoArbol(valor))
        
    def firstAddHijoConNodo(self,Nodo):
        self.hijos.insert(0,Nodo)
        
    
    
    
    
    