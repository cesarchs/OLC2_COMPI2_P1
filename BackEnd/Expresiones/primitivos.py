from padres.Nodo import NodoArbol
from padres.expresion import Expresion
from almacenar.generador import Generador
from almacenar.tipo import Return,Tipo
#from padres.Nodo import NodoArbol
#from padres.instruccion import Instruccion

class Primitivo(Expresion):
    def __init__(self, tipo, valor, fil, col):
        super().__init__(fil, col)
        self.tipo = tipo
        self.valor = valor
        self.fila = fil
        self.columna = col 
        self.bandera_arreglo = False
        self.struct = False
        self.mutable = False
    
    def compilar(self, arbol, tabla):
        genAux = Generador()
        generator = genAux.getInstance()
        #TRADUCION PARA TIPO ENTERO O DECIMAL:
        if self.tipo == Tipo.ENTERO or self.tipo == Tipo.DECIMAL:
            return Return(str(self.valor),self.tipo,False)
        
        #TRADUCION PARA TIPO CHAR:
        if self.tipo == Tipo.CARACTER:
            return Return(str(ord(self.valor)),self.tipo,False)
        #TRADUCION PARA TIPO BOOL:
        elif self.tipo == Tipo.BOOLEANO:
            generator.agregarComentario("Inicia primitivo Bool")
            if self.trueLbl == '':
                self.trueLbl = generator.agregarLabel()#L0
            if self.falseLbl == '':
                self.falseLbl = generator.agregarLabel()#L1
            #si es true el valor entonces se agrega de primero 
            #label de true para que vaya a etiqueta de true
            if self.valor:
                generator.agregarGoto(self.trueLbl)#goto L1;
                generator.agregarComentario("GOTO PARA EVITAR ERROR DE GO")
                generator.agregarGoto(self.falseLbl)
            else:
                generator.agregarGoto(self.falseLbl)
                generator.agregarComentario("GOTO PARA EVITAR ERROR DE GO")
                generator.agregarGoto(self.trueLbl)
                
            generator.agregarComentario("Finaliza primitivo Bool")   
            ret = Return(self.valor,self.tipo,False)
            ret.trueLbl     = self.trueLbl
            ret.falseLbl    = self.falseLbl
            
            return ret
        #TRADUCION PARA TIPO CADENA:
        elif self.tipo == Tipo.CADENA:
            #esto agrega un temporal para almacenar la posicion inicial del heap
            #en el stack
            retTemp = generator.agregarTemporal()
            #tn=H
            generator.agregarComentario("inicia primitivo String")
            generator.addExp(retTemp,'H','','')

            for caracter in str(self.valor):
                #esto va agregado de esta forma:
                generator.setHeap('H', ord(caracter))
                #obtengo el codigo ascii del caracter y luego
                #lo almaceno en heap, así:
                # heap[int(h)] = ascii
                generator.nextHeap()
                #luego se suma para la siguiente posicion de h:
                # h = h+1
                
            generator.setHeap('H','-1') #-1 para indicar fin de cadena
            generator.nextHeap()
            generator.agregarComentario("Finaliza primitivo String")
            return Return(retTemp,Tipo.CADENA,True)

    def setBanderaArreglo(self,bandera):
        self.bandera_arreglo=bandera
    
    def getBanderaArreglo(self):
        return self.bandera_arreglo

    
    def getNode(self):
        'CONSTRUYE NODO PARA PRIMITIVOS'
        nodoPrimitivo = NodoArbol("PRIMITIVO") #NOMBRE PADRE
        nodoPrimitivo.agregarHijoSinNodo(str(self.valor)) #valor = valor de cadena,entero,bool,ide
        return nodoPrimitivo
    
