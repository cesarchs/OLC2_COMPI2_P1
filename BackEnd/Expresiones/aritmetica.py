
from TS.Generador import Generator
from Expresiones.primitivos import Primitivos
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion
from TS.Return2 import ReturnC3D
from TS.Tipo import tipo, operador_aritmetico

from decimal import Decimal




#QUI AGREGAR SUM CADENAS ETC


class Aritmetica(instruccion):
    def __init__(self, operador, OperacionIzq,OperacionDer,fila,columna):
        self.operador =operador
        self.OperacionIzq=OperacionIzq
        self.OperacionDer=OperacionDer
        self.fila=fila
        self.columna=columna
        self.tipo=None


        self.TMP=""
        self.C3D=""


        

    def interpretar(self, tree, table):#ahora unas validaciones para ver si existen o no
        izq = self.OperacionIzq.interpretar(tree,table)         #almacena el valor
        if isinstance(izq,Excepcion):return izq#verificamos si es error

        #negativo
        if self.OperacionDer!=None:
            der = self.OperacionDer.interpretar(tree,table)     #almacena el valor
            if isinstance(der,Excepcion):return der#verificamos si es error

#***********************************************************************************************************************************


#OJO lee javier el if de abajo
        if self.operador==operador_aritmetico.MAS:  #SUMA elif seria para string * string de julia, String ^ 3 
            
            if self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como int + int = int; tonces el tipo se define como int
                self.tipo=tipo.ENTERO
                return self.obtenerVal(self.OperacionIzq,izq) + self.obtenerVal(self.OperacionDer,der)

#----------------------------------------------------------------------------------float
            elif self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como int + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                return self.obtenerVal(self.OperacionIzq,izq) + self.obtenerVal(self.OperacionDer,der)

            elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como float + int = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                return self.obtenerVal(self.OperacionIzq,izq) + self.obtenerVal(self.OperacionDer,der)           

            elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como float + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                return self.obtenerVal(self.OperacionIzq,izq) + self.obtenerVal(self.OperacionDer,der)
           
            #si no entra en nada F es error
            return Excepcion("Semantico","tipo erroneo de operacion para la (+)",self.fila,self.columna)





#***********************************************************************************************************************************


        elif self.operador==operador_aritmetico.MENOS:
                        
            if self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como int + int = int; tonces el tipo se define como int
                self.tipo=tipo.ENTERO
                return self.obtenerVal(self.OperacionIzq,izq) - self.obtenerVal(self.OperacionDer,der)
            #----------------------------------------------------------------------------------float
            elif self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como int + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                return self.obtenerVal(self.OperacionIzq,izq) - self.obtenerVal(self.OperacionDer,der)

            elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como float + int = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                return self.obtenerVal(self.OperacionIzq,izq) - self.obtenerVal(self.OperacionDer,der)           

            elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como float + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                return self.obtenerVal(self.OperacionIzq,izq) - self.obtenerVal(self.OperacionDer,der)
        
            return Excepcion("Semantico","tipo erroneo de operacion para la (-) opizq tipo:"+str(self.OperacionIzq.tipo)+" opder tipo:"+str(self.OperacionDer.tipo)+"",self.fila,self.columna)


#***********************************************************************************************************************************

        elif self.operador==operador_aritmetico.POR:
                        
            if self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como int + int = int; tonces el tipo se define como int
                self.tipo=tipo.ENTERO
                return self.obtenerVal(self.OperacionIzq,izq) * self.obtenerVal(self.OperacionDer,der)
            #----------------------------------------------------------------------------------float
            elif self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como int + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                return self.obtenerVal(self.OperacionIzq,izq) * self.obtenerVal(self.OperacionDer,der)

            elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como float + int = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                return self.obtenerVal(self.OperacionIzq,izq) * self.obtenerVal(self.OperacionDer,der)           

            elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como float + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                return self.obtenerVal(self.OperacionIzq,izq) * self.obtenerVal(self.OperacionDer,der)
            
            elif self.OperacionIzq.tipo ==tipo.CADENA and self.OperacionDer.tipo ==tipo.CADENA:#izq almacena el valor pero no el tipo
                #como float + float = float; tonces el tipo se define como float
                self.tipo=tipo.CADENA
                return self.obtenerVal(self.OperacionIzq,izq) + self.obtenerVal(self.OperacionDer,der)
            
            return Excepcion("Semantico","tipo erroneo de operacion para la (*)",self.fila,self.columna)


