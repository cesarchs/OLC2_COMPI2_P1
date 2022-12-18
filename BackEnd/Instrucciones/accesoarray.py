from almacenar.generador import Generador
from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol
from almacenar.error import Error
from almacenar.tipo import Return, Tipo

#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol
#from almacenar.error import Error
#from almacenar.tipo import Tipo
import copy
class AccesoArreglo(Instruccion):
    def __init__(self, identificador, expresiones,  fila, columna):
        self.identificador = identificador
        self.expresiones = expresiones
        self.fila = fila
        self.columna = columna
        self.struct = False
        self.mutable = False
        
    def compilar(self, arbol, tabla):
        self.dimensiones=len(self.expresiones)
        arraysimbolo=tabla.getSimboloEnTs(self.identificador)
        genAux = Generador()
        generador = genAux.getInstance()
        
        generador.agregarComentario(" ACCESO A ARREGLO ")
        
        if arraysimbolo == None:
            return Error("SEMANTICO","ARREGLO: "+self.identificador+ "NO ESTA DECLARADO",self.fila,self.columna)
        
        self.tipo = arraysimbolo.getTipo()
        
        if not arraysimbolo.getArreglo():
            return Error("SEMANTICO", "ETIQUETA: "+self.identificador+" no es un arreglo",self.fila,self.columna)
        
        #BUSQUEDA DE POSICION EN ARREGLO
        #obtengo la posicion que se guardo en la pila para acceder a HEAP
        h = generador.agregarTemporal();generador.liberarTemporal(h)
        if not arraysimbolo.esGlobal:
            tempPos = generador.agregarTemporal();generador.liberarTemporal(tempPos)
            generador.addExp(tempPos,'P',arraysimbolo.posicion,'+')
            generador.getPila(h,tempPos)
        else:
            generador.getPila(h,arraysimbolo.posicion)
        temp = []
        
        #este metodo se usa para saber si posicion a acceder sera un valor en si o todo un arrreglo
        valorArreglo = self.buscarCambiardimension(arbol,tabla,copy.copy(self.expresiones),arraysimbolo.getArray())
        
        
        salir=generador.agregarLabel()
        #genero el codigo de tres direcciones correspondiente
        if self.dimensiones == arraysimbolo.dimensiones:
            valorasig = self.obtenerValorDimension(arbol,tabla,copy.copy(self.expresiones),h,arraysimbolo,temp,salir,generador)
            if isinstance(valorasig,Error):return valorasig
            generador.colocarLabel(salir)
        elif self.dimensiones < arraysimbolo.dimensiones:
            valorasig = self.obtenerValorDimensionarrayreturn(arbol,tabla,copy.copy(self.expresiones),h,arraysimbolo,temp,salir,valorArreglo,generador)
            if isinstance(valorasig,Error):return valorasig
            generador.colocarLabel(salir)
        else:
            return Error("SEMANTICO","DIMENSION A ACCEDER NO EXISTE",self.fila,self.columna)
        if isinstance(valorasig,Error):return valorasig
        #generador.colocarLabel(salir)
        valorasig.LblsalirArray=salir
        
        generador.agregarComentario(" FIN ACCESO A ARREGLO ")
        return valorasig
        
        #1 dim
        
        
        
        
        
    #    self.tipo = self.getTipo(valorasig)
    #    #ESTA VALIDACION ESTA COMENTADA DEBIDO QUE JULIA SI PUEDE DEVOLVER ARREGLOS (LISTAS), VALIDAR SIEMPRE
    #    #QUE FUNCIONE EN TODAS PARTES :
    #    
    #    #if isinstance(valorasig,list):
    #     #   return Error("SEMANTICO", "ACCESO A ARREGLO INCOMPLETO", self.fila,self.columna)
    #    
    #    return valorasig
        
    def getNode(self):
        nodoModArr= NodoArbol("ACCESO_ARRAY")
        nodoModArr.agregarHijoSinNodo(str(self.identificador))
        expredim = NodoArbol("EXPRESIONES DIMENSIONES")
        for expssss in self.expresiones:
            expredim.agregarHijoConNodo(expssss.getNode())
        nodoModArr.agregarHijoConNodo(expredim)
        return nodoModArr
    
    def getTipo(self, val):
        if isinstance(val,int):
            return Tipo.ENTERO
        elif isinstance(val,float):
            return Tipo.DECIMAL
        elif isinstance(val,bool):
            return Tipo.BOOLEANO
        elif isinstance(val,list):
            return Tipo.ARREGLO
        return Tipo.CADENA

    
    def buscarCambiardimension(self,arbol,tabla,expresiones,arreglo):
        valor = None
        if len(expresiones) == 0:
            return arreglo
        
        if not isinstance(arreglo,list):
            return Error("SEMANTICO", "POSICION A ACCEDER EN: "+self.identificador +" NO EXISTE", self.fila,self.columna)
        dimension=expresiones.pop(0)
        num = dimension.compilar(arbol,tabla)
        if isinstance(num, Error): return num
        try:  
            num=int(num.getValor())
            if num <=0:return Error("SEMANTICO", "POSICION A ACCEDER NO EXISTE", self.fila,self.columna)      
        except:
            return Error("SEMANTICO", "EXPRESION DEBE DE SER ENTERO PARA POSICION DE ARREGLO", self.fila,self.columna)
        
        if dimension.tipo != Tipo.ENTERO:
            return Error("SEMANTICO","EXPRESION DEBE DE SER ENTERO PARA POSICION DE ARREGLO",self.fila,self.columna)
        try:
            valor = self.buscarCambiardimension(arbol,tabla,copy.copy(expresiones),arreglo[num-1])
            #self.dimensiones+=1
        except:
            #self.dimensiones+=1
            return Error("SEMANTICO", "POSICION A ACCEDER EN: "+self.identificador +" NO EXISTE", self.fila,self.columna)    
        if isinstance(valor, Error): return valor
        return valor
    
    def obtenerValorDimension(self,arbol,tabla,expresiones,h,arreglo,temp,salir,generador:Generador):
        dimension=expresiones.pop(0)            #obtengo primer dimensión
        valor=generador.agregarTemporal();generador.liberarTemporal(valor)
        tamano=generador.agregarTemporal();generador.liberarTemporal(tamano)
        num = dimension.compilar(arbol,tabla)   #obtengo valor de dimension
        ##->->->->->->->->->->
        if num.tipo != Tipo.ENTERO:return Error("SEMANTICO","EXPRESION A ACCESO DE ARREGLO DEBER SER UN NUMERO",self.fila,self.columna)
        ##->->->->->->->->->->
        temp.append(valor)
        if arreglo.tipo == Tipo.ENTERO or arreglo.tipo == Tipo.CADENA or arreglo.tipo == Tipo.CARACTER:
            #aqui se agregar el codigo para el la comprobacion de si el  denominador es 0     
            generador.getHeap(tamano,h)
            
            generador.agregarComentario("COMPROBACION QUE INDEX EN ARRAY EXISTA")
            ltrue=generador.agregarLabel()
            lfalse=generador.agregarLabel()
            generador.agregarIf(num.getValor(),'1','<',ltrue)
            generador.agregarIf(num.getValor(),tamano,'>',ltrue)
            generador.agregarGoto(lfalse)
            generador.colocarLabel(ltrue)
            generador.printBoundError()
            generador.agregarGoto(salir)
            generador.colocarLabel(lfalse)
            generador.addExp(h,h,num.getValor(),'+')        
            generador.getHeap(valor,h)
            if len(expresiones)>0:
                temp.pop(0)
                self.obtenerValorDimension(arbol,tabla,copy.copy(expresiones),valor,arreglo,temp,salir,generador)
                ##->->->->->->->->->->->->->->
            #generador.colocarLabel(salir)
                ##->->->->->->->->->->->->->->
            return Return(temp[0],arreglo.tipo,True)
        
        elif arreglo.tipo == Tipo.BOOLEANO:
            #aqui se agregar el codigo para el la comprobacion de si el  denominador es 0     
            generador.getHeap(tamano,h)
            
            generador.agregarComentario("COMPROBACION QUE INDEX EN ARRAY EXISTA")
            ltrue=generador.agregarLabel()
            lfalse=generador.agregarLabel()
            generador.agregarIf(num.getValor(),'1','<',ltrue)
            generador.agregarIf(num.getValor(),tamano,'>',ltrue)
            generador.agregarGoto(lfalse)
            generador.colocarLabel(ltrue)
            generador.printBoundError()
            generador.agregarGoto(salir)
            
            generador.colocarLabel(lfalse)
            generador.addExp(h,h,num.getValor(),'+')        
            generador.getHeap(valor,h)
            if len(expresiones)>0:
                temp.pop(0)
                self.obtenerValorDimension(arbol,tabla,copy.copy(expresiones),valor,arreglo,temp,salir,generador)
                ##->->->->->->->->->->->->->->
            #generador.colocarLabel(salir)
                ##->->->->->->->->->->->->->->
            return Return(temp[0],arreglo.tipo,True)
    
    def obtenerValorDimensionarrayreturn(self,arbol,tabla,expresiones,h,arreglo,temp,salir,varreglo,generador:Generador):
        dimension = expresiones.pop(0)
        valor = generador.agregarTemporal();generador.liberarTemporal(valor)
        tamano=generador.agregarTemporal();generador.liberarTemporal(tamano)
        num = dimension.compilar(arbol,tabla)
        ##->->->->->->->->->->
        if num.tipo != Tipo.ENTERO:return Error("SEMANTICO","EXPRESION A ACCESO DE ARREGLO DEBER SER UN NUMERO",self.fila,self.columna)
        ##->->->->->->->->->->
        temp.append(valor)
        if arreglo.tipo == Tipo.ENTERO or arreglo.tipo == Tipo.CADENA:
            generador.getHeap(tamano,h)
            generador.agregarComentario("COMPROBACION QUE INDEX EN ARRAY EXISTA")
            ltrue=generador.agregarLabel()
            lfalse=generador.agregarLabel()
            generador.agregarIf(num.getValor(),'1','<',ltrue)
            generador.agregarIf(num.getValor(),tamano,'>',ltrue)
            generador.agregarGoto(lfalse)
            generador.colocarLabel(ltrue)
            generador.printBoundError()
            generador.agregarGoto(salir)
            generador.colocarLabel(lfalse)
            
            generador.addExp(h,h,num.getValor(),'+')
            generador.getHeap(valor,h)
            if len(expresiones)>0:
                temp.pop(0)
                self.obtenerValorDimensionarrayreturn(arbol,tabla,copy.copy(expresiones),valor,arreglo,temp,salir,varreglo,generador)
            #generador.colocarLabel(salir)
            r=Return(temp[0],Tipo.ARREGLO,True)
            r.dimensionesenacceso=self.dimensiones
            r.dimensiones=arreglo.dimensiones
            r.array=varreglo
            r.auxTipo=arreglo.tipo
            return r
        
        
    
