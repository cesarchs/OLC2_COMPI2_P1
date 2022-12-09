from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Tipo import tipo
from TS.Simbolo import Simbolo

class Declaracion(instruccion):# es como un nodo y se arma el arbol con estos nodos

                    
    def __init__(self,tipo,identificador , fila, columna, expresion=None ):
        self.tipo=tipo
        self.identificador=identificador
        self.expresion=expresion
        self.fila=fila
        self.columna=columna
        self.arreglo=False


    def interpretar(self, tree, table):#va a hacer lo q este en Expresiones(aritmetica,logica,relacional)
        #id ya esta definido tonces obtenemos el valor de la expresion

        if self.expresion==None:
            #print("estoy trabajando en structs.....")
            #print(">tipo:"+str(self.tipo))

            simbolo = Simbolo(str(self.identificador),self.tipo,self.arreglo, self.fila,self.columna,self.expresion)
            result = table.setTabla(simbolo)

            if isinstance(result,Excepcion): return result
            #print(str(result))#si da None si lo guarde en la tabla simbolos del struct
            return None


        value = self.expresion.interpretar(tree,table) #valor a asignar a la variable

        #por si tenemos un error en lo anterior
        if isinstance(value, Excepcion): return value#lo retornamos

        
        #validar si el tipo de la expresion y la variable es igual
        if self.tipo != self.expresion.tipo:# and self.tipo!=tipo.NULO:     #OJO POSIBLE CAGADAL  despues del and si estoy en lo correcto | si tipo==nulo tonces esta bien y no es error

            #fff = table.getTabla(str(self.identificador))
            #print("::::::::::::::::::::::::::")
            #print(str(self.identificador))
            #print(fff)

            #if fff==None:
             #   print("ERROR| esta variable se repeteria:"+str(self.identificador))

            return Excepcion("Semantico","tipo de datos diferente en declaracion", self.fila,self.columna)
        #si no tiene errores




        simbolo = Simbolo(str(self.identificador),self.tipo,self.arreglo, self.fila,self.columna,value)

        result = table.setTabla(simbolo)

        if isinstance(result,Excepcion): return result

        return None

        #tree.updateConsola(simbolo)#esto es semantico falta conbinarlo con lo lexico y sintactico VIDEO 4-> 1:44:54s
        

    def getNodo(self):

        if self.expresion==None:#VIDEO 15 MIN 50MIN:50S OJO AL TIP
            nodo = NodoAST("DECLARACION")
            nodo.agregarHijo(str(self.tipo))#PUEDE COMO NO PUEDE VENIR JAVIER
            nodo.agregarHijo(str(self.identificador))
            #nodo.agregarHijoNodo(self.expresion.getNodo())
            return nodo

        else:
            nodo = NodoAST("DECLARACION")
            nodo.agregarHijo(str(self.tipo))#PUEDE COMO NO PUEDE VENIR JAVIER
            nodo.agregarHijo(str(self.identificador))
            nodo.agregarHijoNodo(self.expresion.getNodo())
            return nodo


    def compilar(self, tree, table):
        genAux = Generator()
        generator = genAux.getInstance()

        generator.addCommit("------------Compilacion de valor de variable, falta un para None-------------")
        if self.expresion==None:

            # Guardado y obtencion de variable. Esta tiene la posicion, lo que nos sirve para asignarlo en el heap esta en newVar
            simbolo = Simbolo(str(self.identificador),self.tipo,self.arreglo, self.fila,self.columna,self.expresion,0)
            result,newVar = table.setTabla(simbolo)

            if isinstance(result,Excepcion): return result
            #print(str(result))#si da None si lo guarde en la tabla simbolos del struct



            #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            #va lo de Obtencion de posicion de la variable
            #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

            return None


        value = self.expresion.compilar(tree,table) #valor a asignar a la variable
        generator.addCommit("-------------------Fin de valor de variable---------------------")

        #por si tenemos un error en lo anterior
        if isinstance(value, Excepcion): return value#lo retornamos

        
        #validar si el tipo de la expresion y la variable es igual
        if self.tipo != self.expresion.tipo:# and self.tipo!=tipo.NULO:     #OJO POSIBLE CAGADAL  despues del and si estoy en lo correcto | si tipo==nulo tonces esta bien y no es error
            return Excepcion("Semantico","tipo de datos diferente en declaracion", self.fila,self.columna)
        #si no tiene errores



        # Guardado y obtencion de variable. Esta tiene la posicion, lo que nos sirve para asignarlo en el heap esta en newVar
        simbolo = Simbolo(str(self.identificador),self.tipo,self.arreglo, self.fila,self.columna,value,0,(value.tipo == tipo.CADENA or value.tipo == tipo.ARREGLO))
        result,newVar = table.setTabla(simbolo)
        
        if isinstance(result,Excepcion): return result

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