#***********************************************************************************************************************************

        elif self.operador==operador_aritmetico.DIV:
                        
            if self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como int + int = int; tonces el tipo se define como int
                self.tipo=tipo.DECIMAL
                if der ==0:
                    return Excepcion("Semantico","DIVIDIDO ENTRE 0!",self.fila,self.columna)

                return self.obtenerVal(self.OperacionIzq,izq) / self.obtenerVal(self.OperacionDer,der)
            #----------------------------------------------------------------------------------float
            elif self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como int + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                if der ==0:
                    return Excepcion("Semantico","DIVIDIDO ENTRE 0!",self.fila,self.columna)
                return self.obtenerVal(self.OperacionIzq,izq) / self.obtenerVal(self.OperacionDer,der)

            elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como float + int = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                if der ==0:
                    return Excepcion("Semantico","DIVIDIDO ENTRE 0!",self.fila,self.columna)
                return self.obtenerVal(self.OperacionIzq,izq) / self.obtenerVal(self.OperacionDer,der)           

            elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como float + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                if der ==0:
                    return Excepcion("Semantico","DIVIDIDO ENTRE 0!",self.fila,self.columna)
                return self.obtenerVal(self.OperacionIzq,izq) / self.obtenerVal(self.OperacionDer,der)

            return Excepcion("Semantico","tipo erroneo de operacion para la (/)",self.fila,self.columna)

#***********************************************************************************************************************************

        elif self.operador==operador_aritmetico.MODULO:
                        
            if self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como int + int = int; tonces el tipo se define como int
                self.tipo=tipo.ENTERO
                return self.obtenerVal(self.OperacionIzq,izq) % self.obtenerVal(self.OperacionDer,der)
            #----------------------------------------------------------------------------------float
            elif self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como int + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                return self.obtenerVal(self.OperacionIzq,izq) % self.obtenerVal(self.OperacionDer,der)

            elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como float + int = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                return self.obtenerVal(self.OperacionIzq,izq) % self.obtenerVal(self.OperacionDer,der)           

            elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como float + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                return self.obtenerVal(self.OperacionIzq,izq) % self.obtenerVal(self.OperacionDer,der)

            return Excepcion("Semantico","tipo erroneo de operacion para la (%)",self.fila,self.columna)


        elif self.operador==operador_aritmetico.POTENCIA:
                        
            if self.OperacionIzq.tipo ==tipo.CADENA and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como int + int = int; tonces el tipo se define como int
                self.tipo=tipo.CADENA
                return self.POTENCIA_CADENA( self.obtenerVal(self.OperacionIzq,izq), self.obtenerVal(self.OperacionDer,der) )
            #----------------------------------------------------------------------------------float
            elif self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como int + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL

                try:
                    return pow(self.obtenerVal(self.OperacionIzq,izq), self.obtenerVal(self.OperacionDer,der)) 
                except:
                    return Excepcion("OverflowError","Result too large operacion (^)",self.fila,self.columna)
                

            elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como float + int = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                try:
                    return pow(self.obtenerVal(self.OperacionIzq,izq),self.obtenerVal(self.OperacionDer,der))
                except:
                    return Excepcion("OverflowError","Result too large operacion (^)",self.fila,self.columna)        

            elif self.OperacionIzq.tipo ==tipo.DECIMAL and self.OperacionDer.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como float + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                try:
                    return pow(self.obtenerVal(self.OperacionIzq,izq),self.obtenerVal(self.OperacionDer,der))
                except:
                    return Excepcion("OverflowError","Result too large operacion (^)",self.fila,self.columna)        


            elif self.OperacionIzq.tipo ==tipo.ENTERO and self.OperacionDer.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como int + float = float; tonces el tipo se define como float
                self.tipo=tipo.ENTERO
                try:
                    return pow(self.obtenerVal(self.OperacionIzq,izq),self.obtenerVal(self.OperacionDer,der))
                except:
                    return Excepcion("OverflowError","Result too large operacion (^)",self.fila,self.columna)        


            
            return Excepcion("Semantico","tipo erroneo de operacion para la (^)",self.fila,self.columna)


        elif self.operador==operador_aritmetico.COMA:

            if self.OperacionIzq.tipo ==tipo.CADENA and self.OperacionDer.tipo ==tipo.CADENA:#izq almacena el valor pero no el tipo
                #como float + float = float; tonces el tipo se define como float
                self.tipo=tipo.CADENA
                return self.obtenerVal(self.OperacionIzq,izq) + self.obtenerVal(self.OperacionDer,der)
            
            return Excepcion("Semantico","tipo erroneo de operacion para la (,) en IMPRESIONES",self.fila,self.columna)


