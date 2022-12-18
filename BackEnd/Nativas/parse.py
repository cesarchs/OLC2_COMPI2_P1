from Expresiones.primitivos import Primitivo
from almacenar.generador import Generador
from almacenar.tipo import Return, Tipo
from almacenar.error import Error
from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol

#from almacenar.tipo import Tipo
#from almacenar.error import Error
#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol

class Parse(Instruccion):
    def __init__(self,tipo,exp, fila, columna):
        self.tipo = tipo
        self.expresion = exp
        self.fila = fila
        self.columna = columna
        self.struct = False
        self.mutable = False
    
    def compilar(self, arbol, tabla):
        
        resultadoExp = self.expresion.compilar(arbol,tabla)#veo que es la exp
        if isinstance(resultadoExp,Error): return resultadoExp
        
        genAux = Generador()
        generator = genAux.getInstance()
        
        if self.expresion.tipo != Tipo.CADENA:
            return Error("SEMANTICO", "UNICAMENTE SE CONVIERTEN CADENAS",self.fila,self.columna)

        if self.tipo == Tipo.ENTERO:    
            try:
                cadena = self.expresion
                prueba = int(cadena.valor)
                generator.toParseInt()
                paramtemp=generator.agregarTemporal();generator.liberarTemporal(paramtemp)#genero temproal
                
                #cambio de entorno simulado
                generator.addExp(paramtemp,'P',tabla.size,'+')
                generator.addExp(paramtemp,paramtemp,'1','+')
                #param1
                generator.setPila(paramtemp,resultadoExp.getValor())#pos cadena 1
                
                #cambio de entorno formal
                generator.newEnv(tabla.size)
                generator.llamandaFuncion('nativaToParseInt')
                
                #obtengo valor de retorno:
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.getPila(temp,'P')
                
                #regreso a entorno main
                generator.returnEntorno(tabla.size)
                
                return Return(temp,Tipo.ENTERO,True)
                #return int(self.getValor(self.expresion.tipo,resultadoExp))
            except:
                return Error("SEMANTICO","ESTA CADENA NO CONTIENE CARACTERES VALIDOS PARA CONVETIR A INT",self.fila,self.columna)
        
        if self.tipo == Tipo.DECIMAL:
            try:
                cadena = self.expresion
                prueba = float(cadena.valor)
                generator.toParseFloat()
                paramtemp=generator.agregarTemporal()#genero temproal
                
                #cambio de entorno simulado
                generator.addExp(paramtemp,'P',tabla.size,'+')
                generator.addExp(paramtemp,paramtemp,'1','+')
                #param1
                generator.setPila(paramtemp,resultadoExp.getValor())#pos cadena 1
                
                #cambio de entorno formal
                generator.newEnv(tabla.size)
                generator.llamandaFuncion('nativaToParseFloat')
                
                #obtengo valor de retorno:
                temp = generator.agregarTemporal()
                generator.getPila(temp,'P')
                
                #regreso a entorno main
                generator.returnEntorno(tabla.size)
                
                return Return(temp,Tipo.DECIMAL,True)
            except:
                return Error("SEMANTICO","ESTA CADENA NO CONTIENE CARACTERES VALIDOS PARA CONVERTIR A FLOAT",self.fila,self.columna)
        return Error("SEMANTICO","PARSE UNICAMENTE CONVERITE A INT64 Y FLOAT64",self.fila,self.columna)
    
    def getValor(self, tipo, val):
        if tipo == Tipo.ENTERO:
            return int(val)
        elif tipo == Tipo.DECIMAL:
            return float(val)
        elif tipo == Tipo.BOOLEANO:
            return bool(val)
        return str(val)
    
    def getNode(self):
        nodoPars = NodoArbol("PARSE") #NOMBRE PADRE
        nodoPars.agregarHijoSinNodo(str(self.tipo))
        nodoPars.agregarHijoConNodo(self.expresion.getNode())
        return nodoPars