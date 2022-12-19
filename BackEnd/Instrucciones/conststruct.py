from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol
from almacenar.error import Error
from instrucciones.llamda import Llamada
from almacenar.simbolo import Simbolo
from almacenar.tipo import Ambito, Tipo

#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol
#from almacenar.error import Error
#from instrucciones.llamda import Llamada
#from almacenar.simbolo import Simbolo
#from almacenar.tipo import Ambito, Tipo

class ConstruccionStruct(Instruccion):
    def __init__(self,idvar,struc, tipo,fila, columna):
        self.idvar=idvar
        self.struc = struc
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.atributos={}
        self.arreglo=False
        self.structs=True

    def compilar(self, arbol, tabla,prueba=None,llave=None):
        
       # print("")
        #return None
        for atributo in self.struc.atributos:
            if isinstance(atributo,Llamada): 
                resp=atributo.ejecutar(arbol,tabla)
        
        retornoStruct = arbol.getStuct(self.struc.id)
        if retornoStruct == None : return Error("SEMANTICO", "NO EXISTE STRUCT: ",self.fila,self.columna)
        ##VALIDAR TIPO SI TRAE:
        if self.tipo != None:
            if self.tipo != retornoStruct.idStruct: return Error("SEMANTICO","TIPO DECLARADO PARA STRUCT NO COINCIDE",self.fila,self.columna)
        ##validar si no hay id's repetidos de atributos en declaracion de structs
        responseStruct = retornoStruct.ejecutar(arbol,tabla)
        if isinstance(responseStruct,Error):return responseStruct
        
        self.atributos['##_nombre_padre_struct_##']={'id':str(self.struc.id),'valor':''}
        
        if len(responseStruct) == len(self.struc.atributos):
            noparams = 0 #variable para conteo de parametros
            #self.atributos={}#diccionario de atributos de nuevo structo de la forma var = Struct(valores)
            for atributo in self.struc.atributos:
                #atributos pueden venir llamadas o primitivos
                #SI ES LLAMADA:
                if isinstance(atributo,Llamada):
                    #SI TIENE TIPO VERIFICO SI ES IGUAL
                    if responseStruct[noparams]['tipo']!=Tipo.NULO:
                        if atributo.id != responseStruct[noparams]['tipo']:return Error("SEMANTICO","TIPO INCORRECTO EN CONSTRUCCION DE STRUCT",self.fila,self.columna)   
                    #SI ESTA TODDO BIEN:
                    nuevoStruct=Strucs(atributo.id,atributo.parametros)
                    a=ConstruccionStruct(self.idvar,nuevoStruct,None,self.fila,self.columna)
                    #self.atributos={responseStruct[noparams]['id']:self.atributos}
                    self.atributos.update({responseStruct[noparams]['id']:None})
                    llamdaresp =a.ejecutar(arbol,tabla,self.atributos,responseStruct[noparams]['id'])
                    if isinstance(llamdaresp,Error):return llamdaresp
                    noparams+=1
                    continue
                    #aqui se agrega ya a diccionario
                resexp = atributo.ejecutar(arbol,tabla)
                if isinstance(resexp,Error):return resexp
                if responseStruct[noparams]['tipo'] != Tipo.NULO:
                    if responseStruct[noparams]['tipo'] == atributo.tipo:
                        self.atributos[responseStruct[noparams]['id']]={'valor':resexp,'tipo':responseStruct[noparams]['tipo'],'bandera':responseStruct[noparams]['bandera']}
                        #print(self.atributos)
                    else:
                        return Error("SEMANTICO","DATO -> "+str(resexp) +" PARA STRUCT ES INCORRECTO: ",self.fila,self.columna)
                    noparams +=1
                else:
                    self.atributos[responseStruct[noparams]['id']]={'valor':resexp,'tipo':atributo.tipo,'bandera':responseStruct[noparams]['bandera']}
                    #print(self.atributos)
                    noparams +=1       
        #   return atributos
        else:
            return Error("SEMANTICO","CANTIDAD DE ATRIBUTOS EN LLAMADA A STRUCT, ES INCORRECTA",self.fila,self.columna)
        
        if llave != None:
            prueba.update({llave:self.atributos})
            return None
        else:
            #print("STRUCT: "+str(self.atributos))
            simboleStruct=Simbolo(str(self.idvar),Tipo.STRUCT,self.atributos,self.fila,self.columna,Ambito.LOCAL,self.arreglo,self.structs,retornoStruct.mutable)
            retornoAsignacion = tabla.setSimboloEnTs(simboleStruct)
            if isinstance(retornoAsignacion,Error):return retornoAsignacion
            return None
        
        
        #if retornoStruct == None:
        #    return Error("SEMANTICO", "NO EXISTE STRUCT: "+str(self.idStruct),self.fila,self.columna)
        ##validar si no hay id's repetidos de atributos en declaracion de structs
        #responseStruct = retornoStruct.ejecutar(arbol,tabla)
        #if isinstance(responseStruct,Error):return responseStruct
        #
        #
        #if len(responseStruct) == len(self.expresiones):
        #    noParams=0
        #    
        #    laStructs={}#diccionario de atributos para variable de tipo struct
        #    laStructs['##_nombre_padre_struct_##']={'id':str(self.idStruct),'valor':''}
        #    for exp in self.expresiones:
        #        resExp = exp.ejecutar(arbol,tabla)
        #        if isinstance(resExp,Error): return resExp
        #        if responseStruct[noParams]['tipo'] != Tipo.NULO:
        #            if responseStruct[noParams]['tipo'] == exp.tipo:
        #                laStructs[responseStruct[noParams]['id']]={'tipo':responseStruct[noParams]['tipo'],'valor':resExp,'bandera':responseStruct[noParams]['bandera']}
        #                #laStructs[responseStruct[noParams]['id']]=Simbolo(str(self.idStruct),responseStruct[noParams]['tipo'],resExp,self.fila,self.columna,Ambito.LOCAL,False,False,retornoStruct.mutable)
        #            else:
        #                return Error("SEMANTICO","DATO -> "+str(resExp) +" PARA STRUCT ES INCORRECTO: ",self.fila,self.columna)
        #            noParams+=1
        #        else:
        #            if exp.tipo == Tipo.ARREGLO:
        #                laStructs[responseStruct[noParams]['id']]={'tipo':exp.tipo,'valor':resExp,'bandera':responseStruct[noParams]['bandera']}
        #                #laStructs[responseStruct[noParams]['id']]=Simbolo(str(self.idStruct),exp.tipo,resExp,self.fila,self.columna,Ambito.LOCAL,True,False,retornoStruct.mutable)
        #            else:
        #                laStructs[responseStruct[noParams]['id']]={'tipo':exp.tipo,'valor':resExp,'bandera':responseStruct[noParams]['bandera']}
        #                #laStructs[responseStruct[noParams]['id']]=Simbolo(str(self.idStruct),exp.tipo,resExp,self.fila,self.columna,Ambito.LOCAL,False,False,retornoStruct.mutable)
        #            noParams +=1
        #else:
        #    return Error("SEMANTICO","CANTIDAD DE ATRIBUTOS EN LLAMADA A STRUCT, ES INCORRECTA",self.fila,self.columna)
        #
        ##si todo salio bien se asigna el simbolo de tipo struct a la tabla de simbolos:
        #simboleStruct = Simbolo(str(self.idvar),Tipo.STRUCT,laStructs,self.fila,self.columna,Ambito.LOCAL,False,True,retornoStruct.mutable)
        #retornoAsignacion = tabla.setSimboloEnTs(simboleStruct)
        #if isinstance(retornoAsignacion,Error):return retornoAsignacion
        #
        #return None
      
        
    
    def getNode(self):
        nodoStruct = NodoArbol("Struct")
        return nodoStruct
    
class Strucs():
    def __init__(self,idStruct,atributos):
        self.id = idStruct
        self.atributos=atributos
            
            
            
            #0:
            # id=actor = {tipo: Actor, valor : cadena,entero,struct bandera=False}
            # id=pelicula = { }