#NEGATIVOS
        elif self.operador==operador_aritmetico.UMENOS:
                        
            if self.OperacionIzq.tipo ==tipo.ENTERO :
                #como int + int = int; tonces el tipo se define como int
                self.tipo=tipo.ENTERO
                return self.obtenerVal(self.OperacionIzq,izq) * -1
            #----------------------------------------------------------------------------------float
            elif self.OperacionIzq.tipo ==tipo.DECIMAL :
                #como int + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                return - self.obtenerVal(self.OperacionIzq,izq)

            return Excepcion("Semantico","tipo erroneo de operacion para -unario",self.fila,self.columna)
        
        return Excepcion("Semantico","tipo de operacion no especificado",self.fila,self.columna)




















    def compilar(self, tree, table):#ahora unas validaciones para ver si existen o no
        

        izq = self.OperacionIzq.compilar(tree,table)         #almacena el valor
        if isinstance(izq,Excepcion):return izq#verificamos si es error

        #negativo
        if self.OperacionDer!=None:
            der = self.OperacionDer.compilar(tree,table)     #almacena el valor
            if isinstance(der,Excepcion):return der#verificamos si es error


        genAux = Generator()
        generator = genAux.getInstance()
        

#***********************************************************************************************************************************

        if self.operador==operador_aritmetico.MAS:
            temp = generator.addTemporal()
            if izq.tipo ==tipo.ENTERO and der.tipo ==tipo.ENTERO:
                self.tipo=tipo.ENTERO
                generator.addExp(temp,izq.valor,der.valor,"+")
                return ReturnC3D(temp,self.tipo,True)

#----------------------------------------------------------------------------------float
            elif izq.tipo ==tipo.ENTERO and der.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como int + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                generator.addExp(temp,izq.valor,der.valor,"+")
                return ReturnC3D(temp,self.tipo,True)

            elif izq.tipo ==tipo.DECIMAL and der.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como float + int = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                generator.addExp(temp,izq.valor,der.valor,"+")
                return ReturnC3D(temp,self.tipo,True)       

            elif izq.tipo ==tipo.DECIMAL and der.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como float + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                generator.addExp(temp,izq.valor,der.valor,"+")
                return ReturnC3D(temp,self.tipo,True)
           
            #si no entra en nada F es error
            return Excepcion("Semantico","tipo erroneo de operacion para la (+) izq:"+str(izq.tipo)+", der:"+str(der.tipo)+"",self.fila,self.columna)







#***********************************************************************************************************************************


        elif self.operador==operador_aritmetico.MENOS:
            temp = generator.addTemporal()
            if izq.tipo ==tipo.ENTERO and der.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como int + int = int; tonces el tipo se define como int
                self.tipo=tipo.ENTERO
                generator.addExp(temp,izq.valor,der.valor,"-")
                return ReturnC3D(temp,self.tipo,True)
            #----------------------------------------------------------------------------------float
            elif izq.tipo ==tipo.ENTERO and der.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como int + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                generator.addExp(temp,izq.valor,der.valor,"-")
                return ReturnC3D(temp,self.tipo,True)

            elif izq.tipo ==tipo.DECIMAL and der.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como float + int = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                generator.addExp(temp,izq.valor,der.valor,"-")
                return ReturnC3D(temp,self.tipo,True)        

            elif izq.tipo ==tipo.DECIMAL and der.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como float + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                generator.addExp(temp,izq.valor,der.valor,"-")
                return ReturnC3D(temp,self.tipo,True)
        
            return Excepcion("Semantico","tipo erroneo de operacion para la (-) opizq tipo:"+str(izq.tipo)+" opder tipo:"+str(der.tipo)+"",self.fila,self.columna)


