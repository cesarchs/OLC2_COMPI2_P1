
class Generator:
    generator = None
    def __init__(self):
        self.ambito=""
        self.ambito2=None
        self.parImpar=False

        # Contador Ts
        self.contadorTemporal = 0
        # Contador Ls
        self.contadorLabel = 0

        #contador Heap
        self.contadorH=0

        # Codigo
        self.code = ''#txt seg codigo dentro de main
        self.funcs = ''#txt seg afuera main, func las leidas
        self.natives = ''#txt seg afuera main, func por mi

        self.inFunc = False#si es una funcion leidas
        self.inNatives = False#si es una funcion por mi

        # Lista de Temporales
        self.temps = []
        self.tempsNO=[]
        self.tempsB = []
        self.temps_backUp=[]

        #Lista de funciones
        self.Lfuncs ={}

        # Lista de Nativas
        self.printString = False
        self.concatString= False #"cadena"*"hola"
        self.concatString2= False#cadena^78
        self.elevateNumber=False#89^7
        self.printARRAY = False#no use

        self.stringIgual=False#cadena==cadena
        self.stringNotIgual=False#   !=


        #----------------------
        self.lowercase=False
        self.uppercase=False
        self.printARRAY2 = False#length

        self.math=''
        self.funcsB=''

      
    def ResetC3D(self):
        self.ambito=""
        self.ambito2=None
        self.parImpar=False
        # Contadores
        self.contadorTemporal = 0
        self.contadorLabel = 0
        #contador Heap
        self.contadorH=0
        # Code
        self.code = ''
        self.funcs = ''
        self.natives = ''
        self.inFunc = False
        self.inNatives = False
        # Lista de Temporales
        self.temps = []
        self.tempsNO=[]
        self.tempsB = []
        self.temps_backUp=[]

        #Lista de funciones
        self.Lfuncs ={}

        # Lista de Nativas
        self.printString = False
        self.concatString= False
        self.concatString2= False
        self.elevateNumber=False
        self.printARRAY = False

        self.stringIgual=False
        self.stringNotIgual=False

        #----------------------
        self.lowercase=False
        self.uppercase=False
        self.printARRAY2 = False#length

        self.math=''
        self.funcsB=''

        
        Generator.generator = Generator()#me puede causar error quizas
    
    #############
    # CODE
    #############
    def getEncabezado(self):
        ret = '/*----HEADER----*/\npackage main;\n\nimport (\n\t"fmt"'+''+self.math+' \n);\n\n'
        if len(self.temps) > 0:
            ret += 'var '
            for temp in range(len(self.temps)):
                ret += self.temps[temp]
                if temp != (len(self.temps) - 1):
                    ret += ", "
            ret += " float64;\n"
        ret += "var P, H float64;\nvar stack [30101999]float64;\nvar heap [30101999]float64;\n\n"
        return ret

    def getCodigo(self):
        return f'{self.getEncabezado()}{self.natives}\n{self.funcs}\nfunc main(){{\n{self.code}\n}}'

    def codeInput(self, code, tab="\t"):
        if(self.inNatives):
            if(self.natives == ''):
                self.natives = self.natives + '/*-----NATIVES-----*/\n'
            self.natives = self.natives + tab + code
        elif(self.inFunc):
            if(self.funcs == ''):
                self.funcs = self.funcs + '/*-----FUNCS-----*/\n'
            self.funcsB+=code
            self.funcs = self.funcs + tab +  code
            
        else:
            self.code = self.code + '\t' +  code

    def addCommit(self, comment):
        self.codeInput(f'/* {comment} */\n')
    
    def getInstance(self):
        if Generator.generator == None:
            Generator.generator = Generator()
        return Generator.generator

    def addSaltoLinea(self):
        self.codeInput("\n")

    ########################
    # Manejo de Temporales
    ########################
    def addTemporal(self):
        temp = f'T{self.contadorTemporal}'
        self.contadorTemporal += 1
        self.temps.append(temp)
        return temp


    def addTemporal2(self):
        temp = f'T{self.contadorTemporal}'
        self.contadorTemporal += 1
        self.temps.append(temp)
        self.tempsNO.append(temp)
        return temp


    ####################
    # copia de temporales
    ####################

    def GetTemporales(self):
        self.tempsB = self.temps
        self.temps=[]#aqui se guardan los Ts de la funcion actual



    def GetTemporalesAgain(self):
        self.temps = self.tempsB + self.temps
        self.tempsB=[]
        self.tempsNO=[]


    #####################
    # Manejo de Labels
    #####################
    def newLabel(self):
        label = f'L{self.contadorLabel}'
        self.contadorLabel += 1
        return label

    def inputLabel(self, label):
        self.codeInput(f'{label}:\n')

    ###################
    # GOTO
    ###################
    def addGoto(self, label):
        self.codeInput(f'goto {label};\n')
    
    ###################
    # IF
    ###################
    def addIf(self, left, right, op, label):
        self.codeInput(f'if {left} {op} {right} {{goto {label};}}\n')

    ###################
    # EXPRESIONES
    ###################
    def addExp(self, result, left, right, op):
        self.codeInput(f'{result}={left}{op}{right};\n')
    
    ###################
    # FUNCS
    ###################
    def addBeginFunc(self, id):
        if(not self.inNatives):
            self.inFunc = True
        self.ambito=id
        self.codeInput(f'func {id}(){{\n', '')
        self.Lfuncs[id] = id
    
    def addEndFunc(self):
        self.codeInput('return;\n}\n');
        self.ambito=""
        if(not self.inNatives):
            self.inFunc = False

    def addReturn(self):
        self.codeInput('return;\n');
        #if(not self.inNatives):
        #    self.inFunc = False


    ###################
    # FUNCS EXISTE
    ###################
    def getFuncion(self, simbolo):
        if simbolo in self.Lfuncs:
            return True
        else:
            return False



    ###############
    # STACK
    ###############
    def setStack(self, pos, value):
        self.codeInput(f'stack[int({pos})]={value};\n')
    
    def getStack(self, place, pos,commit=""):
        self.codeInput(f'{place}=stack[int({pos})];{commit}\n')

    #############
    # ENTORNOS PARA FUNCS
    #############
    def newEnv(self, size):
        self.codeInput(f'P=P+{size};\n')

    def callFuncion(self, id):
        self.codeInput(f'{id}();\n')

    def retEnv(self, size):
        self.codeInput(f'P=P-{size};\n')

    ###############
    # HEAP
    ###############
    def setHeap(self, pos, value):
        self.codeInput(f'heap[int({pos})]={value};\n')

    def getHeap(self, place, pos):
        self.codeInput(f'{place}=heap[int({pos})];\n')

    def nextHeap(self):
        self.codeInput('H=H+1;\n')
    

    def nextHeapArray(self):
        self.contadorH+=1

    # INSTRUCCIONES
    def addPrint(self, type, value,commit=""):

        if type =="f":
            self.codeInput(f'fmt.Printf("%{type}", {value});{commit}\n')

        else:
            self.codeInput(f'fmt.Printf("%{type}", int({value}));{commit}\n')
    
    def printTrue(self):
        self.addPrint("c", 116,"//T")#T
        self.addPrint("c", 114,"//R")#R
        self.addPrint("c", 117,"//U")#U
        self.addPrint("c", 101,"//E")#E

    def printFalse(self):
        self.addPrint("c", 102,"//F")#F
        self.addPrint("c", 97,"//A")#A
        self.addPrint("c", 108,"//L")#L
        self.addPrint("c", 115,"//S")#S
        self.addPrint("c", 101,"//E")#E
    
    ###############-------------------------------------------------------------------------------------------------
    # NATIVAS
    ###############-------------------------------------------------------------------------------------------------
    def fUpperString(self):
        #------------------
        # 0-return
        # 1-param_cadena1

        if(self.uppercase):
            return
        self.uppercase = True#para q no crea copias y copias de si misma
        self.inNatives = True#para escribir en Natives

        #le agrego nombre a la funcion
        self.addBeginFunc('uppercase')

        # Label para salir de la funcion q mete la palabra 1vez
        returnLbl = self.newLabel()#L0

        

        # Label bucle para la comparacion para buscar fin de cadena -1
        compareLbl = self.newLabel()#L1

        # creo Temporal puntero a Stack para Heap
        tempP = self.addTemporal()#T1

        # creo Temporal puntero a Heap de la cadena en si
        tempH = self.addTemporal()#T2


        # Label por si el char es menor a 65
        fase2 = self.newLabel()#L1
        # Label por si el char es mayor a 91
        fase3 = self.newLabel()#L1



        #ojo para indice a guardar en stakc***********************
        retTemp = self.addTemporal()
        self.addCommit("-------------CADENA 1-----------------")
        self.addExp(retTemp, 'H', '', '')#temporal q apunta a heap debo meter en pos return


        #obtener posicion de param_cadena de esta funcion
        self.addExp(tempP, 'P', '1', '+')

        #obtener el valor de param_cadena
        self.getStack(tempH, tempP,"//obtengo la cadena a lowercasear")

        

        # Temporal para comparar cadena en heap; lo usare para acceder al heap
        tempC = self.addTemporal()


        

        #escribo en el area de codigo el label
        self.inputLabel(compareLbl)

        #codigo para obtener valor en heap
        self.getHeap(tempC, tempH)#tempC = HEAP[int(tempH)]

        #comparo con if lo q obtuve en heap si es el fin de cadena osea el -1
        self.addIf(tempC, '-1', '==', returnLbl)


        ##################################################### 
        #AQUI DEBERIA DE VENIR EL PARSEO DE A - a etc.
        #porq guardo en el HEAP

        #65-90
        #CONDICION PARA Q LOS DEL RANGO DE ARRBIBA SEAN LOS UNICOS AFECTADOS DEL LOWERCASE
        self.addIf(tempC, '96', '<=', fase2)
        self.addIf(tempC, '123', '>=', fase3)


        self.addExp(tempC,tempC,32,'-')

        #self.addPrint('c', tempC)
        self.inputLabel(fase2)
        self.inputLabel(fase3)
        self.setHeap('H', tempC)   # heap[H] = ascii de c/u de los caracter de la cadena;
        self.nextHeap()
         
        #################################################### 

        self.addExp(tempH, tempH, '1', '+')#hay q avanzar para recorrer la cadena en heap por eso inc el valor del stack

        self.addGoto(compareLbl)

        self.inputLabel(returnLbl)#escribo la posicion donde esta la salida




        #FINALIZO LA CADENA LOWERCASE CON UN -1

        self.setHeap('H', '-1')            # FIN DE CADENA q es -1
        self.nextHeap()                    # H = H + 1;
         

        tempret = self.addTemporal()#T2
        self.addExp(tempret, 'P', '0', '+')
        
        #obtener el valor de param_cadena
        self.setStack(tempret, retTemp)

        self.addEndFunc()#finalizo la funcion siempre asi
        self.inNatives = False#para q ya no escriba en nativas sino en code





