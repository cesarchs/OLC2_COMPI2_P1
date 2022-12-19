from werkzeug.datastructures import FileStorage
from Expresiones.aritmeticas import Aritmetica
from Expresiones.ids import Identificador
from Expresiones.primitivos import Primitivo
from Expresiones.relacionales import Relacion
from Nativas.stringgg import Stringgss
from almacenar.generador import Generador
from instrucciones.declaraciones import Declaracion
from padres.instruccion import Instruccion
from almacenar.error import Error
from almacenar.ts import TablaSimbolos
from instrucciones.breeak import Break
from instrucciones.continuar import Continue
from padres.Nodo import NodoArbol
from almacenar.simbolo import Simbolo
from almacenar.tipo import OpsAritmetico, Return, Tipo,Ambito,OpsRelacional
from instrucciones.retorn import Error
from instrucciones.retorn import Retorno

#from copy import deepcopy
#from padres.instruccion import Instruccion
#from almacenar.error import Error
#from almacenar.ts import TablaSimbolos
#from instrucciones.breeak import Break
#from instrucciones.continuar import Continue
#from padres.Nodo import NodoArbol
#from almacenar.simbolo import Simbolo
#from almacenar.tipo import Tipo,Ambito
#from instrucciones.retorn import Error
#from instrucciones.retorn import Retorno

class Para(Instruccion):
    def __init__(self,id,exp,instrcs ,fila, columna):
        self.id = id
        self.exp = exp
        self.instrucciones = instrcs
        self.fila = fila
        self.columna = columna
        self.arreglo=False
        self.struct=False
        self.mutable=False
        self.etiquetaverdadero=''
        self.etiquetafalso=''
    
    def compilar(self, arbol, tabla):
        
        genAux = Generador()
        generador = genAux.getInstance()
        
        expr= self.exp.compilar(arbol,tabla)
        if isinstance(expr,Error): return expr
        
        forTabla = TablaSimbolos(tabla)
        forTabla.setTsAnterior(tabla)
        arbol.agregarAListaTablas('FOR',forTabla)#aqui agrego la tabla
        if arbol.getValorAmbitoFuncion() == False: arbol.setValorAmbitoFuncion(True)
        
        
        #declaracion de variable de iteracion
        if self.exp.tipo == Tipo.RANGO:
            primiuno = Primitivo(Tipo.ENTERO,expr[0],self.fila,self.columna)
            declararvarit = Declaracion(self.id,primiuno,Tipo.ENTERO,self.fila,self.columna)

            retdecla = declararvarit.compilar(arbol,forTabla)
            if isinstance(retdecla,Error): return retdecla  

            #traduccion de for a c3d
            etiquetaInicio = generador.agregarLabel()
            
            generador.agregarComentario('INICIA FOR')
            generador.colocarLabel(etiquetaInicio)
            #condicional de for por ejemplo i<=10 goto l1; goto l2
            id=Identificador(self.id,self.fila,self.columna)
            primitivo = Primitivo(Tipo.ENTERO,expr[1],self.fila,self.columna)
            prueba=Relacion(OpsRelacional.MENORIGUALQ,id,primitivo,self.fila,self.columna)
            #prueba=Relacion(OpsRelacional.MENORQ,id,primitivo,self.fila,self.columna)
            condicion = prueba.compilar(arbol,forTabla)
            if isinstance(condicion,Error): return condicion
   
                        
            
        if self.exp.tipo == Tipo.RANGO: 
            
            forTabla.breakLbl = condicion.falseLbl 
            forTabla.continueLbl = etiquetaInicio
            
            generador.colocarLabel(condicion.trueLbl)
            for instruccion in  self.instrucciones:
                cuerpoFor=instruccion.compilar(arbol,forTabla)
                if isinstance(cuerpoFor,Error):
                    arbol.getListaErrores().append(cuerpoFor)
                    arbol.actualizarConsola(cuerpoFor.toString())
            primidos = Primitivo(Tipo.ENTERO,1,self.fila,self.columna)
            iddos=Identificador(self.id,self.fila,self.columna)
            incrementar=Aritmetica(OpsAritmetico.MAS,iddos,primidos,self.fila,self.columna)
            #res=incrementar.compilar(arbol,forTabla)
            #if isinstance(res,Error): return res
            #declaracion de nuevo valor

            declarar = Declaracion(self.id,incrementar,Tipo.ENTERO,self.fila,self.columna)
            retornodeclaracion = declarar.compilar(arbol,forTabla)
            if isinstance(retornodeclaracion,Error): return retornodeclaracion
            
            generador.agregarGoto(etiquetaInicio)
            generador.colocarLabel(condicion.falseLbl)
            generador.agregarComentario("FINALIZA FOR")
        
        arbol.setValorAmbitoFuncion(False)
        
    def getNode(self):
        nodoFor = NodoArbol("FOR")
        nodoFor.agregarHijoConNodo(self.exp.getNode())
        instrcsFor = NodoArbol("CUERPO FOR")
        for instruccion in self.instrucciones:
            instrcsFor.agregarHijoConNodo(instruccion.getNode())
        nodoFor.agregarHijoConNodo(instrcsFor)
        return nodoFor
    
    def getTipo(self,val):
        if isinstance(val,int): return Tipo.ENTERO
        elif isinstance(val,float): return Tipo.DECIMAL
        return Tipo.ENTERO