#***********************************************************************************************************************************

        elif self.operador==operador_aritmetico.POR:
            temp = generator.addTemporal()
            if izq.tipo ==tipo.ENTERO and der.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como int + int = int; tonces el tipo se define como int
                self.tipo=tipo.ENTERO
                generator.addExp(temp,izq.valor,der.valor,"*")
                return ReturnC3D(temp,self.tipo,True)
            #----------------------------------------------------------------------------------float
            elif izq.tipo ==tipo.ENTERO and der.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como int + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                generator.addExp(temp,izq.valor,der.valor,"*")
                return ReturnC3D(temp,self.tipo,True)

            elif izq.tipo ==tipo.DECIMAL and der.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como float + int = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                generator.addExp(temp,izq.valor,der.valor,"*")
                return ReturnC3D(temp,self.tipo,True)        

            elif izq.tipo ==tipo.DECIMAL and der.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como float + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                generator.addExp(temp,izq.valor,der.valor,"*")
                return ReturnC3D(temp,self.tipo,True)
            
            elif izq.tipo ==tipo.CADENA and der.tipo ==tipo.CADENA:#izq almacena el valor pero no el tipo
                #como float + float = float; tonces el tipo se define como float
                self.tipo=tipo.CADENA

                ##################
                # IN PROGRESS(SUCCESSFUL)
                generator.addCommit("-------------CONCATENAR CADENA*CADENA-------------")
                generator.fConcatString()

                paramTemp = generator.addTemporal()
                paramTemp2 = generator.addTemporal()
                #--------------------1 param
                generator.addExp(paramTemp, 'P', table.size, '+')
                generator.addExp(paramTemp, paramTemp, '1', '+')
                generator.setStack(paramTemp, izq.valor)
                #--------------------fin 1 param

                #--------------------2 param
                generator.addExp(paramTemp2, 'P', table.size, '+')
                generator.addExp(paramTemp2, paramTemp2, '2', '+')
                generator.setStack(paramTemp2, der.valor)
                #--------------------fin 2 param

                generator.newEnv(table.size)
                generator.callFuncion('concatString')

                temp = generator.addTemporal()
                generator.getStack(temp, 'P')#obtengo el valor dela funcion creada por mi "la cadena ya sumada"
                generator.retEnv(table.size)

                ##################
                #END
                return ReturnC3D(temp,self.tipo,True)
            
            return Excepcion("Semantico","tipo erroneo de operacion para la (*) izq:"+str(izq.tipo)+", der:"+str(der.tipo)+"",self.fila,self.columna)


