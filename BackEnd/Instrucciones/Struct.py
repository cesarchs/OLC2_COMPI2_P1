from Instrucciones.declaracion import Declaracion
from Instrucciones.Continue import Continue
from Abstract.NodoAST import NodoAST
from Instrucciones.Return import Return
from Instrucciones.Break import Break
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Tipo import tipo
from TS.TablaSimbolo import TablaSimbolos
from TS.Simbolo import Simbolo

class Struct(instruccion): #           id,cuerpo,tipo,fila,columna
            
    def __init__(self,nombre,instrucciones,tipoS,fila,columna ):
        self.nombre=nombre      
        self.tipoS=tipoS#     0=mutable pueden cambiar        1=inmutable no pueden cambiar despues de su creacion
        self.instrucciones=instrucciones
        self.fila=fila
        self.columna=columna
        
        self.tablaSimbolosFuncion=None

        self.instruccionesMalas=[]
        
        
        #self.tipo=tipo.NULO#valor de return de una funcion


    def interpretar(self, tree, table):

        nuevaTabla =TablaSimbolos(table)#creamos un nueva tabla de simbolos para este ambito creo
        self.tablaSimbolosFuncion = nuevaTabla

        if self.tipoS==0:
            print("-----------MUTABLE-----------")
        else:
            print("-----------INMUTABLE-----------")

        indice =0
        for instruccion in self.instrucciones:#recorre sus instrucciones


            if isinstance(instruccion, Declaracion):#en struct solo declaraciones deben de haber sino F
                value=instruccion.interpretar(tree,nuevaTabla)#si hay errores los guardamos
                if isinstance(value, Excepcion):
                    tree.getExcepciones().append(value)
                    tree.updateConsola(value.toString(),1)



                if value==None:#en struct solo declaraciones deben de haber sino F
                    print("---desde struct ---")
                    print(str(instruccion.identificador))
                    #print(str(instruccion.tipo))#validar si es un typo de struct el instruccion.tipo|tipo.ALGO
                    


                    if instruccion.tipo==tipo.ENTERO or instruccion.tipo==tipo.CADENA or instruccion.tipo==tipo.CHARACTER or instruccion.tipo==tipo.DECIMAL or instruccion.tipo==tipo.NULO or instruccion.tipo==tipo.ARREGLO or instruccion.tipo==tipo.BOOLEANO:
                        print(str(instruccion.tipo))


                    else:
                        print("TIPO STRUCT A VALIDARSE")
                        result = tree.getStruct(instruccion.tipo)
                        if result ==None:#no se encontro la funcion
                            error= Excepcion("Semantico","Error semantico, tipo dato struct["+str(instruccion.tipo)+"],  en struct [ "+str(self.nombre)+" ] no exite! ",instruccion.fila,instruccion.columna)
                            tree.getExcepciones().append(error)
                            tree.updateConsola(error.toString(),1)

                            self.instruccionesMalas.append(instruccion)

                            print("TIPO STRUCT NO EXISTE (T.T)")

                        else:print("TIPO STRUCT EXISTE (*u*)")


                    print(">>>>>"+str(indice))
                    print("-------------------")
                    

                    indice+=1

                    
                else:
                    error = Excepcion("Semantico","Error semantico en struct, recuerde solo declararse puede en el struct",instruccion.fila,instruccion.columna)
                    tree.getExcepciones().append(error)
                    tree.updateConsola(error.toString(),1)


            else:
                error = Excepcion("Semantico","Error semantico en struct, recuerde solo declaraciones pueden haber en un STRUCT y con tipos reales",instruccion.fila,instruccion.columna)
                tree.getExcepciones().append(error)
                tree.updateConsola(error.toString(),1)

        print("instrucciones malas:"+str(len(self.instruccionesMalas)))
        print("\n")

        #self.tablaSimbolosFuncion = nuevaTabla
        return self





    def tipeof(self,num):
        
        switch={

        "tipo.ENTERO":'Int64',
        "tipo.DECIMAL":'Float64',
        "tipo.BOOLEANO":'Bool',
        "tipo.CHARACTER":'Char',
        "tipo.CADENA":'String',
        "tipo.NULO":'Nothing',
        "tipo.ARREGLO":'Arreglo'

        }

        return switch.get(num,"Invalid input")

        

    def getNodo(self):
        nodo = NodoAST("STRUCT")
        nodo.agregarHijo(str(self.nombre))#PUEDE COMO NO PUEDE VENIR JAVIER


        instrucciones = NodoAST("INSTRUCCIONES")

        for instr in self.instrucciones:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        
        return nodo





















#[VIDEO 10]-------------------------------------------
#min 4 video para saber guardar funciones
#min 48 video para saber llamarlas
#-----------------------------------------------------

#video 11 ya hago lo de params






            