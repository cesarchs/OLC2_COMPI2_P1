import copy
from almacenar.generador import Generador
from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol
from almacenar.error import Error
from almacenar.tipo import Tipo

#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol
#from almacenar.error import Error
#from almacenar.tipo import Tipo

class Imprimir(Instruccion): 
    def __init__(self,expresion, fila, columna): #expresion ya que puede venir int, sumas, cadenas, etc
        self.expresion = expresion #obtiene un objeto de tipo expresion
        self.fila = fila
        self.columna = columna
        self.struct = False
        self.mutable = False

    def compilar(self, arbol, tabla):
        genAux = Generador()
        generator = genAux.getInstance()
        for expresion in self.expresion:
            exp = expresion.compilar(arbol,tabla) #retorna objeto o un valor contreto
            
            if isinstance(exp,Error):return exp 
            
            #si retorna Error entonces:
            
            
            if exp.tipo == Tipo.ENTERO:
                generator.agregarComentario("inicio instruccion print")
                generator.agregarPrint("d","int("+exp.valor+")")
                generator.agregarComentario("fin instruccion print")
                
            elif exp.tipo == Tipo.DECIMAL:
                generator.agregarComentario("inicio instruccion print")
                generator.agregarPrint("f",exp.valor)
                generator.agregarComentario("fin instruccion print")
            
            elif exp.tipo == Tipo.CARACTER:
                generator.agregarComentario("inicio instruccion print")
                generator.agregarPrint("c","int("+exp.valor+")")
                generator.agregarComentario("fin instruccion print")
            
            elif exp.tipo == Tipo.BOOLEANO:
                if exp.trueLbl != '':
                    tempLbl = generator.agregarLabel()  #esta etiqueta es para la salida luego de la impresion sino sigue imprimiendo lo de abajo
                    generator.colocarLabel(exp.trueLbl) #coloco label de true
                    generator.printTrue() #imprimo true
                    generator.agregarGoto(tempLbl) #coloco label de salida 
                    generator.colocarLabel(exp.falseLbl) #coloco label de false
                    generator.printFalse()#imprimo falses
                    generator.colocarLabel(tempLbl) #coloco el label de salida en codigo
                else:
                    lblTrue = generator.agregarLabel()
                    lblFalse = generator.agregarLabel()
                    tempLbl = generator.agregarLabel()
                    generator.agregarIf(exp.getValor(),'1','==',lblTrue)
                    generator.agregarGoto(lblFalse)
                    generator.colocarLabel(lblTrue)
                    generator.printTrue()
                    generator.agregarGoto(tempLbl)
                    generator.colocarLabel(lblFalse)
                    generator.printFalse()
                    generator.colocarLabel(tempLbl)
                
            elif exp.tipo == Tipo.CADENA:
                generator.printf()#imprimo en C3D funcion nativa de impresion
                
                paramTemp=generator.agregarTemporal();generator.liberarTemporal(paramTemp) # genero temporal para entorno simulado
                
                #cambio de entorno simulado:
                generator.addExp(paramTemp, 'P', tabla.size, '+')
                generator.addExp(paramTemp, paramTemp, '1', '+')
                generator.setPila(paramTemp, exp.getValor())
                
                #cambio de entorno:
                generator.newEnv(tabla.size)
                generator.llamandaFuncion('nativePrintString')
                
                #obtengo valor de retorno:
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.getPila(temp,'P')
                
                #REGRESO A ENTORNO MAIN
                generator.returnEntorno(tabla.size)
            elif exp.tipo == Tipo.ARREGLO:
                try:
                    if exp.auxTipo == Tipo.ENTERO:
                        generator.agregarPrint("c","int("+"91"+")")#"["
                        self.obtenerSiguienteDimension(copy.copy(exp.array),exp.dimensionesenacceso,exp.dimensiones,exp.getValor(),generator)
                        generator.agregarPrint("c","int("+"93"+")")#"]"
                        #if exp.LblsalirArray != None:
                        #    generator.colocarLabel(exp.LblsalirArray)
                    elif exp.auxTipo == Tipo.CADENA:
                        generator.agregarPrint("c","int("+"91"+")")#"["
                        self.obtenerSiguienteDimensionCad(copy.copy(exp.array),exp.dimensionesenacceso,exp.dimensiones,exp.getValor(),tabla,generator)
                        generator.agregarPrint("c","int("+"93"+")")#"]"
                except:
                    #generator.colocarLabel(exp.LblsalirArray)
                    return Error("SEMANTICO","NO SE PUEDE IMPRIMIR ARREGLO POR PROBLEMAS DE DIMENSION",self.fila,self.columna)
                #pass
    def obtenerSiguienteDimension(self,arraytemp,sizeAcesso,sizeArreglo,temp,generador:Generador):
        dimension=arraytemp.pop(0)
        #if sizeAcesso < sizeArreglo:
        #    generador.getHeap(temp)#con este obtengo posicion tamaño de arreglo(primera posicion)
        #    generador.addExp()
        if not isinstance(dimension,list):
            generador.addExp(temp,temp,'1','+')#avanzo una posicion para obtener el primer valor y saltar el tamano de ese arreglo
            elemento=generador.agregarTemporal()
            generador.getHeap(elemento,temp)
            generador.agregarPrint("d","int("+str(elemento)+")")
            if len(arraytemp)>0:
                generador.agregarPrint("c","int("+"44"+")")
                self.obtenerSiguienteDimension(copy.copy(arraytemp),sizeAcesso,sizeArreglo,temp,generador)
            return
        else:
            #posicionarray=generador.agregarTemporal()
            #generador.getHeap(posicionarray,temp)#obtengo posicion de h en donde empieza array
            generador.addExp(temp,temp,'1','+')#avanzo una posicion para obtener el primer valor y saltar el tamano de ese arreglo
            posicionarray=generador.agregarTemporal()
            generador.getHeap(posicionarray,temp)
            generador.agregarPrint("c","int("+"91"+")")#"["
            self.obtenerSiguienteDimension(copy.copy(dimension),sizeAcesso,sizeArreglo,posicionarray,generador)
            generador.agregarPrint("c","int("+"93"+")")#"]"
            if len(arraytemp)>0:
                generador.agregarPrint("c","int("+"44"+")")
                self.obtenerSiguienteDimension(copy.copy(arraytemp),sizeAcesso,sizeArreglo,temp,generador)
            return
            
    def obtenerSiguienteDimensionCad(self,arraytemp,sizeAcesso,sizeArreglo,temp,tabla,generador:Generador):
        dimension=arraytemp.pop(0)
        #if sizeAcesso < sizeArreglo:
        #    generador.getHeap(temp)#con este obtengo posicion tamaño de arreglo(primera posicion)
        #    generador.addExp()
        if not isinstance(dimension,list):
            generador.addExp(temp,temp,'1','+')#avanzo una posicion para obtener el primer valor y saltar el tamano de ese arreglo
            elemento=generador.agregarTemporal()
            generador.getHeap(elemento,temp)
            
            generador.printf()#imprimo en C3D funcion nativa de impresion
            
            paramTemp=generador.agregarTemporal();generador.liberarTemporal(paramTemp) # genero temporal para entorno simulado
            
            #cambio de entorno simulado:
            generador.addExp(paramTemp, 'P', tabla.size, '+')
            generador.addExp(paramTemp, paramTemp, '1', '+')
            generador.setPila(paramTemp, elemento)
            
            #cambio de entorno:
            generador.newEnv(tabla.size)
            generador.llamandaFuncion('nativePrintString')
            
            #obtengo valor de retorno:
            tempd = generador.agregarTemporal();generador.liberarTemporal(tempd)
            generador.getPila(tempd,'P')
            
            #REGRESO A ENTORNO MAIN
            generador.returnEntorno(tabla.size)
            
            #generador.agregarPrint("d","int("+str(elemento)+")")
            if len(arraytemp)>0:
                generador.agregarPrint("c","int("+"44"+")")
                self.obtenerSiguienteDimensionCad(copy.copy(arraytemp),sizeAcesso,sizeArreglo,temp,tabla,generador)
            return
        else:
            #posicionarray=generador.agregarTemporal()
            #generador.getHeap(posicionarray,temp)#obtengo posicion de h en donde empieza array
            generador.addExp(temp,temp,'1','+')#avanzo una posicion para obtener el primer valor y saltar el tamano de ese arreglo
            posicionarray=generador.agregarTemporal()
            generador.getHeap(posicionarray,temp)
            generador.agregarPrint("c","int("+"91"+")")#"["
            self.obtenerSiguienteDimensionCad(copy.copy(dimension),sizeAcesso,sizeArreglo,posicionarray,tabla,generador)
            generador.agregarPrint("c","int("+"93"+")")#"]"
            if len(arraytemp)>0:
                generador.agregarPrint("c","int("+"44"+")")
                self.obtenerSiguienteDimensionCad(copy.copy(arraytemp),sizeAcesso,sizeArreglo,temp,tabla,generador)
            return
    
    def getNode(self):
        nodoimprimir = NodoArbol("PRINT") #NOMBRE PADRE
        #nodoimprimir.agregarHijoConNodo(self.expresion.getNode())
        return nodoimprimir

    def checkLabels(self):
        genAux = Generador()
        generator = genAux.getInstance()
        if self.trueLbl == '':
            self.trueLbl = generator.agregarLabel()
        if self.falseLbl == '':
            self.falseLbl = generator.agregarLabel()
    

