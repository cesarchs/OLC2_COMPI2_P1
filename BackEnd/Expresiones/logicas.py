from almacenar.generador import Generador
from padres.expresion import Expresion

from padres.Nodo import NodoArbol
from almacenar.error import Error
from almacenar.tipo import Return, Tipo, OpsLogical

#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol
#from almacenar.error import Error
#from almacenar.tipo import Tipo, OpsLogical


class Logica(Expresion):
    def __init__(self, operador, operacionI, operacionD, fil, col):
        super().__init__(fil, col)
        self.operador = operador
        self.operacionI = operacionI
        self.operacionD = operacionD  # si fuera unaria esta seria None
        self.fila = fil
        self.columna = col
        self.tipo = Tipo.BOOLEANO  # se definira deendiendo de la operación
        self.struct = False
        self.mutable = False
        
    def compilar(self, arbol, tabla):
        'resisq = resultado opE izquierda, resder = resultado opE derecha'
        
        genAux = Generador()
        generator = genAux.getInstance()
        generator.agregarComentario("INICIO EXPRESION LOGICA")
        self.checkLabels()
        lblAndOr=''
        
        
            
        if self.operacionD != None:
            #BINARIAS
            
            # OPE1 && OPE2
            
            if self.operador == OpsLogical.AND:
                lblAndOr = self.operacionI.trueLbl = generator.agregarLabel()
                self.operacionD.trueLbl = self.trueLbl
                self.operacionI.falseLbl = self.operacionD.falseLbl = self.falseLbl
                #bool and bool
                resizq = self.operacionI.compilar(arbol, tabla)
                if isinstance(resizq, Error): return resizq  # ya no se sigue y se retorna el error almacenado en resizq
                if self.operacionI.tipo == Tipo.BOOLEANO: 
                    #return self.getValor(self.operacionI.tipo, resizq) and self.getValor(self.operacionD.tipo, resder)
                    generator.colocarLabel(lblAndOr)
                    
                    resder = self.operacionD.compilar(arbol, tabla)
                    if isinstance(resder, Error): return resder
                    if self.operacionD.tipo == Tipo.BOOLEANO:  
                        generator.agregarComentario("FINALIZA EXPRESION LOGICA")
                        generator.agregarSalto()
                        ret = Return(None,Tipo.BOOLEANO,False)
                        ret.trueLbl = self.trueLbl
                        ret.falseLbl = self.falseLbl
                        return ret
                return Error("SEMANTICO","Operacion no valida con '&&'",self.fila,self.columna)
            # OPE1 || OPE2
            elif self.operador == OpsLogical.OR:
                self.operacionI.trueLbl = self.operacionD.trueLbl = self.trueLbl
                lblAndOr = self.operacionI.falseLbl = generator.agregarLabel()
                self.operacionD.falseLbl = self.falseLbl
                
                #bool and bool
                resizq = self.operacionI.compilar(arbol, tabla)
                if isinstance(resizq, Error): return resizq  # ya no se sigue y se retorna el error almacenado en resizq
                if self.operacionI.tipo == Tipo.BOOLEANO: 
                    #return self.getValor(self.operacionI.tipo, resizq) and self.getValor(self.operacionD.tipo, resder)
                    generator.colocarLabel(lblAndOr)
                    
                    resder = self.operacionD.compilar(arbol, tabla)
                    if isinstance(resder, Error): return resder
                    if self.operacionD.tipo == Tipo.BOOLEANO:  
                        generator.agregarComentario("FINALIZA EXPRESION LOGICA")
                        generator.agregarSalto()
                        ret = Return(None,Tipo.BOOLEANO,False)
                        ret.trueLbl = self.trueLbl
                        ret.falseLbl = self.falseLbl
                        return ret
                return Error("SEMANTICO","Operacion no valida con '||'",self.fila,self.columna)
        
        #UNARIA
        
        #op!
        elif self.operador == OpsLogical.NOT:
            #!bool
            if self.operacionI.tipo == Tipo.BOOLEANO:
                copiaTrue=self.trueLbl
                self.trueLbl = self.falseLbl
                self.falseLbl = copiaTrue
                
                self.operacionI.trueLbl=self.trueLbl
                self.operacionI.falseLbl=self.falseLbl
                resizq = self.operacionI.compilar(arbol, tabla)
                if isinstance(resizq, Error): return resizq  # ya no se sigue y se retorna el error almacenado en resizq
                ret = Return('',self.operacionI.tipo,False)
                ret.trueLbl = self.trueLbl
                ret.falseLbl = self.falseLbl
                return ret
                
            return Error("SEMANTICO","Operacion no valida con '!'",self.fila,self.columna)
        
        return Error("SEMANTICO","Operacion no válida",self.fila,self.columna)


    def getValor(self, tipo, val):
        if tipo == Tipo.ENTERO:
            return int(val)
        elif tipo == Tipo.DECIMAL:
            return float(val)
        elif tipo == Tipo.BOOLEANO:
            return bool(val)
        return str(val)
    
    def getTipo(self, val):
        if isinstance(val,int):
            return Tipo.ENTERO
        elif isinstance(val,float):
            return Tipo.DECIMAL
        elif isinstance(val,bool):
            return Tipo.BOOLEANO
        return Tipo.CADENA
    
    def getNode(self):
        nodoLogicas = NodoArbol("LOGIC") #NOMBRE PADRE
        #binarias
        if self.operacionD != None:
            nodoLogicas.agregarHijoConNodo(self.operacionI.getNode()) #valor = trae un Nodo Primitivo por eso es con Nodo
            nodoLogicas.agregarHijoSinNodo(str(self.operador)) 
            nodoLogicas.agregarHijoConNodo(self.operacionD.getNode()) #valor = trae un Nodo Primitivo por eso es con Nodo
        #unarias
        else:
            nodoLogicas.agregarHijoSinNodo(self.operador)
            nodoLogicas.agregarHijoConNodo(self.operacionI.getNode()) #valor = trae un Nodo Primitivo por eso es con Nodo
        return nodoLogicas

    def checkLabels(self):
        genAux = Generador()
        generator = genAux.getInstance()
        if self.trueLbl == '':
            self.trueLbl = generator.agregarLabel()
        if self.falseLbl == '':
            self.falseLbl = generator.agregarLabel()