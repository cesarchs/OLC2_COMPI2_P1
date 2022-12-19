from TS.Excepcion import Excepcion
from TS.Tipo import tipo

class TablaSimbolos:
    def __init__(self, anterior = None):#anterior seria un puntero de mayor precedencia, seria otra tabla de simbolos
        self.tabla={}#diccionario
        self.anterior=anterior

        self.size=0
        #-------------------------------continue String for
        self.continueString=False
        self.tempLblPlusOne=""
        self.temp2Lbl=""
        self.retTemp=""
        self.simboloSize=None
        #-------------------------------continue int for
        self.continueInt=False
        self.t0=""
        self.intSimboloSize=None


        self.breakLbl = ''
        self.continueLbl = ''
        self.returnLbl = ''

        if anterior!=None:#GRACIAS Dios, por apiadarte y mostrarme mi error
            self.size = anterior.size

            self.breakLbl = self.anterior.breakLbl
            self.continueLbl = self.anterior.continueLbl
            self.returnLbl = self.anterior.returnLbl

            #-------------------------------para continue de for string
            self.continueString=self.anterior.continueString
            self.tempLblPlusOne=self.anterior.tempLblPlusOne
            self.temp2Lbl=self.anterior.temp2Lbl
            self.retTemp=self.anterior.retTemp
            self.simboloSize=self.anterior.simboloSize
            #-------------------------------para continue de for int
            self.continueInt=self.anterior.continueInt
            self.t0=self.anterior.t0
            self.intSimboloSize=self.anterior.intSimboloSize
        
        
        


#tenemos una lista de tablas
#ojo esto es para declarar a global luego en otro ambito y asi recursivamente
# por ejemplo global A y luego dentro de ifs mas A
#ver si JULIA lo permite

    def setTabla(self, simbolo):#agregar una variable
        if simbolo.id in self.tabla:#retornamos error           @@@@@@ lower()
            #validamos que una varibale no se declare mas de una vez
            return Excepcion("Semantico","variable "+simbolo.id+" ya existente",simbolo.fila,simbolo.columna),None

        else:
            simbolo.size=self.size
            #if self.anterior!=None:
             #   simbolo.size=simbolo.size-1

            simbolo.global1 = self.anterior==None
            self.size+=1

            self.tabla[simbolo.id]=simbolo#metemos en la tabla de simbolos      @@@@@@ lower()
            
            return None,simbolo


    def getTabla(self,id):#obtener una variable
        tablaActual=self
        while tablaActual != None:#quite el error de q puede ser None tablaActual.tabla

            if id in tablaActual.tabla:

                #print(">>>>>>id:"+str(tablaActual.tabla[id].id)+" valor:"+str(tablaActual.tabla[id].valor))
                return tablaActual.tabla[id]       #retorna simbolo (supuestamente xd) arreglado ya
            else:
                tablaActual = tablaActual.anterior   
                #print("este simbolo:"+str(id)+" no esta se procedio a cambiar de tabla")
                #print(str(self.anterior==None))
        return None       






        #lo q sucede esq al crear ambito este [NEW_AMBITO] -> global    pero global no apunta a [NEW_AMBITO]    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<







    def actualizarTabla(self,simbolo):#actualizar los datos en tabla de simbolo
        tablaActual=self
        while tablaActual != None:
            if simbolo.id in tablaActual.tabla:#sin el .lower() F en funciones recursivas no se actualiza el dato de un NUM global

             # if tablaActual.tabla[simbolo.id].getTipo() == simbolo.getTipo():# or simbolo.getTipo()==tipo.NULO :#or simbolo.getTipo==tipo.nulo para cambiarle VALOR a nulo
