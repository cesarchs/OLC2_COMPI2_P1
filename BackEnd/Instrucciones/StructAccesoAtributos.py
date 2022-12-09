

from Expresiones.primitivos import Primitivos
from Instrucciones.declaracion import Declaracion
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion


class StructAccesoAtributos(instruccion):
    def __init__(self, identificador,atributo,fila,columna):
        self.identificador =identificador
        self.atributo = atributo
        self.fila=fila
        self.columna=columna
        self.tipo=None

        
#estp es para obtener el valor de por ejemplo A que vale 4 y mostrarlo por ejemplo en print
    def interpretar(self, tree, table):

        if self.identificador=="length":
            
            return None



        simboloA = table.getTabla(self.identificador)
        if isinstance(simboloA, Excepcion):return simboloA

        if simboloA ==None:#no se encontro struct
            return Excepcion("Semantico","Error semantico, struct con nombre [ "+str(self.identificador)+" ] no exite! ",self.fila,self.columna)

        #print("\n\n\nentre >:v :::::::")
        #print("tipo de struct para "+str(self.identificador)+" : "+str(simboloA.valor.nombre))


        #print("nombre objeto/struct guardado en TS:"+str(simboloA.id))

        
        ash = simboloA.valor.tablaSimbolosFuncion.getTabla(self.atributo)#accedo  a la tabla simbolos de su valor y de ahi obtengo lo q me piden

        if isinstance(ash, Excepcion):return simboloA

        if ash ==None:#no se encontro struct
            return Excepcion("Semantico","Error semantico, atributo con nombre [ "+str(self.atributo)+" ] no exite en el objeto estipulado! ",self.fila,self.columna)

        #print("================"+str(ash.valor))
                
     

        #print("shjsahsajshja "+str(ash.tipo))

        self.tipo=ash.tipo

        return Primitivos(ash.tipo,ash.valor,ash.fila,ash.columna)



    def getNodo(self):
        nodo = NodoAST("ATRIBUTO STRUCT")
        nodo.agregarHijo(str(self.identificador))
        return nodo



