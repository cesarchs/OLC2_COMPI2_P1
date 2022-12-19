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

class AsignacionStruct(Instruccion):
    def __init__(self,idstruct,idatributo,exp, fila, columna):
        self.idstruct = idstruct
        self.idatributo = idatributo
        self.expresion = exp
        self.fila = fila
        self.columna = columna
        self.struct = True
    
    def compilar(self, arbol, tabla):
        #se valida expresion
        valExp = self.expresion.ejecutar(arbol,tabla)
        if isinstance(valExp,Error): return valExp
        
        structSimbolo = tabla.getSimboloEnTs(self.idstruct)
        if structSimbolo == None: return Error("SEMANTICO","STRUCT: "+self.idstruct+ " NO ESTA DECLARADO",self.fila,self.columna)
        #se valida que sea un struct sino f
        if not structSimbolo.getStruct(): return Error("SEMANTICO","ETIQUETA: "+self.idstruct+" no es un struct",self.fila,self.columna)
        
        #aqui hay que arreglar bug ya que no se estan guardando bien si son mutables o no, encontrar la validacion correcta
        #EMPEZAR A DEBUGUEAR DESDE DECLARACIONES Y YA CON ESO SALIO
        #GRACIAS DIOS!!!!!!!!!!!!!!!!!!!!!!!!!!
        if not structSimbolo.getMuta(): return Error("SEMANTICO","STRUCT INMUTABLE",self.fila,self.columna)
        
        #SE INTENTA CAMBIAR EL VALOR DE ATRIBUTO
        dictaux = structSimbolo.getValor()
        for llave in self.idatributo:
            if llave in dictaux:
                dictaux = dictaux[llave]
                if llave == self.idatributo[-1]:
                    if 'valor' in dictaux:
                        if 'tipo' in dictaux:
                            if self.expresion.tipo != dictaux['tipo']:
                                if not dictaux['bandera']: return Error("SEMANTICO","ATRIBUTO EN STRUCT NO PUEDE CAMBIAR TIPO",self.fila,self.columna)
                                #si la bandera si esta en true entonces se procede al cambio de tipo y valor
                                dictaux['valor'] = valExp
                                dictaux['tipo'] = self.expresion.tipo
                            else:
                                dictaux['valor'] = valExp   
                        #return dictaux['valor']  #este seria el valor
                    
                        else:
                            return Error("SEMANTICO","ATRIBUTO: "+str(self.idatributo)+"NO EXISTE EN STRUCT",self.fila,self.columna)
                    else:
                        return Error("SEMANTICO","ATRIBUTO: "+str(self.idatributo)+"NO EXISTE EN STRUCT",self.fila,self.columna)
                else:
                    dictaux = dictaux['valor']
            else: 
                return Error("SEMANTICO","ATRIBUTO: "+str(self.idatributo)+"NO EXISTE EN STRUCT",self.fila,self.columna)
        
        return None
        
        
        #try:
        #    if self.expresion.tipo != structSimbolo.getValor()[self.idatributo]['tipo']:#se valida que si se quiere asignar otro tipo tenga la bandera true
        #        if not structSimbolo.getValor()[self.idatributo]['bandera']: return Error("SEMANTICO","ATRIBUTO EN STRUCT NO PUEDE CAMBIAR TIPO",self.fila,self.columna)
        #        #si la bandera si esta en true entonces se procede al cambio de tipo y valor
        #        structSimbolo.getValor()[self.idatributo]['valor']=valExp
        #        structSimbolo.getValor()[self.idatributo]['tipo']=self.expresion.tipo
        #    else:
        #        structSimbolo.getValor()[self.idatributo]['valor']=valExp
        #        
        #except:
        #    return Error("SEMANTICO","ATRIBUTO NO PERTENECE A STRUCT",self.fila,self.columna)
        #
        #return None
        
    
    def getNode(self):
        nodoStruct = NodoArbol("Struct_Asignacion")
        nodoStruct.agregarHijoSinNodo(str(self.idstruct))
        nodoStruct.agregarHijoSinNodo(str(self.idatributo))
        nodoStruct.agregarHijoSinNodo(str(" = "))
        nodoStruct.agregarHijoConNodo(self.expresion.getNode())
        
        return nodoStruct