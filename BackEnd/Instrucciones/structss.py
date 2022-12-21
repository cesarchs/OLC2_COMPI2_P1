from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol
from almacenar.error import Error
from almacenar.simbolo import Simbolo
from almacenar.tipo import Ambito, Tipo

#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol
#from almacenar.error import Error
#from almacenar.simbolo import Simbolo
#from almacenar.tipo import Ambito, Tipo

class NuevoStruct(Instruccion):
    def __init__(self,idstruct,atributos, muta,fila, columna):
        self.idStruct = idstruct
        self.atributos = atributos
        self.mutable = muta
        self.fila = fila
        self.columna = columna
        self.tipo = Tipo.NULO
 
    
    def compilar(self, arbol, tabla):
        listaParam=[]
        for atributo in self.atributos:
            var={'id':atributo.id,'tipo':atributo.tipo,'bandera':atributo.cambiaTipo }
            if not var in listaParam:
                listaParam.append(var)
            else:
                return Error("SEMANTICO","ids de atributos en struct repetidos",self.fila,self.columna)
        #simboloStruct = Simbolo(self.idStruct,Tipo.STRUCT,listaParam,self.fila,self.columna,Ambito.LOCAL,self.arreglo,self.struct,self.mutable)
        #resultadoAsig = tabla.setSimboloEnTs(simboloStruct)
        #if isinstance(resultadoAsig,Error): return resultadoAsig
        #return None
        return listaParam
    
    def getNode(self):
        nodoStruct = NodoArbol("Struct")
        if self.mutable:
            nodoStruct.agregarHijoSinNodo(str("mutable"))
        nodoStruct.agregarHijoSinNodo(str(self.idStruct))    
        nodoatributos = NodoArbol("atributos")
        for atributo in self.atributos:
            nodoatributos.agregarHijoSinNodo(str(atributo.id))
        nodoStruct.agregarHijoConNodo(nodoatributos)
        return nodoStruct
    
class AtributosStruct():
    def __init__(self,id,tipo,cambiaTipo):
        self.id = id
        self.tipo = tipo
        self.cambiaTipo = cambiaTipo
    
    def getId(self):
        return self.id
    
    def getTipo(self):
        return self.tipo
    
    def getBandera(self):
        return self.cambiaTipo
    
    def setId(self,id):
        self.id = id
        
    def setTipo(self,tipo):
        self.tipo=tipo
        
    def setBandra(self,bandera):
        self.cambiaTipo=bandera
        
#coloco esto por que necesito mandar un cambio desde instruccines para que se guarde el cambio de nombre
# a la carpeta en el repo,, buenoooooo eso espero xd