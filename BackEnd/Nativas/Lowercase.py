

from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Return2 import ReturnC3D
from TS.Simbolo import Simbolo
from TS.Tipo import tipo
from Instrucciones.FuncionSimple import FuncionSP


class Lowercase(FuncionSP):#PARA ESTA NO SE AGREGA PRODUCCION SOLO EN LOS FOR DE LAS PASADAAS 
            
    def __init__(self,nombre,parametros,instrucciones,fila,columna ):
        self.nombre=nombre      #self.nombre=nombre.lower()#para ayudar en las funciones
        self.parametros=parametros#es un diccionario
        self.instrucciones=instrucciones
        self.fila=fila
        self.columna=columna
        self.tipo=tipo.NULO#valor de return de una funcion


    def interpretar(self, tree, table):

        #ya esta definido q sea un Lowercase q reciba la cadena y  la pase a MAYUSCULAS
        simbolo = table.getTabla("toLower##Param1")#para q no choque con otra variable ya existente en la tabla de simbolos
        if simbolo==None: return Excepcion("Semantico","No se encontro el parametro de Lowercase",self.fila,self.columna)
                    
        if simbolo.getTipo()!=tipo.CADENA:
            return Excepcion("Semantico","Solo cadenas pueden ser el parametro de Lowercase",self.fila,self.columna)
                    
        #ya tenemos una cadena para poner en mayusculas

        self.tipo=simbolo.getTipo()
        return simbolo.getValor().lower()#aqui cabal lo devolvemos en mayuscula la cadena 




    def compilar(self, tree, table):
        #ya esta definido q sea un Lowercase q reciba la cadena y  la pase a MAYUSCULAS
        simbolo = table.getTabla("toLower##Param1")#para q no choque con otra variable ya existente en la tabla de simbolos
        if simbolo==None: return Excepcion("Semantico","No se encontro el parametro de Lowercase",self.fila,self.columna)
                    
        if simbolo.getTipo()!=tipo.CADENA and simbolo.getTipo()!=tipo.CHARACTER:
            return Excepcion("Semantico","Solo cadenas pueden ser el parametro de Lowercase",self.fila,self.columna)
                    
        
        self.tipo=simbolo.getTipo()
        anderson = simbolo.getValor()

        genAux = Generator()
        generator = genAux.getInstance()
        generator.addCommit("-------------LOWERCASE CADENA -------------")

        #1- return
        #2- cadena a to lowercase

        generator.fLowerString()

        return False#para q en llamada de funcion retorne el valor de la funcion nativa lowercase