#-------------------------------------------------------------------------------------------------

    def fLowerString(self):
        #------------------
        # 0-return
        # 1-param_cadena1

        if(self.lowercase):
            return
        self.lowercase = True#para q no crea copias y copias de si misma
        self.inNatives = True#para escribir en Natives

        #le agrego nombre a la funcion
        self.addBeginFunc('lowercase')

        # Label para salir de la funcion q mete la palabra 1vez
        returnLbl = self.newLabel()#L0

        

        # Label bucle para la comparacion para buscar fin de cadena -1
        compareLbl = self.newLabel()#L1

        # creo Temporal puntero a Stack para Heap
        tempP = self.addTemporal()#T1

        # creo Temporal puntero a Heap de la cadena en si
        tempH = self.addTemporal()#T2


        # Label por si el char es menor a 65
        fase2 = self.newLabel()#L1
        # Label por si el char es mayor a 91
        fase3 = self.newLabel()#L1



        #ojo para indice a guardar en stakc***********************
        retTemp = self.addTemporal()
        self.addCommit("-------------CADENA 1-----------------")
        self.addExp(retTemp, 'H', '', '')#temporal q apunta a heap debo meter en pos return


        #obtener posicion de param_cadena de esta funcion
        self.addExp(tempP, 'P', '1', '+')

        #obtener el valor de param_cadena
        self.getStack(tempH, tempP,"//obtengo la cadena a lowercasear")

        

        # Temporal para comparar cadena en heap; lo usare para acceder al heap
        tempC = self.addTemporal()


        

        #escribo en el area de codigo el label
        self.inputLabel(compareLbl)

        #codigo para obtener valor en heap
        self.getHeap(tempC, tempH)#tempC = HEAP[int(tempH)]

        #comparo con if lo q obtuve en heap si es el fin de cadena osea el -1
        self.addIf(tempC, '-1', '==', returnLbl)


        ##################################################### 
        #AQUI DEBERIA DE VENIR EL PARSEO DE A - a etc.
        #porq guardo en el HEAP

        #65-90
        #CONDICION PARA Q LOS DEL RANGO DE ARRBIBA SEAN LOS UNICOS AFECTADOS DEL LOWERCASE
        self.addIf(tempC, '64', '<=', fase2)
        self.addIf(tempC, '91', '>=', fase3)


        self.addExp(tempC,tempC,32,'+')

        #self.addPrint('c', tempC)
        self.inputLabel(fase2)
        self.inputLabel(fase3)
        self.setHeap('H', tempC)   # heap[H] = ascii de c/u de los caracter de la cadena;
        self.nextHeap()
         
        #################################################### 

        self.addExp(tempH, tempH, '1', '+')#hay q avanzar para recorrer la cadena en heap por eso inc el valor del stack

        self.addGoto(compareLbl)

        self.inputLabel(returnLbl)#escribo la posicion donde esta la salida




        #FINALIZO LA CADENA LOWERCASE CON UN -1

        self.setHeap('H', '-1')            # FIN DE CADENA q es -1
        self.nextHeap()                    # H = H + 1;
         

        tempret = self.addTemporal()#T2
        self.addExp(tempret, 'P', '0', '+')
        
        #obtener el valor de param_cadena
        self.setStack(tempret, retTemp)

        self.addEndFunc()#finalizo la funcion siempre asi
        self.inNatives = False#para q ya no escriba en nativas sino en code





