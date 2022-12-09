

from Expresiones.primitivos import Primitivos
from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Return2 import ReturnC3D
from TS.Tipo import tipo
from Instrucciones.FuncionSimple import FuncionSP


class Length(FuncionSP):#PARA ESTA NO SE AGREGA PRODUCCION SOLO EN LOS FOR DE LAS PASADAAS 
            
    def __init__(self,nombre,parametros,instrucciones,fila,columna ):
        self.nombre=nombre      #self.nombre=nombre.lower()#para ayudar en las funciones
        self.parametros=parametros#es un diccionario
        self.instrucciones=instrucciones
        self.fila=fila
        self.columna=columna
        self.tipo=tipo.NULO#valor de return de una funcion


    def interpretar(self, tree, table):

        #ya esta definido q sea un Lowercase q reciba la cadena y  la pase a MAYUSCULAS
        simbolo = table.getTabla("longitudArray##Param1")#para q no choque con otra variable ya existente en la tabla de simbolos
        if simbolo==None: return Excepcion("Semantico","No se encontro el parametro de Length",self.fila,self.columna)
                    
        if simbolo.getTipo()!=tipo.ARREGLO:
            return Excepcion("Semantico","Solo IDs de arreglos pueden ser el parametro de Length",self.fila,self.columna)
                    
        #ya tenemos una cadena para poner en mayusculas

        self.tipo=tipo.ENTERO

        #print("AAAAAASSSSSSSSSSSSSSSSHHHHHHHHHHHHHH")
        #print(str(len(simbolo.getValor())))
        #print(str(self.tipo))


        if isinstance(simbolo.getValor(), Primitivos):
            value = simbolo.getValor().interpretar(tree,table)
            if isinstance(value, Excepcion):return value

            return len(value)




        return len(simbolo.getValor())#aqui cabal lo devolvemos en mayuscula la cadena 



    def compilar(self, tree, table):
        #ya esta definido q sea un Lowercase q reciba la cadena y  la pase a MAYUSCULAS
        simbolo = table.getTabla("longitudArray##Param1")#para q no choque con otra variable ya existente en la tabla de simbolos
        if simbolo==None: return Excepcion("Semantico","No se encontro el parametro de Length",self.fila,self.columna)
                    
        if simbolo.getTipo()!=tipo.ARREGLO:
            return Excepcion("Semantico","Solo IDs de arreglos pueden ser el parametro de Length",self.fila,self.columna)
                    
        #ya tenemos una cadena para poner en mayusculas

        self.tipo=tipo.ENTERO#porq devuelvo la longitud del array q es un INT

        genAux = Generator()
        generator = genAux.getInstance()#el q me hara el paro en todo
        generator.addCommit("~~~~TAM DE UN ARRAY~~~~")

        #1- return
        #2- posicion en heap q tiene el tam


        generator.fLength()

        #len = generator.addTemporal()
        #generator.getHeap(len,simbolo.valor.valor)


        return False#ReturnC3D(len,tipo.ENTERO,True)#aqui cabal lo devolvemos en mayuscula la cadena