class ParaArray(Instruccion):
    def __init__(self,id,exp,instrcs ,fila, columna):
        self.id = id
        self.exp = exp
        self.instrucciones = instrcs
        self.fila = fila
        self.columna = columna
        self.arreglo=False
        self.struct=False
        self.mutable=False
    
    def compilar(self, arbol, tabla):
        genAux = Generador()
        generador = genAux.getInstance()
        self.expr=[]
        for exp in self.exp:
            ex=exp.compilar(arbol,tabla)
            if isinstance(ex,Error): return ex
            self.expr.append(ex)
            
        forTabla = TablaSimbolos(tabla)
        forTabla.setTsAnterior(tabla)
        arbol.agregarAListaTablas('FORARRAY',forTabla)#aqui agrego la tabla 
        if arbol.getValorAmbitoFuncion() == False: arbol.setValorAmbitoFuncion(True)
        
        #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
        
        #variable iterativa que sera validando con el tamano de array 
        primiuno = Primitivo(Tipo.ENTERO,0,self.fila,self.columna)
        declararvarit= Declaracion('tam',primiuno,Tipo.ENTERO,self.fila,self.columna)
        
        retdecla = declararvarit.compilar(arbol,forTabla)
        if isinstance(retdecla,Error):return retdecla
        
        #guardo array en heap
        generador.agregarComentario('INICIA ALMACEN DE FORARRAY')
        tempI = generador.agregarTemporal();generador.liberarTemporal(tempI)
        generador.addExp(tempI,'H','','')
        generador.setHeap('H',len(self.exp))#TAMANO DE ARRAY
        generador.nextHeap()
        for val in self.expr:
            generador.setHeap('H',val.getValor())
            generador.nextHeap()
        #gurado array en tabla for
        #creacion de simbolo de array para for
        simbolodearreglo= Simbolo('arrayyyforrrr#',Tipo.ENTERO,tempI,self.fila,self.columna,forTabla.size,True,True,Ambito.LOCAL,self.arreglo,self.struct,self.mutable)
        simbolodearreglo.dimensiones=len(self.exp)
        simbolodearreglo.array = self.exp
        tempPos = generador.agregarTemporal();generador.liberarTemporal(tempPos)
        #--almaceno en tabla se simbolos de for el array--
        resultadoAsig = forTabla.setSimboloEnTs(simbolodearreglo)
        if isinstance(resultadoAsig,Error): return resultadoAsig
        #--obtengo posicion donse se almaceno--
        nuevoarreglo = forTabla.getSimboloEnTs('arrayyyforrrr#')
        #tempPos=nuevoarreglo.posicion
        #--mover puntero P
        generador.addExp(tempPos,'P',nuevoarreglo.posicion,"+")#validar temppos ya que puede o tiene que ser un temp
        generador.setPila(tempPos,tempI)
        generador.agregarComentario('FINALIZA ALMACEN DE FORARRAY')
        #finaliza almacen de array 
        #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
   
        #etiqueta para regresar a validar condicion
        etiquetaInicio = generador.agregarLabel()
        
        generador.agregarComentario('INICIA FOR ARRAY')
        generador.colocarLabel(etiquetaInicio)
        #condicional para validar que la variable iterativa no sobrepase len de array
        id = Identificador('tam',self.fila,self.columna)
        primitivo = Primitivo(Tipo.ENTERO,len(self.exp),self.fila,self.columna)
        #con esto sera tam < len(array)
        prueba=Relacion(OpsRelacional.MENORQ,id,primitivo,self.fila,self.columna)
        #genero condicion en c3d
        condicion = prueba.compilar(arbol,forTabla)
        if isinstance(condicion,Error):return condicion   
        
        #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
        #si encuentra un break en el ciclo mandara a la etiqueta falsa
        forTabla.breakLbl = condicion.falseLbl
        #si encuentra un continue en el cilco mandara a etiqueta inicio
        forTabla.continueLbl = etiquetaInicio
        
        generador.colocarLabel(condicion.trueLbl)
          
        #ACCESO A ARRAY DE FORARRAY:
        h = generador.agregarTemporal();generador.liberarTemporal(h)
        tempPosd = generador.agregarTemporal();generador.liberarTemporal(tempPosd)
        generador.addExp(tempPosd,'P',nuevoarreglo.posicion,'+')
        generador.getPila(h,tempPosd)
        #obtener valor de array:
        valoraux = generador.agregarTemporal();generador.liberarTemporal(valoraux)
        valorTemp = generador.agregarTemporal();generador.liberarTemporal(valorTemp)
        generador.addExp(valoraux,h,'1','+')
        id=Identificador('tam',self.fila,self.columna)
        res=id.compilar(arbol,forTabla)
        if isinstance(res,Error): return res
        generador.addExp(valorTemp,valoraux,res.getValor(),'+')
        h2 = generador.agregarTemporal();generador.liberarTemporal(h2)
        generador.getHeap(h2,valorTemp)
        
        #aqui hay que crear variable iterativa de arreglo
        #se hace esto por que previamente se valida el tamaño
        #y ahora la variable iterativa ira cambiando sus valores 
        #de acuerdo en la posicion que se encuentre del array
        primidos = Primitivo(Tipo.ENTERO,h2,self.fila,self.columna)#vavlidar valortemp
        declararvaritt = Declaracion(self.id,primidos,Tipo.ENTERO,self.fila,self.columna)
        
        rettdecla=declararvaritt.compilar(arbol,forTabla)
        if isinstance(retdecla,Error):return rettdecla
        
        for instruccion in self.instrucciones:
            cuerpoFor = instruccion.compilar(arbol,forTabla)
            if isinstance(cuerpoFor,Error):
                arbol.getListaErrores().append(cuerpoFor)
                arbol.actualizarConsola(cuerpoFor.toString())
        primidos = Primitivo(Tipo.ENTERO,1,self.fila,self.columna)
        iddos=Identificador('tam',self.fila,self.columna)
        incrementar=Aritmetica(OpsAritmetico.MAS,iddos,primidos,self.fila,self.columna)   
        ##
        declarar = Declaracion('tam',incrementar,Tipo.ENTERO,self.fila,self.columna)
        retornodeclaracion = declarar.compilar(arbol,forTabla)
        if isinstance(retornodeclaracion,Error): return retornodeclaracion
        
        generador.agregarGoto(etiquetaInicio)
        generador.colocarLabel(condicion.falseLbl)
        generador.agregarComentario("FINALIZA FOR")
    
        arbol.setValorAmbitoFuncion(False)
        

        
        
    def getNode(self):
        nodoFor = NodoArbol("FORARRAY")
        nodoFor.agregarHijoSinNodo(str(self.expr))
        instrcsFor = NodoArbol("CUERPO_FOR")
        for instruccion in self.instrucciones:
            instrcsFor.agregarHijoConNodo(instruccion.getNode())
        nodoFor.agregarHijoConNodo(instrcsFor)
        return nodoFor
        
    def getTipo(self,val):
        if isinstance(val,int): return Tipo.ENTERO
        elif isinstance(val,float): return Tipo.DECIMAL
        return Tipo.ENTERO
    
    
