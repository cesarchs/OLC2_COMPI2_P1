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

class AccesoStruct(Instruccion):
    def __init__(self,idstruct,idatributo, fila, columna):
        self.idstruct = idstruct
        self.idatributo = idatributo
        self.fila = fila
        self.columna = columna
        self.tipo = None
    
    def compilar(self, arbol, tabla):
        #print("")
        simboloStruct = tabla.getSimboloEnTs(self.idstruct)
        
        #se valida que exissta el ID
        if simboloStruct == None: return Error("SEMANTICO","ETIQUETA: "+str(self.idstruct)+" NO EXISTE",self.fila,self.columna)
        #SE VALIDA QUE EL ID SI EXISTE SEA DE TIPO STRUCT
        if not simboloStruct.getTipo()==Tipo.STRUCT: return Error("SEMANTICO","ETIQUETA: "+str(self.idstruct)+" NO ES UN STRUCT",self.fila,self.columna)

        dictaux = simboloStruct.getValor()# aqui obteners el dict principal, creo
        self.mutable=simboloStruct.mutable
        self.arreglo=False
        self.struct = True
        for llave in self.idatributo:
            if llave in dictaux:
                dictaux = dictaux[llave]
                if llave == self.idatributo[-1]:
                    if 'valor' in dictaux:
                        self.tipo = dictaux['tipo']
                        return dictaux['valor']  #este seria el valor
                    else:
                        return self.desempaquetarvalor(dictaux)
                else:
                    dictaux = dictaux['valor']
            else: 
                return Error("SEMANTICO","ATRIBUTO: "+str(self.idatributo)+"NO EXISTE EN STRUCT",self.fila,self.columna)
        
        return None

        
    
    def getNode(self):
        nodoStruct = NodoArbol("AccesoStruct")
        nodoStruct.agregarHijoSinNodo(str(self.idstruct))
        nodoStruct.agregarHijoSinNodo(str(self.idatributo))
        return nodoStruct
    
    def getTipo(self, val):
        if isinstance(val,int):
            return Tipo.ENTERO
        elif isinstance(val,float):
            return Tipo.DECIMAL
        elif isinstance(val,bool):
            return Tipo.BOOLEANO
        elif isinstance(val,list):
            return Tipo.ARREGLO
        return Tipo.CADENA
    
    def desempaquetarvalor(self,diccionario):
        valor =""
        tamano=1
        valor=str(diccionario['##_nombre_padre_struct_##']['id'])+"("
        for key in diccionario:
            if key!='##_nombre_padre_struct_##' and isinstance(diccionario[key],dict) and '##_nombre_padre_struct_##' in diccionario[key]: 
                valor+=self.desempaquetarvalor(diccionario[key])
                tamano+=2
                continue
            if  diccionario[key]['valor'] != '':
                if isinstance(diccionario[key]['valor'],dict):
                    valor+= self.desempaquetarvalor(diccionario[key]['valor'])
                    tamano+=1
                else:
                    valor += str(diccionario[key]['valor'])
                    if tamano <= len(diccionario):valor += ','
            tamano+=1
        valor+=")"
        return valor