class AccesoArregloBE(Instruccion):
    def __init__(self,identificador,expresiones, fila, columna):
        self.identificador=identificador
        self.expresiones = expresiones
        self.fila=fila
        self.columna=columna
    
    def ejecutar(self, arbol, tabla):
        arraysimbolo=tabla.getSimboloEnTs(self.identificador)
        
        if arraysimbolo == None:
            return Error("SEMANTICO","ARREGLO: "+self.identificador+ "NO ESTA DECLARADO",self.fila,self.columna)
        
        self.tipo = arraysimbolo.getTipo()
        
        if not arraysimbolo.getArreglo():
            return Error("SEMANTICO", "ETIQUETA: "+self.identificador+" no es un arreglo",self.fila,self.columna)
        
        try:
            valor = copy.copy(arraysimbolo.getValor())#obtengo arreglo
            if self.expresiones[0] == 'begin': indice1 = 1 #verifico si trae la palabra reservada begin 
            else: indice1 = self.expresiones[0].ejecutar(arbol,tabla) #sino obtener valor de exp
            if self.expresiones[1] == 'end': indice2 = len(valor)#verifico si trae la palabra reservada end
            else: indice2 = self.expresiones[1].ejecutar(arbol,tabla)#sino obtener valor de exp
            if isinstance(indice1,int):#valido que el valor de expresion sea entero
                if indice1 <=0:#valido que el indice sea mayor que cero sino F
                    return Error("SEMANTICO","Para acceder debe ser un numero mayor a cero",self.fila,self.columna)
            else:#sino es un error
                return Error("SEMANTICO","Expresion debe de ser un numero o la palabra begin",self.fila,self.columna)
            if isinstance(indice2,int):#valido que el valor de expresion sea entero
                if indice2 <=0:#valido que el indice sea mayor que cero sino F
                    return Error("SEMANTICO","Para acceder debe ser un numero mayor a cero",self.fila,self.columna)
            else:
                return Error("SEMANTICO","Expresion debe de ser un numero o la palabra end",self.fila,self.columna)
            valor = valor[indice1-1:indice2]
            if valor:
                return valor
            else:
                return Error("SEMANTICO","NO SE PUEDE ACCEDER A ESE RANGO EN ARRAY", self.fila,self.columna)
        except:
            return Error("SEMANTICO","NO SE PUEDE ACCEDER A ESE RANGO EN ARRAY", self.fila,self.columna)
        
    def getNode(self):
        nodoModArr= NodoArbol("ARRAY ACCESO B:E")
        nodoModArr.agregarHijoSinNodo(str(self.identificador))
        expredim = NodoArbol("ACCESO")
        if self.expresiones[0] == 'begin': expredim.agregarHijoSinNodo("begin")
        else: expredim.agregarHijoConNodo(self.expresiones[0].getNode())
        expredim.agregarHijoSinNodo(":")
        if self.expresiones[1] == 'end': expredim.agregarHijoSinNodo("end")
        else: expredim.agregarHijoConNodo(self.expresiones[1].getNode())
        nodoModArr.agregarHijoConNodo(expredim)
        return nodoModArr

#try:
#    a = copy.copy(arr)
#    a = a[0:4]
#    #print(a)
#    if a :
#        print(a)  # [2,3,4]
#    else:
#        print("f")
#except:
#        print("fff")

