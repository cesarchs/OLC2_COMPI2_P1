from Expresiones.primitivos import Primitivos
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Return2 import ReturnC3D
from TS.Tipo import tipo, operador_relacional


class Relacional(instruccion):
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
        der = self.OperacionDer.interpretar(tree,table)     #almacena el valor
        if isinstance(der,Excepcion):return der#verificamos si es error
        

#***********************************************************************************************************************************


#OJO lee javier el if de abajo y el ctrl+h para cambiar megadatos


        if self.operador==operador_relacional.MENOR:  #SUMA elif seria para string * string de julia, String ^ 3 
            
          if self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) < self.obtenerVal(self.OperacionDer,der)

          elif self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo      
                return self.obtenerVal(self.OperacionIzq,izq) < self.obtenerVal(self.OperacionDer,der)

          elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo            
                return self.obtenerVal(self.OperacionIzq,izq) < self.obtenerVal(self.OperacionDer,der)           

          elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) < self.obtenerVal(self.OperacionDer,der)
          
          
          elif self.OperacionIzq.tipo ==tipo.CADENA and self.OperacionDer.tipo ==tipo.CADENA:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) < self.obtenerVal(self.OperacionDer,der)
           
            #si no entra en nada F es error
          return Excepcion("Semantico","tipo erroneo de operacion para la (<)",self.fila,self.columna)




        elif self.operador==operador_relacional.MAYOR:  #SUMA elif seria para string * string de julia, String ^ 3 
            
          if self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) > self.obtenerVal(self.OperacionDer,der)

          elif self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo      
                return self.obtenerVal(self.OperacionIzq,izq) > self.obtenerVal(self.OperacionDer,der)

          elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo            
                return self.obtenerVal(self.OperacionIzq,izq) > self.obtenerVal(self.OperacionDer,der)           

          elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) > self.obtenerVal(self.OperacionDer,der)
          
          
          elif self.OperacionIzq.tipo ==tipo.CADENA and self.OperacionDer.tipo ==tipo.CADENA:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) > self.obtenerVal(self.OperacionDer,der)
           
          #si no entra en nada F es error
          return Excepcion("Semantico","tipo erroneo de operacion para la (>) opizq tipo:"+str(self.OperacionIzq.tipo)+" opder tipo:"+str(self.OperacionDer.tipo)+"",self.fila,self.columna)







        elif self.operador==operador_relacional.MAYORQUE:  #SUMA elif seria para string * string de julia, String ^ 3 
            
          if self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) >= self.obtenerVal(self.OperacionDer,der)

          elif self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo      
                return self.obtenerVal(self.OperacionIzq,izq) >= self.obtenerVal(self.OperacionDer,der)

          elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo            
                return self.obtenerVal(self.OperacionIzq,izq) >= self.obtenerVal(self.OperacionDer,der)           

          elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) >= self.obtenerVal(self.OperacionDer,der)
          
          
          elif self.OperacionIzq.tipo ==tipo.CADENA and self.OperacionDer.tipo ==tipo.CADENA:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) >= self.obtenerVal(self.OperacionDer,der)
           
          #si no entra en nada F es error
          return Excepcion("Semantico","tipo erroneo de operacion para la (>=)",self.fila,self.columna)






        elif self.operador==operador_relacional.MENORQUE:  #SUMA elif seria para string * string de julia, String ^ 3 
            
          if self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) <= self.obtenerVal(self.OperacionDer,der)

          elif self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo      
                return self.obtenerVal(self.OperacionIzq,izq) <= self.obtenerVal(self.OperacionDer,der)

          elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo            
                return self.obtenerVal(self.OperacionIzq,izq) <= self.obtenerVal(self.OperacionDer,der)           

          elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) <= self.obtenerVal(self.OperacionDer,der)
          
          
          elif self.OperacionIzq.tipo ==tipo.CADENA and self.OperacionDer.tipo ==tipo.CADENA:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) <= self.obtenerVal(self.OperacionDer,der)
           
          #si no entra en nada F es error
          return Excepcion("Semantico","tipo erroneo de operacion para la (<=)",self.fila,self.columna)



        elif self.operador==operador_relacional.IGUALIGUAL:  #SUMA elif seria para string * string de julia, String ^ 3 
            
          if self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) == self.obtenerVal(self.OperacionDer,der)

          elif self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo      
                return self.obtenerVal(self.OperacionIzq,izq) == self.obtenerVal(self.OperacionDer,der)

          elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo            
                return self.obtenerVal(self.OperacionIzq,izq) == self.obtenerVal(self.OperacionDer,der)           

          elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) == self.obtenerVal(self.OperacionDer,der)
          
          
          elif self.OperacionIzq.tipo ==tipo.CADENA and self.OperacionDer.tipo ==tipo.CADENA:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) == self.obtenerVal(self.OperacionDer,der)

            #cad-int,cad-float,cad-bool,cad-char
            #no se si agregar estas relaciones
          elif self.OperacionIzq.tipo ==tipo.BOOLEANO and self.OperacionDer.tipo ==tipo.BOOLEANO:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) == self.obtenerVal(self.OperacionDer,der)
           
          #si no entra en nada F es error
          return Excepcion("Semantico","tipo erroneo de operacion para la (==)",self.fila,self.columna)




        elif self.operador==operador_relacional.DIFERENTE:  #SUMA elif seria para string * string de julia, String ^ 3 
            
          if self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) != self.obtenerVal(self.OperacionDer,der)

          elif self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo      
                return self.obtenerVal(self.OperacionIzq,izq) != self.obtenerVal(self.OperacionDer,der)

          elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo            
                return self.obtenerVal(self.OperacionIzq,izq) != self.obtenerVal(self.OperacionDer,der)           

          elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) != self.obtenerVal(self.OperacionDer,der)
          
          
          elif self.OperacionIzq.tipo ==tipo.CADENA and self.OperacionDer.tipo ==tipo.CADENA:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) != self.obtenerVal(self.OperacionDer,der)

            #cad-int,cad-float,cad-bool,cad-char
            #no se si agregar estas relaciones
          elif self.OperacionIzq.tipo ==tipo.BOOLEANO and self.OperacionDer.tipo ==tipo.BOOLEANO:#izq almacena el valor pero no el tipo
                return self.obtenerVal(self.OperacionIzq,izq) != self.obtenerVal(self.OperacionDer,der)
           
          #si no entra en nada F es error
          return Excepcion("Semantico","tipo erroneo de operacion para la (!=)",self.fila,self.columna)




      #posible error sino entra a nada relacional
        return Excepcion("Semantico","tipo de operacion no especificado",self.fila,self.columna)