#***********************************************************************************************************************************

        elif self.operador==operador_aritmetico.DIV:
            temp = generator.addTemporal()       
            if izq.tipo ==tipo.ENTERO and der.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como int + int = int; tonces el tipo se define como int
                self.tipo=tipo.DECIMAL

                der2 = self.OperacionDer.interpretar(tree,table)     #almacena el valor
                if isinstance(der2,Excepcion):return der2#verificamos si es error ejem DIV 0

                if float(der2) ==0:
                    #self.MathError( tree, table)--------------------------------------------------

                    self.MathError(generator,izq,der,temp)

                    #generator.addExp(temp,izq.valor,der.valor,"/")  #temp=izq.v/der.v
                    return ReturnC3D(temp,self.tipo,True)

                #-----------------------------------------------------------------------------------
                self.MathError(generator,izq,der,temp)
                return ReturnC3D(temp,self.tipo,True)
            #----------------------------------------------------------------------------------float
            elif izq.tipo ==tipo.ENTERO and der.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como int + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL

                der2 = self.OperacionDer.interpretar(tree,table)     #almacena el valor
                if isinstance(der2,Excepcion):return der2#verificamos si es error ejem DIV 0

                if float(der2) ==0:
                    #self.MathError( tree, table)
                    self.MathError(generator,izq,der,temp)

                    #generator.addExp(temp,izq.valor,der.valor,"/")  #temp=izq.v/der.v
                    return ReturnC3D(temp,self.tipo,True)
                
                self.MathError(generator,izq,der,temp)
                return ReturnC3D(temp,self.tipo,True)

            elif izq.tipo ==tipo.DECIMAL and der.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como float + int = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL

                der2 = self.OperacionDer.interpretar(tree,table)     #almacena el valor
                if isinstance(der2,Excepcion):return der2#verificamos si es error ejem DIV 0

                if float(der2) ==0:
                    #self.MathError( tree, table)

                    self.MathError(generator,izq,der,temp)
                    #generator.addExp(temp,izq.valor,der.valor,"/")  #temp=izq.v/der.v
                    return ReturnC3D(temp,self.tipo,True)
                
                self.MathError(generator,izq,der,temp)
                return ReturnC3D(temp,self.tipo,True)         

            elif izq.tipo ==tipo.DECIMAL and der.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como float + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                
                der2 = self.OperacionDer.interpretar(tree,table)     #almacena el valor
                if isinstance(der2,Excepcion):return der2#verificamos si es error ejem DIV 0

                if float(der2) ==0:
                    #self.MathError( tree, table)
                    self.MathError(generator,izq,der,temp)
                    #generator.addExp(temp,izq.valor,der.valor,"/")  #temp=izq.v/der.v
                    return ReturnC3D(temp,self.tipo,True)
                    
                
                self.MathError(generator,izq,der,temp)
                return ReturnC3D(temp,self.tipo,True)

            return Excepcion("Semantico","tipo erroneo de operacion para la (/) izq:"+str(izq.tipo)+", der:"+str(der.tipo)+"",self.fila,self.columna)







#***********************************************************************************************************************************



