from padres.expresion import Expresion
from padres.expresion import Expresion
from padres.Nodo import NodoArbol
from almacenar.error import Error
from almacenar.tipo import Return, Tipo,OpsAritmetico
from almacenar.generador import Generador

#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol
#from almacenar.error import Error
#from almacenar.tipo import Tipo,OpsAritmetico

class Aritmetica(Expresion):
    def __init__(self, operador, operacionI, operacionD, fil, col):
        super().__init__(fil, col)
        self.operador = operador
        self.operacionI = operacionI
        self.operacionD = operacionD #si fuera unaria esta seria None
        self.fila = fil
        self.columna = col
        self.struct = False
        self.mutable = False
        self.tipo = None #se definira deendiendo de la operación
        
    def compilar(self, arbol, tabla):
        'resisq = resultado opE izquierda, resder = resultado opE derecha'
        
        genAux = Generador()
        generator = genAux.getInstance()
        
        resizq = self.operacionI.compilar(arbol,tabla)
        if isinstance(resizq,Error): return resizq #ya no se sigue y se retorna el error almacenado en resizq
        if self.operacionI.tipo == Tipo.ARREGLO: self.operacionI.tipo = self.getTipo(resizq)
        if self.operacionD != None:
            resder = self.operacionD.compilar(arbol,tabla)
            if isinstance(resder,Error): return resder
            if self.operacionD.tipo == Tipo.ARREGLO: self.operacionD.tipo = self.getTipo(resder)
            
        #BINARIAS:
        
        # OPE1 + OPE2  en julia solo hay sumas aritmeticas con + (SUMA)
        if self.operador == OpsAritmetico.MAS: 
            temp = generator.agregarTemporal();generator.liberarTemporal(temp)
            op = '+'
            #Int64 + Int64
            if self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.ENTERO:
                self.tipo = Tipo.ENTERO
                #return self.getValor(self.operacionI.tipo,resizq) + self.getValor(self.operacionD.tipo,resder)#int64
                generator.addExp(temp,resizq.getValor(),resder.getValor(),op)
                return Return(temp,self.tipo,True)
            #Float64 + Float64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.DECIMAL:
                self.tipo = Tipo.DECIMAL
                generator.addExp(temp,resizq.getValor(),resder.getValor(),op)
                return Return(temp,self.tipo,True)
        
            #Int64 + Float64
            elif self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.DECIMAL:
                self.tipo = Tipo.DECIMAL
                generator.addExp(temp,resizq.getValor(),resder.getValor(),op)
                return Return(temp,self.tipo,True)
        
            #Float64 + Int64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.ENTERO:
                self.tipo = Tipo.DECIMAL
                generator.addExp(temp,resizq.getValor(),resder.getValor(),op)
                return Return(temp,self.tipo,True)
            
            return Error("Semantico", "Este tipo de operacion en '+' no es admitivido.", self.fila, self.columna)
            
        # OPE1 - OPE2 en julia solo hay restas aritmeticas con - (RESTA)
        elif self.operador == OpsAritmetico.MENOS: 
            temp = generator.agregarTemporal();generator.liberarTemporal(temp)
            op = '-'
            #Int64 - Int64
            if self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.ENTERO:
                self.tipo = Tipo.ENTERO
                generator.addExp(temp,resizq.getValor(),resder.getValor(),op)
                return Return(temp,self.tipo,True)
        
            #Float64 + Float64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.DECIMAL:
                self.tipo = Tipo.DECIMAL
                generator.addExp(temp,resizq.getValor(),resder.getValor(),op)
                return Return(temp,self.tipo,True)
        
            #Int64 + Float64
            elif self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.DECIMAL:
                self.tipo = Tipo.DECIMAL
                generator.addExp(temp,resizq.getValor(),resder.getValor(),op)
                return Return(temp,self.tipo,True)
        
            #Float64 + Int64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.ENTERO:
                self.tipo = Tipo.DECIMAL
                generator.addExp(temp,resizq.getValor(),resder.getValor(),op)
                return Return(temp,self.tipo,True)
            
            return Error("Semantico", "Este tipo de operacion en '-' no es admitivido.", self.fila, self.columna)
            
        # OPE1 , OPE2 en julia hay concatenaciones con coma (CONCATENACION)
        elif self.operador == OpsAritmetico.COMA:
            listaexps = [] 
            if self.operacionI.tipo == Tipo.STRUCT and isinstance(resizq,dict): resizq=self.desempaquetarvalor(resizq)
            if self.operacionD.tipo == Tipo.STRUCT and isinstance(resder,dict): resder=self.desempaquetarvalor(resder)
            self.tipo = Tipo.CADENA
            
            if self.operacionI.tipo == Tipo.ENTERO or self.operacionI == Tipo.DECIMAL:
                listaexps.append(self.operacionI)
            if self.operacionD.tipo == Tipo.ENTERO or self.operacionD == Tipo.ENTERO:
                listaexps.append(self.operacionD)
            if self.operacionI.tipo == Tipo.CADENA or self.operacionI.tipo == Tipo.STRUCT:
                generator.concatenarCadena()
                generator.concatenarCadena()
            #  
                paramTemp = generator.agregarTemporal();generator.liberarTemporal(paramTemp)# genero temporal para entorno simulado
            #   #                       CAMBIO DE ENTORNO SIMULADO:
                generator.addExp(paramTemp, 'P', tabla.size, '+') #tn=p+n

            #   #                          ENVÍO DE PARAMETROS
                #param1:
                generator.addExp(paramTemp, paramTemp, '1', '+')  #tn=tn+1
                #valorparam1:
                generator.setPila(paramTemp,resizq.getValor())         #stack[tn]=resizq.temp

            #   #param2:
                generator.addExp(paramTemp, paramTemp, '1', '+')  #tn=tn+1
            #   #valorparam2:
                generator.setPila(paramTemp,resder.getValor())         #stack[tn]=resizq.temp

            #   #                        CAMBIO DE ENTORNO FORMAL
                generator.newEnv(tabla.size)
                generator.llamandaFuncion("nativaconcatenarCadena")

            #   #                        obtengo valor de retorno
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.getPila(temp,'P')

            #   #                       regreso a entorno 

                generator.returnEntorno(tabla.size)

                return Return(temp,self.tipo,True)
                
            
            #if self.operacionI.tipo == Tipo.CADENA and self.operacionD.tipo == Tipo.CADENA or self.operacionI.tipo == Tipo.CADENA and self.operacionD.tipo == Tipo.STRUCT or self.operacionI.tipo == Tipo.STRUCT and self.operacionD.tipo == Tipo.CADENA or self.operacionI.tipo == Tipo.STRUCT and self.operacionD.tipo == Tipo.STRUCT:
            #    generator.concatenarCadena()
            #   
            #    paramTemp = generator.agregarTemporal()# genero temporal para entorno simulado
            #    #                       CAMBIO DE ENTORNO SIMULADO:
            #    generator.addExp(paramTemp, 'P', tabla.size, '+') #tn=p+n