#-------------------------------------------------------------------------------------------------


    def fElevateNumber(self):
        #------------------
        # 0-return
        # 1-param_number    (mejor si lo tomo como decimal) y retorno decimal
        # 2-veces a elevar
        #------------------

        if(self.elevateNumber):
            return
        self.elevateNumber = True#para q no crea copias y copias de si misma
        self.inNatives = True#para escribir en Natives

        #le agrego nombre a la funcion
        self.addBeginFunc('elevateNumber')

        # Label para salir de la funcion q mete la palabra 1vez
        #returnLbl = self.newLabel()#L0
        # Label para concatenar nuevamente la funcion, definitiva para volver a concatenar la palabra
        returnLbl2 = self.newLabel()#L0

        returnLbl23 = self.newLabel()#L0 por si exponente ==0
        # Label bucle para la comparacion para buscar fin de cadena -1
        #compareLbl = self.newLabel()#L1



        # creo Temporal puntero a Stack para Heap
        tempP = self.addTemporal()#T1
        # obtendre el numero a elevar
        tempH = self.addTemporal()#T2
        tempH0 = self.addTemporal()#el numero bkup



                #ojo para indice a guardar en stakc***********************          (YA NEL)
        #retTemp = self.addTemporal()
        #self.addCommit("-------------CADENA 1-----------------")
        #self.addExp(retTemp, 'H', '', '')#temporal q apunta a heap debo meter en pos return

        self.addExp(tempH0, '1', '', '')
        self.inputLabel(returnLbl2)

        #obtener posicion de param_cadena de esta funcion
        
        self.addExp(tempP, 'P', '1', '+')

        #obtener el valor de param_cadena
        self.getStack(tempH, tempP,"//obtengo el num a elevar")
        #self.getStack(tempH0, tempP)

        ######################################################################para el param2
        # creo Temporal puntero a Stack para Heap
        tempP2 = self.addTemporal()#T1
        # obtendre el num de veces a multiplicar
        tempH2 = self.addTemporal()#T2

        #obtener posicion de param_cadena de esta funcion
        self.addExp(tempP2, 'P', '2', '+')

        #obtener el valor de las N veces a concatenar
        self.getStack(tempH2, tempP2,"//obtengo el exponente")

        #################################################

        self.addIf(tempH2, '0', '<=', returnLbl23)



        # Temporal para comparar cadena en heap; lo usare para acceder al heap
        #tempC = self.addTemporal()


        



        #escribo en el area de codigo el label
        #self.inputLabel(compareLbl)#L46






        #codigo para obtener valor en heap&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        #self.getHeap(tempC, tempH)#tempC = HEAP[int(tempH)]

        #comparo con if lo q obtuve en heap si es el fin de cadena osea el -1
        #self.addIf(tempC, '-1', '==', returnLbl)



        #pilas$$$$  #################################################### 
        #self.addPrint('c', tempC)
        #self.setHeap('H', tempC)   # heap[H] = ascii de c/u de los caracter de la cadena;
        #self.nextHeap()
        #################################################### 

        self.addExp(tempH0, tempH0,tempH , '*')#hay q avanzar para recorrer la cadena en heap por eso inc el valor del stack

        #self.addGoto(compareLbl)

        #self.inputLabel(returnLbl)#escribo la posicion donde esta la salida




        ############TENGO Q REDUCIR EL CONTADOR-- PARAM2
        self.addExp(tempH2, tempH2, '1', '-')#hay q avanzar para recorrer la cadena en heap por eso inc el valor del stack
        self.setStack(tempP2,tempH2)
        

        #comparo con if lo q obtuve en heap si es el fin de cadena osea el -1
        self.addIf(tempH2, '0', '!=', returnLbl2)

        #self.setHeap('H', '-1')            # FIN DE CADENA q es -1
        #self.nextHeap()                    # H = H + 1;

        self.inputLabel(returnLbl23)
        tempret = self.addTemporal()#T2
        self.addExp(tempret, 'P', '0', '+')
        
        #obtener el valor de param_cadena
        self.setStack(tempret, tempH0)

        self.addEndFunc()#finalizo la funcion siempre asi
        self.inNatives = False#para q ya no escriba en nativas sino en code