#falta implemetar aqui el self.MathError(generator,izq,der,temp)



        elif self.operador==operador_aritmetico.MODULO:####AQUI TIENE ERRORES :( CON LOS Ts
            temp = generator.addTemporal() 
            if izq.tipo ==tipo.ENTERO and der.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como int + int = int; tonces el tipo se define como int
                self.tipo=tipo.ENTERO
                generator.math=";\n\t\"math\""
                generator.addExp(temp,'math.Mod('+izq.valor,der.valor+')',",")
                #generator.addExp(temp,izq.valor,der.valor,"%")
                return ReturnC3D(temp,self.tipo,True)
            #----------------------------------------------------------------------------------float
            elif izq.tipo ==tipo.ENTERO and der.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como int + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                generator.math=";\n\t\"math\""
                generator.addExp(temp,'math.Mod('+izq.valor,der.valor+')',",")
                #generator.addExp(temp,izq.valor,der.valor,"%")
                return ReturnC3D(temp,self.tipo,True)

            elif izq.tipo ==tipo.DECIMAL and der.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como float + int = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                generator.math=";\n\t\"math\""
                generator.addExp(temp,'math.Mod('+izq.valor,der.valor+')',",")
                #generator.addExp(temp,izq.valor,der.valor,"%")
                return ReturnC3D(temp,self.tipo,True)         

            elif izq.tipo ==tipo.DECIMAL and der.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como float + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                generator.math=";\n\t\"math\""
                generator.addExp(temp,'math.Mod('+izq.valor,der.valor+')',",")
                #generator.addExp(temp,izq.valor,der.valor,"%")
                return ReturnC3D(temp,self.tipo,True)

            return Excepcion("Semantico","tipo erroneo de operacion para la (%) izq:"+str(izq.tipo)+", der:"+str(der.tipo)+"",self.fila,self.columna)







        elif self.operador==operador_aritmetico.POTENCIA:
                        
            if izq.tipo ==tipo.CADENA and der.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como int + int = int; tonces el tipo se define como int
                self.tipo=tipo.CADENA

                ##################
                # IN PROGRESS(SUCCESSFUL)
                generator.addCommit("-------------POTENCIA CADENA^N -------------")
                generator.fElevateString()

                paramTemp = generator.addTemporal()
                paramTemp2 = generator.addTemporal()
                #--------------------1 param
                generator.addExp(paramTemp, 'P', table.size, '+')
                generator.addExp(paramTemp, paramTemp, '1', '+')
                generator.setStack(paramTemp, izq.valor)
                #--------------------fin 1 param

                #--------------------2 param
                generator.addExp(paramTemp2, 'P', table.size, '+')
                generator.addExp(paramTemp2, paramTemp2, '2', '+')
                generator.setStack(paramTemp2, der.valor)
                #--------------------fin 2 param

                generator.newEnv(table.size)
                generator.callFuncion('elevateString')

                temp = generator.addTemporal()
                generator.getStack(temp, 'P')#obtengo el valor dela funcion creada por mi "la cadena ya sumada"
                generator.retEnv(table.size)

                ##################
                #END
                return ReturnC3D(temp,self.tipo,True)
            #----------------------------------------------------------------------------------float
                '''
            elif izq.tipo ==tipo.ENTERO and der.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como int + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL

                try:
                    return pow(self.obtenerVal(self.OperacionIzq,izq), self.obtenerVal(self.OperacionDer,der)) 
                except:
                    return Excepcion("OverflowError","Result too large operacion (^)",self.fila,self.columna)'''
                

            elif izq.tipo ==tipo.DECIMAL and der.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como float + int = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                ##################
                # IN PROGRESS(SUCCESSFUL)
                generator.addCommit("-------------POTENCIA NUMBER^N -------------")
                generator.fElevateNumber()

                paramTemp = generator.addTemporal()
                paramTemp2 = generator.addTemporal()
                #--------------------1 param
                generator.addExp(paramTemp, 'P', table.size, '+')
                generator.addExp(paramTemp, paramTemp, '1', '+')
                generator.setStack(paramTemp, izq.valor)
                #--------------------fin 1 param

                #--------------------2 param
                generator.addExp(paramTemp2, 'P', table.size, '+')
                generator.addExp(paramTemp2, paramTemp2, '2', '+')
                generator.setStack(paramTemp2, der.valor)
                #--------------------fin 2 param

                generator.newEnv(table.size)
                generator.callFuncion('elevateNumber')

                temp = generator.addTemporal()
                generator.getStack(temp, 'P')#obtengo el valor dela funcion creada por mi "la cadena ya sumada"
                generator.retEnv(table.size)

                ##################
                #END
                return ReturnC3D(temp,self.tipo,True)        

                '''
            elif izq.tipo ==tipo.DECIMAL and der.tipo ==tipo.DECIMAL:#izq almacena el valor pero no el tipo
                #como float + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL
                try:
                    return pow(self.obtenerVal(self.OperacionIzq,izq),self.obtenerVal(self.OperacionDer,der))
                except:
                    return Excepcion("OverflowError","Result too large operacion (^)",self.fila,self.columna)'''        


            elif izq.tipo ==tipo.ENTERO and der.tipo ==tipo.ENTERO:#izq almacena el valor pero no el tipo
                #como int + float = float; tonces el tipo se define como float
                self.tipo=tipo.ENTERO
                ##################
                # IN PROGRESS(SUCCESSFUL)
                generator.addCommit("-------------POTENCIA NUMBER^N -------------")
                generator.fElevateNumber()

                paramTemp = generator.addTemporal()
                paramTemp2 = generator.addTemporal()
                #--------------------1 param
                generator.addExp(paramTemp, 'P', table.size, '+')
                generator.addExp(paramTemp, paramTemp, '1', '+')
                generator.setStack(paramTemp, izq.valor)
                #--------------------fin 1 param

                #--------------------2 param
                generator.addExp(paramTemp2, 'P', table.size, '+')
                generator.addExp(paramTemp2, paramTemp2, '2', '+')
                generator.setStack(paramTemp2, der.valor)
                #--------------------fin 2 param

                generator.newEnv(table.size)
                generator.callFuncion('elevateNumber')

                temp = generator.addTemporal()
                generator.getStack(temp, 'P')#obtengo el valor dela funcion creada por mi "la cadena ya sumada"
                generator.retEnv(table.size)

                ##################
                #END
                return ReturnC3D(temp,self.tipo,True)       


            
            return Excepcion("Semantico","tipo erroneo de operacion para la (^) izq:"+str(izq.tipo)+", der:"+str(der.tipo)+"",self.fila,self.columna)