#
            #    #                          ENVÍO DE PARAMETROS
            #    #param1:
            #    generator.addExp(paramTemp, paramTemp, '1', '+')  #tn=tn+1
            #    #valorparam1:
            #    generator.setPila(paramTemp,resizq.valor)         #stack[tn]=resizq.temp
#
            #    #param2:
            #    generator.addExp(paramTemp, paramTemp, '1', '+')  #tn=tn+1
            #    #valorparam2:
            #    generator.setPila(paramTemp,resder.valor)         #stack[tn]=resizq.temp
#
            #    #                        CAMBIO DE ENTORNO FORMAL
            #    generator.newEnv(tabla.size)
            #    generator.llamandaFuncion("nativaconcatenarCadena")
#
            #    #                        obtengo valor de retorno
            #    temp = generator.agregarTemporal()
            #    generator.getPila(temp,'P')
#
            #    #                       regreso a entorno 
#
            #    generator.returnEntorno(tabla.size)
#
            #    return Return(temp,self.tipo,True)
            
#            elif (self.operacionI.tipo == Tipo.CADENA and self.operacionD.tipo == Tipo.ENTERO) or (self.operacionI.tipo == Tipo.CADENA and self.operacionD.tipo == Tipo.DECIMAL):
#                generator.concatStringNum()
#                paramTemp = generator.agregarTemporal()# genero temporal para entorno simulado
#                #                       CAMBIO DE ENTORNO SIMULADO:
#                generator.addExp(paramTemp, 'P', tabla.size, '+') #tn=p+n
#                
#                #                          ENVÍO DE PARAMETROS
#                #param1:
#                generator.addExp(paramTemp, paramTemp, '1', '+')  #tn=tn+1
#                #valorparam1:
#                generator.setPila(paramTemp,resizq.valor)         #stack[tn]=resizq.temp
#                
#                #param2:
#                generator.addExp(paramTemp, paramTemp, '1', '+')  #tn=tn+1
#                #valorparam2:
#                generator.setPila(paramTemp,resder.valor)         #stack[tn]=resizq.temp
#                
#                #                        CAMBIO DE ENTORNO FORMAL
#                generator.newEnv(tabla.size)
#                generator.llamandaFuncion("nativaconcatStringNum")
#                
#                #                        obtengo valor de retorno
#                temp = generator.agregarTemporal()
#                generator.getPila(temp,'P')
#                
#                #                       regreso a entorno 
#                 
#                generator.returnEntorno(tabla.size)
#                 
#                return Return(temp,self.tipo,True)
            
            
            
            #try:
            #    return str(self.getValor(self.operacionI.tipo,resizq)) + str(self.getValor(self.operacionD.tipo,resder))#STRING
            #except:
            #    return Error("Semantico", "Este tipo de operacion en ',' no es admitivido.", self.fila, self.columna)
            #return Error("Semantico", "Este tipo de operacion en ',' no es admitivido.", self.fila, self.columna)
            
        # OPE1 * OPE2  en julia hay multiplicaciones con * y concatenaciones unicamente de strings con * (MULTIPLICACION)
        elif self.operador == OpsAritmetico.POR: 
            temp = generator.agregarTemporal();generator.liberarTemporal(temp)
            op = '*'
            #Int64 * Int64
            if self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.ENTERO:
                self.tipo = Tipo.ENTERO
                generator.addExp(temp,resizq.getValor(),resder.getValor(),op)
                return Return(temp,self.tipo,True)
        
            #Float64 * Float64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.DECIMAL:
                self.tipo = Tipo.DECIMAL
                generator.addExp(temp,resizq.getValor(),resder.getValor(),op)
                return Return(temp,self.tipo,True)
        
            #Int64 * Float64
            elif self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.DECIMAL:
                self.tipo = Tipo.DECIMAL
                generator.addExp(temp,resizq.getValor(),resder.getValor(),op)
                return Return(temp,self.tipo,True)
        
            #Float64 * Int64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.ENTERO:
                self.tipo = Tipo.DECIMAL
                generator.addExp(temp,resizq.getValor(),resder.getValor(),op)
                return Return(temp,self.tipo,True)
            
            #String * String 
            elif self.operacionI.tipo == Tipo.CADENA and self.operacionD.tipo== Tipo.CADENA:
                self.tipo = Tipo.CADENA
                #generator.addExp(temp,resizq.getValor(),resder.valor,op)
                generator.concatenarCadena()
                paramTemp = generator.agregarTemporal();generator.liberarTemporal(temp)# genero temporal para entorno simulado
                
                #   #                       CAMBIO DE ENTORNO SIMULADO:
                generator.addExp(paramTemp, 'P', tabla.size, '+') #tn=p+n

            #   #                          ENVÍO DE PARAMETROS
                #param1:
                generator.addExp(paramTemp, paramTemp, '1', '+')  #tn=tn+1
                #valorparam1:
                generator.setPila(paramTemp,resizq.getValor())         #stack[tn]=resizq.temp
                
                #param2:
                generator.addExp(paramTemp, paramTemp, '1', '+')  #tn=tn+1
            #   #valorparam2:
                generator.setPila(paramTemp,resder.getValor())         #stack[tn]=resizq.temp
                
                #   #                        CAMBIO DE ENTORNO FORMAL
                generator.newEnv(tabla.size)
                generator.llamandaFuncion("nativaconcatenarCadena")

            #   #                        obtengo valor de retorno
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.getPila(temp,'P')
                
                 #   #                       regreso a entorno 

                generator.returnEntorno(tabla.size)

                return Return(temp,self.tipo,True)
            
            return Error("Semantico", "Este tipo de operacion con '*' no es admitivido.", self.fila, self.columna)
         
        # OPE1 / OPE2  en julia hay divisiones con / (DIVISION)
        elif self.operador == OpsAritmetico.DIV:
            if resder.valor != '0':
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                op = '/'
                labelmathTrue= generator.agregarLabel()
                labelmathFalse= generator.agregarLabel()
                #aqui se agregar el codigo para el la comprobacion de si el  denominador es 0
                generator.agregarComentario("COMPROBACION DENOMINADOR ES DIFERENTE DE CERO")
                #generator.agregarIf(resder.temp)
                generator.agregarIf(resder.getValor(),0,'!=',labelmathTrue)
                generator.printMathError()
                generator.addExp(temp,0,'','')
                generator.agregarGoto(labelmathFalse)
                #Int64 / Int64
                if self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.ENTERO:
                    self.tipo = Tipo.DECIMAL
                    generator.colocarLabel(labelmathTrue)
                    generator.addExp(temp,resizq.getValor(),resder.getValor(),op)
                    generator.colocarLabel(labelmathFalse)
                    return Return(temp,self.tipo,True)


                #Float64 / Float64
                elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.DECIMAL:
                    self.tipo = Tipo.DECIMAL
                    generator.colocarLabel(labelmathTrue)
                    generator.addExp(temp,resizq.getValor(),resder.getValor(),op)
                    generator.colocarLabel(labelmathFalse)
                    return Return(temp,self.tipo,True)

                #Int64 / Float64
                elif self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.DECIMAL:
                    self.tipo = Tipo.DECIMAL
                    generator.colocarLabel(labelmathTrue)
                    generator.addExp(temp,resizq.getValor(),resder.getValor(),op)
                    generator.colocarLabel(labelmathFalse)
                    return Return(temp,self.tipo,True)

                #Float64 / Int64
                elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.ENTERO:
                    self.tipo = Tipo.DECIMAL
                    generator.colocarLabel(labelmathTrue)
                    generator.addExp(temp,resizq.getValor(),resder.getValor(),op)
                    generator.colocarLabel(labelmathFalse)
                    return Return(temp,self.tipo,True)
                return Error("Semantico", "Este tipo de operacion en '/' no es admitivido.", self.fila, self.columna)
            else:
                return Error("Semantico", "No se puede dividir por cero",self.fila,self.columna)
        
        # OPE1 % OPE2  en julia hay mods con % (MOD)
        elif self.operador == OpsAritmetico.MOD:
            temp = generator.agregarTemporal();generator.liberarTemporal(temp)
            op = ','
            #Int64 % Int64
            if self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.ENTERO:
                self.tipo = Tipo.ENTERO
                generator.addMathImport()
                generator.addExp(temp,'math.Mod('+resizq.getValor(),resder.getValor()+')',op)
                return Return(temp,self.tipo,True)
        
            #Float64 % Float64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.DECIMAL:
                self.tipo = Tipo.DECIMAL
                generator.addMathImport()
                generator.addExp(temp,'math.Mod('+resizq.getValor(),resder.getValor()+')',op)
                return Return(temp,self.tipo,True)
        
            #Int64 % Float64
            elif self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.DECIMAL:
                self.tipo = Tipo.DECIMAL
                generator.addMathImport()
                generator.addExp(temp,'math.Mod('+resizq.getValor(),resder.getValor()+')',op)
                return Return(temp,self.tipo,True)
        
            #Float64 % Int64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.ENTERO:
                self.tipo = Tipo.DECIMAL
                generator.addMathImport()
                generator.addExp(temp,'math.Mod('+resizq.getValor(),resder.getValor()+')',op)
                return Return(temp,self.tipo,True)
            
            return Error("Semantico", "Este tipo de operacion en '%' no es admitivido.", self.fila, self.columna)
        
        # OPE1 ^ OPE2  en julia hay potencias con ^ y ademas tambien con strings duplicaciones String ^3 = "CadenaCadenaCadena" (POTENCIA)
        elif self.operador == OpsAritmetico.POT:
            tempaux = generator.agregarTemporal();generator.liberarTemporal(tempaux)
            #op = '^'
            #Int64 ^ Int64
            if self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.ENTERO:
                self.tipo = Tipo.ENTERO
                generator.potenciafunc()
                
                tempaux = generator.agregarTemporal();generator.liberarTemporal(tempaux)# genero temporal para entorno simulado
                
                #   #                       CAMBIO DE ENTORNO SIMULADO:
                generator.addExp(tempaux, 'P', tabla.size, '+') #tn=p+n

            #   #                          ENVÍO DE PARAMETROS
                #param1:
                generator.addExp(tempaux, tempaux, '1', '+')  #tn=tn+1
                #valorparam1:
                generator.setPila(tempaux,resizq.getValor())         #stack[tn]=resizq.temp
                
                #param2:
                generator.addExp(tempaux, tempaux, '1', '+')  #tn=tn+1
            #   #valorparam2:
                generator.setPila(tempaux,resder.getValor())         #stack[tn]=resizq.temp
                
                #   #                        CAMBIO DE ENTORNO FORMAL
                generator.newEnv(tabla.size)
                generator.llamandaFuncion("nativaPotencia")

            #   #                        obtengo getValor() de retorno
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.getPila(temp,'P')
                
                 #   #                       regreso a entorno 

                generator.returnEntorno(tabla.size)

                return Return(temp,self.tipo,True)
        
            #Float64 ^ Float64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.DECIMAL:
                self.tipo = Tipo.DECIMAL
                generator.potenciafunc()
                
                tempaux = generator.agregarTemporal();generator.liberarTemporal(tempaux)# genero temporal para entorno simulado
                
                #   #                       CAMBIO DE ENTORNO SIMULADO:
                generator.addExp(tempaux, 'P', tabla.size, '+') #tn=p+n

            #   #                          ENVÍO DE PARAMETROS
                #param1:
                generator.addExp(tempaux, tempaux, '1', '+')  #tn=tn+1
                #valorparam1:
                generator.setPila(tempaux,resizq.getValor())         #stack[tn]=resizq.temp
                
                #param2:
                generator.addExp(tempaux, tempaux, '1', '+')  #tn=tn+1
            #   #valorparam2:
                generator.setPila(tempaux,resder.getValor())         #stack[tn]=resizq.temp
                
                #   #                        CAMBIO DE ENTORNO FORMAL
                generator.newEnv(tabla.size)
                generator.llamandaFuncion("nativaPotencia")

            #   #                        obtengo getValor() de retorno
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.getPila(temp,'P')
                
                 #   #                       regreso a entorno 

                generator.returnEntorno(tabla.size)

                return Return(temp,self.tipo,True)
        
            #Int64 ^ Float64
            elif self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.DECIMAL:
                self.tipo = Tipo.DECIMAL
                generator.potenciafunc()
                
                tempaux = generator.agregarTemporal();generator.liberarTemporal(tempaux)# genero temporal para entorno simulado
                
                #   #                       CAMBIO DE ENTORNO SIMULADO:
                generator.addExp(tempaux, 'P', tabla.size, '+') #tn=p+n

            #   #                          ENVÍO DE PARAMETROS
                #param1:
                generator.addExp(tempaux, tempaux, '1', '+')  #tn=tn+1
                #valorparam1:
                generator.setPila(tempaux,resizq.getValor())         #stack[tn]=resizq.temp
                
                #param2:
                generator.addExp(tempaux, tempaux, '1', '+')  #tn=tn+1
            #   #valorparam2:
                generator.setPila(tempaux,resder.getValor())         #stack[tn]=resizq.temp
                
                #   #                        CAMBIO DE ENTORNO FORMAL
                generator.newEnv(tabla.size)
                generator.llamandaFuncion("nativaPotencia")

            #   #                        obtengo getValor() de retorno
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.getPila(temp,'P')
                
                 #   #                       regreso a entorno 

                generator.returnEntorno(tabla.size)

                return Return(temp,self.tipo,True)
        
            #Float64 * Int64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.ENTERO:
                self.tipo = Tipo.DECIMAL
                generator.potenciafunc()
                
                tempaux = generator.agregarTemporal();generator.liberarTemporal(tempaux)# genero temporal para entorno simulado
                
                #   #                       CAMBIO DE ENTORNO SIMULADO:
                generator.addExp(tempaux, 'P', tabla.size, '+') #tn=p+n

            #   #                          ENVÍO DE PARAMETROS
                #param1:
                generator.addExp(tempaux, tempaux, '1', '+')  #tn=tn+1
                #valorparam1:
                generator.setPila(tempaux,resizq.getValor())         #stack[tn]=resizq.temp
                
                #param2:
                generator.addExp(tempaux, tempaux, '1', '+')  #tn=tn+1
            #   #valorparam2:
                generator.setPila(tempaux,resder.getValor())         #stack[tn]=resizq.temp
                
                #   #                        CAMBIO DE ENTORNO FORMAL
                generator.newEnv(tabla.size)
                generator.llamandaFuncion("nativaPotencia")

            #   #                        obtengo getValor() de retorno
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.getPila(temp,'P')
                
                 #   #                       regreso a entorno 

                generator.returnEntorno(tabla.size)

                return Return(temp,self.tipo,True)
            
            #String * Int64
            elif self.operacionI.tipo == Tipo.CADENA and self.operacionD.tipo== Tipo.ENTERO:
                self.tipo = Tipo.CADENA
                generator.potenciaCadena()
                
                tempaux = generator.agregarTemporal();generator.liberarTemporal(tempaux)# genero temporal para entorno simulado
                
                #   #                       CAMBIO DE ENTORNO SIMULADO:
                generator.addExp(tempaux, 'P', tabla.size, '+') #tn=p+n

            #   #                          ENVÍO DE PARAMETROS
                #param1:
                generator.addExp(tempaux, tempaux, '1', '+')  #tn=tn+1
                #valorparam1:
                generator.setPila(tempaux,resizq.getValor())         #stack[tn]=resizq.temp
                
                #param2:
                generator.addExp(tempaux, tempaux, '1', '+')  #tn=tn+1
            #   #valorparam2:
                generator.setPila(tempaux,resder.getValor())         #stack[tn]=resizq.temp
                
                #   #                        CAMBIO DE ENTORNO FORMAL
                generator.newEnv(tabla.size)
                generator.llamandaFuncion("nativaPotenciaCadena")

            #   #                        obtengo getValor() de retorno
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.getPila(temp,'P')
                
                 #   #                       regreso a entorno 

                generator.returnEntorno(tabla.size)

                return Return(temp,self.tipo,True)
            
            return Error("Semantico", "Este tipo de operacion en '^' no es admitivido.", self.fila, self.columna)
        
        # OPE1 : OPE2  en julia hay declaraciones de rangos a = 1:8
        elif self.operador == OpsAritmetico.DP:
            #Int64 : Int64
            if self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.ENTERO:
                self.tipo = Tipo.RANGO#prueba
                #self.checkLabels()
                #generator.agregarIf(resizq.getValor(),resder.getValor(),'<=',self.trueLbl)
                #generator.agregarGoto(self.falseLbl)
                #r=Return(None,self.tipo,False)
                #r.trueLbl=self.trueLbl
                #r.falseLbl=self.falseLbl
                r =[]
                r.append(resizq.getValor())
                r.append(resder.getValor())
                return r
        
            #Float64 : Float64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.DECIMAL:
                self.tipo = Tipo.RANGO
                lista=[]
                lista.append(self.getValor(self.operacionI.tipo,resizq))
                lista.append(self.getValor(self.operacionD.tipo,resder))
                return lista
        
            #Int64 : Float64
            elif self.operacionI.tipo == Tipo.ENTERO and self.operacionD.tipo== Tipo.DECIMAL:
                self.tipo = Tipo.RANGO
                lista=[]
                lista.append(self.getValor(self.operacionI.tipo,resizq))
                lista.append(self.getValor(self.operacionD.tipo,resder))
                return lista
        
            #Float64 : Int64
            elif self.operacionI.tipo == Tipo.DECIMAL and self.operacionD.tipo== Tipo.ENTERO:
                self.tipo = Tipo.RANGO
                lista=[]
                lista.append(self.getValor(self.operacionI.tipo,resizq))
                lista.append(self.getValor(self.operacionD.tipo,resder))
                return lista
            
            return Error("Semantico", "Este tipo de operacion en RANGO ':' no es admitivido.", self.fila, self.columna)
         
        
            
        #UNARIAS:
        #-OPE
        elif self.operador == OpsAritmetico.UMENOS:
            if self.operacionI.tipo == Tipo.ENTERO:
                self.tipo = Tipo.ENTERO
                #return -(self.getValor(self.operacionI.tipo,resizq))
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.addExp(temp,resizq.getValor(),'-1','*')
                return Return(temp,self.tipo,True)
            elif self.operacionI.tipo == Tipo.DECIMAL:
                self.tipo = Tipo.DECIMAL
                temp = generator.agregarTemporal();generator.liberarTemporal(temp)
                generator.addExp(temp,resizq.getValor(),'-1','*')
                return Return(temp,self.tipo,True)
            return Error("SEMANTICO", "Tipo incorrecto para signo '-'",self.fila,self.columna)
        return Error("SEMANTICO", "Tipo de operacion incorrecta, verifique",self.fila, self.columna)
        
    def checkLabels(self):
        genAux = Generador()
        generator = genAux.getInstance()
        if self.trueLbl == '':
            self.trueLbl = generator.agregarLabel()
        if self.falseLbl == '':
            self.falseLbl = generator.agregarLabel()
        
    def getValor(self, tipo, val):
        if tipo == Tipo.ENTERO:
            return int(val)
        elif tipo == Tipo.DECIMAL:
            return float(val)
        elif tipo == Tipo.BOOLEANO:
            return bool(val)
        return str(val)
    
    def getTipo(self, val):
        if isinstance(val,int):
            return Tipo.ENTERO
        elif isinstance(val,float):
            return Tipo.DECIMAL
        elif isinstance(val,bool):
            return Tipo.BOOLEANO
        return Tipo.CADENA
    
    def getNode(self):
        nodoAritmetico = NodoArbol("ARIT") #NOMBRE PADRE
        #binarias
        if self.operacionD != None:
            nodoAritmetico.agregarHijoConNodo(self.operacionI.getNode()) #valor = trae un Nodo Primitivo por eso es con Nodo
            nodoAritmetico.agregarHijoSinNodo(str(self.operador)) 
            nodoAritmetico.agregarHijoConNodo(self.operacionD.getNode()) #valor = trae un Nodo Primitivo por eso es con Nodo
        #unarias
        else:
            nodoAritmetico.agregarHijoSinNodo(self.operador)
            nodoAritmetico.agregarHijoConNodo(self.operacionI.getNode()) #valor = trae un Nodo Primitivo por eso es con Nodo
        return nodoAritmetico
    
    def desempaquetarvalor(self,diccionario):
        valor =""
        tamano=1
        valor=str(diccionario['##_nombre_padre_struct_##']['id'])+"("
        for key in diccionario:
            tamano+=1
            if key != '##_nombre_padre_struct_##':
                if isinstance(diccionario[key]['valor'],dict):
                    valor+= self.desempaquetarvalor(diccionario[key]['valor'])
                else:
                    if diccionario[key]['valor']== None: 
                        valor += 'nothing'
                    else:
                        valor += str(diccionario[key]['valor'])
                    if tamano <= len(diccionario):valor += ','
        valor+=")"
        return valor