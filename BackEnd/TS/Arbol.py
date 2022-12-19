from TS.Generador import Generator


class Arbol:#va a ser nuestro AST
    def __init__(self, instrucciones):
        self.instrucciones= instrucciones
        self.funciones = []#lista de funciones; si va en tabla simbolos F porq hay q respetar el ambito
        self.excepciones=[]
        self.consola=""#lista de la salida del interprete
        self.TablaSimbolosGlobal=None
        self.structs = []#lista de funciones; si va en tabla simbolos F porq hay q respetar el ambito
        self.dot =""
        self.contadorAST=0
        #--------------------------------
        #self.size=0#para el ambito actual: cuando cree variables INC =++
        self.genAux = Generator()




        self.returnLbl ={} #tipo de un return para cada funcion leida



        #-------------------------------- creo q ya no se usaran
        self.contador=0#contador para diferenciar Ts etc.

        self.contadorLV_LF=0#contador para diferenciar Ls etc.

        self.PILA=0#valor de la pila donde apunte a vacio
        self.PILAenPosicionVacia=0
        self.HEAP=0#valor de heap donde apunte a vacio

        self.C3D=""
#--------------------------------------------
    def finalizarC3D(self):
        paquete = "package main;\n"
        importacion = "import ( \"fmt\" ); // importar para el uso de printf\n"
        stack ="var stack [30101999]float64; // estructura Stack\n"
        heap ="var heap [30101999]float64; // estructura Heap\n"
        apuntadoresSH="var P, H float64; // declaración de Stack y heap pointer\n"#P y H
        TsFor="var "
        count = 0
        while(count < self.contador):
            count = count + 1
            if count < self.contador:
                TsFor+="T"+str(count)+","

            if count == self.contador:
                TsFor+="T"+str(count)
        
        TsFor+=" float64;"



        Ts=TsFor+"\nfunc main(){\n"#crear dinamicamente todos los Ts con el self.contador>0 con for dinamico

        self.C3D= paquete+importacion+stack+heap+apuntadoresSH+Ts+self.C3D+"\n}\n"




#--------------------------------------------
    def getInstrucciones(self):
        return self.instrucciones

    def setInstrucciones(self, instruc):
        self.instrucciones= instruc
#--------------------------------------------
    def getExcepciones(self):
        return self.excepciones

    def setExcepciones(self, excp):
        self.excepciones= excp
#--------------------------------------------
    def getConsola(self):
        return self.consola

    def updateConsola(self,cadena,tipo):#para agregar a consola una cadena al final consola es lo q mostramos todos los errores (del proyecto)
        #if tercer params =1 println else print
        if tipo==1:
            self.consola+='\n'+str(cadena)+'\n'#aguas \n
            self.C3D+='\n'+str(cadena)+'\n'#aguas \n
        else:
            self.consola+=str(cadena)
            self.C3D+='\n'+str(cadena)+'\n'#aguas \n


    def setConsola(self, consola):
        self.consola= consola
#--------------------------------------------
    def getTablaSimbolosGlobal(self):
        return self.TablaSimbolosGlobal

    def setTablaSimbolosGlobal(self, TablaSimbolosGlobal):
        self.TablaSimbolosGlobal= TablaSimbolosGlobal




# V2.0
#--------------------------------------------
    def getFunciones(self):
        return self.funciones


    def getFuncion(self,id):
        for funcion in self.funciones:
            if funcion.nombre==id:
                return funcion
        return None
            

    def addFuncion(self,func):
        self.funciones.append(func)

# V2.0
#--------------------------------------------
    def getStructssss(self):
        return self.structs


    def getStruct(self,id):
        for funcion in self.structs:
            if funcion.nombre==id:
                return funcion
        return None

        
    def addStruct(self,func):
        self.structs.append(func)



    def getDot(self, raiz):#DEVUELVE EL STRING-GRAPHVIZ DE LA GRAFICA
        self.dot=""#reset
        self.dot += "digraph {\n"

        self.dot+= "n0[label=\"" +raiz.getValor().replace("\"","\\\"")+"\"];\n"
        self.contadorAST=1
        self.recorrerAST("n0",raiz)
        self.dot+="\n}"
        return self.dot


    def recorrerAST(self,idPadre,nodoPadre):


            try:
                for hijo in nodoPadre.getHijos():
                    nombreHijo = "n"+str(self.contadorAST)
                
                    self.dot+=nombreHijo+"[label=\"" +hijo.getValor().replace("\"","\\\"")+"\"];\n"
                    self.dot+=idPadre+"->"+nombreHijo+";\n"
                    self.contadorAST+=1
                    self.recorrerAST(nombreHijo,hijo)
            except:
                pass

        
            

            
        
            
        