#como en julia se puede sobreescribir un tipo de variable tonces

                #simbolo.size=self.size
                #simbolo.global1 = self.anterior==None
                #self.size+=1
                

                tablaActual.tabla[simbolo.id].setValor(simbolo.getValor())#sin el .lower() F en funciones recursivas no se actualiza el dato de un NUM global
                tablaActual.tabla[simbolo.id].setTipo(simbolo.getTipo())#sin el .lower() F en funciones recursivas no se actualiza el dato de un NUM global
                
                return None,tablaActual.tabla[simbolo.id] #variable actualizada

              #return Excepcion("Semantico","tipo de dato diferente al de la asignacion original",simbolo.getFILA(),simbolo.getCOLUMNA() )


            else:
                tablaActual = tablaActual.anterior   
        
        return Excepcion("Semantico","variable no encontrada en asignacion",simbolo.getFILA(),simbolo.getCOLUMNA() ),None


    def actualizarTablaARRAY(self,simbolo):#actualizar los datos en tabla de simbolo
        tablaActual=self
        while tablaActual != None:
            if simbolo.id in tablaActual.tabla:#sin el .lower() F en funciones recursivas no se actualiza el dato de un NUM global

             # if tablaActual.tabla[simbolo.id].getTipo() == simbolo.getTipo():# or simbolo.getTipo()==tipo.NULO :#or simbolo.getTipo==tipo.nulo para cambiarle VALOR a nulo
#como en julia se puede sobreescribir un tipo de variable tonces

                #print("00000000000000000000000000000000000000")

                #print(str(tablaActual.tabla[simbolo.id].getValor()) )

                newValor = tablaActual.tabla[simbolo.id].getValor()

                newValor.append(simbolo.tipo)

                #print(str(len(newValor)))
                #print(str(newValor))

                tablaActual.tabla[simbolo.id].setValor(newValor)#sin el .lower() F en funciones recursivas no se actualiza el dato de un NUM global
                #tablaActual.tabla[simbolo.id.lower()].setTipo(simbolo.getTipo())#sin el .lower() F en funciones recursivas no se actualiza el dato de un NUM global
                return None #variable actualizada

              #return Excepcion("Semantico","tipo de dato diferente al de la asignacion original",simbolo.getFILA(),simbolo.getCOLUMNA() )


            else:
                tablaActual = tablaActual.anterior   
        
        return Excepcion("Semantico","array no encontrado en push",simbolo.getFILA(),simbolo.getCOLUMNA() )






    def actualizarTablaARRAY2(self,simbolo):#actualizar los datos en tabla de simbolo
        tablaActual=self
        while tablaActual != None:
            if simbolo.id in tablaActual.tabla:#sin el .lower() F en funciones recursivas no se actualiza el dato de un NUM global

             # if tablaActual.tabla[simbolo.id].getTipo() == simbolo.getTipo():# or simbolo.getTipo()==tipo.NULO :#or simbolo.getTipo==tipo.nulo para cambiarle VALOR a nulo
#como en julia se puede sobreescribir un tipo de variable tonces

                #print("111111111111111111111111111111111")

                #print(str(tablaActual.tabla[simbolo.id].getValor()) )

                newValor = tablaActual.tabla[simbolo.id].getValor()

                ash = newValor.pop()
                #print("--- que retorna?")
                #print(str(ash))

                #print(str(len(newValor)))
                #print(str(newValor))

                tablaActual.tabla[simbolo.id].setValor(newValor)#sin el .lower() F en funciones recursivas no se actualiza el dato de un NUM global
                #tablaActual.tabla[simbolo.id.lower()].setTipo(simbolo.getTipo())#sin el .lower() F en funciones recursivas no se actualiza el dato de un NUM global
                return ash #variable actualizada

              #return Excepcion("Semantico","tipo de dato diferente al de la asignacion original",simbolo.getFILA(),simbolo.getCOLUMNA() )


            else:
                tablaActual = tablaActual.anterior   
        
        return Excepcion("Semantico","array no encontrado en pop",simbolo.getFILA(),simbolo.getCOLUMNA() )












































