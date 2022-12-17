from almacenar.error import Error
from almacenar.generador import Generador
from almacenar.tipo import Return, Tipo
from padres.expresion import Expresion
from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol

#from almacenar.error import Error
#from almacenar.tipo import Tipo
#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol

class Identificador(Expresion):
    def __init__(self, id,fil, col):
        super().__init__(fil, col)
        self.identificador = id
        self.fila = fil
        self.columna = col 
        self.tipo=None
        self.struct = False
        self.mutable = False
    
    def compilar(self, arbol, tabla):
        genAux = Generador()
        generador = genAux.getInstance()
        
        generador.agregarComentario("ACCESO A VARIABLE")
    
        simbolo = tabla.getSimboloEnTs(self.identificador)
        if simbolo == None:
            return Error('SEMANTICO','Identificador: '+self.identificador+' no ah sido declarado',self.fila,self.columna)  
        
        
        if simbolo.arreglo == True:
            indice=generador.agregarTemporal();generador.liberarTemporal(indice)
            if not simbolo.esGlobal:
                tempPos = generador.agregarTemporal();generador.liberarTemporal(tempPos)
                generador.addExp(tempPos,'P',simbolo.posicion,'+')
                generador.getPila(indice,tempPos)
            else:
                generador.getPila(indice,simbolo.posicion)
            #indice = generador.agregarTemporal();generador.liberarTemporal(indice)
            #generador.getHeap(indice,h)
            r = Return(indice,Tipo.ARREGLO,True)
            r.dimensionesenacceso=simbolo.dimensiones
            r.dimensiones=simbolo.dimensiones
            r.array=simbolo.array
            r.auxTipo=simbolo.tipo
            return r












        #temporal para guardar variable
        temp = generador.agregarTemporal()
        
        #obtencion de posicion de la variable
        #tempPos = simbolo.posicion
        if not simbolo.esGlobal:
            tempPos = generador.agregarTemporal();generador.liberarTemporal(tempPos)
            generador.addExp(tempPos,'P',simbolo.posicion,'+')
            generador.getPila(temp,tempPos)
        else:
            generador.getPila(temp,simbolo.posicion)
        
        if simbolo.tipo != Tipo.BOOLEANO:
            generador.agregarComentario("FIN ACCESO A VARIABLE")
            generador.agregarSalto()
            self.tipo = simbolo.tipo
            return Return(temp, simbolo.tipo, True)
        
        if self.trueLbl == '':
            self.trueLbl = generador.agregarLabel()
        if self.falseLbl == '':
            self.falseLbl = generador.agregarLabel()
            
        generador.agregarIf(temp,'1','==',self.trueLbl)
        generador.agregarGoto(self.falseLbl)
        
        generador.agregarComentario("FIN ACCESO A VARIABLE")
        generador.agregarSalto()
        
        ret = Return(None,Tipo.BOOLEANO,False)
        ret.trueLbl = self.trueLbl
        ret.falseLbl = self.falseLbl
        self.tipo = simbolo.tipo
        return ret
        
        
        
       # self.tipo = simbolo.getTipo()
       # if simbolo.getValor() != None or simbolo.tipo==Tipo.NULO: #imbolo.tipo!=Tipo.NULO:
       #     #if simbolo.getTipo()==Tipo.STRUCT:
       #     #    manipularValStruct=simbolo.getValor()
       #     #    tamano=1
       #     #    valor=str(manipularValStruct['##_nombre_padre_struct_##']['id'])+"("
       #     #    for key in manipularValStruct:
       #     #        tamano+=1
       #     #        if  manipularValStruct[key]['valor'] != '':
       #     #            valor += str(manipularValStruct[key]['valor'])
       #     #            if tamano <= len(manipularValStruct):valor += ','
       #     #    valor+=")"
       #     #    return valor
       #     self.mutable = simbolo.getMuta()
       #     self.struct = simbolo.getStruct()
       #     return simbolo.getValor()
       # else:
       #     return Error('SEMANTICO','IDENTIFICADOR: '+self.identificador+' FUE DECLARADO PERO NO SE DEFINIO VALOR',self.fila,self.columna)
    
    def getNode(self):
        nodoId = NodoArbol("ID") #NOMBRE PADRE
        nodoId.agregarHijoSinNodo(str(self.identificador))#valor del ID      
        return nodoId
