from instrucciones.retorn import Retorno
from padres.instruccion import Instruccion
from padres.expresion import Expresion
from almacenar.error import Error
from almacenar.tipo import Return, Tipo,Ambito,OpsAritmetico
from almacenar.ts import TablaSimbolos
from almacenar.simbolo import Simbolo
from instrucciones.breeak import Break
from instrucciones.continuar import Continue
from padres.Nodo import NodoArbol
from Expresiones.aritmeticas import Aritmetica
from almacenar.generador import Generador


#from padres.instruccion import Instruccion
#from almacenar.error import Error
#from almacenar.tipo import Tipo,Ambito,OpsAritmetico
#from almacenar.ts import TablaSimbolos
#from almacenar.simbolo import Simbolo
#from instrucciones.breeak import Break
#from instrucciones.continuar import Continue
#from padres.Nodo import NodoArbol
#from Expresiones.aritmeticas import Aritmetica


class Llamada(Expresion):
    def __init__(self,id,parametros,fil, col):
        super().__init__(fil, col)
        self.id = id
        self.parametros = parametros
        self.fila = fil
        self.columna = col
        self.arreglo=False
        self.struct=False
        self.mutable=False
        self.tipo = Tipo.NULO
        
    def compilar(self, arbol, tabla):
        simbolofunc = tabla.getFuncion(self.id)
        if simbolofunc == None:
            return Error("SEMANTICO","FUNCION NO EXISTE",self.fila,self.columna)
        genAux = Generador()
        generador = genAux.getInstance()
        tamano = generador.guardarTemps(tabla)#size
        
        #para llamadas a nativas ->->->->->->->->->->->->
        if simbolofunc.esNativa:
            generador.simbolofunc.id
        #->->->->->->->->->->->->->->->->-<-<-<-<->->->->
        
        temp = generador.agregarTemporal(); generador.liberarTemporal(temp)
        
        #validacion de cantidad de parametros es correcta en llamada a funcion
        if len(self.parametros) != simbolofunc.tamano: return Error("SEMANTICO","LA CANTIDAD DE PARAMETROS EN LLAMADA A FUNCION ES INCORRECTA",self.fila,self.columna)
        
        #falta validacion de cada parametro si es el tipo correcto que espera la función
        
        
        
        if len(self.parametros)>0:
            generador.addExp(temp,'P',tabla.size+1,'+')
            
        #banderaEntro = False
        contador =0#->->->->
        for exp in self.parametros:
            #banderaEntro = True
            resExp = exp.compilar(arbol,tabla)
            if isinstance(resExp,Error): return resExp
            if resExp.tipo == Tipo.BOOLEANO:
                salida = generador.agregarLabel()
                generador.colocarLabel(resExp.trueLbl)
                generador.setPila(temp,'1')
                generador.agregarGoto(salida)
                generador.colocarLabel(resExp.falseLbl)
                generador.setPila(temp,'0')
                generador.colocarLabel(salida)
            else:
                generador.setPila(temp,resExp.getValor())
            if contador != (len(self.parametros)-1):
                generador.addExp(temp,temp,'1','+')
            contador+=1
        generador.newEnv(tabla.size)#cambio de entorno 
        generador.llamandaFuncion(simbolofunc.IdUnico)#ingreso a funcion
        generador.getPila(temp,'P')#Obteengo valor de return 
        generador.returnEntorno(tabla.size)#regreso a entorno
        generador.recuperarTemps(tabla,tamano)
        generador.addTemp(temp)#esto es por si hay algun return, aqui esta el valor
        #generador.agregarTemporal(temp)}
        self.tipo = simbolofunc.tipo
        if simbolofunc.tipo != Tipo.BOOLEANO: return Return(temp,simbolofunc.tipo,True)
        
        #si es booleano
        retorno = Return('',simbolofunc.tipo,False)
        self.checkLabels()
        generador.agregarIf(temp,'1','==',self.trueLbl)
        generador.agregarGoto(self.falseLbl)
        retorno.trueLbl=self.trueLbl
        retorno.falseLbl=self.falseLbl
        return retorno
        
        
        
        
        
        
        
    #    retornoLlamada = tabla
    #    #aqui tambien puede retornar structs
    #    if retornoLlamada == None:
    #        #return Error("SEMANTICO", "NO EXISTE LA FUNCION: "+str(self.id),self.fila,self.columna)
    #        
    #        #TODOO LO QUE ESTA AQUI ABAJO ES NUEVO SE PUEDE BORRAR FACILMENTE SI NO FUNCIONA
    #        #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
    #        retornoLlamada = arbol.getStuct(self.id)
    #        if retornoLlamada == None:
    #            return Error("SEMANTICO", "NO EXISTE LA FUNCION: "+str(self.id),self.fila,self.columna)
    #        else:
    #            ##validar si no hay id's repetidos de atributos en declaracion de structs
    #            responseStruct = retornoLlamada.ejecutar(arbol,tabla)
    #            if isinstance(responseStruct,Error):return responseStruct
    #            self.atributos={}
    #            diccionario = self.metodoparastruct(responseStruct,self.parametros,self.id,arbol,tabla)
    #            if isinstance(diccionario,Error):return diccionario
    #            self.atributos=diccionario
    #            self.tipo = Tipo.STRUCT
    #            simboloStruct= Simbolo('',Tipo.STRUCT,self.atributos,'','',Ambito.GLOBAL,False,True,retornoLlamada.mutable)
    #            #simbolo va incompleto se debe de completar en declaracion FFFF
    #            return simboloStruct
    #        #->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
    #            
    #    #tabla para ambito llamada
    #    tablaLLamada = TablaSimbolos()
    #    tablaLLamada.setTsAnterior(arbol.getTsGlobal())
    #    #arbol.agregarAListaTablas('Llamada', tablaLLamada)
    #    #get parameters:
    #    if len(retornoLlamada.parametros) == len(self.parametros):
    #        
    #        noParams=0
    #        
    #        for exp in self.parametros:
    #            resExp = exp.ejecutar(arbol,tabla)
    #            if isinstance(resExp,Error): return resExp
    #            if retornoLlamada.parametros[noParams]['tipo'] != Tipo.NULO:#si tiene nulo no se valida que la exp que se manda sea del mismo tipo
    #                #if exp.tipo == Tipo.STRUCT:
    #                #    if arbol.tipoStruct(retornoLlamada.parametros[noParams]['tipo']):
    #                #        simboloStruct = tabla.getSimboloEnTs(exp.identificador)
    #                #        simbole = Simbolo(str(retornoLlamada.parametros[noParams]["id"]),exp.tipo,simboloStruct.valor,self.fila,self.columna,Ambito.LOCAL,False,True,simboloStruct.mutable)
    #                #        retornTabla= tablaLLamada.setSimboloEnTs(simbole)
    #                #        if isinstance(retornTabla,Error): return retornTabla
    #                #    else:
    #                #        return Error("SEMANTICO","TIPO DE DATO ENVIADO EN LLAMADA A FUNCION ES INCORRECTO: ",self.fila,self.columna)                        
    #                ################->->->->->->->->->->->->->->->->->->->->->->->->
    #                if exp.tipo == Tipo.STRUCT:
    #                    try:
    #                        if retornoLlamada.parametros[noParams]['tipo'] == resExp['##_nombre_padre_struct_##']['id']:
    #                            simbole = Simbolo(str(retornoLlamada.parametros[noParams]['id']),Tipo.STRUCT,resExp,self.fila,self.columna,Ambito.LOCAL,False,True,exp.mutable)
    #                            retornTabla= tablaLLamada.setSimboloEnTs(simbole)
    #                            if isinstance(retornTabla,Error): return retornTabla
    #                        else:
    #                            return Error("SEMANTICO","TIPO DE DATO ENVIADO EN LLAMADA A FUNCION  ES INCORRECTO: ",self.fila,self.columna)
    #                    except:
    #                        return Error("SEMANTICO","TIPO DE DATO ENVIADO EN LLAMADA A FUNCION  ES INCORRECTO: ",self.fila,self.columna)
    #                ################->->->->->->->->->->->->->->->->->->->->->->->->
    #                elif retornoLlamada.parametros[noParams]['tipo'] == exp.tipo:
    #                    #creacion de simbolo
    #                    simbole = Simbolo(str(retornoLlamada.parametros[noParams]["id"]),retornoLlamada.parametros[noParams]['tipo'],resExp,self.fila,self.columna,Ambito.LOCAL,self.arreglo,self.struct,self.mutable)
    #                    retornTabla= tablaLLamada.setSimboloEnTs(simbole)
    #                    if isinstance(retornTabla,Error): return retornTabla
    #                else:
    #                    return Error("SEMANTICO","TIPO DE DATO ENVIADO EN LLAMADA A FUNCION -> "+str(resExp) +" ES INCORRECTO: ",self.fila,self.columna)
    #                noParams +=1
    #            else:
    #                #aqui agrego si no tiene tipo de una vez el simbolo
    #                #creacion de simbolo
    #                if exp.tipo == Tipo.ARREGLO:
    #                    simbole = Simbolo(str(retornoLlamada.parametros[noParams]["id"]),exp.tipo,resExp,self.fila,self.columna,Ambito.LOCAL,True,self.struct,self.mutable)
    #                ################->->->->->->->->->->->->->->->->->->->->->->->->
    #                elif exp.tipo == Tipo.STRUCT:
    #                    try:
    #                        simbole = Simbolo(str(retornoLlamada.parametros[noParams]['id']),Tipo.STRUCT,resExp,self.fila,self.columna,Ambito.LOCAL,False,True,exp.mutable)
    #                        #retornTabla= tablaLLamada.setSimboloEnTs(simbole)
    #                        #if isinstance(retornTabla,Error): return retornTabla
    #                    except:
    #                        return Error("SEMANTICO","LLAMADA A FUNCION  ES INCORRECTA: ",self.fila,self.columna)
    #                ################->->->->->->->->->->->->->->->->->->->->->->->->
    #                else:
    #                    simbole = Simbolo(str(retornoLlamada.parametros[noParams]["id"]),exp.tipo,resExp,self.fila,self.columna,Ambito.LOCAL,self.arreglo,self.struct,self.mutable)
    #                retornTabla= tablaLLamada.setSimboloEnTs(simbole)
    #                if isinstance(retornTabla,Error): return retornTabla 
    #                noParams +=1
    #    else:
    #        return Error("SEMANTICO","CANTIDAD DE PARAMETRO EN LLAMADA A FUNCION, ES INCORRECTA",self.fila,self.columna)
    #      
    #            
    #    valor = retornoLlamada.ejecutar(arbol,tablaLLamada)
    #    if isinstance(valor,Error): return valor
    #    self.tipo = retornoLlamada.tipo #aqui con la validacion de tipos si en caso es nulo pues puede ser cualquiera y si es diferente pues ya se valida que sea el mismo tipo
    #    
    #    return valor
    def checkLabels(self):
        genAux = Generador()
        generator = genAux.getInstance()
        if self.trueLbl == '':
            self.trueLbl = generator.agregarLabel()
        if self.falseLbl == '':
            self.falseLbl = generator.agregarLabel()
    
    def getNode(self):
        llamadanode = NodoArbol("LLamadaFuncion")
        llamadanode.agregarHijoSinNodo(str(self.id))
        params = NodoArbol("PARAMS")
        if self.parametros:
            for param in self.parametros:
                params.agregarHijoConNodo(param.getNode())         
        llamadanode.agregarHijoConNodo(params)
        return llamadanode
    
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
 
 
    def metodoparastruct(self,responseStruct,parametros,id,arbol,tabla):
        atributos={}
        atributos['##_nombre_padre_struct_##']={'id':str(id),'valor':''}
        if len(responseStruct) == len(parametros):
            noparams = 0
            for parametro in parametros:
                resexp = parametro.ejecutar(arbol,tabla)
                if isinstance(resexp,Error):return resexp 
                if responseStruct[noparams]['tipo'] != Tipo.NULO:
                    if isinstance(parametro,Llamada):
                        if responseStruct[noparams]['tipo'] == parametro.id:
                            atributos[responseStruct[noparams]['id']]={'valor':resexp.valor,'tipo':responseStruct[noparams]['tipo'],'bandera':responseStruct[noparams]['bandera']} 
                        else:
                            return Error("SEMANTICO","ATRIBUTO -> "+str(parametro.id) +" PARA STRUCT ES INCORRECTO: ",self.fila,self.columna)
                    #####->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                    elif parametro.tipo == Tipo.STRUCT:
                        atributos[responseStruct[noparams]['id']]={'valor':resexp,'tipo':responseStruct[noparams]['tipo'],'bandera':responseStruct[noparams]['bandera']} 
                    #####->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->
                    elif responseStruct[noparams]['tipo'] == parametro.tipo: 
                        atributos[responseStruct[noparams]['id']]={'valor':resexp,'tipo':responseStruct[noparams]['tipo'],'bandera':responseStruct[noparams]['bandera']}
                    else:
                        return Error("SEMANTICO","ATRIBUTO -> "+str(resexp) +" PARA STRUCT ES INCORRECTO: ",self.fila,self.columna)
                    noparams +=1
                else:
                    atributos[responseStruct[noparams]['id']]={'valor':resexp,'tipo':parametro.tipo,'bandera':responseStruct[noparams]['bandera']}
                            #print(self.atributos)
                    noparams +=1
            return atributos 
        else:
            return Error("SEMANTICO","CANTIDAD DE ATRIBUTOS EN LLAMADA A STRUCT, ES INCORRECTA",self.fila,self.columna)