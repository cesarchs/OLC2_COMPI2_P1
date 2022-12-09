
from typing import List
from Expresiones.primitivos import Primitivos
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Return2 import ReturnC3D
from TS.Tipo import tipo
from TS.Simbolo import Simbolo

class Asignacion(instruccion):# es como un nodo y se arma el arbol con estos nodos

                    
    def __init__(self,identificador , expresion, fila, columna ):
        self.identificador=identificador
        self.expresion=expresion
        self.fila=fila
        self.columna=columna
        self.arreglo=False
        self.cuerpoSiesArray=None

        self.C3D=""
        self.TMP=""
        self.posicionInSTACKoHEAP=None


    def interpretar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)
        #id ya esta definido tonces obtenemos el valor de la expresion
        value = self.expresion.interpretar(tree,table) #valor a asignar a la variable

        #por si tenemos un error en lo anterior
        if isinstance(value, Excepcion): return value#lo retornamos


        if self.expresion.tipo==tipo.ARREGLO:
            #print("~~~~~~~~~~~~~~~~~~OHHHH YEAHHH~~~~~~~~~~~~~~~~~~")
            #print(str(value))
            self.cuerpoSiesArray=value
            self.arreglo=True


            #PENSABA AQUI SUMARLE +1 PARA SABER LAS DIMENSIONES DEL ARRAY       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



        #obtener el simbolo de la variable en tabla simbolos
        

        #                       identificador, tipo, fila, columna, valor
        simbolo = Simbolo(self.identificador,self.expresion.tipo,self.arreglo, self.fila,self.columna,value)#buscar si esta en la tabla y se modifica ahi, sino entra en if isinstance(result,Excepcion): 
        

        result = table.actualizarTabla(simbolo)#lo modifico o no lo hizo 

        #si entro aqui entonces no existe en la tabla de simbolos por ende la creo y la meto en la tabla simbolos
        if isinstance(result,Excepcion): 
            #como no existe en la tabla lo creo y guardo
            table.setTabla(simbolo)#fijo la creo y la guardo
            #return result
            return None


        return None

        #tree.updateConsola(simbolo)#esto es semantico falta conbinarlo con lo lexico y sintactico VIDEO 4-> 1:44:54s
        

    def getNodo(self):
        
        if self.arreglo==True:
            nodo = NodoAST("ASIGNACION")
            nodo.agregarHijo(str(self.identificador))
            parametros = NodoAST("LISTA ELEMENTOS")
            if isinstance(self.cuerpoSiesArray,ReturnC3D):
                return nodo
                
            for param in self.cuerpoSiesArray:
                try:
                    parametros.agregarHijoNodo(param.getNodo())
                except:
                    parametros.agregarHijoNodo(str(param))

            nodo.agregarHijoNodo(parametros)
            return nodo

        else:
            nodo = NodoAST("ASIGNACION")
            nodo.agregarHijo(str(self.identificador))
            nodo.agregarHijoNodo(self.expresion.getNodo())
            return nodo





    #ARRAY[][]=?;
    
    def compilar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)
        #id ya esta definido tonces obtenemos el valor de la expresion

        genAux = Generator()
        generator = genAux.getInstance()

        generator.addCommit("------------Compilacion de valor de variable, falta un para None-------------")
        
        value = self.expresion.compilar(tree,table) #valor a asignar a la variable
        generator.addCommit("-------------------Fin de valor de variable---------------------")

        #por si tenemos un error en lo anterior
        if isinstance(value, Excepcion): return value#lo retornamos


        if self.expresion.tipo==tipo.ARREGLO:
            #print("~~~~~~~~~~~~~~~~~~OHHHH YEAHHH~~~~~~~~~~~~~~~~~~")
            #print(str(value))
            self.cuerpoSiesArray=value
            self.arreglo=True

        simbolo = Simbolo(self.identificador,value.tipo,self.arreglo, self.fila,self.columna,value,0,(value.tipo == tipo.CADENA or value.tipo == tipo.ARREGLO))#buscar si esta en la tabla y se modifica ahi, sino entra en if isinstance(result,Excepcion): 
        
        if isinstance(value.valor,str):
            simbolo.index=value.index
        else:
            simbolo.index=value.valor
        result,newVar = table.actualizarTabla(simbolo)#lo modifico o no lo hizo 
        
        
        #si entro aqui entonces no existe en la tabla de simbolos por ende la creo y la meto en la tabla simbolos
        if isinstance(result,Excepcion): 
            #como no existe en la tabla lo creo y guardo
            result,newVar = table.setTabla(simbolo)#fijo la creo y la guardo
            #return result
            #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            # Obtencion de posicion de la variable
            tempPos = newVar.size

            #print(":::::::::::::::::::::::::::::::::::::::::::::::::::: no hay tabla simbolos anterior?"+str(newVar.global1)+"::::::::::::::::::::::::::::::::::\n")

            if(not newVar.global1):#si hay otra tabla de simbolos entro aqui
                tempPos = generator.addTemporal()
                #print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
                generator.addExp(tempPos, 'P', newVar.size, "+")
            
            if(value.tipo == tipo.BOOLEANO):
                tempLbl = generator.newLabel()
                
                generator.inputLabel(value.trueLbl)
                generator.setStack(tempPos, "1")
                
                generator.addGoto(tempLbl)

                generator.inputLabel(value.falseLbl)
                generator.setStack(tempPos, "0")

                generator.inputLabel(tempLbl)
            else:
                generator.setStack(tempPos, value.valor)
            generator.addSaltoLinea()


            #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            return None

        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        # Obtencion de posicion de la variable
        tempPos = newVar.size
        if(not newVar.global1):#ME DA MIEDO LO DE GLOBAL1 QUE LO IMPLEMENTO EL AUX A COMPARACION DE QUE YO MUEVO Y MUEVO EN TS HASTA HALLAR LA VARIABLE "GLOBAL"
            tempPos = generator.addTemporal()
            generator.addExp(tempPos, 'P', newVar.size, "+")
        
        if(value.tipo == tipo.BOOLEANO):
            tempLbl = generator.newLabel()
            
            generator.inputLabel(value.trueLbl)
            generator.setStack(tempPos, "1")
            
            generator.addGoto(tempLbl)

            generator.inputLabel(value.falseLbl)
            generator.setStack(tempPos, "0")

            generator.inputLabel(tempLbl)
        else:
            #generator.addCommit("aqui se caga...")
            generator.setStack(tempPos, value.valor)
        generator.addSaltoLinea()


        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


        return None