#-------------------------------------------------------------------------------------------------



    def fElevateString(self):
        #------------------
        # 0-return
        # 1-param_cadena1
        # 2-veces a elevar
        #------------------
        if(self.concatString2):
            return
        self.concatString2 = True#para q no crea copias y copias de si misma
        self.inNatives = True#para escribir en Natives

        #le agrego nombre a la funcion
        self.addBeginFunc('elevateString')

        # Label para salir de la funcion q mete la palabra 1vez
        returnLbl = self.newLabel()#L0

        # Label para concatenar nuevamente la funcion, definitiva para volver a concatenar la palabra
        returnLbl2 = self.newLabel()#L0

        # Label bucle para la comparacion para buscar fin de cadena -1
        compareLbl = self.newLabel()#L1

        # creo Temporal puntero a Stack para Heap
        tempP = self.addTemporal()#T1

        # creo Temporal puntero a Heap de la cadena en si
        tempH = self.addTemporal()#T2



                #ojo para indice a guardar en stakc***********************
        retTemp = self.addTemporal()
        self.addCommit("-------------CADENA 1-----------------")
        self.addExp(retTemp, 'H', '', '')#temporal q apunta a heap debo meter en pos return


        self.inputLabel(returnLbl2)

        #obtener posicion de param_cadena de esta funcion
        self.addExp(tempP, 'P', '1', '+')

        #obtener el valor de param_cadena
        self.getStack(tempH, tempP,"//obtengo la cadena a elevar")

        ######################################################################para el param2
        # creo Temporal puntero a Stack para Heap
        tempP2 = self.addTemporal()#T1

        # creo Temporal puntero a Heap de la cadena en si
        tempH2 = self.addTemporal()#T2

        #obtener posicion de param_cadena de esta funcion
        self.addExp(tempP2, 'P', '2', '+')

        #obtener el valor de las N veces a concatenar
        self.getStack(tempH2, tempP2,"//obtengo el exponente")
        #################################################

        # Temporal para comparar cadena en heap; lo usare para acceder al heap
        tempC = self.addTemporal()


        

        #escribo en el area de codigo el label
        self.inputLabel(compareLbl)

        #codigo para obtener valor en heap
        self.getHeap(tempC, tempH)#tempC = HEAP[int(tempH)]

        #comparo con if lo q obtuve en heap si es el fin de cadena osea el -1
        self.addIf(tempC, '-1', '==', returnLbl)



        #pilas$$$$  #################################################### 
        #self.addPrint('c', tempC)
        self.setHeap('H', tempC)   # heap[H] = ascii de c/u de los caracter de la cadena;
        self.nextHeap()
         
        #################################################### 

        self.addExp(tempH, tempH, '1', '+')#hay q avanzar para recorrer la cadena en heap por eso inc el valor del stack

        self.addGoto(compareLbl)

        self.inputLabel(returnLbl)#escribo la posicion donde esta la salida




        ############TENGO Q REDUCIR EL CONTADOR-- PARAM2
        self.addExp(tempH2, tempH2, '1', '-')#hay q avanzar para recorrer la cadena en heap por eso inc el valor del stack
        self.setStack(tempP2,tempH2)
        

        #comparo con if lo q obtuve en heap si es el fin de cadena osea el -1
        self.addIf(tempH2, '0', '!=', returnLbl2)

        self.setHeap('H', '-1')            # FIN DE CADENA q es -1
        self.nextHeap()                    # H = H + 1;
         

        tempret = self.addTemporal()#T2
        self.addExp(tempret, 'P', '0', '+')
        
        #obtener el valor de param_cadena
        self.setStack(tempret, retTemp)

        self.addEndFunc()#finalizo la funcion siempre asi
        self.inNatives = False#para q ya no escriba en nativas sino en code





