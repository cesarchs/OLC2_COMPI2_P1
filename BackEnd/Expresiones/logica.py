from Expresiones.primitivos import Primitivos
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Return2 import ReturnC3D
from TS.Tipo import tipo, operador_logico


class Logica(instruccion):
      def __init__(self, operador, OperacionIzq,OperacionDer,fila,columna):
        self.operador =operador
        self.OperacionIzq=OperacionIzq
        self.OperacionDer=OperacionDer
        self.fila=fila
        self.columna=columna

        self.tipo=tipo.BOOLEANO
        self.LV=""
        self.LF=""

        

      def interpretar(self, tree, table):
        izq = self.OperacionIzq.interpretar(tree,table)         #almacena el valor
        if isinstance(izq,Excepcion):return izq#verificamos si es error

        #negativo
        if self.OperacionDer!=None:
            der = self.OperacionDer.interpretar(tree,table)     #almacena el valor
            if isinstance(der,Excepcion):return der#verificamos si es error
        


        if self.operador==operador_logico.AND: 
          if self.OperacionIzq.tipo ==tipo.BOOLEANO and self.OperacionDer.tipo ==tipo.BOOLEANO:   #izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) and self.obtenerVal(self.OperacionDer,der)
            #si no entra en nada F es error
          return Excepcion("Semantico","tipo erroneo de operacion para la (&&) opizq tipo:"+str(self.OperacionIzq.tipo)+" opder tipo:"+str(self.OperacionDer.tipo)+"",self.fila,self.columna)

        



        elif self.operador==operador_logico.OR:    
          if self.OperacionIzq.tipo ==tipo.BOOLEANO and self.OperacionDer.tipo ==tipo.BOOLEANO:   #izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) or self.obtenerVal(self.OperacionDer,der)
            #si no entra en nada F es error
          return Excepcion("Semantico","tipo erroneo de operacion para la (||)",self.fila,self.columna)




        if self.operador==operador_logico.NOT: 
            
          if self.OperacionIzq.tipo ==tipo.BOOLEANO:   #izq almacena el valor pero no el tipo
                
                return not self.obtenerVal(self.OperacionIzq,izq)

            #si no entra en nada F es error
          return Excepcion("Semantico","tipo erroneo de operacion para la (!)",self.fila,self.columna)



        return Excepcion("Semantico","tipo de operacion no especificado",self.fila,self.columna)


      def obtenerVal(self,nodo,val):
    
            if isinstance(val,Primitivos):

                  if nodo.tipo ==tipo.ENTERO:
                        return int(val.valor)
                  if nodo.tipo ==tipo.DECIMAL:
                        return float(val.valor)
                  if nodo.tipo ==tipo.CADENA:
                        return str(val.valor) 
                  if nodo.tipo ==tipo.BOOLEANO:#bool estaba comentado
                        return bool(val.valor)

                  return val# OJO POSIBLE ERROR!~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


            else:


                  if nodo.tipo ==tipo.ENTERO:
                        return int(val)
                  if nodo.tipo ==tipo.DECIMAL:
                        return float(val)
                  if nodo.tipo ==tipo.CADENA:
                        return str(val) 
                  if nodo.tipo ==tipo.BOOLEANO:#bool estaba comentado
                        return bool(val)

                  return val# OJO POSIBLE ERROR!~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



      def getNodo(self):#ahora unas validaciones para ver si existen o no
        nodo = NodoAST("LOGICO")


        if self.OperacionDer!=None:
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())

            nodo.agregarHijo(str(self.operador))#CAMBIAR PARA Q SALGA EL +,- ETC
            #ejemplo tipo SUMA = 0 se debe de ver + switch case

            nodo.agregarHijoNodo(self.OperacionDer.getNodo())



        else:
            nodo.agregarHijo(str(self.operador))#CAMBIAR PARA Q SALGA EL +,- ETC
            #ejemplo tipo SUMA = 0 se debe de ver + switch case

            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())

        return nodo


################################################################################################################################
################################################################################################################################
################################################################################################################################  proyeto 2

      def checkLabels(self):#si no hay labels true o false las creo para mis expresiones relacionales
            genAux = Generator()
            generator = genAux.getInstance()
            if self.LV == '':
                  self.LV = generator.newLabel()
            if self.LF == '':
                  self.LF = generator.newLabel()



      def compilar(self, tree, table):
            genAux = Generator()
            generator = genAux.getInstance()
            generator.addCommit("______________INICIO EXPRESION LOGICA______________")
            self.checkLabels()#inicializo o no las banderas o labels Verdaderas o Falsas
            lblAndOr = ''#label aux para verificar a donde se tiene que ir || label que une el lado izq y lado der dice

            if self.operador == operador_logico.AND:#comparten la etiqueta verdadera
                  lblAndOr = self.OperacionIzq.LV = generator.newLabel()#si del lado izq es verdadero toca q del lado der sea tambien por eso se comparten
                  self.OperacionDer.LV = self.LV#la etiqueta verdadera del lado der va a ser igual al la etiqueta verdadera FINAL de la expresion
                  self.OperacionIzq.LF = self.OperacionDer.LF = self.LF#las etiquetas se comparten tanto del lado izq como der con la FINAL

            elif self.operador == operador_logico.OR:#comparten la etiqueta falsa
                  self.OperacionIzq.LV = self.OperacionDer.LV = self.LV#se comparten etiquetas verdaderas en ambos lados

                  lblAndOr = self.OperacionIzq.LF = generator.newLabel()#si del lado izq es falso toca q del lado der pueda ser o no tambien por eso se comparten
                  self.OperacionDer.LF = self.LF
            else:
                  #print("NOT")##################################  debe de cambiar la labels falsas por las verdaderas y viceversa
                  # analizarndo.................
                  #backupLV = self.LV
                  #self.LV = self.LF
                  #self.LF = backupLV

                  self.OperacionIzq.LF =  self.LV

                  self.OperacionIzq.LV =  self.LF

                  #lblAndOr ='MIERDA'


                  left = self.OperacionIzq.compilar(tree,table)
                  if left.tipo != tipo.BOOLEANO:
                        #print("No se puede utilizar en expresion booleana")
                        return Excepcion("Semantico","tipo erroneo de operacion para la (!)",self.fila,self.columna)

                  #generator.inputLabel(lblAndOr)
                  
                  generator.addCommit("FINALIZO EXPRESION LOGICA")
                  generator.addSaltoLinea()
                  ret = ReturnC3D(None, tipo.BOOLEANO, False)
                  ret.trueLbl = self.LV
                  ret.falseLbl = self.LF
                  return ret






            left = self.OperacionIzq.compilar(tree,table)
            if left.tipo != tipo.BOOLEANO:
                  #print("No se puede utilizar en expresion booleana")
                  return Excepcion("Semantico","operador izq no aplica a bool",self.fila,self.columna)
            generator.inputLabel(lblAndOr)
            right = self.OperacionDer.compilar(tree,table)
            if right.tipo != tipo.BOOLEANO:
                  #print("No se puede utilizar en expresion booleana")
                  return Excepcion("Semantico","operador der no aplica a bool",self.fila,self.columna)
            generator.addCommit("FINALIZO EXPRESION LOGICA")
            generator.addSaltoLinea()
            ret = ReturnC3D(None, tipo.BOOLEANO, False)
            ret.trueLbl = self.LV
            ret.falseLbl = self.LF
            return ret