#NEGATIVOS
        elif self.operador==operador_aritmetico.UMENOS:
            temp = generator.addTemporal()            
            if izq.tipo ==tipo.ENTERO :
                #como int + int = int; tonces el tipo se define como int
                self.tipo=tipo.ENTERO
                
                generator.addExp(temp,"0",izq.valor,"-")
                return ReturnC3D(temp,self.tipo,True)
            #----------------------------------------------------------------------------------float
            elif izq.tipo ==tipo.DECIMAL :
                #como int + float = float; tonces el tipo se define como float
                self.tipo=tipo.DECIMAL

                generator.addExp(temp,"0",izq.valor,"-")
                return ReturnC3D(temp,self.tipo,True)

            return Excepcion("Semantico","tipo erroneo de operacion para -unario",self.fila,self.columna)
        
        return Excepcion("Semantico","tipo de operacion no especificado",self.fila,self.columna)



    def POTENCIA_CADENA(self,string,veces):
        cadena=string
        count = 1
        while (count < veces):
            cadena+=string
            count+=1
        return cadena




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
        nodo = NodoAST("ARITMETICA")


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
            


    def MathError(self,generator,izq,der,temp):
        
       
       # tree.contadorLV_LF = tree.contadorLV_LF+1#contador de Ls

        #return self.C3D creo q deberia ser self, para que sepa q tipo es y ademas ya con eso obtengo el c3d
        
        #larga_cadena = "fmt.Printf(\"%c\", 77);\nfmt.Printf(\"%c\", 97);\nfmt.Printf(\"%c\", 116);\nfmt.Printf(\"%c\", 104);\nfmt.Printf(\"%c\", 69);\nfmt.Printf(\"%c\", 114);\nfmt.Printf(\"%c\", 114);\nfmt.Printf(\"%c\", 111);\nfmt.Printf(\"%c\", 114);\nT"+str(tree.contador+1)+" = 0;\ngoto L"+str(tree.contadorLV_LF+1)+";\nL"+str(tree.contadorLV_LF)+":\nT"+str(tree.contador+1)+" = "+self.OperacionIzq.TMP+" / "+self.OperacionDer.TMP+";\nL"+str(tree.contadorLV_LF+1)+":\n"
                                                                                                                                                                                                                                                                                                                                                                                                   

        #tree.contador=tree.contador+1#contador de Ts
        #self.TMP="T"+str(tree.contador)
        #self.C3D = self.OperacionIzq.C3D + self.OperacionDer.C3D+""
        #self.C3D+="if (T"+str(tree.contador-1)+" !=0){goto L"+str(tree.contadorLV_LF)+"};\n"+larga_cadena
        #return Excepcion("Semantico","DIVIDIDO ENTRE 0!",self.fila,self.columna)
        #tree.contadorLV_LF = tree.contadorLV_LF+1#contador de Ls
        generator.addCommit("-------------DIVIDIDO 0!-----------------")                                       
        LV = generator.newLabel()
        generator.addIf(der.valor,"0","!=",LV)
        generator.addPrint("c",77,"//M")
        generator.addPrint("c",97,"//a")
        generator.addPrint("c",116,"//t")
        generator.addPrint("c",104,"//h")
        generator.addPrint("c",69,"//E")
        generator.addPrint("c",114,"//r")
        generator.addPrint("c",114,"//r")
        generator.addPrint("c",111,"//o")
        generator.addPrint("c",114,"//r")
        #generator.addPrint('c',10,"//salto de linea")
        generator.addExp(temp,"0","","")
        LS = generator.newLabel()
        generator.addGoto(LS)
        generator.inputLabel(LV)
        if der.valor!='0':
            generator.addExp(temp,izq.valor,der.valor,"/")
        else:#==0 F xd
            generator.addExp(temp,'0','1',"/")
        generator.inputLabel(LS)
      
        