#-------------------------------------------------------------------------------------------------



    def fConcatString(self):
        #------------------
        # 0-return
        # 1-param_cadena1
        # 2-param_cadena2
        #------------------
        if(self.concatString):
            return
        self.concatString = True#para q no crea copias y copias de si misma
        self.inNatives = True#para escribir en Natives

        #le agrego nombre a la funcion
        self.addBeginFunc('concatString')

        # Label para salir de la funcion
        returnLbl = self.newLabel()#L0

        # Label bucle para la comparacion para buscar fin de cadena -1
        compareLbl = self.newLabel()#L1

        # creo Temporal puntero a Stack para Heap
        tempP = self.addTemporal()#T1

        # creo Temporal puntero a Heap de la cadena en si
        tempH = self.addTemporal()#T2

        #obtener posicion de param_cadena de esta funcion
        self.addExp(tempP, 'P', '1', '+')

        #obtener el valor de param_cadena
        self.getStack(tempH, tempP,"//obtengo posicion en heap de la cadena1")

        # Temporal para comparar cadena en heap; lo usare para acceder al heap
        tempC = self.addTemporal()

        #ojo para indice a guardar en stakc***********************
        retTemp = self.addTemporal()
        self.addCommit("-------------CADENA 1-----------------")
        self.addExp(retTemp, 'H', '', '')#temporal q apunta a heap debo meter en pos return
        

        #escribo en el area de codigo el label
        self.inputLabel(compareLbl)

        #codigo para obtener valor en heap
        self.getHeap(tempC, tempH)#tempC = HEAP[int(tempH)]

        #comparo con if lo q obtuve en heap si es el fin de cadena osea el -1
        self.addIf(tempC, '-1', '==', returnLbl)



        #pilas$$$$  #################################################### 
        #self.addPrint('c', tempC)
        self.setHeap('H', tempC)   # heap[H] = ascii de c/u de los caracter de la cadena;
        self.nextHeap()
         
        #################################################### 

        self.addExp(tempH, tempH, '1', '+')#hay q avanzar para recorrer la cadena en heap por eso inc el valor del stack

        self.addGoto(compareLbl)

        self.inputLabel(returnLbl)#escribo la posicion donde esta la salida
        
        



        ###################################################### ahora para la seugnda cadena
        # Label para salir de la funcion
        returnLbl = self.newLabel()#L0

        # Label bucle para la comparacion para buscar fin de cadena -1
        compareLbl = self.newLabel()#L1

        # creo Temporal puntero a Stack para Heap
        tempP = self.addTemporal()#T1

        # creo Temporal puntero a Heap de la cadena en si
        tempH = self.addTemporal()#T2

        #obtener posicion de param_cadena de esta funcion
        self.addExp(tempP, 'P', '2', '+')

        #obtener el valor de param_cadena
        self.getStack(tempH, tempP,"//obtengo posicion en heap de la cadena2")

        # Temporal para comparar cadena en heap; lo usare para acceder al heap
        tempC = self.addTemporal()

        #escribo en el area de codigo el label
        self.inputLabel(compareLbl)

        #codigo para obtener valor en heap
        self.getHeap(tempC, tempH)#tempC = HEAP[int(tempH)]

        #comparo con if lo q obtuve en heap si es el fin de cadena osea el -1
        self.addIf(tempC, '-1', '==', returnLbl)

        #pilas$$$$  #################################################### 
        #self.addPrint('c', tempC)
        
        self.addCommit("-------------CADENA 2-----------------")
        self.setHeap('H', tempC)   # heap[H] = ascii de c/u de los caracter de la cadena;
        self.nextHeap()
         
        #################################################### 

        self.addExp(tempH, tempH, '1', '+')#hay q avanzar para recorrer la cadena en heap por eso inc el valor del stack

        self.addGoto(compareLbl)


        #ya el final ahora toca asignar el valor a P0 del ret
        self.inputLabel(returnLbl)#escribo la posicion donde esta la salida

        self.setHeap('H', '-1')            # FIN DE CADENA q es -1
        self.nextHeap()                    # H = H + 1;
         

        tempret = self.addTemporal()#T2
        self.addExp(tempret, 'P', '0', '+')
        
        #obtener el valor de param_cadena
        self.setStack(tempret, retTemp)

        self.addEndFunc()#finalizo la funcion siempre asi
        self.inNatives = False#para q ya no escriba en nativas sino en code
        



#-------------------------------------------------------------------------------------------------


    def fPrintString(self):
        #------------------
        # 0-return
        # 1-param_cadena
        #------------------
        if(self.printString):
            return
        self.printString = True#para q no crea copias y copias de si misma
        self.inNatives = True

        #le agrego nombre a la funcion
        self.addBeginFunc('printString')

        # Label para salir de la funcion
        returnLbl = self.newLabel()#L0

        # Label bucle para la comparacion para buscar fin de cadena -1
        compareLbl = self.newLabel()#L1

        # creo Temporal puntero a Stack para Heap
        tempP = self.addTemporal()#T1

        # creo Temporal puntero a Heap de la cadena en si
        tempH = self.addTemporal()#T2

        #obtener posicion de param_cadena de esta funcion
        self.addExp(tempP, 'P', '1', '+')

        #obtener el valor de param_cadena
        self.getStack(tempH, tempP,"//obtengo posicion en heap de la cadena a imprimir")

        # Temporal para comparar cadena en heap; lo usare para acceder al heap
        tempC = self.addTemporal()

        #escribo en el area de codigo el label
        self.inputLabel(compareLbl)

        #codigo para obtener valor en heap
        self.getHeap(tempC, tempH)#tempC = HEAP[int(tempH)]

        #comparo con if lo q obtuve en heap si es el fin de cadena osea el -1
        self.addIf(tempC, '-1', '==', returnLbl)

        self.addPrint('c', tempC)

        self.addExp(tempH, tempH, '1', '+')#hay q avanzar para recorrer la cadena en heap por eso inc el valor del stack

        self.addGoto(compareLbl)

        self.inputLabel(returnLbl)#escribo la posicion donde esta la salida
        self.addEndFunc()#finalizo la funcion siempre asi
        self.inNatives = False#para q ya no escriba en nativas sino en code



