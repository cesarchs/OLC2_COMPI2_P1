
from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol
from almacenar.tipo import OpsAritmetico,Tipo,Ambito
from almacenar.error import Error
from almacenar.simbolo import Simbolo

#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol
#from almacenar.tipo import OpsAritmetico,Tipo,Ambito
#from almacenar.error import Error
#from almacenar.simbolo import Simbolo

import copy


class CopiarArreglo(Instruccion):
    def __init__(self, identificadorI, identificadorD,fila, columna):
        self.identificadorI = identificadorI
        self.identificadorD = identificadorD
        self.fila = fila
        self.columna = columna
        self.arreglo=True
        self.struct = False
        self.mutable = False
    
    def compilar(self, arbol, tabla):
        #se busca el id del arreglo que se desea copiar
        arraysimbolo=tabla.getSimboloEnTs(self.identificadorD)
        #se valida si existe:
        if arraysimbolo == None:
            return Error("SEMANTICO","ARREGLO: "+self.identificadorD+ "NO ESTA DECLARADO",self.fila,self.columna)
        #se valida que sea de tipo arreglo
        if not arraysimbolo.getArreglo():
            return Error("SEMANTICO", "ETIQUETA: "+self.identificadorD+" no es un arreglo",self.fila,self.columna)       
        #se hace un nuevo simbolo:
        try:
            arraycopia=copy.deepcopy(arraysimbolo.getValor())
        except:
            Error("SEMANTICO", "No se pudo copiar el arreglo: ",self.identificadorD, "a etiqueta: ",self.identificadorI,self.fila,self.columna)
        nuevoArreglo=Simbolo(self.identificadorI,Tipo.ARREGLO,arraycopia,self.fila,self.columna,Ambito.LOCAL,self.arreglo,False,False)
        guardarentabla=tabla.setSimboloEnTs(nuevoArreglo)
        if isinstance(guardarentabla,Error):return guardarentabla #aqui si dicen que si se puede volver a usar el mismo id solo se actualiza en ts
        return None
        
    def getNode(self):
        nodoCopy= NodoArbol("COPIAR_ARREGLO")
        nodoCopy.agregarHijoSinNodo(str(self.identificadorI))
        nodoCopy.agregarHijoSinNodo(" : ")
        nodoCopy.agregarHijoSinNodo(str(self.identificadorD))
        return nodoCopy