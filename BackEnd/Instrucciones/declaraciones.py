from almacenar.generador import Generador
from padres.instruccion import Instruccion
from almacenar.error import Error
from almacenar.simbolo import Simbolo
from padres.Nodo import NodoArbol
from almacenar.tipo import Ambito,Tipo

#from padres.instruccion import Instruccion
#from almacenar.error import Error
#from almacenar.simbolo import Simbolo
#from padres.Nodo import NodoArbol
#from almacenar.tipo import Ambito,Tipo

class Declaracion(Instruccion): #LOCAL
    # ID = Expresión;
    # ID = Expresión ::TIPO;
    def __init__(self,identificador,exp,tipo, fila, columna):
        self.identificador = identificador
        self.exp = exp
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.arreglo=False
        self.struct=False
        self.mutable=False
    
    def compilar(self, arbol, tabla):
        #if self.exp
        genAux = Generador()
        generator = genAux.getInstance()
        generator.agregarComentario("VALOR QUE TOMARA VARIABLE")
        
        #VALOR QUE TOMARA LA VARIABLE
        resultadoExpresion = self.exp.compilar(arbol,tabla) #valor que recibe ID
        if isinstance(resultadoExpresion,Error): return resultadoExpresion
        
        generator.agregarComentario("FIN DE VALOR QUE TOMA VARIABLE")
        
        #nueva prueba->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
        #self.struct = self.exp.struct
        #self.mutable = self.exp.mutable
        #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
        
        
        #//////////////////////////////////////////////////////////////////////////////////               
        #//// SI AMBITO FUNCION ES FALSE LAS DECLARACIONES POR DEFAULT SERAN GLOBAL //////
        #////////////////////////////////////////////////////////////////////////////////
        if arbol.getValorAmbitoFuncion()==False: #AMBITO FUNCION ES FALSO
            #si tiene tipo se verifica que sea válido 
            if self.tipo != None:
                if self.tipo != self.exp.tipo and self.exp.tipo != Tipo.STRUCT:
                    return Error("SEMANTICO", 'Tipo de dato incorrecto en declaracion se esperaba '+str(self.tipo),self.fila,self.columna)
                else:
                    #nsimbolostruct = Simbolo()
                    ########################################->->->->->->->
                    if isinstance(resultadoExpresion,Simbolo) and self.exp.tipo == Tipo.STRUCT:
                        resultadoExpresion.id=self.identificador
                        resultadoExpresion.fil=self.fila
                        resultadoExpresion.col=self.columna
                        nsimbolocontipo=resultadoExpresion
                    else:
                    ########################################->->->->->->->
                    #if not isinstance(resultadoExpresion,list): self.tipo=self.getTipo(resultadoExpresion)
                        nsimbolocontipo = Simbolo(str(self.identificador),self.tipo,resultadoExpresion.valor,self.fila,self.columna,tabla.size,True,(self.tipo == Tipo.STRUCT or self.tipo == Tipo.CADENA),Ambito.GLOBAL,self.arreglo,self.struct,self.mutable) #si fuese global se busca unicamtente en getTsGLobal        
                    if tabla.tablaAnterior():
                        #busco en tabla actual 
                        #resul = tabla.actualizarTs(nsimbolocontipo)
                        resul = tabla.getSimboloEnTs(self.identificador)
                        if resul != None: #sino esta el simbolo en la tabla actual me voy al else
                            nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                            tempPos = nuevaVariable.posicion
                            if not nuevaVariable.esGlobal:
                                tempPos = generator.agregarTemporal();generator.liberarTemporal(tempPos)
                                generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                            
                            if self.tipo == Tipo.BOOLEANO:
                                tempLbl = generator.agregarLabel()
                                
                                generator.colocarLabel(resultadoExpresion.trueLbl)
                                generator.setPila(tempPos,"1")
                                
                                generator.agregarGoto(tempLbl)
                                
                                generator.colocarLabel(resultadoExpresion.falseLbl)
                                generator.setPila(tempPos,"0")
                                
                                generator.colocarLabel(tempLbl)
                            else:
                                generator.setPila(tempPos,resultadoExpresion.valor)
                                generator.agregarSalto()
                            return None
                        else:#y ya valido si existe
                            #resul = arbol.getTsGlobal().actualizarTs(nsimbolocontipo)
                            resul = arbol.getTsGlobal().getSimboloEnTs(self.identificador)
                            if resul == None:
                                declaracion = arbol.getTsGlobal().setSimboloEnTs(nsimbolocontipo)
                                if isinstance(declaracion,Error): return declaracion
                            
                            nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                            tempPos = nuevaVariable.posicion
                            if not nuevaVariable.esGlobal:
                                tempPos = generator.agregarTemporal();generator.liberarTemporal(tempPos)
                                generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                            
                            if self.tipo == Tipo.BOOLEANO:
                                tempLbl = generator.agregarLabel()
                                
                                generator.colocarLabel(resultadoExpresion.trueLbl)
                                generator.setPila(tempPos,"1")
                                
                                generator.agregarGoto(tempLbl)
                                
                                generator.colocarLabel(resultadoExpresion.falseLbl)
                                generator.setPila(tempPos,"0")
                                
                                generator.colocarLabel(tempLbl)
                            else:
                                generator.setPila(tempPos,resultadoExpresion.valor)
                                generator.agregarSalto()
                            
                            return None   
                        
                    else:                           
                    
                        #BUSCO EN LA TS SI EL AMBITO ES LOCAL SOLO SE BUSCA EN LA TABLA ACTUAL
                        #resul = arbol.getTsGlobal().actualizarTs(nsimbolocontipo)
                        resul = arbol.getTsGlobal().getSimboloEnTs(self.identificador)
                        if resul == None:
                            declaracion = arbol.getTsGlobal().setSimboloEnTs(nsimbolocontipo)
                            if isinstance(declaracion,Error): return declaracion
                        
                        nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                        tempPos = nuevaVariable.posicion
                        if not nuevaVariable.esGlobal:
                            tempPos = generator.agregarTemporal();generator.liberarTemporal(tempPos)
                            generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                        
                        if self.tipo == Tipo.BOOLEANO:
                            tempLbl = generator.agregarLabel()
                            
                            generator.colocarLabel(resultadoExpresion.trueLbl)
                            generator.setPila(tempPos,"1")
                            
                            generator.agregarGoto(tempLbl)
                            
                            generator.colocarLabel(resultadoExpresion.falseLbl)
                            generator.setPila(tempPos,"0")
                            
                            generator.colocarLabel(tempLbl)
                        else:
                            generator.setPila(tempPos,resultadoExpresion.valor)
                            generator.agregarSalto()
                        
                        return None
                        
            #de lo contrario se crea el simbolo sin tipo 
            #y se buscar si existe antes de crearlo en la tabla 
            # por que puede que sea solo una asignacion
            # y seria solo de actulizar el valor del ID
            #de lo contrario se agrega a la tabla de simbolos en el ambito correspondiente
            else:  
                if not isinstance(resultadoExpresion,list) and self.exp.tipo == Tipo.ARREGLO: self.exp.tipo=self.getTipo(resultadoExpresion)                      
                ########################################->->->->->->->
                if isinstance(resultadoExpresion,Simbolo) and self.exp.tipo == Tipo.STRUCT:
                    resultadoExpresion.id=self.identificador
                    resultadoExpresion.fil=self.fila
                    resultadoExpresion.col=self.columna
                    nsimbolosintipo=resultadoExpresion
                else:
                    ########################################->->->->->->->
                    nsimbolosintipo = Simbolo(str(self.identificador),self.exp.tipo,resultadoExpresion.valor,self.fila,self.columna,tabla.size,True,(self.exp.tipo == Tipo.STRUCT or self.exp.tipo == Tipo.CADENA),Ambito.GLOBAL,self.arreglo,self.struct,self.mutable) #CREO EL SIMBOLO
                    
                #BUSCO EN LA TS SI EL AMBITO ES LOCAL SOLO SE BUSCA EN LA TABLA ACTUAL
                if tabla.tablaAnterior():
                    #busco en tabla actual 
                    #resul = tabla.actualizarTs(nsimbolosintipo)
                    resul = tabla.getSimboloEnTs(self.identificador)
                    if resul != None: #sino esta el simbolo en la tabla actual me voy al else
                        nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                        tempPos = nuevaVariable.posicion
                        if not nuevaVariable.esGlobal:
                            tempPos = generator.agregarTemporal();generator.liberarTemporal(tempPos)
                            generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                        
                        #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                        self.tipo = self.exp.tipo
                        #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                        
                        if self.tipo == Tipo.BOOLEANO:
                            tempLbl = generator.agregarLabel()
                            
                            generator.colocarLabel(resultadoExpresion.trueLbl)
                            generator.setPila(tempPos,"1")
                            
                            generator.agregarGoto(tempLbl)
                            
                            generator.colocarLabel(resultadoExpresion.falseLbl)
                            generator.setPila(tempPos,"0")
                            
                            generator.colocarLabel(tempLbl)
                        else:
                            generator.setPila(tempPos,resultadoExpresion.valor)
                            generator.agregarSalto()
                        return None
                    else:
                        resul = tabla.getSimboloEnTs(self.identificador)
                        if resul == None:
                            declaracionn = arbol.getTsGlobal().setSimboloEnTs(nsimbolosintipo)
                            if isinstance(declaracionn,Error): return declaracionn
                        nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                        tempPos = nuevaVariable.posicion
                        if not nuevaVariable.esGlobal:
                            tempPos = generator.agregarTemporal();generator.liberarTemporal(tempPos)
                            generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                        
                        #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                        self.tipo = self.exp.tipo
                        #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                        
                        if self.tipo == Tipo.BOOLEANO:
                            tempLbl = generator.agregarLabel()
                            
                            generator.colocarLabel(resultadoExpresion.trueLbl)
                            generator.setPila(tempPos,"1")
                            
                            generator.agregarGoto(tempLbl)
                            
                            generator.colocarLabel(resultadoExpresion.falseLbl)
                            generator.setPila(tempPos,"0")
                            
                            generator.colocarLabel(tempLbl)
                        else:
                            generator.setPila(tempPos,resultadoExpresion.valor)
                            generator.agregarSalto()
                        return None
                
                else:
                    #resul = arbol.getTsGlobal().actualizarTs(nsimbolosintipo) 
                    resul = arbol.getTsGlobal().getSimboloEnTs(self.identificador)
                    if resul == None:
                        declaracionn = arbol.getTsGlobal().setSimboloEnTs(nsimbolosintipo)
                        if isinstance(declaracionn,Error): return declaracionn
                    
                    nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                    tempPos = nuevaVariable.posicion
                    if not nuevaVariable.esGlobal:
                        tempPos = generator.agregarTemporal();generator.liberarTemporal(tempPos)
                        generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                    
                    #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                    self.tipo = self.exp.tipo
                    #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                    
                    if self.tipo == Tipo.BOOLEANO:
                        tempLbl = generator.agregarLabel()
                        
                        generator.colocarLabel(resultadoExpresion.trueLbl)
                        generator.setPila(tempPos,"1")
                        
                        generator.agregarGoto(tempLbl)
                        
                        generator.colocarLabel(resultadoExpresion.falseLbl)
                        generator.setPila(tempPos,"0")
                        
                        generator.colocarLabel(tempLbl)
                    else:
                        generator.setPila(tempPos,resultadoExpresion.valor)
                        generator.agregarSalto()
                        
                    return None
        #//////////////////////////////////////////////////////////////////////////////////                
        #//// SI AMBITO FUNCION ES TRUE LAS DECLARACIONES POR DEFAULT SERAN LOCAL ////////
        #////////////////////////////////////////////////////////////////////////////////  
        else:#
            #si tiene tipo se verifica que sea válido 
            if self.tipo != None:
                if not isinstance(resultadoExpresion,list) and self.exp.tipo == Tipo.ARREGLO: self.exp.tipo=self.getTipo(resultadoExpresion)                      
                if self.tipo != self.exp.tipo and self.exp.tipo != Tipo.STRUCT:
                    return Error("SEMANTICO", 'Tipo de dato incorrecto en declaracion se esperaba '+str(self.tipo),self.fila,self.columna)
                else:
                     #nsimbolostruct = Simbolo()
                    ########################################->->->->->->->
                    if isinstance(resultadoExpresion,Simbolo) and self.exp.tipo == Tipo.STRUCT:
                        resultadoExpresion.id=self.identificador
                        resultadoExpresion.fil=self.fila
                        resultadoExpresion.col=self.columna
                        nsimbolocontipo=resultadoExpresion
                    else:
                    ########################################->->->->->->->
                        nsimbolocontipo = Simbolo(str(self.identificador),self.tipo,resultadoExpresion.valor,self.fila,self.columna,tabla.size,False,(self.tipo == Tipo.STRUCT or self.tipo == Tipo.CADENA),Ambito.LOCAL,self.arreglo,self.struct,self.mutable) #si fuese global se busca unicamtente en getTsGLobal        
                    if tabla.buscarEtiquetaGlobal(self.identificador)==False:
                        if tabla.tablaAnterior() and tabla.getTablaAnterior()!=arbol.getTsGlobal():
                            resul = tabla.getTsSinGLobal(self.identificador,arbol.getTsGlobal())
                            if resul != None:
                                nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                                tempPos = nuevaVariable.posicion
                                if not nuevaVariable.esGlobal:
                                    tempPos = generator.agregarTemporal();generator.liberarTemporal(tempPos)
                                    generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                            
                                if self.tipo == Tipo.BOOLEANO:
                                    tempLbl = generator.agregarLabel()
                                    
                                    generator.colocarLabel(resultadoExpresion.trueLbl)
                                    generator.setPila(tempPos,"1")
                                    
                                    generator.agregarGoto(tempLbl)
                                    
                                    generator.colocarLabel(resultadoExpresion.falseLbl)
                                    generator.setPila(tempPos,"0")
                                    
                                    generator.colocarLabel(tempLbl)
                                else:
                                    generator.setPila(tempPos,resultadoExpresion.valor)
                                    generator.agregarSalto()
                                return None
                            else:
                                resul = tabla.getTsLocal(self.identificador)
                                if resul == None:
                                    declaracion = tabla.setSimboloEnTs(nsimbolocontipo)
                                    if isinstance(declaracion,Error): return declaracion
                                    
                                nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                                tempPos = nuevaVariable.posicion
                                if not nuevaVariable.esGlobal:
                                    tempPos = generator.agregarTemporal()
                                    generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                                
                                if self.tipo == Tipo.BOOLEANO:
                                    tempLbl = generator.agregarLabel()
                                    
                                    generator.colocarLabel(resultadoExpresion.trueLbl)
                                    generator.setPila(tempPos,"1")
                                    
                                    generator.agregarGoto(tempLbl)
                                    
                                    generator.colocarLabel(resultadoExpresion.falseLbl)
                                    generator.setPila(tempPos,"0")
                                    
                                    generator.colocarLabel(tempLbl)
                                else:
                                    generator.setPila(tempPos,resultadoExpresion.valor)
                                    generator.agregarSalto()
                                
                                return None   
                        else:
                            resul = tabla.getTsLocal(self.identificador)
                            if resul == None:
                                declaracion = tabla.setSimboloEnTs(nsimbolocontipo)
                                if isinstance(declaracion,Error): return declaracion
                            nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                            tempPos = nuevaVariable.posicion
                            if not nuevaVariable.esGlobal:
                                tempPos = generator.agregarTemporal();generator.liberarTemporal(tempPos)
                                generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                            
                            if self.tipo == Tipo.BOOLEANO:
                                tempLbl = generator.agregarLabel()
                                
                                generator.colocarLabel(resultadoExpresion.trueLbl)
                                generator.setPila(tempPos,"1")
                                
                                generator.agregarGoto(tempLbl)
                                
                                generator.colocarLabel(resultadoExpresion.falseLbl)
                                generator.setPila(tempPos,"0")
                                
                                generator.colocarLabel(tempLbl)
                            else:
                                generator.setPila(tempPos,resultadoExpresion.valor)
                                generator.agregarSalto()
                            
                            return None
                    else:
                        nsimbolocontipo.esGlobal=True
                        resul = arbol.getTsGlobal().getSimboloEnTs(self.identificador)
                        if resul == None:
                            declaracion = arbol.getTsGlobal().setSimboloEnTs(nsimbolocontipo)
                            if isinstance(declaracion,Error): return declaracion
                        
                        nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                        tempPos = nuevaVariable.posicion
                        if not nuevaVariable.esGlobal:
                            tempPos = generator.agregarTemporal();generator.liberarTemporal(tempPos)
                            generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                        
                        if self.tipo == Tipo.BOOLEANO:
                            tempLbl = generator.agregarLabel()
                            
                            generator.colocarLabel(resultadoExpresion.trueLbl)
                            generator.setPila(tempPos,"1")
                            
                            generator.agregarGoto(tempLbl)
                            
                            generator.colocarLabel(resultadoExpresion.falseLbl)
                            generator.setPila(tempPos,"0")
                            
                            generator.colocarLabel(tempLbl)
                        else:
                            generator.setPila(tempPos,resultadoExpresion.valor)
                            generator.agregarSalto()
                        
                        return None
            else:
                if not isinstance(resultadoExpresion,list) and self.exp.tipo == Tipo.ARREGLO: self.exp.tipo=self.getTipo(resultadoExpresion)
                 #nsimbolostruct = Simbolo()
                ########################################->->->->->->->
                if isinstance(resultadoExpresion,Simbolo) and self.exp.tipo == Tipo.STRUCT:
                    resultadoExpresion.id=self.identificador
                    resultadoExpresion.fil=self.fila
                    resultadoExpresion.col=self.columna
                    nsimbolosintipo=resultadoExpresion
                else:
                    ########################################->->->->->->->
                    nsimbolosintipo = Simbolo(str(self.identificador),self.exp.tipo,resultadoExpresion.valor,self.fila,self.columna,tabla.size,False,(self.exp.tipo == Tipo.STRUCT or self.exp.tipo == Tipo.CADENA),Ambito.LOCAL,self.arreglo,self.struct,self.mutable) #CREO EL SIMBOLO
                if tabla.buscarEtiquetaGlobal(self.identificador)==False:
                    #BUSCO EN LA TS SI EL AMBITO ES LOCAL SOLO SE BUSCA EN LA TABLA ACTUAL
                    if tabla.tablaAnterior() and tabla.getTablaAnterior()!=arbol.getTsGlobal():
                        resul = tabla.getTsSinGLobal(self.identificador,arbol.getTsGlobal())
                        if resul != None:
                            nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                            tempPos = nuevaVariable.posicion
                            if not nuevaVariable.esGlobal:
                                tempPos = generator.agregarTemporal();generator.liberarTemporal(tempPos)
                                generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                        
                            #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                            self.tipo = self.exp.tipo
                            #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                            
                            if self.tipo == Tipo.BOOLEANO:
                                tempLbl = generator.agregarLabel()
                                
                                generator.colocarLabel(resultadoExpresion.trueLbl)
                                generator.setPila(tempPos,"1")
                                
                                generator.agregarGoto(tempLbl)
                                
                                generator.colocarLabel(resultadoExpresion.falseLbl)
                                generator.setPila(tempPos,"0")
                                
                                generator.colocarLabel(tempLbl)
                            else:
                                generator.setPila(tempPos,resultadoExpresion.valor)
                                generator.agregarSalto()
                            return None
                            
                        else:
                            resul = tabla.getTsLocal(self.identificador)
                            if resul == None:
                                declaracionn = tabla.setSimboloEnTs(nsimbolosintipo)
                                if isinstance(declaracionn,Error): return declaracionn
                            nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                            tempPos = nuevaVariable.posicion
                            if not nuevaVariable.esGlobal:
                                tempPos = generator.agregarTemporal();generator.liberarTemporal(tempPos)
                                generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                            
                            #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                            self.tipo = self.exp.tipo
                            #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                            
                            if self.tipo == Tipo.BOOLEANO:
                                tempLbl = generator.agregarLabel()
                                
                                generator.colocarLabel(resultadoExpresion.trueLbl)
                                generator.setPila(tempPos,"1")
                                
                                generator.agregarGoto(tempLbl)
                                
                                generator.colocarLabel(resultadoExpresion.falseLbl)
                                generator.setPila(tempPos,"0")
                                
                                generator.colocarLabel(tempLbl)
                            else:
                                generator.setPila(tempPos,resultadoExpresion.valor)
                                generator.agregarSalto()
                            return None
                            
                    else:
                        resul = tabla.getTsLocal(self.identificador)
                        if resul == None:
                            declaracionn = tabla.setSimboloEnTs(nsimbolosintipo)
                            if isinstance(declaracionn,Error): return declaracionn
                            
                        nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                        tempPos = nuevaVariable.posicion
                        if not nuevaVariable.esGlobal:
                            tempPos = generator.agregarTemporal();generator.liberarTemporal(tempPos)
                            generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                        
                        #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                        self.tipo = self.exp.tipo
                        #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                        
                        if self.tipo == Tipo.BOOLEANO:
                            tempLbl = generator.agregarLabel()
                            
                            generator.colocarLabel(resultadoExpresion.trueLbl)
                            generator.setPila(tempPos,"1")
                            
                            generator.agregarGoto(tempLbl)
                            
                            generator.colocarLabel(resultadoExpresion.falseLbl)
                            generator.setPila(tempPos,"0")
                            
                            generator.colocarLabel(tempLbl)
                        else:
                            generator.setPila(tempPos,resultadoExpresion.valor)
                            generator.agregarSalto()
                            
                        return None
                else:
                    nsimbolosintipo.esGlobal=True
                    resul = arbol.getTsGlobal().getSimboloEnTs(self.identificador)
                    if resul == None:
                        declaracion = arbol.getTsGlobal().setSimboloEnTs(nsimbolosintipo)
                        if isinstance(declaracion,Error): return declaracion
                    
                    nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                    tempPos = nuevaVariable.posicion
                    if not nuevaVariable.esGlobal:
                        tempPos = generator.agregarTemporal();generator.liberarTemporal(tempPos)
                        generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                    
                    #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                    self.tipo = self.exp.tipo
                    #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                    
                    if self.tipo == Tipo.BOOLEANO:
                        tempLbl = generator.agregarLabel()
                        
                        generator.colocarLabel(resultadoExpresion.trueLbl)
                        generator.setPila(tempPos,"1")
                        
                        generator.agregarGoto(tempLbl)
                        
                        generator.colocarLabel(resultadoExpresion.falseLbl)
                        generator.setPila(tempPos,"0")
                        
                        generator.colocarLabel(tempLbl)
                    else:
                        generator.setPila(tempPos,resultadoExpresion.valor)
                        generator.agregarSalto()
                        
                    return None
               
    def getNode(self):
        nodoDeclaracion = NodoArbol("DEC") #NOMBRE PADRE
        nodoDeclaracion.agregarHijoSinNodo(str(self.identificador))
        nodoDeclaracion.agregarHijoConNodo(self.exp.getNode())
        return nodoDeclaracion
    
    def getTipo(self, val):
        if isinstance(val,int):
            return Tipo.ENTERO
        elif isinstance(val,float):
            return Tipo.DECIMAL
        elif isinstance(val,bool):
            return Tipo.BOOLEANO
        return Tipo.CADENA