#-------------------------------------------------------------------------------------------------


    def fPrintArray(self):
        #------------------
        # 0-return
        # 1-param_array
        #------------------
        if(self.printARRAY):
            return
        self.printARRAY = True#para q no crea copias y copias de si misma
        self.inNatives = True

        #le agrego nombre a la funcion
        self.addBeginFunc('printArray')

        # Label para salir de la funcion
        returnLbl = self.newLabel()#L0

        # Label bucle para la comparacion para buscar fin de array -1
        compareLbl = self.newLabel()#L1

        # creo Temporal puntero a Stack para Heap
        tempP = self.addTemporal()#T1

        # creo Temporal puntero a Heap de la array en si
        tempH = self.addTemporal()#T2

        tempTam2= self.addTemporal()#T2
        tempTam= self.addTemporal()#T2

        #obtener posicion de param_array de esta funcion
        self.addExp(tempP, 'P', '1', '+')

        self.addExp(tempTam2, '0', '', '')#INICIALIZO CONTADOR DEL TAM DEL ARREGLO

        #obtener el valor de param_array
        self.getStack(tempH, tempP,"//obtengo tam del array a imprimir q esta en heap")

        # Temporal para comparar array en heap; lo usare para acceder al heap
        tempC = self.addTemporal()




        #codigo para obtener valor en heap del tam del array
        self.getHeap(tempTam, tempH)#GUARDARA EL N TAM DEL ARRAY

        #self.addExp(tempTam, tempTam, '1', '+')#incremento el tam +1

        self.addExp(tempH, tempH, '1', '+')#incremento para obtener el 1er elemento del array
        
        #escribo en el area de codigo el label
        self.addPrint('c', 91)
        self.inputLabel(compareLbl)

        #codigo para obtener valor en heap
        self.getHeap(tempC, tempH)#tempC = HEAP[int(tempH)] :: saque el 1er elemento del array

        

        #comparo con if lo q obtuve en heap si es el fin de array osea el -1
        self.addIf(tempTam2, tempTam, '==', returnLbl)

        self.addPrint('d', tempC)
        

        self.addExp(tempH, tempH, '1', '+')#hay q avanzar para recorrer la array en heap por eso inc el valor del stack
        self.addExp(tempTam2, tempTam2, '1', '+')#hay q reducir el tam del array

        self.addIf(tempTam2, tempTam, '==', returnLbl)
        self.addPrint('c', 44)
        self.addGoto(compareLbl)

        self.inputLabel(returnLbl)#escribo la posicion donde esta la salida
        self.addPrint('c', 93)
        self.addEndFunc()#finalizo la funcion siempre asi
        self.inNatives = False#para q ya no escriba en nativas sino en code




#-------------------------------------------------------------------------------------------------


    def fLength(self):
        #------------------
        # 0-return
        # 1-param_array
        #------------------
        if(self.printARRAY2):
            return
        self.printARRAY2 = True#para q no crea copias y copias de si misma
        self.inNatives = True

        #le agrego nombre a la funcion
        self.addBeginFunc('length')

        # Label para salir de la funcion
        #returnLbl = self.newLabel()#L0

        # Label bucle para la comparacion para buscar fin de array -1
        #compareLbl = self.newLabel()#L1

        # creo Temporal puntero a Stack para Heap
        tempP = self.addTemporal()#T1

        # creo Temporal puntero a Heap de la array en si
        tempH = self.addTemporal()#T2

        #tempTam2= self.addTemporal()#T2
        tempTam= self.addTemporal()#T2

        #obtener posicion de param_array de esta funcion
        self.addExp(tempP, 'P', '1', '+')

        #self.addExp(tempTam2, '0', '', '')#INICIALIZO CONTADOR DEL TAM DEL ARREGLO

        #obtener el valor de param_array
        self.getStack(tempH, tempP,"//obtengo tam del array a imprimir q esta en heap")

        # Temporal para comparar array en heap; lo usare para acceder al heap
        #tempC = self.addTemporal()




        #codigo para obtener valor en heap del tam del array
        self.getHeap(tempTam, tempH)#GUARDARA EL N TAM DEL ARRAY

        '''#self.addExp(tempTam, tempTam, '1', '+')#incremento el tam +1

        self.addExp(tempH, tempH, '1', '+')#incremento para obtener el 1er elemento del array
        
        #escribo en el area de codigo el label
        self.addPrint('c', 91)
        self.inputLabel(compareLbl)

        #codigo para obtener valor en heap
        self.getHeap(tempC, tempH)#tempC = HEAP[int(tempH)] :: saque el 1er elemento del array

        

        #comparo con if lo q obtuve en heap si es el fin de array osea el -1
        self.addIf(tempTam2, tempTam, '==', returnLbl)

        self.addPrint('d', tempC)
        

        self.addExp(tempH, tempH, '1', '+')#hay q avanzar para recorrer la array en heap por eso inc el valor del stack
        self.addExp(tempTam2, tempTam2, '1', '+')#hay q reducir el tam del array

        self.addIf(tempTam2, tempTam, '==', returnLbl)
        self.addPrint('c', 44)
        self.addGoto(compareLbl)'''

        #self.inputLabel(returnLbl)#escribo la posicion donde esta la salida
        #self.addPrint('c', 93)

        tempret = self.addTemporal()#T2
        self.addExp(tempret, 'P', '0', '+')
        
        #obtener el valor de param_cadena
        self.setStack(tempret,tempTam)
        self.addEndFunc()#finalizo la funcion siempre asi
        self.inNatives = False#para q ya no escriba en nativas sino en code