class ParaArrayD(Instruccion):
    def __init__(self,id,idd,instrcs ,fila, columna):
        self.id = id
        self.idd = idd
        self.instrucciones = instrcs
        self.fila = fila
        self.columna = columna
        self.arreglo=False
        self.struct=False
        self.mutable=False
    
    def compilar(self, arbol, tabla):
        genAux = Generador()
        generador = genAux.getInstance()
        
        #obtengo variable a iterar, puede ser arreglo o string
        simboll= tabla.getSimboloEnTs(self.idd)
        if simboll == None:
            return Error("SEMANTICO","IDENTIFICADOR "+str(self.idd)+"NO AH SIDO DECLARADO",self.fila,self.columna)
    
        
        
        if simboll.tipo == Tipo.CADENA and simboll.dimensiones == None:
            crearAcceso= Identificador(simboll.id,self.fila,self.columna)
            RetornoAcceso = crearAcceso.compilar(arbol,tabla)
            if isinstance(RetornoAcceso,Error):return RetornoAcceso
            
            forTabla = TablaSimbolos(tabla)
            forTabla.setTsAnterior(tabla)
            arbol.agregarAListaTablas('FORARRAY',forTabla)#aqui agrego la tabla 
            if arbol.getValorAmbitoFuncion() == False: arbol.setValorAmbitoFuncion(True)
            #variable de iteracion
            #esta debe de almacenar el primer caracter ascii de la cadena
            #tempH = generador.agregarTemporal()
            #ya obtenido el valor de h, se obtiene el ascii
            tempAscii=generador.agregarTemporal();generador.liberarTemporal(tempAscii)
            generador.getHeap(tempAscii,RetornoAcceso.valor)
            #almaceno la variable iterativa en TS
            self.declararvariableIterativa(self.id,Tipo.CARACTER,tempAscii,self.fila,self.columna,forTabla,generador)
            #INICIA FOR 
            etiquetaInicio = generador.agregarLabel()
        
            generador.agregarComentario("INICIA FOR")
            generador.colocarLabel(etiquetaInicio)
            #condicional de for por ejemplo i<=10 goto l1; goto l2
            id=Identificador(self.id,self.fila,self.columna)
            returnid=id.compilar(arbol,forTabla)
            #primitivo = Primitivo(Tipo.ENTERO,'-1',self.fila,self.columna)
            #prueba=Relacion(OpsRelacional.DIFERENTE,id,primitivo,self.fila,self.columna)
            condicion=self.CrearCondicional(generador,returnid.valor,'-1')
            #condicion = prueba.compilar(arbol,forTabla)
            #if isinstance(condicion,Error): return condicion
            
            forTabla.breakLbl = condicion.falseLbl
            forTabla.continueLbl = etiquetaInicio
            
            generador.colocarLabel(condicion.trueLbl)
            
            for instruccion in self.instrucciones:
                cuerpoFor=instruccion.compilar(arbol,forTabla)
                if isinstance(cuerpoFor,Error):
                    arbol.getListaErrores().append(cuerpoFor)
                    arbol.actualizarConsola(cuerpoFor.toString())
            #actualizo el valor del ascii
            generador.addExp(RetornoAcceso.valor,RetornoAcceso.valor,'1','+')
            generador.getHeap(tempAscii,RetornoAcceso.valor)
            
            self.declararvariableIterativa(self.id,Tipo.CARACTER,tempAscii,self.fila,self.columna,forTabla,generador)

            
            generador.agregarGoto(etiquetaInicio)
            generador.colocarLabel(condicion.falseLbl)
            generador.agregarComentario("FINALIZA FOR")

            
            arbol.setValorAmbitoFuncion(False)
            
        elif simboll.tipo == Tipo.ENTERO and simboll.dimensiones != None:
            
            forTabla = TablaSimbolos(tabla)
            forTabla.setTsAnterior(tabla)
            arbol.agregarAListaTablas('FORARRAY',forTabla)#aqui agrego la tabla 
            if arbol.getValorAmbitoFuncion() == False: arbol.setValorAmbitoFuncion(True)
            
            
            
            #variable iterativa que sera validando con el tamano de array 
            primiuno = Primitivo(Tipo.ENTERO,0,self.fila,self.columna)
            declararvarit= Declaracion('tamarr',primiuno,Tipo.ENTERO,self.fila,self.columna)
            
            retdecla = declararvarit.compilar(arbol,forTabla)
            if isinstance(retdecla,Error):return retdecla
            
            #guardo array en heap//en este caso ya esta almacenado no se hace nada
            #etiqueta para regresar a validar condicion
            etiquetaInicio = generador.agregarLabel()
            
            generador.agregarComentario('INICIA FOR ARRAY')
            generador.colocarLabel(etiquetaInicio)
            #condicional para validar que la variable iterativa no sobrepase len de array
            id = Identificador('tamarr',self.fila,self.columna)
            primitivo = Primitivo(Tipo.ENTERO,len(simboll.array),self.fila,self.columna)
            #con esto sera tam < len(array)
            prueba=Relacion(OpsRelacional.MENORQ,id,primitivo,self.fila,self.columna)
            #genero condicion en c3d
            condicion = prueba.compilar(arbol,forTabla)
            if isinstance(condicion,Error):return condicion
            
            #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
            #si encuentra un break en el ciclo mandara a la etiqueta falsa
            forTabla.breakLbl = condicion.falseLbl
            #si encuentra un continue en el cilco mandara a etiqueta inicio
            forTabla.continueLbl = etiquetaInicio

            generador.colocarLabel(condicion.trueLbl)
            
            #ACCESO A ARRAY DE FORARRAY:
            h = generador.agregarTemporal();generador.liberarTemporal(h)
            if not simboll.esGlobal:
                tempPosd = generador.agregarTemporal();generador.liberarTemporal(tempPosd)
                generador.addExp(tempPosd,'P',simboll.posicion,'+')
                generador.getPila(h,tempPosd)
            else:
               generador.getPila(h,simboll.posicion) 
            #obtener valor de array:
            valoraux = generador.agregarTemporal();generador.liberarTemporal(valoraux)
            valorTemp = generador.agregarTemporal();generador.liberarTemporal(valorTemp)
            generador.addExp(valoraux,h,'1','+')
            id=Identificador('tamarr',self.fila,self.columna)
            res=id.compilar(arbol,forTabla)
            if isinstance(res,Error): return res
            generador.addExp(valorTemp,valoraux,res.getValor(),'+')
            h2 = generador.agregarTemporal();generador.liberarTemporal(h2)
            generador.getHeap(h2,valorTemp)
            #aqui hay que crear variable iterativa de arreglo
            #se hace esto por que previamente se valida el tamaño
            #y ahora la variable iterativa ira cambiando sus valores 
            #de acuerdo en la posicion que se encuentre del array
            primidos = Primitivo(Tipo.ENTERO,h2,self.fila,self.columna)#vavlidar valortemp
            declararvaritt = Declaracion(self.id,primidos,Tipo.ENTERO,self.fila,self.columna)
            
            rettdecla=declararvaritt.compilar(arbol,forTabla)
            if isinstance(retdecla,Error):return rettdecla
            
            for instruccion in self.instrucciones:
                cuerpoFor = instruccion.compilar(arbol,forTabla)
                if isinstance(cuerpoFor,Error):
                    arbol.getListaErrores().append(cuerpoFor)
                    arbol.actualizarConsola(cuerpoFor.toString())
            primidos = Primitivo(Tipo.ENTERO,1,self.fila,self.columna)
            iddos=Identificador('tamarr',self.fila,self.columna)
            incrementar=Aritmetica(OpsAritmetico.MAS,iddos,primidos,self.fila,self.columna)
            ##
            declarar = Declaracion('tamarr',incrementar,Tipo.ENTERO,self.fila,self.columna)
            retornodeclaracion = declarar.compilar(arbol,forTabla)
            if isinstance(retornodeclaracion,Error): return retornodeclaracion
            
            generador.agregarGoto(etiquetaInicio)
            generador.colocarLabel(condicion.falseLbl)
            generador.agregarComentario("FINALIZA FOR ARRAY")
    
            arbol.setValorAmbitoFuncion(False)
        else:
            return Error("SEMANTICO", "FOR VALIDO SOLO PARA VARIABLES CON CADENAS O ARREGLOS",self.fila,self.columna)
        
        

                
    
    def declararvariableIterativa(self,id,tipo,valor,fil,col,tabla,generador):
        #creacion de simbolo a almacenar:
        simboloIt = Simbolo(str(id),tipo,valor,fil,col,tabla.size,False,False,Ambito.LOCAL,False,False,False)
        resul = tabla.getSimboloEnTs(id)
        if resul == None:
            declaracion = tabla.setSimboloEnTs(simboloIt)
            if isinstance(declaracion,Error): return declaracion
        
        nuevaVariable = tabla.getSimboloEnTs(id)
        tempPos = nuevaVariable.posicion
        
        if nuevaVariable.esGlobal==False:
            tempPos = generador.agregarTemporal()
            generador.addExp(tempPos,'P',nuevaVariable.posicion,"+")
        
        generador.setPila(tempPos,valor)
        generador.agregarSalto() 
    
    def CrearCondicional(self,generador,resizq,resder,):
        truelbl=generador.agregarLabel()
        falselbl=generador.agregarLabel()
        generador.agregarIf(resizq,resder,'!=',truelbl)
        generador.agregarGoto(falselbl)
        r=Return(None,Tipo.ENTERO,False)
        r.trueLbl=truelbl
        r.falseLbl=falselbl
        
        return r
    
        
    def getNode(self):
        nodoFor = NodoArbol("FOR")
        nodoFor.agregarHijoSinNodo(str(self.idd))
        instrcsFor = NodoArbol("CUERPO_FOR")
        for instruccion in self.instrucciones:
            instrcsFor.agregarHijoConNodo(instruccion.getNode())
        nodoFor.agregarHijoConNodo(instrcsFor)
        return nodoFor
    
    def getTipo(self,val):
        if isinstance(val,int): return Tipo.ENTERO
        elif isinstance(val,float): return Tipo.DECIMAL
        return Tipo.ENTERO

