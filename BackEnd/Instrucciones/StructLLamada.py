

from Abstract.NodoAST import NodoAST
from Instrucciones.FuncionSimple import FuncionSP
from posixpath import normcase
from Instrucciones.Break import Break
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import tipo
from TS.TablaSimbolo import TablaSimbolos
from TS.Simbolo import Simbolo

class LlamadaStruct(instruccion):
            
    def __init__(self,nombre,parametros,fila,columna ):
        self.nombre=nombre
        self.parametros = parametros #expresiones
        self.fila=fila
        self.columna=columna
        self.arreglo =False


    def interpretar(self, tree, table):
        #obtener la funcion en el ast
        result = tree.getStruct(self.nombre)

        if result ==None:#no se encontro struct
            
            
            return Excepcion("Semantico","Error semantico, struct [ "+str(self.nombre)+" ] para creacion no exite! ",self.fila,self.columna)

        nuevaTabla =TablaSimbolos(tree.getTablaSimbolosGlobal())#creamos un nueva tabla de simbolos para este ambito creo
        #pero debe de ser la de la tabla de simbolos y obtenerla de la llamada de funcion
        #pasamos en la tabla a pasar lo de la anterior para q no se pierda nada;ya q con ackermann se perdia info y no se pasaba



        #OBTENER PARAMS: hay q modificarla TuT pero valera la pena :D
        #comprobamos si el tam de params es igual al de la funcion
        if len(result.instrucciones)==len(self.parametros):



            #tengo q validar sino esta en la blackList de atributos del struct



            contador=0#para validar q sean del mismo tipo
            for expresion in self.parametros:#se obtiene el valor de param en la llamada

                resultExpresion = expresion.interpretar(tree,table)#obtener los params de la tabla que nos trae el metodo interpretar 
                #porq estamos en el abito de la llamada pero los nuevos valores se van a meter en la tabla simbolos global ;para q no se pierdan nuestras variables
                
                
                
                if isinstance(resultExpresion, Excepcion):return resultExpresion
                

                #validar q sean del mismo tipo
                #JULIA ['tipo'] DEBO DE CAMBIARLO JAVIER PORQ NO LO LLEVA
                if result.instrucciones[contador].tipo==expresion.tipo or result.instrucciones[contador].tipo==tipo.NULO :
                    #creacion de simbolo e ingresarlo a la tabla de simbolos

                    TypeNull=False#me va aservir si viene un param con atributo nothing, debido a que asi se concibio en los params de la funcion

                    if result.instrucciones[contador].tipo==tipo.NULO:
                        TypeNull=True


                        #print("\n\nKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK\n\n")
                        #print("en mis params de STRUCT->  "+str(result.instrucciones[contador].tipo))
                        #print("en mis params de CREACION->  "+str(self.parametros[contador].tipo))

                        simbolo = Simbolo(str(result.instrucciones[contador].identificador),self.parametros[contador].tipo,self.arreglo ,self.fila,self.columna,resultExpresion)
                        resultTablaS = nuevaTabla.setTabla(simbolo)#lo metemos a la tabla simbolos
                        if isinstance(resultTablaS,Excepcion): return resultTablaS#por si hubo error

                        #print("\n\nKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")


                    if TypeNull==False:

                        simbolo = Simbolo(str(result.instrucciones[contador].identificador),result.instrucciones[contador].tipo,self.arreglo  ,self.fila,self.columna,resultExpresion)
                        resultTablaS = nuevaTabla.setTabla(simbolo)#lo metemos a la tabla simbolos
                        if isinstance(resultTablaS,Excepcion): return resultTablaS#por si hubo error

                else:
                    return Excepcion("Semantico","tipo de datos diferente en Parametros de CREACION STRUCT", self.fila,self.columna)
                
                
                contador+=1


        else: 
            return Excepcion("Semantico","Error semantico, STRUCT [ "+str(self.nombre)+" ] tiene un numero de PARAMETROS incorrectos! ",self.fila,self.columna)

        #como si encontro la funcion entonces tenemos q interpretar
        value = result.interpretar(tree, nuevaTabla)#ejecutar la funcion; enviamos la nueva tabla a la funcion para q no se pierdan los datos
        if isinstance(value, Excepcion):return value
        #si no es error tonces lo q podemos pasar en la llamada venga como expresion tmabien le tenemos q asignar tipo

        self.tipo = result.tipoS        #sacrificio para obtener la funciones expresion de una           0=mutable    1=inmutable

        

        value.tablaSimbolosFuncion = nuevaTabla
        
        return value#sacrificio para obtener la funciones y expresion de una


#video 11 modifico la llamada debido aque aqui si los params alteran la cosa no como en la funcion q ahi solo se definen





    def getNodo(self):
        nodo = NodoAST("CREACION DE STRUCT")
        nodo.agregarHijo(str(self.nombre))#PUEDE COMO NO PUEDE VENIR JAVIER
        parametros = NodoAST("PARAMETROS")
        #VIDEO 15 MIN 51:40
        for param in self.parametros:
            parametros.agregarHijoNodo(param.getNodo())
        nodo.agregarHijoNodo(parametros)
        
        return nodo

        