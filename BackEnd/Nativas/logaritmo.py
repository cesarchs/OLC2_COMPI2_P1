from almacenar.tipo import OpsAritmetico, Tipo
from almacenar.error import Error
from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol
from Expresiones.aritmeticas import Aritmetica

#from almacenar.tipo import OpsAritmetico, Tipo
#from almacenar.error import Error
#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol
#from Expresiones.aritmeticas import Aritmetica
import math

class LogaritmoDiez(Instruccion):
    def __init__(self,exp, fila, columna):
        self.tipo= Tipo.NULO
        self.expresion = exp
        self.fila = fila
        self.columna = columna
        self.struct = False
        self.mutable = False
    
    def compilar(self, arbol, tabla):
        
        resultadoExp = self.expresion.ejecutar(arbol,tabla)#veo que es la exp
        if isinstance(resultadoExp,Error): return resultadoExp
        
        if isinstance(self.expresion,Aritmetica):
            if self.expresion.operador == OpsAritmetico.COMA:
                return Error("SEMANTICO", "PARAMETRO INVALIDO PARA LOG10()",self.fila,self.columna)
        
        try:
            valorLog = math.log10(resultadoExp)     
            self.tipo= self.getTipo(valorLog)
            return valorLog
        except:
            return Error("SEMANTICO","FUNCION LOG10() UNICAMENTE RECIBE EXPRESION DE TIPO NUMERICO",self.fila,self.columna)

    def getTipo(self, val):
        if isinstance(val,int):
            return Tipo.ENTERO
        elif isinstance(val,float):
            return Tipo.DECIMAL
    
    
    def getNode(self):
        nodoLog10 = NodoArbol("LOG10") #NOMBRE PADRE
        nodoLog10.agregarHijoConNodo(self.expresion.getNode())
        return nodoLog10
    
class Logaritmoo(Instruccion):
    def __init__(self,exp, fila, columna):
        self.tipo= Tipo.NULO
        self.expresion = exp
        self.fila = fila
        self.columna = columna
        self.struct = False
        self.mutable = False
    
    def compilar(self, arbol, tabla):
        self.listaParms=[]
        self.exps=[]
        if isinstance(self.expresion,Aritmetica):
            if self.expresion.operador == OpsAritmetico.COMA:
                self.separarParametros(self.expresion,self.listaParms)
        
        if len(self.listaParms)>0:
            for exp in self.listaParms:
                self.exps.append(exp.ejecutar(arbol,tabla))
            for error in self.exps:
                if isinstance(error,Error):return error
            if len(self.exps)==2:
                try:
                    valorLog = math.log(self.exps[1],self.exps[0])     
                    self.tipo= self.getTipo(valorLog)
                    return valorLog
                except:
                    return Error("SEMANTICO","FUNCION LOG() UNICAMENTE RECIBE EXPRESION DE TIPO NUMERICO",self.fila,self.columna)
            else:
                return Error("SEMANTICO", "PARAMETRO(S) INVALIDO PARA LOG()",self.fila,self.columna)
        else:               
            resultadoExp = self.expresion.ejecutar(arbol,tabla)#veo que es la exp
            if isinstance(resultadoExp,Error): return resultadoExp
            try:
                valorLog = math.log(resultadoExp)     
                self.tipo= self.getTipo(valorLog)
                return valorLog
            except:
                return Error("SEMANTICO","FUNCION LOG() UNICAMENTE RECIBE EXPRESION DE TIPO NUMERICO",self.fila,self.columna)
        
    def separarParametros(self,arit:Aritmetica,nuevaLista:list):
        if arit.operador == OpsAritmetico.COMA: # suma(4,5);
            #tiene hijo izquierdo si ese hijo tiene izquerd o dercha y si tiene que llegue hasta ultimo izq , der
            #if isinstance(arit.operacionI,Identificador) and isinstance(arit.operacionD,Identificador): # SUMA(4+5, b , c)=> ARIMETICO=>OPI , OPD
            
            if isinstance (arit.operacionI,Aritmetica):# EXP COMA EXP
                self.separarParametros(arit.operacionI,nuevaLista)
            else:
                nuevaLista.append(arit.operacionI)
            if isinstance(arit.operacionD,Aritmetica): # EXP COMA EXP
                self.separarParametros(arit.operacionD,nuevaLista)
            else:
                nuevaLista.append(arit.operacionD)
        else:
            nuevaLista.append(arit) # agrego  raiz de una vez
            #puede traer un 4+5 - 4*3 - 4+5*3 (4+6+8*8-5/8,b)  opi * opd 8 

    def getTipo(self, val):
        if isinstance(val,int):
            return Tipo.ENTERO
        elif isinstance(val,float):
            return Tipo.DECIMAL
    
    
    def getNode(self):
        nodoLog10 = NodoArbol("LOG") #NOMBRE PADRE
        nodoLog10.agregarHijoConNodo(self.expresion.getNode())
        return nodoLog10