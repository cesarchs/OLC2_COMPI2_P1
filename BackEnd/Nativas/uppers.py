from re import S
from almacenar.generador import Generador
from instrucciones.funcs import Funcion
from almacenar.tipo import Return, Tipo
from almacenar.error import Error
from padres.Nodo import NodoArbol
from padres.expresion import Expresion
from padres.instruccion import Instruccion

#from instrucciones.funcs import Funcion
#from almacenar.tipo import Tipo
#from almacenar.error import Error

class Upper(Instruccion):
    def __init__(self,exp, fila, columna):
        self.expresion = exp
        self.fila = fila
        self.columna = columna
        self.tipo = None
    def compilar(self, arbol, tabla):
        retornExp = self.expresion.compilar(arbol,tabla)
        if isinstance(retornExp,Error):return retornExp
        
        genAux = Generador()
        generator = genAux.getInstance()
        
        if retornExp.tipo != Tipo.CADENA: return Error("SEMANTICO",'UPPERCASE SOLO ES VALIDO CON CADENAS')
        
        generator.toUpper()#imprimo en C3D funcion nativa de impresion
                
        paramTemp=generator.agregarTemporal() # genero temporal para entorno simulado
        generator.liberarTemporal(paramTemp)
        #cambio de entorno simulado:
        generator.addExp(paramTemp, 'P', tabla.size, '+')
        generator.addExp(paramTemp, paramTemp, '1', '+')
        generator.setPila(paramTemp, retornExp.getValor())
        
        #cambio de entorno:
        generator.newEnv(tabla.size)
        generator.llamandaFuncion('nativaToUpper')
        
        #obtengo valor de retorno:
        temp = generator.agregarTemporal()
        generator.liberarTemporal(temp)
        generator.getPila(temp,'P')
        
        #REGRESO A ENTORNO MAIN
        generator.returnEntorno(tabla.size)
        self.tipo = Tipo.CADENA
        return Return(temp,Tipo.CADENA,True)
    
    def getNode(self):
        nodoTRUNC = NodoArbol("UPPERCASE") #NOMBRE PADRE
        #nodoTRUNC.agregarHijoConNodo(self.expresion.getNode())
        return nodoTRUNC

class Lower(Instruccion):
    def __init__(self,exp, fila, columna):
        self.expresion = exp
        self.fila = fila
        self.columna = columna
        self.tipo = None
    
    def compilar(self, arbol, tabla):
        retornExp = self.expresion.compilar(arbol,tabla)
        if isinstance(retornExp,Error):return retornExp
        
        genAux = Generador()
        generator = genAux.getInstance()
        
        if retornExp.tipo != Tipo.CADENA: return Error("SEMANTICO",'UPPERCASE SOLO ES VALIDO CON CADENAS')
        
        generator.toLower()#imprimo en C3D funcion nativa de impresion
                
        paramTemp=generator.agregarTemporal() # genero temporal para entorno simulado
        generator.liberarTemporal(paramTemp)
        #cambio de entorno simulado:
        generator.addExp(paramTemp, 'P', tabla.size, '+')
        generator.addExp(paramTemp, paramTemp, '1', '+')
        generator.setPila(paramTemp, retornExp.getValor())
        
        #cambio de entorno:
        generator.newEnv(tabla.size)
        generator.llamandaFuncion('nativaToLower')
        
        #obtengo valor de retorno:
        temp = generator.agregarTemporal()
        generator.liberarTemporal(temp)
        generator.getPila(temp,'P')
        
        #REGRESO A ENTORNO MAIN
        generator.returnEntorno(tabla.size)
        self.tipo = Tipo.CADENA
        return Return(temp,Tipo.CADENA,True)
    
    def getNode(self):
        nodoTRUNC = NodoArbol("LOWERCASE") #NOMBRE PADRE
        #nodoTRUNC.agregarHijoConNodo(self.expresion.getNode())
        return nodoTRUNC()