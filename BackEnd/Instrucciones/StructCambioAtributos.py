

from TS.Simbolo import Simbolo
from Expresiones.primitivos import Primitivos
from Instrucciones.declaracion import Declaracion
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion


class StructCambioAtributos(instruccion):
    def __init__(self, identificador,atributo,expresion,fila,columna):
        self.identificador =identificador
        self.atributo = atributo
        self.expresion=expresion
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



        if simboloA.valor.tipoS==1:
            value = self.expresion.interpretar(tree,table) #valor a asignar a la variable

            #por si tenemos un error en lo anterior
            if isinstance(value, Excepcion): return value#lo retornamos



            #ash = simboloA.valor.tablaSimbolosFuncion.getTabla(self.atributo)#accedo  a la tabla simbolos de su valor y de ahi obtengo lo q me piden

            

            simbolo = Simbolo(self.atributo,self.expresion.tipo,False, self.fila,self.columna,value)#buscar si esta en la tabla y se modifica ahi, sino entra en if isinstance(result,Excepcion): 
            

            simboloA.valor.tablaSimbolosFuncion.actualizarTabla(simbolo)

    

            return None
        else:
            return Excepcion("Semantico","Error semantico, tipo de struct["+str(simboloA.valor.nombre)+"] no es mutable ",self.fila,self.columna)
                            



    def getNodo(self):
        nodo = NodoAST("ATRIBUTO STRUCT ASIGNACION")
        nodo.agregarHijo(str(self.identificador))
        return nodo