class DeclaracionLocal(Instruccion):
    # ID = Expresión;
    # ID = Expresión ::TIPO;
    def __init__(self,identificador,exp,tipo, fila, columna):
        self.identificador = identificador
        self.exp = exp
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.arreglo=False
        self.struct=False
        self.mutable=False
    
    def compilar(self, arbol, tabla):
        genAux = Generador()
        generator = genAux.getInstance()
        generator.agregarComentario("VALOR QUE TOMARA VARIABLE")
        
        resultadoExpresion = self.exp.compilar(arbol,tabla) #valor que recibe ID
        if isinstance(resultadoExpresion,Error): return resultadoExpresion
        
        generator.agregarComentario("FIN DE VALOR QUE TOMA VARIABLE")
        
        #si tiene tipo se verifica que sea válido
        if self.tipo != None:
            if self.tipo != self.exp.tipo:
                return Error("SEMANTICO", 'Tipo de dato incorrecto en declaracion se esperaba '+str(self.tipo),self.fila,self.columna)
            else:
                nsimbolocontipo = Simbolo(str(self.identificador),self.tipo,resultadoExpresion.valor,self.fila,self.columna,tabla.size,False,(self.tipo == Tipo.STRUCT or self.tipo == Tipo.CADENA),Ambito.LOCAL,self.arreglo,self.struct,self.mutable)
                
                if tabla.existeVariableLocalTsActual(self.identificador):
                    return Error("SEMANTICO", "VARIABLE LOCAL: "+ str(self.identificador)+" YA FUE DECLARADA",self.fila,self.columna)
                elif tabla.buscarEtiquetaGlobal(self.identificador):
                    return Error("SEMANTICO", "VARIABLE: "+str(self.identificador)+ " YA FUE DECLARADA COMO GLOBAL",self.fila,self.columna)
                else:    
                    declaracion = tabla.setSimboloEnTs(nsimbolocontipo)
                    if isinstance(declaracion,Error): return declaracion
                    tabla.setEtiquetaLocal(self.identificador)
                    
                    nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                    tempPos = nuevaVariable.posicion
                    if not nuevaVariable.esGlobal:
                        tempPos = generator.agregarTemporal()
                        generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                    
                    if self.tipo == Tipo.BOOLEANO:
                        tempLbl = generator.agregarLabel()
                        
                        generator.colocarLabel(resultadoExpresion.trueLbl)
                        generator.setPila(tempPos,"1")
                        
                        generator.agregarGoto(tempLbl)
                        
                        generator.colocarLabel(resultadoExpresion.falseLbl)
                        generator.setPila(tempPos,"0")
                        
                        generator.colocarLabel(tempLbl)
                    else:
                        generator.setPila(tempPos,resultadoExpresion.valor)
                        generator.agregarSalto()
                    
                    return None   

        #de lo contrario se crea el simbolo sin tipo 
        #y se buscar si existe antes de crearlo en la tabla 
        # por que puede que sea solo una asignacion
        # y seria solo de actulizar el valor del ID
        #de lo contrario se agrega a la tabla de simbolos en el ambito correspondiente
        else:
            if not isinstance(resultadoExpresion,list) and self.exp.tipo == Tipo.ARREGLO: self.exp.tipo=self.getTipo(resultadoExpresion)                      
            nsimbolosintipo = Simbolo(str(self.identificador),self.exp.tipo,resultadoExpresion.valor,self.fila,self.columna,tabla.size,False,(self.exp.tipo == Tipo.STRUCT or self.exp.tipo == Tipo.CADENA),Ambito.LOCAL,self.arreglo,self.struct,self.mutable) #CREO EL SIMBOLO
            
            
            if tabla.existeVariableLocalTsActual(self.identificador):
                return Error("SEMANTICO", "VARIABLE LOCAL: "+ str(self.identificador)+" YA FUE DECLARADA",self.fila,self.columna)
            elif tabla.buscarEtiquetaGlobal(self.identificador):
                return Error("SEMANTICO", "VARIABLE: "+str(self.identificador)+ " YA FUE DECLARADA COMO GLOBAL",self.fila,self.columna)
            else:
                declaracionn = tabla.setSimboloEnTs(nsimbolosintipo)
                if isinstance(declaracionn,Error): return declaracionn
                tabla.setEtiquetaLocal(self.identificador)
                
                nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                tempPos = nuevaVariable.posicion
                if not nuevaVariable.esGlobal:
                    tempPos = generator.agregarTemporal()
                    generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                
                if self.tipo == Tipo.BOOLEANO:
                    tempLbl = generator.agregarLabel()
                    
                    generator.colocarLabel(resultadoExpresion.trueLbl)
                    generator.setPila(tempPos,"1")
                    
                    generator.agregarGoto(tempLbl)
                    
                    generator.colocarLabel(resultadoExpresion.falseLbl)
                    generator.setPila(tempPos,"0")
                    
                    generator.colocarLabel(tempLbl)
                else:
                    generator.setPila(tempPos,resultadoExpresion.valor)
                    generator.agregarSalto()
                
                return None   
    
    def getNode(self):
        nodoDeclaracion = NodoArbol("DEC LOCAL") #NOMBRE PADRE
        nodoDeclaracion.agregarHijoSinNodo(str(self.identificador))
        nodoDeclaracion.agregarHijoConNodo(self.exp.getNode())
        return nodoDeclaracion
    
    def getTipo(self, val):
        if isinstance(val,int):
            return Tipo.ENTERO
        elif isinstance(val,float):
            return Tipo.DECIMAL
        elif isinstance(val,bool):
            return Tipo.BOOLEANO
        return Tipo.CADENA
    
                 
        