class ParaStr(Instruccion):
    def __init__(self,id,cadena,instrcs ,fila, columna):
        self.id = id
        self.cadena = cadena
        self.instrucciones = instrcs
        self.fila = fila
        self.columna = columna
        self.arreglo=False
        self.struct=False
        self.mutable=False
    
    def compilar(self, arbol, tabla):
        genAux = Generador()
        generador = genAux.getInstance()
        
        valor= self.cadena
        
        #almaceno cadena en heap
        prim = Primitivo(Tipo.CADENA,valor,self.fila,self.columna)
        returnprimi = prim.compilar(arbol,tabla)
        if isinstance(returnprimi,Error):returnprimi
        
        #creo tabla para for   
        forTabla = TablaSimbolos(tabla)
        forTabla.setTsAnterior(tabla)
        arbol.agregarAListaTablas('FORARRAY',forTabla)#aqui agrego la tabla  
        if arbol.getValorAmbitoFuncion() == False: arbol.setValorAmbitoFuncion(True)
        
        #ya almacenada guardo el valor de H en pila a traves temporal
        paramtemp = generador.agregarTemporal()
        generador.addExp(paramtemp,'P',forTabla.size,'+')
        generador.setPila(paramtemp,returnprimi.valor)
        
        #variable de iteracion
        #esta debe de almacenar el primer caracter ascii de la cadena
        tempH= generador.agregarTemporal()
        generador.getPila(tempH,paramtemp)
        #ya obtenido el valor de h, se obtiene el ascii
        tempAscii=generador.agregarTemporal()
        generador.getHeap(tempAscii,tempH)
        
        #almaceno variable iterativa en TS
        self.declararvariableIterativa(self.id,Tipo.CARACTER,tempAscii,self.fila,self.columna,forTabla,generador)

        
        #INICIA EL BENDITO FOR
        etiquetaInicio = generador.agregarLabel()
        
        generador.agregarComentario("INICIA FOR")
        generador.colocarLabel(etiquetaInicio)
        #condicional de for por ejemplo i<=10 goto l1; goto l2
        id=Identificador(self.id,self.fila,self.columna)
        returnid=id.compilar(arbol,forTabla)
        #primitivo = Primitivo(Tipo.ENTERO,'-1',self.fila,self.columna)
        #prueba=Relacion(OpsRelacional.DIFERENTE,id,primitivo,self.fila,self.columna)
        condicion=self.CrearCondicional(generador,returnid.valor,'-1')
        #condicion = prueba.compilar(arbol,forTabla)
        #if isinstance(condicion,Error): return condicion
        
        forTabla.breakLbl = condicion.falseLbl
        forTabla.continueLbl = etiquetaInicio
        
        generador.colocarLabel(condicion.trueLbl)
        
        for instruccion in self.instrucciones:
            cuerpoFor=instruccion.compilar(arbol,forTabla)
            if isinstance(cuerpoFor,Error):
                arbol.getListaErrores().append(cuerpoFor)
                arbol.actualizarConsola(cuerpoFor.toString())
        #actualizo el valor del ascii
        generador.addExp(tempH,tempH,'1','+')
        generador.getHeap(tempAscii,tempH)
        
        self.declararvariableIterativa(self.id,Tipo.CARACTER,tempAscii,self.fila,self.columna,forTabla,generador)

        
        generador.agregarGoto(etiquetaInicio)
        generador.colocarLabel(condicion.falseLbl)
        generador.agregarComentario("FINALIZA FOR")

        
        arbol.setValorAmbitoFuncion(False)
        
        
        
    def getNode(self):
        nodoFor = NodoArbol("FOR_STR")
        nodoFor.agregarHijoSinNodo(str(self.cadena))
        instrcsFor = NodoArbol("CUERPO_FOR")
        for instruccion in self.instrucciones:
            instrcsFor.agregarHijoConNodo(instruccion.getNode())
        nodoFor.agregarHijoConNodo(instrcsFor)
        return nodoFor

    def getTipo(self,val):
        if isinstance(val,int): return Tipo.ENTERO
        elif isinstance(val,float): return Tipo.DECIMAL
        return Tipo.ENTERO
    
    def declararvariableIterativa(self,id,tipo,valor,fil,col,tabla,generador):
        #creacion de simbolo a almacenar:
        simboloIt = Simbolo(str(id),tipo,valor,fil,col,tabla.size,False,False,Ambito.LOCAL,False,False,False)
        resul = tabla.getSimboloEnTs(id)
        if resul == None:
            declaracion = tabla.setSimboloEnTs(simboloIt)
            if isinstance(declaracion,Error): return declaracion
        
        nuevaVariable = tabla.getSimboloEnTs(id)
        tempPos = nuevaVariable.posicion
        
        if nuevaVariable.esGlobal==False:
            tempPos = generador.agregarTemporal()
            generador.addExp(tempPos,'P',nuevaVariable.posicion,"+")
        
        generador.setPila(tempPos,valor)
        generador.agregarSalto()   
        
    def CrearCondicional(self,generador,resizq,resder,):
        truelbl=generador.agregarLabel()
        falselbl=generador.agregarLabel()
        generador.agregarIf(resizq,resder,'!=',truelbl)
        generador.agregarGoto(falselbl)
        r=Return(None,Tipo.ENTERO,False)
        r.trueLbl=truelbl
        r.falseLbl=falselbl
        
        return r
        
        
        
        