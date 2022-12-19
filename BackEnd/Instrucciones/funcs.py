import copy
from almacenar.generador import Generador
from padres.instruccion import Instruccion
from almacenar.error import Error
from almacenar.ts import TablaSimbolos
from instrucciones.breeak import Break
from instrucciones.continuar import Continue
from padres.Nodo import NodoArbol
from almacenar.tipo import Tipo
from instrucciones.retorn import Retorno

#from padres.instruccion import Instruccion
#from almacenar.error import Error
#from almacenar.ts import TablaSimbolos
#from instrucciones.breeak import Break
#from instrucciones.continuar import Continue
#from padres.Nodo import NodoArbol
#from almacenar.tipo import Tipo
#from instrucciones.retorn import Retorno

class Funcion(Instruccion):
    def __init__(self,id,params,tipo,instrs, fila, columna):
        self.id = id
        self.parametros = params
        self.instrucciones = instrs
        self.fila = fila
        self.columna = columna
        self.tipo = tipo
        self.precompilar = True
        self.dimensiones = 1
    def compilar(self, arbol, tabla):
        
        if self.precompilar:
            self.precompilar = False
            self.ValidarParametros()
            self.ValidarTipo()
            idUnico = self.IdUnico()
            #resuladdFunc=arbol.agregarFuncs(idUnico,self)#en arbol
            #if isinstance(resuladdFunc,Error):return resuladdFunc
            #self.tipo = Tipo.ENTERO
            resuladdfuncts = tabla.setSimboloEnTsFunc(self,idUnico)#en ts
            if isinstance(resuladdfuncts,Error):return resuladdfuncts
            return 
            
        simbolofunc = tabla.getFuncion(self.id)
        if simbolofunc != None:
            genAux = Generador()
            generador = genAux.getInstance()
            retunrLbl = generador.agregarLabel()
            #aqui todos los temps que podia tener antes los 
            #almacen en almacenamiento temp
            almacenamientoTemp = generador.getAlmacenamientoTemp()
            
            functabla = TablaSimbolos(tabla)
            functabla.setTsAnterior(tabla)
            arbol.agregarAListaTablas('FUNCION',functabla)#aqui agrego la tabla
            #se aumenta 1 para que el return este siempre en 0
            functabla.size=1
            #functabla.prop=str(self.id)
            functabla.returnLbl = retunrLbl
            functabla.actualfunc=simbolofunc
            
            
            for param in self.parametros:
                if param["vector"] == True:
                    self.dimensiones = 1
                    if isinstance(param["tipo"],list):
                        lista=[]
                        param["tipo"]=self.obtenerTipo(param["tipo"],lista)
                    functabla.agregarVec(str(param["id"]),param["tipo"],True,self.dimensiones,self.fila,self.columna)
                else:
                    functabla.agregarVar(str(param["id"]),param["tipo"],self.fila,self.columna)
                
            generador.limpiarAlmacentemp()#limpio lista de temps  
            #bandera para escribir afuera de main
            generador.inFunc = True
            #agrego encabezado de func
            generador.agregarInicioFuncion(simbolofunc.IdUnico)
            #este if es para las declaraciones que puedan haber en funcion sean locales 
            if arbol.getValorAmbitoFuncion() == False: arbol.setValorAmbitoFuncion(True)
            #compilo cada instruccion
            for instruccion in self.instrucciones:
                retorno = instruccion.compilar(arbol,functabla)
                if arbol.getValorAmbitoFuncion() == False: arbol.setValorAmbitoFuncion(True)
                if isinstance(retorno,Error):
                    arbol.getListaErrores().append(retorno)
                    arbol.actualizarConsola(retorno.toString())
            arbol.setValorAmbitoFuncion(False)
            #->->->->->->->->->->->->->->->->->->->->->
            #goto para evitar error de go
            if not functabla.gotoReturn:
                generador.agregarGoto(retunrLbl)
                functabla.gotoReturn = False
            #->->->->->->->->->->->->->->->->->->->->->
            generador.colocarLabel(retunrLbl)#return label
            generador.agregarFinalFuncion()#codigo final de funcion
            generador.inFunc=False
            generador.setAlmacenamientoTemp(almacenamientoTemp)#devuelvo todo los temporales anteriores
            
            
            
        
        
        
        
        
        #funcionTabla = TablaSimbolos()
        #funcionTabla.setTsAnterior(tabla)
        #arbol.agregarAListaTablas('FUNCION',    funcionTabla)#aqui agrego la tabla generada 
        #if arbol.getValorAmbitoFuncion() == False: arbol.setValorAmbitoFuncion(True)
        #for instruccion in self.instrucciones:
        #    retorno = instruccion.ejecutar(arbol,funcionTabla)
        #    if arbol.getValorAmbitoFuncion() == False: arbol.setValorAmbitoFuncion(True)
        #    if isinstance(retorno,Error):
        #        arbol.getListaErrores().append(retorno)
        #        arbol.actualizarConsola(retorno.toString())
        #    if isinstance(retorno, Break):
        #        err=Error("SEMANTICO","Sentencia BREAK fuera de ciclo",instruccion.fila,instruccion.columna)
        #        arbol.getListaErrores().append(err)
        #        arbol.actualizarConsola(err.toString())
        #    if isinstance(retorno, Continue):
        #        err=Error("SEMANTICO","Sentencia CONTINUE fuera de ciclo",instruccion.fila,instruccion.columna)
        #        arbol.getListaErrores().append(err)
        #        arbol.actualizarConsola(err.toString())
        #    if isinstance(retorno, Retorno):
        #        self.tipo = retorno.tipo
        #        return retorno.expRetorno
        #    
        #arbol.setValorAmbitoFuncion(False)
        #return None
    
    
    def getNode(self):
        nodoFunc = NodoArbol("Function")
        nodoFunc.agregarHijoSinNodo(str(self.id))
        paramss= NodoArbol("PARAMETROS")
        for param in self.parametros:
            paraetter= NodoArbol("parametro")
            paraetter.agregarHijoSinNodo(str(param["id"]))
            paraetter.agregarHijoSinNodo(str(param["tipo"]))
            paramss.agregarHijoConNodo(paraetter)
        nodoFunc.agregarHijoConNodo(paramss)
        instrcsFor = NodoArbol("CUERPO Function")
        for instruccion in self.instrucciones:
            instrcsFor.agregarHijoConNodo(instruccion.getNode())
        nodoFunc.agregarHijoConNodo(instrcsFor)
        return nodoFunc
    
    def ValidarParametros(self):
        set = []
        for param in self.parametros:
            if param in set: return Error("SEMANTICO",'YA EXISTE PARAMETRO CON EL ID'+str(param["id"]),self.fila,self.columna)
            #aqui puede estar una validacion para structs tambien.
            set.append(str(param["id"]).lower())        
    
    def ValidarTipo(self):
        pass
    
    def IdUnico(self):
        id = self.id
        if len(self.parametros)==0:
            return id + "_vacio"
        for param in self.parametros:
            id += "_"+self.tipoParam(param)
        return id
    
    def tipoParam(self,parametro):
        if parametro["vector"] == True:
            if isinstance(parametro["tipo"],list):
                lista=[]
                tipo=self.obtenerTipo(copy.copy(parametro["tipo"]),lista)
                if tipo == Tipo.ENTERO:
                    return "int"+""
                elif tipo == Tipo.DECIMAL:
                    return "float"+""
                elif tipo == Tipo.CADENA:
                    return "cadena"+""
        if parametro["tipo"] == Tipo.ENTERO:
            return "int"+""
        elif parametro["tipo"] == Tipo.DECIMAL:
            return "float"+""
        elif parametro["tipo"] == Tipo.CADENA:
            return "cadena"+""
    
    def obtenerTipo(self,lista,arr):
        for elem in lista:  
            self.dimensiones+=1
            arr.append(elem)   
            if isinstance(elem,list):
                arr.pop(0)
                self.obtenerTipo(copy.copy(elem),arr)
        return arr[0]