#-------------------------------------------------------------------------------------------------



    def fStringIgual(self):
        #------------------
        # 0-return  0 si no son iguales, else 1 si son iguales
        # 1-param_cadena1
        # 2-param_cadena2
        #------------------
        if(self.stringIgual):
            return
        self.stringIgual= True#para q no crea copias y copias de si misma
        self.inNatives = True#para escribir en Natives

        #le agrego nombre a la funcion
        self.addBeginFunc('IgualdadString')

        # Label para salir de la funcion
        returnLbl = self.newLabel()#L0

        iguales = self.newLabel()#L0

        noiguales = self.newLabel()#L0

        continuar = self.newLabel()#L0


        # Label para salir de la funcion
        returnLbl2 = self.newLabel()#L0

        # Label bucle para la comparacion para buscar fin de cadena -1
        compareLbl = self.newLabel()#L1

        # creo Temporal puntero a Stack para Heap
        tempP = self.addTemporal()#T1

        # creo Temporal puntero a Heap de la cadena en si
        tempH = self.addTemporal()#T2

        tempH2 = self.addTemporal()#T2



        retTemp2= self.addTemporal()
        self.addExp(retTemp2, '0', '', '')
        finish = self.newLabel()#L1


        #ojo para indice a guardar en stakc***********************
        retTemp = self.addTemporal()
        self.addExp(retTemp, '0', '', '')

        #obtener posicion de param_cadena de esta funcion
        self.addExp(tempP, 'P', '1', '+')

        #obtener el valor de param_cadena
        self.getStack(tempH, tempP,"//obtengo posicion en heap de la cadena1")
        self.addCommit("-------------CADENA 2-----------------")
        #obtener posicion de param_cadena de esta funcion
        self.addExp(tempP, tempP, '1', '+')

        #obtener el valor de param_cadena
        self.getStack(tempH2, tempP,"//obtengo posicion en heap de la cadena2")



        mismaLongitud = self.newLabel()




        #FINAL le seteo 0 o 1 a retTemp
        # Temporal para comparar cadena en heap; lo usare para acceder al heap
        tempC = self.addTemporal()

        
        self.addCommit("-------------CADENA 1-----------------")
        #self.addExp(retTemp, 'H', '', '')#temporal q apunta a heap debo meter en pos return
        

        #escribo en el area de codigo el label
        self.inputLabel(compareLbl)

        #codigo para obtener valor en heap
        self.getHeap(tempC, tempH)#tempC = HEAP[int(tempH)]

        #comparo con if lo q obtuve en heap si es el fin de cadena osea el -1
        self.addIf(tempC, '-1', '==', returnLbl2)



        ###############################


        self.inputLabel(returnLbl2)#escribo la posicion donde esta la salida
        

        # Temporal para comparar cadena en heap; lo usare para acceder al heap
        tempC2 = self.addTemporal()

        #codigo para obtener valor en heap
        self.getHeap(tempC2, tempH2)#tempC = HEAP[int(tempH)]

        #comparo con if lo q obtuve en heap si es el fin de cadena osea el -1
        self.addIf(tempC2, '-1', '==', returnLbl)


        #####################COMPARO AMBAS CHAR DE LAS 2 CADENAS


        self.addIf(tempC, tempC2, '==', iguales)
        self.addGoto(noiguales)


        self.inputLabel(iguales)
        self.addExp(retTemp, '1', '', '')#porq ambas son iguales

        self.addGoto(continuar)

        self.inputLabel(noiguales)
        self.addExp(retTemp, '0', '', '')#porq ambas NO son iguales
        self.addExp(retTemp2, retTemp2, '1', '-')#porq ambas NO son iguales
        



        self.inputLabel(continuar)
        self.addCommit("INCREMENTO AMBAS POSICIONES DE CADENAS")
        self.addExp(tempH, tempH, '1', '+')#hay q avanzar para recorrer la cadena en heap por eso inc el valor del stack
        self.addExp(tempH2, tempH2, '1', '+')#hay q avanzar para recorrer la cadena en heap por eso inc el valor del stack
        
        
        
        self.addGoto(compareLbl)
        #ya el final ahora toca asignar el valor a P0 del ret
        #self.inputLabel(returnLbl)#escribo la posicion donde esta la salida



        ################################


        self.inputLabel(returnLbl)#escribo la posicion donde esta la salida


        #self.addExp(tempH2, tempH2, '1', '+')#hay q avanzar para recorrer la cadena en heap por eso inc el valor del stack
        #self.getHeap(tempC2, tempH2)#tempC = HEAP[int(tempH)]



        self.addIf(tempC2, tempC, '==', mismaLongitud)
        self.addExp(retTemp, '0', '', '')#porq ambas NO son iguales

        
        

        self.inputLabel(mismaLongitud)
        self.addIf(retTemp2, '0', '==', finish)
        self.addExp(retTemp, '0', '', '')#porq ambas NO son iguales


        self.inputLabel(finish)#escribo la posicion donde esta la salida
        ###################################################### ahora para la seugnda cadena
        # Label para salir de la funcion
        returnLbl = self.newLabel()#L0

        # Label bucle para la comparacion para buscar fin de cadena -1
        compareLbl = self.newLabel()#L1

        # creo Temporal puntero a Stack para Heap
        tempP = self.addTemporal()#T1

        # creo Temporal puntero a Heap de la cadena en si
        tempH = self.addTemporal()#T2
        

                     

        tempret = self.addTemporal()#T2
        self.addExp(tempret, 'P', '0', '+')
        
        #obtener el valor de param_cadena
        self.setStack(tempret, retTemp)

        self.addEndFunc()#finalizo la funcion siempre asi
        self.inNatives = False#para q ya no escriba en nativas sino en code
        
