from almacenar.generador import Generador
from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol
from almacenar.error import Error
from almacenar.tipo import Tipo
from almacenar.ts import TablaSimbolos
from instrucciones.breeak import Break
from instrucciones.continuar import Continue
from instrucciones.retorn import Retorno

#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol
#from almacenar.error import Error
#from almacenar.tipo import Tipo
#from almacenar.ts import TablaSimbolos
#from instrucciones.breeak import Break
#from instrucciones.continuar import Continue
#from instrucciones.retorn import Retorno

class InstrSi(Instruccion):
    #def __init__(self,exp, Ifinstrs,ElsInst,ElsIfinstr,fila, columna):
    def __init__(self,exp,instrucciones,instruccioneselse, fila, columna):
        self.condicion = exp
        self.insIF = instrucciones
        self.insElsif=instruccioneselse
        #self.insIF = Ifinstrs
        #self.insEls = ElsInst
        #self.insElsif = ElsIfinstr
        self.fila = fila
        self.columna = columna
        self.exitIf=''
        
    def compilar(self, arbol, tabla):
        genAux = Generador()
        generador = genAux.getInstance()
        
        generador.agregarComentario("INSTRUCCION IF")
        
        ResCond = self.condicion.compilar(arbol,tabla) #devuelve el valor de cualquier exp 
        if isinstance(ResCond,Error): return ResCond #por si retorna un error
        
        
        #para poder ingresar a el cuerpo de un if, lo que debe 
        #retornar la EXP es un booleano
        #de lo contrario seria un error y no 
        #se deberia ingresar al IF
        if self.condicion.tipo == Tipo.BOOLEANO:
            #IF
            #if bool(ResCond) == True: #si la condicion fue TRUE
                tablaIF = TablaSimbolos(tabla) #AMBITO IF
                tablaIF.setTsAnterior(tabla) #ENLAZO TABLA ANTERIOR
                arbol.agregarAListaTablas('IF',    tablaIF)#aqui agrego la tabla generada 
                generador.colocarLabel(ResCond.trueLbl)
                
                                         #ambito #tabla del ambito
                
                
                for instruccion in self.insIF: #este trae todas las instrucciones contenidas en el cuerpo del if
                    cuerpoIf = instruccion.compilar(arbol,tablaIF)
                    if isinstance(cuerpoIf,Error):
                        arbol.getListaErrores().append(cuerpoIf)
                        arbol.actualizarConsola(cuerpoIf.toString())
                    #if isinstance(cuerpoIf,Break): return cuerpoIf #sale con break dentro de ciclo que venga como instruccion
                    #if isinstance(cuerpoIf,Continue): return cuerpoIf
                    #if isinstance(cuerpoIf,Retorno): return cuerpoIf
                if self.insElsif != None:
                    self.exitIf = generador.agregarLabel()
                    generador.agregarGoto(self.exitIf) 
                        
                generador.colocarLabel(ResCond.falseLbl)               
                
                if self.insElsif != None:
                    if isinstance(self.insElsif,InstrSi):
                        self.insElsif.compilar(arbol,tabla)
                    else:
                        for instruccion in self.insElsif: #este trae todas las instrucciones contenidas en el cuerpo del if
                            cuerpoIf = instruccion.compilar(arbol,tablaIF)
                            if isinstance(cuerpoIf,Error):
                                arbol.getListaErrores().append(cuerpoIf)
                                arbol.actualizarConsola(cuerpoIf.toString())
                    generador.colocarLabel(self.exitIf)
            
            ##else:
            #    #ELSE
            #    if self.insEls != None:
            #        tablaElse = TablaSimbolos(tabla) #AMBITO ELSE
            #        tablaElse.setTsAnterior(tabla) #ENLAZO TABLA ANTERIOR
            #        
            #        arbol.agregarAListaTablas('ELSE', tablaElse)#aqui agrego la tabla generada 
            #        for instruccion in self.insEls: 
            #            cuerpoelse = instruccion.compilar(arbol,tablaElse)
            #            if isinstance(cuerpoelse,Error):
            #                arbol.getListaErrores().append(cuerpoelse)
            #                arbol.actualizarConsola(cuerpoelse.toString())
            #            if isinstance(cuerpoelse,Break): return cuerpoelse #sale con break dentro de ciclo que venga como instruccion
            #            if isinstance(cuerpoelse,Continue): return cuerpoelse
            #            if isinstance(cuerpoelse,Retorno): return cuerpoelse
            #        generador.colocarLabel(self.exitIf)####
                
                        
                
                    
                    #if isinstance(cuerpoelseif,Error): return cuerpoelseif
                    #if isinstance(cuerpoelseif,Break): return cuerpoelseif #sale con break dentro de ciclo que venga como instruccion
                    #if isinstance(cuerpoelseif,Continue): return cuerpoelseif
                    #if isinstance(cuerpoelseif,Retorno): return cuerpoelseif
        else:
            return Error("SEMANTICO", "Tipo de dato obtenido en condicion es incorrecto en IF",self.fila,self.columna)    
        
    def getNode(self):
        nodoimprimir = NodoArbol("IF") #NOMBRE PADRE

        return nodoimprimir