class DeclaracionLocalSinValor(Instruccion):
    # ID = Expresión;
    # ID = Expresión ::TIPO;
    def __init__(self,identificador,fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna
        self.arreglo=False
        self.struct=False
        self.mutable=False
    
    def compilar(self, arbol, tabla):
        nsimbolosintipo = Simbolo(str(self.identificador),Tipo.NULO,None,self.fila,self.columna,Ambito.LOCAL,self.arreglo,self.struct,self.mutable) #CREO EL SIMBOLO
        if tabla.existeVariableLocalTsActual(self.identificador):
            return Error("SEMANTICO", "VARIABLE LOCAL: "+ str(self.identificador)+" YA FUE DECLARADA",self.fila,self.columna)
        elif tabla.buscarEtiquetaGlobal(self.identificador):
            return Error("SEMANTICO", "VARIABLE: "+str(self.identificador)+ " YA FUE DECLARADA COMO GLOBAL",self.fila,self.columna)
            
        else:  
            declaracionn = tabla.setSimboloEnTs(nsimbolosintipo)
            if isinstance(declaracionn,Error): return declaracionn
            tabla.setEtiquetaLocal(self.identificador)
            return None
    
    def getNode(self):
        nodoDeclaracion = NodoArbol("DEC LOCAL") #NOMBRE PADRE
        nodoDeclaracion.agregarHijoSinNodo(str(self.identificador))
        nodoDeclaracion.agregarHijoSinNodo("Tipo.Nulo")
        return nodoDeclaracion
    
        

class DeclaracionGlobal(Instruccion):
    def __init__(self,identificador,exp,tipo, fila, columna):
        self.identificador = identificador
        self.exp = exp
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.arreglo=False
        self.struct=False
        self.mutable=False
        
    def compilar(self, arbol, tabla):
        genAux = Generador()
        generator = genAux.getInstance()
        generator.agregarComentario("VALOR QUE TOMARA VARIABLE")
        
        resultadoExpresion = self.exp.compilar(arbol,tabla) #valor que recibe ID
        if isinstance(resultadoExpresion,Error): return resultadoExpresion
        
        generator.agregarComentario("FIN DE VALOR QUE TOMA VARIABLE")
        #si tiene tipo se verifica que sea válido
        if self.tipo != None:
            if self.tipo != self.exp.tipo:
                return Error("SEMANTICO", 'Tipo de dato incorrecto en declaracion se esperaba '+str(self.tipo),self.fila,self.columna)
            else:
                if tabla.buscarEtiquetaLocal(self.identificador):
                    return Error("SEMANTICO","VARIABLE: "+str(self.identificador)+" YA FUE DECLARADA COMO LOCAL",self.fila,self.columna)
                else:             
                    nsimbolocontipo = Simbolo(str(self.identificador),self.tipo,resultadoExpresion.valor,self.fila,self.columna,tabla.size,True,(self.tipo == Tipo.STRUCT or self.tipo == Tipo.CADENA),Ambito.GLOBAL,self.arreglo,self.struct,self.mutable) #si fuese global se busca unicamtente en getTsGLobal
                            
                    resul = arbol.getTsGlobal().getTsLocal(self.identificador)
                    tabla.setEtiquetaGlobal(self.identificador)
                    if resul == None:
                        declaracion = arbol.getTsGlobal().setSimboloEnTs(nsimbolocontipo)
                        if isinstance(declaracion,Error): return declaracion
                        
                    nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                    tempPos = nuevaVariable.posicion
                    if not nuevaVariable.esGlobal:
                        tempPos = generator.agregarTemporal()
                        generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                    
                    if self.tipo == Tipo.BOOLEANO:
                        tempLbl = generator.agregarLabel()
                        
                        generator.colocarLabel(resultadoExpresion.trueLbl)
                        generator.setPila(tempPos,"1")
                        
                        generator.agregarGoto(tempLbl)
                        
                        generator.colocarLabel(resultadoExpresion.falseLbl)
                        generator.setPila(tempPos,"0")
                        
                        generator.colocarLabel(tempLbl)
                    else:
                        generator.setPila(tempPos,resultadoExpresion.valor)
                        generator.agregarSalto()
                    
                    return None 
        
        else:
            if tabla.buscarEtiquetaLocal(self.identificador):
                return Error("SEMANTICO","VARIABLE: "+str(self.identificador)+" YA FUE DECLARADA COMO LOCAL",self.fila,self.columna)
            else:
                if not isinstance(resultadoExpresion,list) and self.exp.tipo == Tipo.ARREGLO: self.exp.tipo=self.getTipo(resultadoExpresion)                      
                nsimbolosintipo = Simbolo(str(self.identificador),self.exp.tipo,resultadoExpresion.valor,self.fila,self.columna,tabla.size,True,(self.exp.tipo == Tipo.STRUCT or self.exp.tipo == Tipo.CADENA),Ambito.GLOBAL,self.arreglo,self.struct,self.mutable) #CREO EL SIMBOLO
                
                #BUSCO EN LA TS SI EL AMBITO ES LOCAL SOLO SE BUSCA EN LA TABLA ACTUAL
                resul = arbol.getTsGlobal().getTsLocal(self.identificador)
                tabla.setEtiquetaGlobal(self.identificador)
                if resul == None:
                    declaracion = arbol.getTsGlobal().setSimboloEnTs(nsimbolosintipo)
                    if isinstance(declaracion,Error): return declaracion
                
                nuevaVariable = tabla.getSimboloEnTs(self.identificador)
                tempPos = nuevaVariable.posicion
                if not nuevaVariable.esGlobal:
                    tempPos = generator.agregarTemporal()
                    generator.addExp(tempPos,'P',nuevaVariable.posicion,"+")
                
                #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                self.tipo = self.exp.tipo
                #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                
                if self.tipo == Tipo.BOOLEANO:
                    tempLbl = generator.agregarLabel()
                    
                    generator.colocarLabel(resultadoExpresion.trueLbl)
                    generator.setPila(tempPos,"1")
                    
                    generator.agregarGoto(tempLbl)
                    
                    generator.colocarLabel(resultadoExpresion.falseLbl)
                    generator.setPila(tempPos,"0")
                    
                    generator.colocarLabel(tempLbl)
                else:
                    generator.setPila(tempPos,resultadoExpresion.valor)
                    generator.agregarSalto()
                return None

    def getNode(self):
        nodoDeclaracion = NodoArbol("DEC GLOBAL") #NOMBRE PADRE
        nodoDeclaracion.agregarHijoSinNodo(str(self.identificador))
        nodoDeclaracion.agregarHijoConNodo(self.exp.getNode())
        return nodoDeclaracion
    
    def getTipo(self, val):
        if isinstance(val,int):
            return Tipo.ENTERO
        elif isinstance(val,float):
            return Tipo.DECIMAL
        elif isinstance(val,bool):
            return Tipo.BOOLEANO
        return Tipo.CADENA
    


class DeclaracionGlobalSinValor(Instruccion):
    # ID = Expresión;
    # ID = Expresión ::TIPO;
    def __init__(self,identificador,fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna
    
    def compilar(self, arbol, tabla):
        if tabla.buscarEtiquetaGlobal(self.identificador):
            return Error("SEMANTICO", "VARIABLE: "+str(self.identificador)+ " YA FUE DECLARADA COMO GLOBAL",self.fila,self.columna)
            
        else:
            tabla.setEtiquetaGlobal(self.identificador)
            return None
    
    def getNode(self):
        nodoDeclaracion = NodoArbol("DEC GLOBAL") #NOMBRE PADRE
        nodoDeclaracion.agregarHijoSinNodo(str(self.identificador))
        return nodoDeclaracion