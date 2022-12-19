
import posixpath
from re import L


class Generador:
    generator = None
    def __init__(self):
        #contadores
        self.contadorTemporal = 0
        self.contadorLabel = 0
        #codigo
        self.code = ''
        self.funcs =''
        self.natives = ''
        self.inFunc = False
        self.inNatives = False
        #Listado de Temporales
        self.tempralesenteros=[]
        self.temporales = []
        #importaciones=
        self.importMath = ''
        self.ptcoma = ''
        #lista nativas
        self.printString = False
        self.concatenar = False
        self.concastrnum = False
        self.mayorquecad = False
        self.mayorigualquecad = False
        self.menorquecad = False
        self.menorigualquecad = False
        self.igualquecad = False
        self.diferentequecad=False
        self.potencianativa = False
        self.potenciastr = False
        self.truncc = False
        self.parseint = False
        self.parsefloat= False
        self.upper = False
        self.lower = False
    
    def limpiarTodo(self):
        #contadores
        self.contadorTemporal=0
        self.contadorLabel=0
        #codigo
        self.code = ''
        self.funcs =''
        self.natives = ''
        self.inFunc = False
        self.inNatives = False
        #Listado de Temporales
        self.tempralesenteros=[]
        self.temporales = []
        #importaciones=
        self.importMath = ''
        self.ptcoma = ''
        #lista nativas
        self.printString = False
        self.concatenar = False
        self.concastrnum = False
        self.mayorquecad = False
        self.mayorigualquecad = False
        self.menorquecad = False
        self.menorigualquecad = False
        self.igualquecad = False
        self.diferentequecad= False
        self.potencianativa = False
        self.potenciastr = False
        self.truncc = False
        self.parseint=False
        self.parsefloat= False
        self.upper = False
        self.lower = False
        Generador.generator = Generador()
        
    #**************************************************
    #*************** GENERAR CODIGO *******************
    #**************************************************
    
    def getEncabezado(self):
        ret = '/*ENCABEZADO*/\npackage main;\n\nimport(\n\t"fmt"'+self.ptcoma+'\n\t'+self.importMath+');\n\n'
        if len(self.tempralesenteros)>0:
            ret += 'var ' 
            for tempin in range(len(self.tempralesenteros)):
                ret += self.tempralesenteros[tempin]
                if tempin != (len(self.tempralesenteros)-1):
                    ret += ","
                ret += " int;\n"
        if self.contadorTemporal > 0:
            #genera listado de declaraciones de variables temporales
            ret += 'var '
            for temp in range(0,self.contadorTemporal):
                ret += "t"+str(temp) #self.temporales[temp]
                #if temp != (len(self.temporales)-1):
                if temp != self.contadorTemporal-1:
                    ret += ", "
            ret += " float64;\n"
        ret += "var P, H float64;\nvar stack [50380202]float64;\nvar heap [50380202]float64;\n\n"
        return ret      
    
    def getCode(self):
        return f'{self.getEncabezado()}{self.natives}\n{self.funcs}\nfunc main() {{\n{self.code}\n}}'  
    
    def codigoIn(self,codigo,tab="\t"):
        if(self.inNatives):
            if(self.natives == ''):
                self.natives = self.natives + '/*---NATIVAS---*/\n'
            self.natives = self.natives + tab + codigo
        elif(self.inFunc):
            if self.funcs == ' ':
                self.funcs = self.funcs + '/*---FUNCS---*/\n'
            self.funcs = self.funcs + tab + codigo
        else:
            self.code = self.code + '\t' + codigo
    
    def agregarComentario(self,comentario):
        self.codigoIn(f'/* {comentario} */\n')
    
    def getInstance(self):
        if Generador.generator == None:
            Generador.generator = Generador()
        return Generador.generator
    
    def agregarSalto(self):
        self.codigoIn("\n")
        
    #**************************************************
    #*************** TEMPORALES ***********************
    #**************************************************
    def agregarTemporalEntero(self):
        temp = f't{self.contadorTemporal}'
        self.contadorTemporal += 1
        self.tempralesenteros.append(temp)
        return temp
    
    def agregarTemporal(self):
        temp = f't{self.contadorTemporal}'
        self.contadorTemporal += 1
        self.temporales.append(temp)
        return temp
    
    #**************************************************
    #************ ALMACEN TEMPORAL ********************
    #**************************************************
    def getAlmacenamientoTemp(self):
        return self.temporales
    
    def setAlmacenamientoTemp(self,almacentemporal):
        self.temporales =almacentemporal
    
    def limpiarAlmacentemp(self):
        self.temporales=[]
    
    def addTemp(self,temporal):
        if not temporal in self.temporales:
            self.temporales.append(temporal)
            
        
    def liberarTemporal(self,temporal):
        if temporal in self.temporales:
            self.temporales.remove(temporal)
        
    def guardarTemps(self,tabla):
        'GUARDA TEMPORALES EN UNA POSICION DEL STACK'
        if len(self.temporales) > 0:
            temp = self.agregarTemporal() ; self.liberarTemporal(temp)
            tamano = 0
            self.agregarComentario('INICIO DE ALMACEN TEMPS')
            self.addExp(temp,'P',tabla.size,'+')
            for valor in self.temporales:
                tamano+=1
                self.setPila(temp,valor)
                if tamano != len(self.temporales):
                    self.addExp(temp,temp,'1','+')
            self.agregarComentario('FINALIZA ALMACEN DE TEMPS')
        ptr = tabla.size
        tabla.size = ptr+len(self.temporales)
        return ptr
    
    def recuperarTemps(self,tabla,posicion):
        if len(self.temporales) > 0:
            temp = self.agregarTemporal() ; self.liberarTemporal(temp)
            tamano = 0
            
            self.agregarComentario('INICIA RECUPERACION TEMP')
            self.addExp(temp,'P',posicion,'+')
            for valor in self.temporales:
                tamano+=1
                self.getPila(valor,temp)
                if tamano != len(self.temporales):
                    self.addExp(temp,temp,'1','+')
            self.agregarComentario('FINALIZA RECUPREACION TEMP')
            tabla.size = posicion
    
    
    #**************************************************
    #***************** LABELS *************************
    #**************************************************
    def agregarLabel(self):
        label = f'L{self.contadorLabel}'
        self.contadorLabel +=1
        return label      
    
    def colocarLabel(self,label):
        self.codigoIn(f'{label}:\n')
    
    
    #**************************************************
    #********************* GOTO ***********************
    #**************************************************     
    def agregarGoto(self,label):
        self.codigoIn(f'goto {label};\n')
    
    #**************************************************
    #********************* IF *************************
    #**************************************************  
    def agregarIf(self,izq,der,op,label):
        self.codigoIn(f'if {izq} {op} {der} {{goto {label};}}\n')
    
    #**************************************************
    #****************** EXPRESIONES *******************
    #**************************************************
    def addExp(self, result,izq,der,op):
        self.codigoIn(f'{result}={izq}{op}{der};\n')

    #**************************************************
    #**************** IMPORTAR MATH *******************
    #**************************************************
    def addMathImport(self):
        self.ptcoma = ";"
        self.importMath = '"math"'
        
    #**************************************************
    #******************** FUNCS ***********************
    #**************************************************
    def agregarInicioFuncion(self,id):
        if not self.inNatives:
            self.inFunc = True
        self.codigoIn(f'func {id}(){{\n','')
    
    def agregarFinalFuncion(self):
        self.codigoIn('return;\n}\n')
        if not self.inNatives:
            self.inFunc = False
    
    #**************************************************
    #******************* STACK ************************
    #**************************************************
    def setPila(self, pos,valor):
        self.codigoIn(f'stack[int({pos})]={valor};\n')
    
    def getPila(self,p,pos):
        self.codigoIn(f'{p}=stack[int({pos})];\n')
    
    #**************************************************
    #******************** HEAP ************************
    #**************************************************
    def setHeap(self, pos, valor):
        self.codigoIn(f'heap[int({pos})]={valor};\n')
    
    def getHeap(self, p, pos):
        self.codigoIn(f'{p}=heap[int({pos})];\n')
    
    def nextHeap(self):
        self.codigoIn('H=H+1;\n')
        
    #**************************************************
    #****************** ENTORNOS **********************
    #**************************************************
    def newEnv(self, tamanio):
        self.codigoIn(f'P=P+{tamanio};\n')
    
    def llamandaFuncion(self, id):
        self.codigoIn(f'{id}();\n')
    
    def returnEntorno(self,size):
        self.codigoIn(f'P=P-{size};\n')
        
    #**************************************************
    #**************** INSTRUCCIONES *******************
    #**************************************************   
    def agregarPrint(self, tipo, valor):
        self.codigoIn(f'fmt.Printf("%{tipo}", {valor});\n')
        
    def printTrue(self):
        self.agregarPrint("c",116)
        self.agregarPrint("c",114)
        self.agregarPrint("c",117)
        self.agregarPrint("c",101)
        
    def printFalse(self):
        self.agregarPrint("c",102)
        self.agregarPrint("c",97)
        self.agregarPrint("c",108)
        self.agregarPrint("c",115)
        self.agregarPrint("c",101)
    
    def printMathError(self):
        self.agregarPrint("c", 77)# M
        self.agregarPrint("c", 97)# a
        self.agregarPrint("c",116)# t
        self.agregarPrint("c",104)# h
        self.agregarPrint("c", 69)# E
        self.agregarPrint("c",114)# r
        self.agregarPrint("c",114)# r
        self.agregarPrint("c",111)# o 
        self.agregarPrint("c",114)# r
        self.saltoLinea()
    def printBoundError(self):
        self.agregarPrint("c", 66)# B
        self.agregarPrint("c",111)# o 
        self.agregarPrint("c",117)# u
        self.agregarPrint("c",110)# n
        self.agregarPrint("c",100)# d
        self.agregarPrint("c",115)# s
        self.agregarPrint("c", 69)# E
        self.agregarPrint("c",114)# r
        self.agregarPrint("c",114)# r
        self.agregarPrint("c",111)# o 
        self.agregarPrint("c",114)# r
        self.saltoLinea()
        
    def saltoLinea(self):
        self.agregarPrint("c",10)#\n
    
    #**********************************************************************************
    #***************************************** NATIVAS ********************************
    #**********************************************************************************
    
    #*****************************************************
    #**************** IMPRESION CADENA *******************
    #***************************************************** 
    def printf(self):
        if (self.printString):
            return 
        self.printString = True
        self.inNatives = True
        
        self.agregarInicioFuncion('nativePrintString')
        # Label para salir de funcion
        returnLbl = self.agregarLabel()
        # label para la comparacion para bucar fin de cadena
        compararLbl = self.agregarLabel()

        #temporal puntero a stack
        tempP = self.agregarTemporal();self.liberarTemporal(tempP)
        
        #temporal puntero Heap 
        tempH = self.agregarTemporal();self.liberarTemporal(tempH)
        
        self.addExp(tempP,'P','1','+')
        self.getPila(tempH,tempP)
        
        #Temporal para comparar
        tempC = self.agregarTemporal();self.liberarTemporal(tempC)
        
        self.colocarLabel(compararLbl)
        
        self.getHeap(tempC,tempH)
        
        self.agregarIf(tempC,'-1','==', returnLbl)
        
        self.agregarPrint('c','int('+tempC+')')
        
        self.addExp(tempH,tempH,'1','+')
        
        self.agregarGoto(compararLbl)
        
        self.colocarLabel(returnLbl)
        
        self.agregarFinalFuncion()
        
        self.inNatives=False
    
    #*****************************************************
    #*************** CONCATENAR CADENA *******************
    #*****************************************************
    
    def concatenarCadena(self):
        if (self.concatenar):
            return 
        self.concatenar= True
        self.inNatives = True
        self.agregarInicioFuncion('nativaconcatenarCadena')
        
        temp1 = self.agregarTemporal();self.liberarTemporal(temp1)
        self.addExp(temp1,'H','','')                        #tn=H;
        
        temp2 = self.agregarTemporal();self.liberarTemporal(temp2)
        self.addExp(temp2,'P','1','+')                      #tn=P+1; //posicion parametro 1
        
        temp3 = self.agregarTemporal();self.liberarTemporal(temp3)
        self.getPila(temp3,temp2)                           #tn = stack[tn]
        
        temp4 = self.agregarTemporal();self.liberarTemporal(temp4)
        self.addExp(temp4,'P','2','+')                      #tn= P+2 //posicion parametro 2
        
        
        lblParam1In = self.agregarLabel()
        lblParam1Salida = self.agregarLabel()
        lblParam2In = self.agregarLabel()
        lblSalida = self.agregarLabel()
        #ciclo para almacenar en heap param1
        self.colocarLabel(lblParam1In)                      #L0:
        temp5=self.agregarTemporal();self.liberarTemporal(temp5)
        self.getHeap(temp5,temp3)                           #tn=HEAP[tn]
        self.agregarIf(temp5,'-1','==',lblParam1Salida)     #if(tn == -1) goto Ln;
        self.setHeap('H',temp5)
        self.nextHeap()                                     #H=H+1
        self.addExp(temp3,temp3,'1','+')                    #tn=tn+1
        self.agregarGoto(lblParam1In)
        
        #etiqueta de salida ciclo:
        self.colocarLabel(lblParam1Salida)
        #obtencion de posicion param2:
        self.getPila(temp3,temp4) 
        
        #ciclo para almacenar en heap param2
        self.colocarLabel(lblParam2In)                      #L0:
        temp5=self.agregarTemporal();self.liberarTemporal(temp5)
        self.getHeap(temp5,temp3)                           #tn=HEAP[tn]
        self.agregarIf(temp5,'-1','==',lblSalida)     #if(tn == -1) goto Ln;
        self.setHeap('H',temp5)
        self.nextHeap()                                     #H=H+1
        self.addExp(temp3,temp3,'1','+')                    #tn=tn+1
        self.agregarGoto(lblParam2In)
        
        #etiqueta de salida
        self.colocarLabel(lblSalida)
        self.setHeap('H','-1')
        self.nextHeap()
        self.setPila('P',temp1)
        self.agregarFinalFuncion()
        self.inNatives=False
    
    #*****************************************************
    #*********** CONCATENAR  CADENA Y NUMERO *************
    #*****************************************************
    
    def concatStringNum(self):
        if self.concastrnum:return 
        self.concastrnum = True
        self.inNatives = True
        self.importMath = '"math"'
        self.agregarComentario("FUNCION PARA CONCATENAR STRING Y NUMERO")
        self.agregarInicioFuncion('nativaconcatStringNum')
        
        #conversion
        etiquetaS = self.agregarLabel()
        temp1 = self.agregarTemporal();self.liberarTemporal(temp1)
        tempN = self.agregarTemporal();self.liberarTemporal(tempN)
        
        self.addExp(temp1,'P','2','+')        #tn = p+2
        self.getPila(temp1,temp1)           #tn = stack[tn]
        self.addExp(tempN,temp1,'','')            #tn = tn;
        self.agregarIf(temp1,'0','>',etiquetaS) #if t1>0 goto ls
        self.addExp(temp1,temp1,'-1','*')   #t1 = t1*-1
        self.colocarLabel(etiquetaS)        #ls:
        
        etiqueta1 = self.agregarLabel()
        etiqueta2 = self.agregarLabel()
        etiqueta3 = self.agregarLabel()
        temp2 = self.agregarTemporal();self.liberarTemporal(temp2)
        
        self.addExp(temp2,'0','','')              #t2=0
        self.colocarLabel(etiqueta1)        #L1:
        
        temp3=self.agregarTemporal();self.liberarTemporal(temp3)
        
        self.addExp(temp3,'math.Mod('+temp1,'1)',',')    # tn = tn % 1
        self.agregarIf(temp3,'0','!=',etiqueta2) #if t3 != 0 goto Ln
        self.agregarGoto(etiqueta3)         # goto Ln
        self.colocarLabel(etiqueta2)        # L2:
        self.addExp(temp1,temp1,'10','*')   # tn = tn * 10
        self.addExp(temp2,temp2,'1','+')    # tn = tn + 1
        self.agregarGoto(etiqueta1)         # goto L1
        self.colocarLabel(etiqueta3)        # L3:
        
        self.addExp(temp3,'math.Mod('+temp1,'10)',',')   # t3 = t3 % 10
        tempR1 = self.agregarTemporalEntero()
        self.addExp(tempR1,'int('+temp1,'10)','/')  # tr1=t1/10
        self.addExp(temp1,'float64('+tempR1+')','','')           # t1 = tr1
        self.addExp(temp3,temp3,'48','+')   # t3 = t3+48
        self.setHeap('H',temp3)             # heap[H] = t3
        self.nextHeap()                     # h = h + 1
        self.addExp(temp2,temp2,'1','-')    # t2 = t2 -1
        etiqueta4 = self.agregarLabel()
        etiqueta5 = self.agregarLabel()
        self.agregarIf(temp2,'0','>',etiqueta3) # if t2>0 goto Ln
        self.agregarIf(temp2,'0','==',etiqueta4) #if t2 == 0 goto L4
        self.agregarGoto(etiqueta5)         # goto L5
        self.colocarLabel(etiqueta4)        # l4:
        self.setHeap('H',46)                #heap[h] = .
        self.nextHeap()                     # h = h+1
        self.colocarLabel(etiqueta5)        #l5:
        self.addExp(temp3,'math.Mod(float64('+tempR1+')','10)',',')  #   t3 = tn % 10
        self.addExp(temp3,temp3,'48','+')   # t3 = t3+48
        self.setHeap('H',temp3)             # heap[h]=t3
        self.nextHeap()                     # h = h + 1
        self.addExp(tempR1, tempR1,'10','/') # t1 = t1 / 10
        etiqueta6 = self.agregarLabel()
        self.agregarIf(tempR1,'0','==',etiqueta6) # if t1 == 0 goto L6
        self.agregarGoto(etiqueta5)         # goto L5:
        self.colocarLabel(etiqueta6)
        etiquetaN = self.agregarLabel()
        
        self.agregarIf(tempN,'0','>',etiquetaN) #if tn > 0 goto Ln
        self.setHeap('H','45')              # heap[h]='-'
        self.nextHeap()                     # h = h + 1
        self.colocarLabel(etiquetaN)
        self.setHeap('H','-1')
        self.nextHeap()
        #fin conversion
        
        #se le da la vuelta
        inicioNum = self.agregarTemporal();self.liberarTemporal(inicioNum)
        self.addExp(inicioNum,'H','','')
        
        inicioCadena = self.agregarTemporal();self.liberarTemporal(inicioCadena)
        nuevaEtiqueta = self.agregarLabel()
        etiquetaS2 = self.agregarLabel()
        self.addExp(inicioCadena,'H','','')       # tn = H
        
        temp1s = self.agregarTemporal();self.liberarTemporal(temp1s)
        self.addExp(temp1s,'P','1','+')     # t1 = p + 1
        self.getPila(temp1s,temp1s)
        self.setPila('P','H')
        
        etiquetaEnt = self.agregarLabel()
        etiquetaSal = self.agregarLabel()
        etiquetaIns = self.agregarLabel()
        self.colocarLabel(etiquetaEnt)      #Ln:
        temp2s=self.agregarTemporal();self.liberarTemporal(temp2s)
        self.getHeap(temp2s,temp1s)         #t2=heap[t1]
        self.agregarIf(temp2s,'-1','!=',etiquetaIns)  # if t2!=-1 goto ln
        self.agregarGoto(etiquetaSal)      # goto Ls
        self.colocarLabel(etiquetaIns)     # Ln:
        self.setHeap('H',temp2s)           #    heap[h]=t2
        self.nextHeap()                    #    h=h+1
        self.addExp(temp1s,temp1s,'1','+') #    t1 = t1+1
        self.agregarGoto(etiquetaEnt)      # goto Ln
        self.colocarLabel(etiquetaSal)     # Ls:
        #string agregado
        
        self.addExp(temp1,inicioNum,'2','-') #t1 = h-2
        self.colocarLabel(nuevaEtiqueta)     # ln:
        self.getHeap(temp2,temp1)            #   t2 = heap[t1]
        self.agregarIf(temp2,'-1','==',etiquetaS2) #if t2 == -1 goto ls
        self.addExp(temp1,temp1,'1','-')    #    t1 = t1-1
        self.setHeap('H',temp2)             #    heap[h] = t2
        self.nextHeap()                     # h = h+1
        self.agregarGoto(nuevaEtiqueta)     # goto Ln
        self.colocarLabel(etiquetaS2)       # Ln:
        
        self.setHeap('H','-1')
        self.nextHeap()
        self.setPila('P',inicioCadena)
        self.agregarFinalFuncion()
        self.inNatives=False
        
    #*****************************************************
    #***************** CADENA MAYORQUE *******************
    #*****************************************************
    
    def mayorquestr(self):
        if (self.mayorquecad):
            return 
        self.mayorquecad= True
        self.inNatives = True
        self.agregarInicioFuncion('nativaCadenaMayorQue')
        #empieza codigo
        self.setPila('P','0')#esto para borrar 1 de condicion anterior si fuese 
        t0 = self.agregarTemporal();self.liberarTemporal(t0) 
        self.addExp(t0,'P','1','+')     # t0 = P + 1
        self.getPila(t0,t0)             # t0=stack[t0]
        t1 = self.agregarTemporal();self.liberarTemporal(t1)
        self.addExp(t1,'P','2','+')     # t1 = P + 2
        self.getPila(t1,t1)
        tdos=t2=self.agregarTemporal();self.liberarTemporal(tdos)
        ttres=t3=self.agregarTemporal();self.liberarTemporal(ttres)
        t2=self.getHeap(t2,t0)          # primer caracter de oper izq
        t3=self.getHeap(t3,t1)          # primer caracter de oper der
        
        l0=self.agregarLabel()          #
        #l1=self.agregarLabel()
        l2=self.agregarLabel()
        l3=self.agregarLabel()
        l4=self.agregarLabel()
        self.colocarLabel(l0)           # l0:
        self.agregarIf(tdos,'-1','==',l3)# if t2 == -1 goto l3
        self.agregarIf(ttres,'-1','==',l3)   # if t3 == -1 goto l3
        #self.colocarLabel(l1)           # l1:
        self.agregarIf(tdos,ttres,'==',l2)   #   if t2==t3 goto l2
        self.agregarGoto(l3)            #    goto l3
        self.colocarLabel(l2)           # l2:
        self.addExp(t0,t0,'1','+') #t0 = t0+1
        self.addExp(t1,t1,'1','+') #t1 = t1+1
        self.getHeap(tdos,t0)# t2 = heap[t0]
        self.getHeap(ttres,t1)# t3 = heap[t1]
        self.agregarGoto(l0) # goto l0
        self.colocarLabel(l3) # L3:
        self.agregarIf(tdos,ttres,'<=',l4)#if t2 <= t3 goto l4
        self.setPila('P','1') #true stack[p]=true
        self.colocarLabel(l4)#l4:
        self.agregarFinalFuncion()#return
        self.inNatives=False
        
    #*****************************************************
    #************* CADENA MAYORIGUALQUE ******************
    #*****************************************************
    
    def mayorigualquestr(self):
        if (self.mayorigualquecad):
            return 
        self.mayorigualquecad= True
        self.inNatives = True
        self.agregarInicioFuncion('nativaCadenaMayorIgualQue')
        #empieza codigo
        self.setPila('P','0')#esto para borrar 1 de condicion anterior si fuese 
        t0 = self.agregarTemporal();self.liberarTemporal(t0) 
        self.addExp(t0,'P','1','+')     # t0 = P + 1
        self.getPila(t0,t0)             # t0=stack[t0]
        t1 = self.agregarTemporal();self.liberarTemporal(t1)
        self.addExp(t1,'P','2','+')     # t1 = P + 2
        self.getPila(t1,t1)
        tdos=t2=self.agregarTemporal();self.liberarTemporal(tdos)
        ttres=t3=self.agregarTemporal();self.liberarTemporal(ttres)
        t2=self.getHeap(t2,t0)          # primer caracter de oper izq
        t3=self.getHeap(t3,t1)          # primer caracter de oper der
        
        l0=self.agregarLabel()          #
        #l1=self.agregarLabel()
        l2=self.agregarLabel()
        l3=self.agregarLabel()
        l4=self.agregarLabel()
        self.colocarLabel(l0)           # l0:
        self.agregarIf(tdos,'-1','==',l3)# if t2 == -1 goto l3
        self.agregarIf(ttres,'-1','==',l3)   # if t3 == -1 goto l3
        #self.colocarLabel(l1)           # l1:
        self.agregarIf(tdos,ttres,'==',l2)   #   if t2==t3 goto l2
        self.agregarGoto(l3)            #    goto l3
        self.colocarLabel(l2)           # l2:
        self.addExp(t0,t0,'1','+') #t0 = t0+1
        self.addExp(t1,t1,'1','+') #t1 = t1+1
        self.getHeap(tdos,t0)# t2 = heap[t0]
        self.getHeap(ttres,t1)# t3 = heap[t1]
        self.agregarGoto(l0) # goto l0
        self.colocarLabel(l3) # L3:
        self.agregarIf(tdos,ttres,'<',l4)#if t2 <= t3 goto l4
        self.setPila('P','1') #true stack[p]=true
        self.colocarLabel(l4)#l4:
        self.agregarFinalFuncion()#return
        self.inNatives=False    
        
        
    #*****************************************************
    #***************** CADENA MENORQUE *******************
    #*****************************************************
    
    def menorquestr(self):
        if (self.menorquecad):
            return 
        self.menorquecad= True
        self.inNatives = True
        self.agregarInicioFuncion('nativaCadenaMenorQue')
        #empieza codigo
        self.setPila('P','0')#esto para borrar 1 de condicion anterior si fuese 
        t0 = self.agregarTemporal();self.liberarTemporal(t0) 
        self.addExp(t0,'P','1','+')     # t0 = P + 1
        self.getPila(t0,t0)             # t0=stack[t0]
        t1 = self.agregarTemporal();self.liberarTemporal(t1) 
        self.addExp(t1,'P','2','+')     # t1 = P + 2
        self.getPila(t1,t1)
        tdos=t2=self.agregarTemporal();self.liberarTemporal(tdos) 
        ttres=t3=self.agregarTemporal();self.liberarTemporal(ttres) 
        t2=self.getHeap(t2,t0)          # primer caracter de oper izq
        t3=self.getHeap(t3,t1)          # primer caracter de oper der
        
        l0=self.agregarLabel()          #
        #l1=self.agregarLabel()
        l2=self.agregarLabel()
        l3=self.agregarLabel()
        l4=self.agregarLabel()
        self.colocarLabel(l0)           # l0:
        self.agregarIf(tdos,'-1','==',l3)# if t2 == -1 goto l3
        self.agregarIf(ttres,'-1','==',l3)   # if t3 == -1 goto l3
        #self.colocarLabel(l1)           # l1:
        self.agregarIf(tdos,ttres,'==',l2)   #   if t2==t3 goto l2
        self.agregarGoto(l3)            #    goto l3
        self.colocarLabel(l2)           # l2:
        self.addExp(t0,t0,'1','+') #t0 = t0+1
        self.addExp(t1,t1,'1','+') #t1 = t1+1
        self.getHeap(tdos,t0)# t2 = heap[t0]
        self.getHeap(ttres,t1)# t3 = heap[t1]
        self.agregarGoto(l0) # goto l0
        self.colocarLabel(l3) # L3:
        self.agregarIf(tdos,ttres,'>=',l4)#if t2 <= t3 goto l4
        self.setPila('P','1') #true stack[p]=true
        self.colocarLabel(l4)#l4:
        self.agregarFinalFuncion()#return
        self.inNatives=False
        
    #*****************************************************
    #************* CADENA MENORIGUALQUE ******************
    #*****************************************************
    
    def menorigualquestr(self):
        if (self.menorigualquecad):
            return 
        self.menorigualquecad = True
        self.inNatives = True
        self.agregarInicioFuncion('nativaCadenaMenorIgualQue')
        #empieza codigo
        self.setPila('P','0')#esto para borrar 1 de condicion anterior si fuese 
        t0 = self.agregarTemporal();self.liberarTemporal(t0)  
        self.addExp(t0,'P','1','+')     # t0 = P + 1
        self.getPila(t0,t0)             # t0=stack[t0]
        t1 = self.agregarTemporal();self.liberarTemporal(t1) 
        self.addExp(t1,'P','2','+')     # t1 = P + 2
        self.getPila(t1,t1)
        tdos=t2=self.agregarTemporal();self.liberarTemporal(tdos) 
        ttres=t3=self.agregarTemporal();self.liberarTemporal(ttres) 
        t2=self.getHeap(t2,t0)          # primer caracter de oper izq
        t3=self.getHeap(t3,t1)          # primer caracter de oper der
        
        l0=self.agregarLabel()          #
        #l1=self.agregarLabel()
        l2=self.agregarLabel()
        l3=self.agregarLabel()
        l4=self.agregarLabel()
        self.colocarLabel(l0)           # l0:
        self.agregarIf(tdos,'-1','==',l3)# if t2 == -1 goto l3
        self.agregarIf(ttres,'-1','==',l3)   # if t3 == -1 goto l3
        #self.colocarLabel(l1)           # l1:
        self.agregarIf(tdos,ttres,'==',l2)   #   if t2==t3 goto l2
        self.agregarGoto(l3)            #    goto l3
        self.colocarLabel(l2)           # l2:
        self.addExp(t0,t0,'1','+') #t0 = t0+1
        self.addExp(t1,t1,'1','+') #t1 = t1+1
        self.getHeap(tdos,t0)# t2 = heap[t0]
        self.getHeap(ttres,t1)# t3 = heap[t1]
        self.agregarGoto(l0) # goto l0
        self.colocarLabel(l3) # L3:
        self.agregarIf(tdos,ttres,'>',l4)#if t2 <= t3 goto l4
        self.setPila('P','1') #true stack[p]=true
        self.colocarLabel(l4)#l4:
        self.agregarFinalFuncion()#return
        self.inNatives=False    
        
    
    #*****************************************************
    #**************** CADENA IGUALQUE ********************
    #*****************************************************
    
    def igualquestr(self):
        if (self.igualquecad):
            return 
        self.igualquecad = True
        self.inNatives = True
        self.agregarInicioFuncion('nativaIgualQue')
        #empieza codigo
        self.setPila('P','0')#esto para borrar 1 de condicion anterior si fuese 
        t0 = self.agregarTemporal() ;self.liberarTemporal(t0) 
        self.addExp(t0,'P','1','+')     # t0 = P + 1
        self.getPila(t0,t0)             # t0=stack[t0]
        t1 = self.agregarTemporal();self.liberarTemporal(t1) 
        self.addExp(t1,'P','2','+')     # t1 = P + 2
        self.getPila(t1,t1)
        tdos=t2=self.agregarTemporal();self.liberarTemporal(tdos) 
        ttres=t3=self.agregarTemporal();self.liberarTemporal(ttres) 
        t2=self.getHeap(t2,t0)          # primer caracter de oper izq
        t3=self.getHeap(t3,t1)          # primer caracter de oper der
        
        l0=self.agregarLabel()          #
        #l1=self.agregarLabel()
        l2=self.agregarLabel()
        l3=self.agregarLabel()
        l4=self.agregarLabel()
        self.colocarLabel(l0)           # l0:
        self.agregarIf(tdos,'-1','==',l3)# if t2 == -1 goto l3
        self.agregarIf(ttres,'-1','==',l3)   # if t3 == -1 goto l3
        #self.colocarLabel(l1)           # l1:
        self.agregarIf(tdos,ttres,'==',l2)   #   if t2==t3 goto l2
        self.agregarGoto(l4)            #    goto l4
        self.colocarLabel(l2)           # l2:
        self.addExp(t0,t0,'1','+') #t0 = t0+1
        self.addExp(t1,t1,'1','+') #t1 = t1+1
        self.getHeap(tdos,t0)# t2 = heap[t0]
        self.getHeap(ttres,t1)# t3 = heap[t1]
        self.agregarGoto(l0) # goto l0
        self.colocarLabel(l3) # L3:
        self.agregarIf(tdos,ttres,'!=',l4)#if t2 != t3 goto l4
        self.setPila('P','1') #true stack[p]=true
        self.colocarLabel(l4)#l4:
        self.agregarFinalFuncion()#return
        self.inNatives=False 
    
    #*****************************************************
    #************* CADENA DIFERENTEQUE *******************
    #*****************************************************
    
    def diferentequestr(self):
        if (self.diferentequecad):
            return 
        self.diferentequecad = True
        self.inNatives = True
        self.agregarInicioFuncion('nativaDiferenteQue')
        #empieza codigo
        self.setPila('P','0')#esto para borrar 1 de condicion anterior si fuese 
        t0 = self.agregarTemporal() ;self.liberarTemporal(t0) 
        self.addExp(t0,'P','1','+')     # t0 = P + 1
        self.getPila(t0,t0)             # t0=stack[t0]
        t1 = self.agregarTemporal();self.liberarTemporal(t1) 
        self.addExp(t1,'P','2','+')     # t1 = P + 2
        self.getPila(t1,t1)
        tdos=t2=self.agregarTemporal();self.liberarTemporal(tdos) 
        ttres=t3=self.agregarTemporal();self.liberarTemporal(ttres) 
        t2=self.getHeap(t2,t0)          # primer caracter de oper izq
        t3=self.getHeap(t3,t1)          # primer caracter de oper der
        
        l0=self.agregarLabel()          #
        #l1=self.agregarLabel()
        l2=self.agregarLabel()
        l3=self.agregarLabel()
        l4=self.agregarLabel()
        self.colocarLabel(l0)           # l0:
        self.agregarIf(tdos,'-1','==',l3)# if t2 == -1 goto l3
        self.agregarIf(ttres,'-1','==',l3)   # if t3 == -1 goto l3
        #self.colocarLabel(l1)           # l1:
        self.agregarIf(tdos,ttres,'==',l2)   #   if t2==t3 goto l2
        self.agregarGoto(l3)            #    goto l4
        self.colocarLabel(l2)           # l2:
        self.addExp(t0,t0,'1','+') #t0 = t0+1
        self.addExp(t1,t1,'1','+') #t1 = t1+1
        self.getHeap(tdos,t0)# t2 = heap[t0]
        self.getHeap(ttres,t1)# t3 = heap[t1]
        self.agregarGoto(l0) # goto l0
        self.colocarLabel(l3) # L3:
        self.agregarIf(tdos,ttres,'==',l4)#if t2 == t3 goto l4
        self.setPila('P','1') #true stack[p]=true
        self.colocarLabel(l4)#l4:
        self.agregarFinalFuncion()#return
        self.inNatives=False 
        
    #*****************************************************
    #**************** POTENCIA NUMEROS *******************
    #*****************************************************
    
    def potenciafunc(self):
        if (self.potencianativa):
            return 
        self.potencianativa = True
        self.inNatives = True
        self.agregarComentario("--NATIVA POTENCIA--")
        self.agregarInicioFuncion('nativaPotencia')
        #empieza codigo
        resultado = self.agregarTemporal();self.liberarTemporal(resultado) 
        multiplicador = self.agregarTemporal();self.liberarTemporal(multiplicador) 
        temp1 = self.agregarTemporal();self.liberarTemporal(temp1) 
        contador = self.agregarTemporal();self.liberarTemporal(contador) 
        
        etiquetaEntrada = self.agregarLabel()
        etiquetaInstrucc = self.agregarLabel()
        etiquetaSalida = self.agregarLabel()
        
        self.addExp(temp1,'P','2','+')#temp1=P+2
        self.getPila(contador,temp1)#contador=stack[temp1]
        
        self.addExp(resultado,'1','','')#tempres = 1;
        self.agregarIf(contador,'0','==',etiquetaSalida)#if contador == 0 goto salida
        
        self.addExp(temp1,'P','1','+')#temp1= P + 1
        self.getPila(resultado,temp1)#resultado = stack[temp1]
        self.addExp(multiplicador,resultado,'','')#multi = resultado
        
        self.addExp(contador,contador,'1','-')#contador = contador - 1
        self.colocarLabel(etiquetaEntrada) #lentrada :
        self.agregarIf(contador,'0','>',etiquetaInstrucc)# if contador > 0 goto etiquetainstrucciones
        self.agregarGoto(etiquetaSalida)
        
        self.colocarLabel(etiquetaInstrucc)
        self.addExp(resultado,resultado,multiplicador,'*')
        self.addExp(contador,contador,'1','-')
        self.agregarGoto(etiquetaEntrada)
        
        self.colocarLabel(etiquetaSalida)
        self.setPila('P',resultado)
        #fin codigo
        self.agregarFinalFuncion()
        self.agregarComentario("--FIN NATIVA POTENCIA--")
        self.inNatives = False
        
    #*****************************************************
    #*************** POTENCIA CADENA *******************
    #*****************************************************
    
    def potenciaCadena(self):
        if (self.potenciastr):
            return 
        self.potenciastr= True
        self.inNatives = True
        self.agregarComentario("--INICIA NATIVA POT CADENA")
        self.agregarInicioFuncion('nativaPotenciaCadena')
        #INICIA CODIGO
        posReturn =self.agregarTemporal();self.liberarTemporal(posReturn)
        posInicial = self.agregarTemporal();self.liberarTemporal(posInicial) #guarda la pos inicial de cadena no se modifica este temp
        tamanoCadena = self.agregarTemporal();self.liberarTemporal(tamanoCadena) 
        tamanoCadenaux = self.agregarTemporal();self.liberarTemporal(tamanoCadenaux) 
        temp2 = self.agregarTemporal();self.liberarTemporal(temp2) 
        caracter = self.agregarTemporal();self.liberarTemporal(caracter) 
        temp1=self.agregarTemporal();self.liberarTemporal(temp1) 
        contador = self.agregarTemporal();self.liberarTemporal(contador) 
        resultado = self.agregarTemporal();self.liberarTemporal(resultado) 
        
        l1=self.agregarLabel()
        l2=self.agregarLabel()
        l3=self.agregarLabel()
        l4=self.agregarLabel()
        l5=self.agregarLabel()
        l6=self.agregarLabel()
        
        
        #obtengo valor de numero de veces a repetir cadena
        self.addExp(tamanoCadena,'0','','')
        self.addExp(temp1,'P','2','+')#temp1=P+2
        self.getPila(contador,temp1)#contador=stack[temp1]
        
        #agrego espacio por si ^ es 0
        self.addExp(resultado,'32','','')#resultado = 32(codigo ascii= espacio)
        #self.addExp('H','H','1','-')
        self.agregarIf(contador,'0','==',l5)#if contador == 0 goto salida
        
        #obtengo valor cadena
        self.addExp(posInicial,'P','1','+')#posinicial=P+1
        self.getPila(posInicial,posInicial)
        self.addExp(temp2,posInicial,'','')
        self.addExp(posReturn,'H','','')
        #recorrer cadena:
        self.colocarLabel(l1)#L1:
        self.getHeap(caracter,temp2)
        self.agregarIf(caracter,'-1','==',l2)#if caracter != -1 goto Linstrucciones
        self.addExp(temp2,temp2,'1','+')
        self.addExp(tamanoCadena,tamanoCadena,'1','+')
        self.agregarGoto(l1)
        
        #l2:
        self.colocarLabel(l2)
        self.addExp(contador,contador,'1','-')
        self.agregarIf(contador,'0','<',l4)
        self.addExp(temp2,posInicial,'','')
        self.addExp(tamanoCadenaux,'0','','')
        #->->->
        
        #l3:
        self.colocarLabel(l3)
        self.agregarIf(tamanoCadenaux,tamanoCadena,'>=',l2)
        self.getHeap(caracter,temp2)
        self.setHeap('H',caracter)
        self.nextHeap()
        self.addExp(tamanoCadenaux,tamanoCadenaux,'1','+')
        self.addExp(temp2,temp2,'1','+')
        
        self.agregarGoto(l3)
        
        #l4:
        self.colocarLabel(l4)
        self.setHeap('H','-1')
        self.nextHeap()
        self.agregarGoto(l6)
        
        #l5://sino se hizo nada regresar heap
        self.colocarLabel(l5)
        self.nextHeap()
        #l6
        self.colocarLabel(l6)
        self.setPila('P',posReturn)
        
        #FINALIZA CODIGO
        self.agregarFinalFuncion()
        self.agregarComentario("--FIN NATIVA POT CADENA--")
        self.inNatives = False
    
    
    #*****************************************************
    #*************** TRUNC *******************
    #*****************************************************
    
    def nativaTrunc(self):
        if (self.truncc):
            return 
        self.truncc= True
        self.inNatives = True
        self.agregarComentario("--NATIVA TRUNC--")
        self.agregarInicioFuncion('nativaTrunc')
        #EMIEZA CODIGO
       
        
    #*****************************************************
    #****************** parseint *************************
    #*****************************************************
    
    def toParseInt(self):
        if (self.parseint):
            return 
        self.parseint= True
        self.inNatives = True
        self.agregarComentario("--toParseInt--")
        self.agregarInicioFuncion('nativaToParseInt')
        #EMPIEZA CODIGO
        t1 = self.agregarTemporal();self.liberarTemporal(t1) 
        t2= self.agregarTemporal();self.liberarTemporal(t2) 
        t3=self.agregarTemporal();self.liberarTemporal(t3) 
        t15=self.agregarTemporal();self.liberarTemporal(t15) 
        l1=self.agregarLabel()
        l0=self.agregarLabel()
        l2=self.agregarLabel()
        l6=self.agregarLabel()
        l4=self.agregarLabel()
        l8=self.agregarLabel()
        l3=self.agregarLabel()
        l9=self.agregarLabel()
        
        l23=self.agregarLabel()
        l24=self.agregarLabel()
        l12=self.agregarLabel()
        l20=self.agregarLabel()
        l21=self.agregarLabel()
        
        self.addExp(t1,'P','1','+') #t1=p+1
        self.getPila(t2,t1)#t2=stack[t1]
        
        t6 = self.agregarTemporal();self.liberarTemporal(t6) 
        self.addExp(t6,'1','','')#t3=1
        
        #validar negativo
        self.getHeap(t3,t2)
        self.agregarIf(t3,'45','==',l12)
        self.agregarGoto(l1)#l0
        #l12:
        self.colocarLabel(l12)
        self.addExp(t15,'1','','')
        self.addExp(t2,t2,'1','+')
        #l0:
        self.colocarLabel(l1)
        self.getHeap(t3,t2)
        self.agregarIf(t3,'-1','==',l0)
        self.addExp(t6,t6,'1','+')
        self.addExp(t2,t2,'1','+')
        self.agregarGoto(l1)
        #l1:
        self.colocarLabel(l0)
        self.agregarIf(t6,'1','>',l2)
        self.agregarGoto(l3)
        #l2
        self.colocarLabel(l2)
        self.getPila(t2,t1)
        #l3
        self.colocarLabel(l6)
        self.getHeap(t3,t2)
        self.agregarIf(t3,'45','==',l20)
        self.agregarGoto(l21)
        #l20
        self.colocarLabel(l20)
        self.addExp(t2,t2,'1','+')
        
        #l21
        self.colocarLabel(l21)
        self.getHeap(t3,t2)
        self.agregarIf(t3,'-1','!=',l4)
        self.agregarGoto(l9)
        
        self.colocarLabel(l4)
        self.addExp(t3,t3,'48','-')
        t5=self.agregarTemporal();self.liberarTemporal(t5) 
        self.addExp(t5,t5,'10','*')
        self.addExp(t5,t5,t3,'+')
        self.addExp(t2,t2,'1','+')
        t4=self.agregarTemporal();self.liberarTemporal(t4) 
        self.getHeap(t4,t2)
        
        self.agregarIf(t4,'-1','==',l9)
        self.agregarGoto(l8)
        
        self.colocarLabel(l8)
        self.addExp(t4,t4,'48','-')
        self.addExp(t5,t5,'10','*')
        self.addExp(t5,t5,t4,'+')
        self.addExp(t2,t2,'1','+')
        self.agregarGoto(l6)
        #l6
        self.colocarLabel(l3)
        self.getPila(t2,t1)
        self.getHeap(t5,t2)
        self.addExp(t5,t3,'48','-')
        #l7
        self.colocarLabel(l9)
        self.agregarIf(t15,'1','==',l23)
        self.agregarGoto(l24)
        #l8
        self.colocarLabel(l23)
        self.addExp(t5,'0',t5,'-')
        self.addExp(t15,'0','','')
        #l9
        self.colocarLabel(l24)
        self.addExp(t1,t1,'1','-')
        self.setPila(t1,t5)
        self.addExp(t5,'0','','')
        self.agregarFinalFuncion()
        self.inNatives = False
        
    #*****************************************************
    #****************** parseFloat *************************
    #*****************************************************
    
    def toParseFloat(self):
        if (self.parsefloat):
            return 
        self.parsefloat= True
        self.inNatives = True
        self.agregarComentario("--toParseFloat--")
        self.agregarInicioFuncion('nativaToParseFloat')
        #EMPIEZA CODIGO
        t1=self.agregarTemporal();self.liberarTemporal(t1) 
        t2=self.agregarTemporal();self.liberarTemporal(t2) 
        t3=self.agregarTemporal();self.liberarTemporal(t3) 
        t4=self.agregarTemporal();self.liberarTemporal(t4) 
        t5=self.agregarTemporal();self.liberarTemporal(t5) 
        t6=self.agregarTemporal();self.liberarTemporal(t6) 
        t10=self.agregarTemporal();self.liberarTemporal(t10) 
        t11=self.agregarTemporal();self.liberarTemporal(t11) 
        l2=self.agregarLabel()
        l5=self.agregarLabel()
        l7=self.agregarLabel()
        l4=self.agregarLabel()
        l8=self.agregarLabel()
        l9=self.agregarLabel()
        l10=self.agregarLabel()
        l11=self.agregarLabel()
        l12=self.agregarLabel()
        l13=self.agregarLabel()
        l14=self.agregarLabel()
        #acceso a param
        self.addExp(t1,'P','1','+')
        self.getPila(t2,t1)
        #valor de heap
        self.getHeap(t4,t2)
        self.agregarIf(t4,'45','==',l12)
        self.agregarGoto(l2)
        self.colocarLabel(l12)
        self.addExp(t11,'1','','')
        self.addExp(t2,t2,'1','+')
        
        self.colocarLabel(l2)
        self.getHeap(t4,t2)
        self.agregarIf(t4,'46','!=',l4)
        self.agregarGoto(l7)
        
        self.colocarLabel(l4)
        self.addExp(t4,t4,'48','-')
        self.addExp(t5,t5,'10','*')
        self.addExp(t5,t5,t4,'+')
        self.addExp(t2,t2,'1','+')
        self.getHeap(t6,t2)
        self.agregarIf(t6,'46','==',l7)
        self.agregarGoto(l5)
        
        self.colocarLabel(l5)
        self.addExp(t6,t6,'48','-')
        self.addExp(t5,t5,'10','*')
        self.addExp(t5,t5,t6,'+')
        self.addExp(t2,t2,'1','+')
        self.agregarGoto(l2)
        
        self.colocarLabel(l7)
        self.addExp(t2,t2,'1','+')
        self.addExp(t3,'1','','')
        
        self.colocarLabel(l8)
        self.getHeap(t4,t2)
        self.agregarIf(t4,'-1','!=',l9)
        self.agregarGoto(l11)
        
        self.colocarLabel(l9)
        self.addExp(t4,t4,'48','-')
        self.addExp(t10,t10,'10','*')
        self.addExp(t10,t10,t4,'+')
        self.addExp(t2,t2,'1','+')
        self.addExp(t3,t3,'10','*')
        self.getHeap(t6,t2)
        self.agregarIf(t6,'-1','==',l11)
        self.agregarGoto(l10)
        
        self.colocarLabel(l10)
        self.addExp(t6,t6,'48','-')
        self.addExp(t10,t10,'10','*')
        self.addExp(t10,t10,t6,'+')
        self.addExp(t2,t2,'1','+')
        self.addExp(t3,t3,'10','*')
        self.agregarGoto(l8)
        
        self.colocarLabel(l11)
        self.addExp(t10,t10,t3,'/')
        self.addExp(t5,t5,t10,'+')
        self.agregarIf(t11,'1','==',l13)
        self.agregarGoto(l14)
        self.colocarLabel(l13)
        self.addExp(t11,'0','','')
        self.addExp(t5,'0',t5,'-')
        self.colocarLabel(l14)
        self.addExp(t1,t1,'1','-')
        self.setPila(t1,t5)
        self.addExp(t5,'0','','')
        self.addExp(t10,'0','','')
        self.agregarFinalFuncion()
        self.inNatives = False
        
    #*****************************************************
    #****************** Uppercase *************************
    #*****************************************************
    
    def toUpper(self):
        if (self.upper):
            return 
        self.upper= True
        self.inNatives = True
        self.agregarComentario("--toUpper--")
        self.agregarInicioFuncion('nativaToUpper')
        #EMPIEZA CODIGO
        temp1=self.agregarTemporal()
        self.liberarTemporal(temp1)
        
        tempR = self.agregarTemporal()
        self.liberarTemporal(tempR)
        self.addExp(temp1,'P','1','+')
        self.getPila(temp1,temp1)
        self.setPila('P','H')
        
        etiqEnt = self.agregarLabel()
        etiqSal = self.agregarLabel()
        etiqIns = self.agregarLabel()
        etiqNo = self.agregarLabel()
        
        self.colocarLabel(etiqEnt)
        temp2=self.agregarTemporal()
        self.liberarTemporal(temp2)
        self.getHeap(temp2,temp1)
        self.agregarIf(temp2,'-1','!=',etiqIns)
        self.agregarGoto(etiqSal)
        self.colocarLabel(etiqIns)
        
        self.agregarIf(temp2,'122','>',etiqNo)
        self.agregarIf(temp2,'97','<',etiqNo)
        self.addExp(temp2,temp2,'32','-')
        self.colocarLabel(etiqNo)
        self.setHeap('H',temp2)
        self.nextHeap()
        self.addExp(temp1,temp1,'1','+')
        self.agregarGoto(etiqEnt)
        self.colocarLabel(etiqSal)
        self.setHeap('H','-1')
        self.nextHeap()
        self.agregarFinalFuncion()
        self.inNatives = False
        
    
    #*****************************************************
    #****************** Lowercase *************************
    #*****************************************************
    
    def toLower(self):
        if (self.lower):
            return 
        self.lower= True
        self.inNatives = True
        self.agregarComentario("--toLower--")
        self.agregarInicioFuncion('nativaToLower')
        #EMPIEZA CODIGO
        temp1=self.agregarTemporal()
        self.liberarTemporal(temp1)
        
        tempR = self.agregarTemporal()
        self.liberarTemporal(tempR)
        self.addExp(temp1,'P','1','+')
        self.getPila(temp1,temp1)
        self.setPila('P','H')
        
        etiqEnt = self.agregarLabel()
        etiqSal = self.agregarLabel()
        etiqIns = self.agregarLabel()
        etiqNo = self.agregarLabel()
        
        self.colocarLabel(etiqEnt)
        temp2=self.agregarTemporal()
        self.liberarTemporal(temp2)
        self.getHeap(temp2,temp1)
        self.agregarIf(temp2,'-1','!=',etiqIns)
        self.agregarGoto(etiqSal)
        self.colocarLabel(etiqIns)
        
        self.agregarIf(temp2,'90','>',etiqNo)
        self.agregarIf(temp2,'65','<',etiqNo)
        self.addExp(temp2,temp2,'32','+')
        self.colocarLabel(etiqNo)
        self.setHeap('H',temp2)
        self.nextHeap()
        self.addExp(temp1,temp1,'1','+')
        self.agregarGoto(etiqEnt)
        self.colocarLabel(etiqSal)
        self.setHeap('H','-1')
        self.nextHeap()
        self.agregarFinalFuncion()
        self.inNatives = False
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
         
        
        
        
        
        
        
    
            
    