class ImprimirLn(Instruccion): 
    def __init__(self,expresion, fila, columna): #expresion ya que puede venir int, sumas, cadenas, etc
        self.expresion = expresion #obtiene un objeto de tipo expresion
        self.fila = fila
        self.columna = columna
        self.struct = False
        self.mutable = False

    def compilar(self, arbol, tabla):
        genAux = Generador()
        generator = genAux.getInstance()
        generator.agregarComentario("Inicia instruccion println")
        for expresion in self.expresion:
            exp = expresion.compilar(arbol,tabla) #retorna objeto o un valor contreto
            
            #si retorna Error entonces:
            
            if isinstance(exp,Error):
                return exp 
            if exp.tipo == Tipo.ENTERO:
                generator.agregarPrint("d","int("+str(exp.getValor())+")")
                ##->->->->->->->->->->
                #if exp.LblsalirArray != None:
                #    generator.colocarLabel(exp.LblsalirArray)
                ##->->->->->->->->->->
                #generator.saltoLinea()
                #generator.agregarComentario("fin instruccion print")
                
            elif exp.tipo == Tipo.DECIMAL:
                #generator.agregarComentario("inicio instruccion print")
                generator.agregarPrint("f",exp.getValor())
                #generator.saltoLinea()
                #generator.agregarComentario("fin instruccion print")
            
            elif exp.tipo == Tipo.CARACTER:
                #generator.agregarComentario("inicio instruccion print")
                generator.agregarPrint("c","int("+str(exp.getValor())+")")
                #generator.saltoLinea()
                #generator.agregarComentario("fin instruccion print")
            
            elif exp.tipo == Tipo.BOOLEANO:
                if exp.trueLbl != '':
                    tempLbl = generator.agregarLabel()  #esta etiqueta es para la salida luego de la impresion sino sigue imprimiendo lo de abajo
                    generator.colocarLabel(exp.trueLbl) #coloco label de true
                    generator.printTrue() #imprimo true
                    #generator.saltoLinea()
                    generator.agregarGoto(tempLbl) #coloco label de salida 
                    generator.colocarLabel(exp.falseLbl) #coloco label de false
                    generator.printFalse()#imprimo false
                    #generator.saltoLinea()
                    generator.colocarLabel(tempLbl) #coloco el label de salida en codigo
                #si no tiene trulbl es por que es un temp de un arreglo
                else:
                    lblTrue = generator.agregarLabel()
                    lblFalse = generator.agregarLabel()
                    tempLbl = generator.agregarLabel()
                    generator.agregarIf(exp.getValor(),'1','==',lblTrue)
                    generator.agregarGoto(lblFalse)
                    generator.colocarLabel(lblTrue)
                    generator.printTrue()
                    generator.agregarGoto(tempLbl)
                    generator.colocarLabel(lblFalse)
                    generator.printFalse()
                    generator.colocarLabel(tempLbl)
            elif exp.tipo == Tipo.CADENA:
                generator.printf()#imprimo en C3D funcion nativa de impresion
                
                paramTemp=generator.agregarTemporal();generator.liberarTemporal(paramTemp) # genero temporal para entorno simulado
                
                #cambio de entorno simulado:
                generator.addExp(paramTemp, 'P', tabla.size, '+')
                generator.addExp(paramTemp, paramTemp, '1', '+')
                generator.setPila(paramTemp, exp.getValor())
                
                #cambio de entorno:
                generator.newEnv(tabla.size)
                generator.llamandaFuncion('nativePrintString')
                
                #obtengo valor de retorno:
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.getPila(temp,'P')
                
                #REGRESO A ENTORNO MAIN
                generator.returnEntorno(tabla.size)
                #generator.saltoLinea()
            elif exp.tipo == Tipo.ARREGLO:
                try:
                    if exp.auxTipo == Tipo.ENTERO:
                        generator.agregarPrint("c","int("+"91"+")")#"["
                        self.obtenerSiguienteDimension(copy.copy(exp.array),exp.dimensionesenacceso,exp.dimensiones,exp.getValor(),generator)
                        generator.agregarPrint("c","int("+"93"+")")#"]"
                        #if exp.LblsalirArray != None:
                        #    generator.colocarLabel(exp.LblsalirArray)
                    elif exp.auxTipo == Tipo.CADENA:
                        generator.agregarPrint("c","int("+"91"+")")#"["
                        self.obtenerSiguienteDimensionCad(copy.copy(exp.array),exp.dimensionesenacceso,exp.dimensiones,exp.getValor(),tabla,generator)
                        generator.agregarPrint("c","int("+"93"+")")#"]"
                except:
                    #generator.colocarLabel(exp.LblsalirArray)
                    return Error("SEMANTICO","NO SE PUEDE IMPRIMIR ARREGLO POR PROBLEMAS DE DIMENSION",self.fila,self.columna)
                #pass
            
        generator.saltoLinea()
        generator.agregarComentario("Finaliza instruccion println")
        
        
    def obtenerSiguienteDimension(self,arraytemp,sizeAcesso,sizeArreglo,temp,generador:Generador):
            dimension=arraytemp.pop(0)
            #if sizeAcesso < sizeArreglo:
            #    generador.getHeap(temp)#con este obtengo posicion tamaño de arreglo(primera posicion)
            #    generador.addExp()
            if not isinstance(dimension,list):
                generador.addExp(temp,temp,'1','+')#avanzo una posicion para obtener el primer valor y saltar el tamano de ese arreglo
                elemento=generador.agregarTemporal();generador.liberarTemporal(elemento)
                generador.getHeap(elemento,temp)
                generador.agregarPrint("d","int("+str(elemento)+")")
                if len(arraytemp)>0:
                    generador.agregarPrint("c","int("+"44"+")")
                    self.obtenerSiguienteDimension(copy.copy(arraytemp),sizeAcesso,sizeArreglo,temp,generador)
                return
            else:
                #posicionarray=generador.agregarTemporal()
                #generador.getHeap(posicionarray,temp)#obtengo posicion de h en donde empieza array
                generador.addExp(temp,temp,'1','+')#avanzo una posicion para obtener el primer valor y saltar el tamano de ese arreglo
                posicionarray=generador.agregarTemporal();generador.liberarTemporal(posicionarray)
                generador.getHeap(posicionarray,temp)
                generador.agregarPrint("c","int("+"91"+")")#"["
                self.obtenerSiguienteDimension(copy.copy(dimension),sizeAcesso,sizeArreglo,posicionarray,generador)
                generador.agregarPrint("c","int("+"93"+")")#"]"
                if len(arraytemp)>0:
                    generador.agregarPrint("c","int("+"44"+")")
                    self.obtenerSiguienteDimension(copy.copy(arraytemp),sizeAcesso,sizeArreglo,temp,generador)
                return
            
    def obtenerSiguienteDimensionCad(self,arraytemp,sizeAcesso,sizeArreglo,temp,tabla,generador:Generador):
            dimension=arraytemp.pop(0)
            #if sizeAcesso < sizeArreglo:
            #    generador.getHeap(temp)#con este obtengo posicion tamaño de arreglo(primera posicion)
            #    generador.addExp()
            if not isinstance(dimension,list):
                generador.addExp(temp,temp,'1','+')#avanzo una posicion para obtener el primer valor y saltar el tamano de ese arreglo
                elemento=generador.agregarTemporal();generador.liberarTemporal(elemento)
                generador.getHeap(elemento,temp)
                
                generador.printf()#imprimo en C3D funcion nativa de impresion
                
                paramTemp=generador.agregarTemporal();generador.liberarTemporal(paramTemp) # genero temporal para entorno simulado
                
                #cambio de entorno simulado:
                generador.addExp(paramTemp, 'P', tabla.size, '+')
                generador.addExp(paramTemp, paramTemp, '1', '+')
                generador.setPila(paramTemp, elemento)
                
                #cambio de entorno:
                generador.newEnv(tabla.size)
                generador.llamandaFuncion('nativePrintString')
                
                #obtengo valor de retorno:
                tempd = generador.agregarTemporal();generador.liberarTemporal(tempd)
                generador.getPila(tempd,'P')
                
                #REGRESO A ENTORNO MAIN
                generador.returnEntorno(tabla.size)
                
                #generador.agregarPrint("d","int("+str(elemento)+")")
                if len(arraytemp)>0:
                    generador.agregarPrint("c","int("+"44"+")")
                    self.obtenerSiguienteDimensionCad(copy.copy(arraytemp),sizeAcesso,sizeArreglo,temp,tabla,generador)
                return
            else:
                #posicionarray=generador.agregarTemporal()
                #generador.getHeap(posicionarray,temp)#obtengo posicion de h en donde empieza array
                generador.addExp(temp,temp,'1','+')#avanzo una posicion para obtener el primer valor y saltar el tamano de ese arreglo
                posicionarray=generador.agregarTemporal();generador.liberarTemporal(posicionarray)
                generador.getHeap(posicionarray,temp)
                generador.agregarPrint("c","int("+"91"+")")#"["
                self.obtenerSiguienteDimensionCad(copy.copy(dimension),sizeAcesso,sizeArreglo,posicionarray,tabla,generador)
                generador.agregarPrint("c","int("+"93"+")")#"]"
                if len(arraytemp)>0:
                    generador.agregarPrint("c","int("+"44"+")")
                    self.obtenerSiguienteDimensionCad(copy.copy(arraytemp),sizeAcesso,sizeArreglo,temp,tabla,generador)
                return
         
            
        
        #if self.expresion.tipo == Tipo.ARREGLO:
         #   return Error("SEMANTICO", "No se puede imprimir un arreglo completo", self.fila, self.columna)
         
        #if isinstance(exp,dict):
        #        #tamano=1
        #        #valor=str(exp['##_nombre_padre_struct_##']['id'])+"("
        #        #for key in exp:
        #        #    tamano+=1
        #        #    if  exp[key]['valor'] != '':
        #        #        valor += str(exp[key]['valor'])
        #        #        if tamano <= len(exp):valor += ','
        #        #valor+=")"
        #    arbol.actualizarConsola(self.desempaquetarvalor(exp)+"\n")
        #    return exp
        #
        #arbol.actualizarConsola(str(exp)+"\n")
    
    def getNode(self):
        nodoimprimir = NodoArbol("PRINTLN") #NOMBRE PADRE
        #nodoimprimir.agregarHijoConNodo(self.expresion.getNode())
        return nodoimprimir
    
    def desempaquetarvalor(self,diccionario):
        valor =""
        tamano=1
        valor=str(diccionario['##_nombre_padre_struct_##']['id'])+"("
        for key in diccionario:
            tamano+=1
            if  key != '##_nombre_padre_struct_##':
                if isinstance(diccionario[key]['valor'],dict):
                    valor+= self.desempaquetarvalor(diccionario[key]['valor'])
                else:
                    if diccionario[key]['valor']==None:
                        valor+='nothing'
                    else:
                        valor += str(diccionario[key]['valor'])
                    if tamano <= len(diccionario):valor += ','
        valor+=")"
        return valor