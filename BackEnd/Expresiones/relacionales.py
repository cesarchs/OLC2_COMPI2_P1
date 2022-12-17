
from almacenar.tipo import Return
from almacenar.generador import Generador
from padres.Nodo import NodoArbol
from padres.expresion import Expresion
from almacenar.error import Error
from almacenar.tipo import Tipo,OpsRelacional

#from padres.Nodo import NodoArbol
#from padres.instruccion import Instruccion
#from almacenar.error import Error
#from almacenar.tipo import Tipo,OpsRelacional

class Relacion(Expresion):
    def __init__(self, operador, operacionI, operacionD, fil, col):
        super().__init__(fil, col)
        self.operador = operador
        self.operacionI = operacionI
        self.operacionD = operacionD #si fuera unaria esta seria None
        self.fila = fil
        self.columna = col
        self.tipo = Tipo.BOOLEANO #se definira deendiendo de la operación
        self.struct = False
        self.mutable = False
        
    def compilar(self, arbol, tabla):
        'resisq = resultado opE izquierda, resder = resultado opE derecha'
        genAux = Generador()
        generator = genAux.getInstance()
        
        generator.agregarComentario("INICIO EXPRESION RELACIONAL")
        
        resizq = self.operacionI.compilar(arbol,tabla)
        if isinstance(resizq,Error): return resizq #ya no se sigue y se retorna el error almacenado en resizq
        resder = None
        #resder = self.operacionD.compilar(arbol,tabla)
        #if isinstance(resder,Error): return resder
        #
        if self.operacionI.tipo == Tipo.ARREGLO: self.operacionI.tipo = self.getTipo(resizq)
        #if self.operacionD.tipo == Tipo.ARREGLO: self.operacionD.tipo = self.getTipo(resder)
        
        #si resizq es de tipo struct hacer esta validacion: resizq[self.operacionI.idatributo]['getValor()'] != resder
        # resder puede ser struct tambien entonces la validaciones para ambos
        
               
        
        # OPE1 > OPE2 
        if self.operador == OpsRelacional.MAYORQ: 
            resder = self.operacionD.compilar(arbol,tabla)
            if isinstance(resder,Error): return resder  
            #Int64 > Int64
            if self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.ENTERO:  
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'>',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
                #return self.getValor(self.operacionI.tipo,resizq) > self.getValor(self.operacionD.tipo,resder)
            #Float64 > Int64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.ENTERO:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'>',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Float64 > Float64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.DECIMAL:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'>',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Int64 > Float64
            elif self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.DECIMAL:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'>',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            elif self.operacionI.tipo == Tipo.CADENA and self.operacionD.tipo== Tipo.CADENA:    
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder   
                generator.mayorquestr()
                paramtemp=generator.agregarTemporal();generator.liberarTemporal(paramtemp)#genero temproal
                
                #cambio de entorno simulado
                generator.addExp(paramtemp,'P',tabla.size,'+')
                generator.addExp(paramtemp,paramtemp,'1','+')
                #param1
                generator.setPila(paramtemp,resizq.getValor())#pos cadena 1
                generator.addExp(paramtemp,paramtemp,'1','+')
                #param2
                generator.setPila(paramtemp,resder.getValor())#pos cadena 2
                
                #cambio de entorno formal
                generator.newEnv(tabla.size)
                generator.llamandaFuncion('nativaCadenaMayorQue')
                
                #obtengo valor de retorno:
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.getPila(temp,'P')
                
                #regreso a entorno main
                generator.returnEntorno(tabla.size)
                
                
                self.checkLabels()
                generator.agregarIf(temp,"1","==",self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return("",self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r

            return Error("Semantico", "Este tipo de operacion en '>' no es admitivido.", self.fila, self.columna)
        
        # OPE1 < OPE2  
        elif self.operador == OpsRelacional.MENORQ: 
            resder = self.operacionD.compilar(arbol,tabla)
            if isinstance(resder,Error): return resder
            #Int64 < Int64
            if self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.ENTERO:
                    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'<',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Float64 < Int64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.ENTERO:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'<',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Float64 < Float64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.DECIMAL:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'<',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Int64 < Float64
            elif self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.DECIMAL:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'<',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            elif self.operacionI.tipo == Tipo.CADENA and self.operacionD.tipo== Tipo.CADENA:    
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder   
                generator.menorquestr()
                paramtemp=generator.agregarTemporal();generator.liberarTemporal(paramtemp)#genero temproal
                
                #cambio de entorno simulado
                generator.addExp(paramtemp,'P',tabla.size,'+')
                generator.addExp(paramtemp,paramtemp,'1','+')
                #param1
                generator.setPila(paramtemp,resizq.getValor())#pos cadena 1
                generator.addExp(paramtemp,paramtemp,'1','+')
                #param2
                generator.setPila(paramtemp,resder.getValor())#pos cadena 2
                
                #cambio de entorno formal
                generator.newEnv(tabla.size)
                generator.llamandaFuncion('nativaCadenaMenorQue')
                
                #obtengo valor de retorno:
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.getPila(temp,'P')
                
                #regreso a entorno main
                generator.returnEntorno(tabla.size)
                
                
                self.checkLabels()
                generator.agregarIf(temp,"1","==",self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return("",self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            return Error("Semantico", "Este tipo de operacion en '<' no es admitivido.", self.fila, self.columna)
    
        # OPE1 >= OPE2  
        elif self.operador == OpsRelacional.MAYORIGUALQ: 
            resder = self.operacionD.compilar(arbol,tabla)
            if isinstance(resder,Error): return resder
            #Int64 >= Int64
            if self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.ENTERO:
                    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'>=',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Float64 >= Int64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.ENTERO:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'>=',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Float64 >= Float64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.DECIMAL:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'>=',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Int64 >= Float64
            elif self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.DECIMAL:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'>=',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #cadena >= cadena
            elif self.operacionI.tipo == Tipo.CADENA and self.operacionD.tipo== Tipo.CADENA:    
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder   
                generator.mayorigualquestr()
                paramtemp=generator.agregarTemporal();generator.liberarTemporal(paramtemp)#genero temproal
                
                #cambio de entorno simulado
                generator.addExp(paramtemp,'P',tabla.size,'+')
                generator.addExp(paramtemp,paramtemp,'1','+')
                #param1
                generator.setPila(paramtemp,resizq.getValor())#pos cadena 1
                generator.addExp(paramtemp,paramtemp,'1','+')
                #param2
                generator.setPila(paramtemp,resder.getValor())#pos cadena 2
                
                #cambio de entorno formal
                generator.newEnv(tabla.size)
                generator.llamandaFuncion('nativaCadenaMayorIgualQue')
                
                #obtengo valor de retorno:
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.getPila(temp,'P')
                
                #regreso a entorno main
                generator.returnEntorno(tabla.size)
                
                
                self.checkLabels()
                generator.agregarIf(temp,"1","==",self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return("",self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            return Error("Semantico", "Este tipo de operacion en '>=' no es admitivido.", self.fila, self.columna)
    
        # OPE1 <= OPE2  
        elif self.operador == OpsRelacional.MENORIGUALQ: 
            resder = self.operacionD.compilar(arbol,tabla)
            if isinstance(resder,Error): return resder 
            #Int64 <= Int64
            if self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.ENTERO:
                   
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'<=',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Float64 <= Int64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.ENTERO:
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'<=',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Float64 <= Float64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.DECIMAL:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'<=',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Int64 <= Float64
            elif self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.DECIMAL:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'<=',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            elif self.operacionI.tipo == Tipo.CADENA and self.operacionD.tipo== Tipo.CADENA:    
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder   
                generator.menorigualquestr()
                paramtemp=generator.agregarTemporal();generator.liberarTemporal(paramtemp)#genero temproal
                
                #cambio de entorno simulado
                generator.addExp(paramtemp,'P',tabla.size,'+')
                generator.addExp(paramtemp,paramtemp,'1','+')
                #param1
                generator.setPila(paramtemp,resizq.getValor())#pos cadena 1
                generator.addExp(paramtemp,paramtemp,'1','+')
                #param2
                generator.setPila(paramtemp,resder.getValor())#pos cadena 2
                
                #cambio de entorno formal
                generator.newEnv(tabla.size)
                generator.llamandaFuncion('nativaCadenaMenorIgualQue')
                
                #obtengo valor de retorno:
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.getPila(temp,'P')
                
                #regreso a entorno main
                generator.returnEntorno(tabla.size)
                
                
                self.checkLabels()
                generator.agregarIf(temp,"1","==",self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return("",self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            return Error("Semantico", "Este tipo de operacion en '<=' no es admitivido.", self.fila, self.columna)
        
        # OPE1 == OPE2  
        elif self.operador == OpsRelacional.IGUALQ: 
            if self.operacionI.tipo != Tipo.BOOLEANO:
                resder = self.operacionD.compilar(arbol,tabla)
                if isinstance(resder,Error): return resder    
            #Int64 == Int64
            if self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.ENTERO:
                
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'==',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Float64 == Int64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.ENTERO:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'==',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Float64 == Float64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.DECIMAL:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'==',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Int64 == Float64
            elif self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.DECIMAL:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'==',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #string == string
            elif self.operacionI.tipo == Tipo.CADENA and self.operacionD.tipo== Tipo.CADENA:    
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder   
                generator.igualquestr()
                paramtemp=generator.agregarTemporal();generator.liberarTemporal(paramtemp)#genero temproal
                
                #cambio de entorno simulado
                generator.addExp(paramtemp,'P',tabla.size,'+')
                generator.addExp(paramtemp,paramtemp,'1','+')
                #param1
                generator.setPila(paramtemp,resizq.getValor())#pos cadena 1
                generator.addExp(paramtemp,paramtemp,'1','+')
                #param2
                generator.setPila(paramtemp,resder.getValor())#pos cadena 2
                
                #cambio de entorno formal
                generator.newEnv(tabla.size)
                generator.llamandaFuncion('nativaIgualQue')
                
                #obtengo valor de retorno:
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.getPila(temp,'P')
                
                #regreso a entorno main
                generator.returnEntorno(tabla.size)
                
                
                self.checkLabels()
                generator.agregarIf(temp,"1","==",self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return("",self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #boolean == boolean
            elif self.operacionI.tipo == Tipo.BOOLEANO:    
                gotoRight = generator.agregarLabel()
                leftTemp = generator.agregarTemporal();generator.liberarTemporal(leftTemp)
                
                generator.colocarLabel(resizq.trueLbl)
                generator.addExp(leftTemp,'1','','')
                generator.agregarGoto(gotoRight)
                
                generator.colocarLabel(resizq.falseLbl)
                generator.addExp(leftTemp,'0','','')    
                            
                generator.colocarLabel(gotoRight)
                
                ###################derecha#########################
                resder = self.operacionD.compilar(arbol,tabla)
                if isinstance(resder,Error): return resder
                if self.operacionD.tipo == Tipo.BOOLEANO:  
                    
                    gotoEnd = generator.agregarLabel()
                    rightTemp = generator.agregarTemporal();generator.liberarTemporal(rightTemp)

                    generator.colocarLabel(resder.trueLbl)

                    generator.addExp(rightTemp,'1','','')
                    generator.agregarGoto(gotoEnd)

                    generator.colocarLabel(resder.falseLbl)
                    generator.addExp(rightTemp,'0','','')

                    generator.colocarLabel(gotoEnd)

                    ###################################################
                    self.checkLabels()
                    generator.agregarIf(leftTemp,rightTemp,'==',self.trueLbl)
                    generator.agregarGoto(self.falseLbl)

                    r=Return("",self.tipo,False)
                    r.trueLbl=self.trueLbl
                    r.falseLbl=self.falseLbl
                    return r
                
                
            return Error("Semantico", "Este tipo de operacion en '==' no es admitivido.", self.fila, self.columna)
            
        
        # OPE1 != OPE2  
        elif self.operador == OpsRelacional.DIFERENTE: 
            if self.operacionI.tipo != Tipo.BOOLEANO:
                resder = self.operacionD.compilar(arbol,tabla)
                if isinstance(resder,Error): return resder  
            #Int64 != Int64
            if self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.ENTERO:#8!=5
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'!=',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Float64 != Int64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.ENTERO:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'!=',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Float64 != Float64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.DECIMAL:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'!=',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            #Int64 != Float64
            elif self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.DECIMAL:
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder    
                self.checkLabels()
                generator.agregarIf(resizq.getValor(),resder.getValor(),'!=',self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return(None,self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r
            elif self.operacionI.tipo == Tipo.CADENA and self.operacionD.tipo== Tipo.CADENA:   
                #resder = self.operacionD.compilar(arbol,tabla)
                #if isinstance(resder,Error): return resder   
                generator.diferentequestr()
                paramtemp=generator.agregarTemporal();generator.liberarTemporal(paramtemp)#genero temproal
                
                #cambio de entorno simulado
                generator.addExp(paramtemp,'P',tabla.size,'+')
                generator.addExp(paramtemp,paramtemp,'1','+')
                #param1
                generator.setPila(paramtemp,resizq.getValor())#pos cadena 1
                generator.addExp(paramtemp,paramtemp,'1','+')
                #param2
                generator.setPila(paramtemp,resder.getValor())#pos cadena 2
                
                #cambio de entorno formal
                generator.newEnv(tabla.size)
                generator.llamandaFuncion('nativaDiferenteQue')
                
                #obtengo valor de retorno:
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.getPila(temp,'P')
                
                #regreso a entorno main
                generator.returnEntorno(tabla.size)
                
                
                self.checkLabels()
                generator.agregarIf(temp,"1","==",self.trueLbl)
                generator.agregarGoto(self.falseLbl)
                r=Return("",self.tipo,False)
                r.trueLbl=self.trueLbl
                r.falseLbl=self.falseLbl
                return r 
            #boolean != boolean
            elif self.operacionI.tipo == Tipo.BOOLEANO and self.operacionD.tipo== Tipo.BOOLEANO:    
                gotoRight = generator.agregarLabel()
                leftTemp = generator.agregarTemporal();generator.liberarTemporal(leftTemp)
                
                generator.colocarLabel(resizq.trueLbl)
                generator.addExp(leftTemp,'1','','')
                generator.agregarGoto(gotoRight)
                
                generator.colocarLabel(resizq.falseLbl)
                generator.addExp(leftTemp,'0','','')    
                            
                generator.colocarLabel(gotoRight)
                
                ###################derecha#########################
                resder = self.operacionD.compilar(arbol,tabla)
                if isinstance(resder,Error): return resder
                if self.operacionD.tipo == Tipo.BOOLEANO:  
                    
                    gotoEnd = generator.agregarLabel()
                    rightTemp = generator.agregarTemporal();generator.liberarTemporal(rightTemp)

                    generator.colocarLabel(resder.trueLbl)

                    generator.addExp(rightTemp,'1','','')
                    generator.agregarGoto(gotoEnd)

                    generator.colocarLabel(resder.falseLbl)
                    generator.addExp(rightTemp,'0','','')

                    generator.colocarLabel(gotoEnd)

                    ###################################################
                    self.checkLabels()
                    generator.agregarIf(leftTemp,rightTemp,'!=',self.trueLbl)
                    generator.agregarGoto(self.falseLbl)

                    r=Return("",self.tipo,False)
                    r.trueLbl=self.trueLbl
                    r.falseLbl=self.falseLbl
                    return r
            elif self.operacionI.tipo == Tipo.NULO and self.operacionD.tipo ==Tipo.NULO:
                return resizq != resder
            elif self.operacionI.tipo == Tipo.STRUCT and self.operacionD.tipo ==Tipo.NULO:
                return resizq != resder
            elif self.operacionI.tipo == Tipo.NULO and self.operacionD.tipo ==Tipo.STRUCT:
                return resizq != resder
            #aqui podria ir una validacion de resqizq y resder
            return Error("Semantico", "Este tipo de operacion en '!=' no es admitivido.", self.fila, self.columna)
        

    def getTipo(self, val):
        if isinstance(val,int):
            return Tipo.ENTERO
        elif isinstance(val,float):
            return Tipo.DECIMAL
        elif isinstance(val,bool):
            return Tipo.BOOLEANO
        return Tipo.CADENA

    def checkLabels(self):
        genAux = Generador()
        generator = genAux.getInstance()
        if self.trueLbl == '':
            self.trueLbl = generator.agregarLabel()
        if self.falseLbl == '':
            self.falseLbl = generator.agregarLabel()
    
    def getValor(self, tipo, val):
        if tipo == Tipo.ENTERO:
            return int(val)
        elif tipo == Tipo.DECIMAL:
            return float(val)
        elif tipo == Tipo.BOOLEANO:
            return bool(val)
        return str(val)
    
    def getNode(self):
        nodoRelacional = NodoArbol("REL") #NOMBRE PADRE
        #binarias

        nodoRelacional.agregarHijoConNodo(self.operacionI.getNode()) #valor = trae un Nodo Primitivo por eso es con Nodo
        nodoRelacional.agregarHijoSinNodo(str(self.operador)) 
        nodoRelacional.agregarHijoConNodo(self.operacionD.getNode()) #valor = trae un Nodo Primitivo por eso es con Nodo
        
        return nodoRelacional