#VIDEO 5 MIN 15:29 no olvidar ctrol+h para remplazar un monton de datos

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
      nodo = NodoAST("RELACIONAL")

      nodo.agregarHijoNodo(self.OperacionIzq.getNodo())

      nodo.agregarHijo(str(self.operador))#CAMBIAR PARA Q SALGA EL +,- ETC
            #ejemplo tipo SUMA = 0 se debe de ver + switch case

      nodo.agregarHijoNodo(self.OperacionDer.getNodo())


      return nodo


################################################################################################################################
################################################################################################################################
################################################################################################################################  proyeto 2

    def getOperador(self):#devuelvo que tipo de operacion estoy usando es para hacerlo mas pro
        if self.operador==operador_relacional.MAYOR:
            return '>'
        elif self.operador==operador_relacional.MENOR:
            return '<'
        elif self.operador==operador_relacional.MAYORQUE:
            return '>='
        elif self.operador==operador_relacional.MENORQUE:
            return '<='
        elif self.operador==operador_relacional.IGUALIGUAL:
            return '=='
        elif self.operador==operador_relacional.DIFERENTE:
            return '!='


    def checkLabels(self):#si no hay labels true o false las creo para mis expresiones relacionales
            genAux = Generator()
            generator = genAux.getInstance()
            if self.LV == '':
                  self.LV = generator.newLabel()
            if self.LF == '':
                  self.LF = generator.newLabel()



    def compilar(self, tree, table):
      genAux = Generator()
      generator = genAux.getInstance()#obtengo mi static generator
      generator.addCommit("_________INICIO EXPRESION RELACIONAL_________")

      left = self.OperacionIzq.compilar(tree,table)
      right=None # para bckup
      result = ReturnC3D(None, tipo.BOOLEANO, False)#lo q retornare a futuro

      if left.tipo != tipo.BOOLEANO:#caso de !BOOL op !BOOL
            right = self.OperacionDer.compilar(tree,table)
            if (left.tipo == tipo.ENTERO or left.tipo == tipo.DECIMAL) and (right.tipo == tipo.ENTERO or right.tipo == tipo.DECIMAL):
                self.checkLabels()
                
                generator.addIf(left.valor, right.valor, self.getOperador(), self.LV)# if Tn (>|<.....) Tm {goto L1}
                #generator.addCommit("MIERDER....")
                generator.addGoto(self.LF)#else goto L0



                result.trueLbl = self.LV
                result.falseLbl = self.LF
                return result




            elif left.tipo == tipo.CADENA and right.tipo == tipo.CADENA:#AQUI AUN HACE FALTA HACER ESTO :(
               
                generator.addCommit("$$$$$$$$$$$$$$$$$$$$$$$$$ COMPARANDO CADENAS $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                
                #llamare a la funcion nativa q compare las 2 cadenas y si son igual devuelve 1 ,else 0
                ##################
                # IN PROGRESS(SUCCESSFUL)
                generator.addCommit("-------------CADENA "+self.getOperador()+" CADENA-------------")
                
                if self.getOperador()=="==":
                      generator.fStringIgual()
                else:
                      generator.fStringNotIgual()

                paramTemp = generator.addTemporal()
                paramTemp2 = generator.addTemporal()
                #--------------------1 param
                generator.addExp(paramTemp, 'P', table.size, '+')
                generator.addExp(paramTemp, paramTemp, '1', '+')
                generator.setStack(paramTemp, left.valor)
                #--------------------fin 1 param

                #--------------------2 param
                generator.addExp(paramTemp2, 'P', table.size, '+')
                generator.addExp(paramTemp2, paramTemp2, '2', '+')
                generator.setStack(paramTemp2, right.valor)
                #--------------------fin 2 param

                generator.newEnv(table.size)

                if self.getOperador()=="==":
                  generator.callFuncion('IgualdadString')
                else:
                  generator.callFuncion('DesigualdadString')

                temp = generator.addTemporal()
                generator.getStack(temp, 'P')#obtengo el valor dela funcion creada por mi "la cadena ya sumada"
                generator.retEnv(table.size)

                ##################
                #END
                
                
                
                
                self.checkLabels()
                #print("+++izq:"+str(left.valor)+" der:"+str(right.valor))
                generator.addIf(temp, 1, self.getOperador(), self.LV)# if Tn (>|<.....) Tm {goto L1}
               
                generator.addGoto(self.LF)#else goto L0



                result.trueLbl = self.LV
                result.falseLbl = self.LF
                return result
            
            else:
                  return Excepcion("Semantico","tipo erroneo de operacion para la ("+self.getOperador()+") izq:"+str(left.tipo)+" der:"+str(right.tipo),self.fila,self.columna)# OJO PORQ PUEDEN GENERAR LABELS INALCANZABLES AL NO SEGUIR EJECUTANDO CODIGO



      else:#caso de BOOL op BOOL donde true=1 y false=0

            gotoRight = generator.newLabel()#label para comparar el lado derecho de nuestra expresion
            leftTemp = generator.addTemporal()# guarda el resultado del lado izq

            generator.inputLabel(left.trueLbl)
            generator.addExp(leftTemp, '1', '', '')#asinga un T=1; representa verdadero
            generator.addGoto(gotoRight)#comparar lado derecho

            generator.inputLabel(left.falseLbl)
            generator.addExp(leftTemp, '0', '', '')#asinga un T=10; representa falso

            generator.inputLabel(gotoRight)

            right = self.OperacionDer.compilar(tree,table)############debe quedar aca dice el aux sino queda feo dice
            if right.tipo != tipo.BOOLEANO:
                #print("Error, no se pueden comparar")
                  return Excepcion("Semantico","tipo erroneo de operador derecho para la operacion entre booleanos ("+self.getOperador()+")",self.fila,self.columna)# OJO PORQ PUEDEN GENERAR LABELS INALCANZABLES AL NO SEGUIR EJECUTANDO CODIGO
                  #right.trueLbl=generator.newLabel()
                  #right.falseLbl=generator.newLabel()
                  pass

            gotoEnd = generator.newLabel()
            rightTemp = generator.addTemporal()

            if right.trueLbl!="":
                  generator.inputLabel(right.trueLbl)
            
            generator.addExp(rightTemp, '1', '', '')
            generator.addGoto(gotoEnd)


            if right.falseLbl!="":
                  generator.inputLabel(right.falseLbl)

            generator.addExp(rightTemp, '0', '', '')
            generator.inputLabel(gotoEnd)

            self.checkLabels()
            generator.addIf(leftTemp, rightTemp, self.getOperador(), self.LV)
            generator.addGoto(self.LF)

      generator.addCommit("FIN DE EXPRESION RELACIONAL")
      generator.addSaltoLinea()
      result.trueLbl = self.LV
      result.falseLbl = self.LF

      return result

