#-------------------------------------------------------------------------------------------------



    def fStringNotIgual(self):
        #------------------
        # 0-return  0 si no son iguales, else 1 si son iguales
        # 1-param_cadena1
        # 2-param_cadena2
        #------------------
        if(self.stringNotIgual):
            return
        self.stringNotIgual= True#para q no crea copias y copias de si misma
        self.inNatives = True#para escribir en Natives

        #le agrego nombre a la funcion
        self.addBeginFunc('DesigualdadString')

        # Label para salir de la funcion
        returnLbl = self.newLabel()#L0

        iguales = self.newLabel()#L0

        noiguales = self.newLabel()#L0

        continuar = self.newLabel()#L0


        # Label para salir de la funcion
        returnLbl2 = self.newLabel()#L0

        # Label bucle para la comparacion para buscar fin de cadena -1
        compareLbl = self.newLabel()#L1

        # creo Temporal puntero a Stack para Heap
        tempP = self.addTemporal()#T1

        # creo Temporal puntero a Heap de la cadena en si
        tempH = self.addTemporal()#T2

        tempH2 = self.addTemporal()#T2



        retTemp2= self.addTemporal()
        self.addExp(retTemp2, '0', '', '')
        finish = self.newLabel()#L1


        #ojo para indice a guardar en stakc***********************
        retTemp = self.addTemporal()
        self.addExp(retTemp, '0', '', '')

        #obtener posicion de param_cadena de esta funcion
        self.addExp(tempP, 'P', '1', '+')

        #obtener el valor de param_cadena
        self.getStack(tempH, tempP,"//obtengo posicion en heap de la cadena1")
        self.addCommit("-------------CADENA 2-----------------")
        #obtener posicion de param_cadena de esta funcion
        self.addExp(tempP, tempP, '1', '+')

        #obtener el valor de param_cadena
        self.getStack(tempH2, tempP,"//obtengo posicion en heap de la cadena2")



        mismaLongitud = self.newLabel()




        #FINAL le seteo 0 o 1 a retTemp
        # Temporal para comparar cadena en heap; lo usare para acceder al heap
        tempC = self.addTemporal()

        
        self.addCommit("-------------CADENA 1-----------------")
        #self.addExp(retTemp, 'H', '', '')#temporal q apunta a heap debo meter en pos return
        

        #escribo en el area de codigo el label
        self.inputLabel(compareLbl)

        #codigo para obtener valor en heap
        self.getHeap(tempC, tempH)#tempC = HEAP[int(tempH)]

        #comparo con if lo q obtuve en heap si es el fin de cadena osea el -1
        self.addIf(tempC, '-1', '==', returnLbl2)



        ###############################


        self.inputLabel(returnLbl2)#escribo la posicion donde esta la salida
        

        # Temporal para comparar cadena en heap; lo usare para acceder al heap
        tempC2 = self.addTemporal()

        #codigo para obtener valor en heap
        self.getHeap(tempC2, tempH2)#tempC = HEAP[int(tempH)]

        #comparo con if lo q obtuve en heap si es el fin de cadena osea el -1
        self.addIf(tempC2, '-1', '==', returnLbl)


        #####################COMPARO AMBAS CHAR DE LAS 2 CADENAS


        self.addIf(tempC, tempC2, '==', iguales)
        self.addGoto(noiguales)


        self.inputLabel(iguales)
        self.addExp(retTemp, '1', '', '')#porq ambas son iguales

        self.addGoto(continuar)

        self.inputLabel(noiguales)
        self.addExp(retTemp, '0', '', '')#porq ambas NO son iguales
        self.addExp(retTemp2, retTemp2, '1', '-')#porq ambas NO son iguales
        



        self.inputLabel(continuar)
        self.addCommit("INCREMENTO AMBAS POSICIONES DE CADENAS")
        self.addExp(tempH, tempH, '1', '+')#hay q avanzar para recorrer la cadena en heap por eso inc el valor del stack
        self.addExp(tempH2, tempH2, '1', '+')#hay q avanzar para recorrer la cadena en heap por eso inc el valor del stack
        
        
        
        self.addGoto(compareLbl)
        #ya el final ahora toca asignar el valor a P0 del ret
        #self.inputLabel(returnLbl)#escribo la posicion donde esta la salida



        ################################


        self.inputLabel(returnLbl)#escribo la posicion donde esta la salida


        #self.addExp(tempH2, tempH2, '1', '+')#hay q avanzar para recorrer la cadena en heap por eso inc el valor del stack
        #self.getHeap(tempC2, tempH2)#tempC = HEAP[int(tempH)]



        self.addIf(tempC2, tempC, '==', mismaLongitud)
        self.addExp(retTemp, '0', '', '')#porq ambas NO son iguales

        
        

        self.inputLabel(mismaLongitud)
        self.addIf(retTemp2, '0', '==', finish)
        self.addExp(retTemp, '0', '', '')#porq ambas NO son iguales


        self.inputLabel(finish)#escribo la posicion donde esta la salida
        ###################################################### ahora para la seugnda cadena
        # Label para salir de la funcion
        returnLbl = self.newLabel()#L0

        # Label bucle para la comparacion para buscar fin de cadena -1
        compareLbl = self.newLabel()#L1

        # creo Temporal puntero a Stack para Heap
        tempP = self.addTemporal()#T1

        # creo Temporal puntero a Heap de la cadena en si
        tempH = self.addTemporal()#T2
        

                     

        tempret = self.addTemporal()#T2
        self.addExp(tempret, 'P', '0', '+')
        
        #obtener el valor de param_cadena
        self.setStack(tempret, retTemp)

        self.addEndFunc()#finalizo la funcion siempre asi
        self.inNatives = False#para q ya no escriba en nativas sino en code