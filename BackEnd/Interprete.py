from gramaticaJL import *   #fase 1 y 2 compilacion
from OptimizadorGram import *#fase 2 optimizacion
from TS.Arbol import Arbol
from TS.TablaSimbolo import TablaSimbolos
from datetime import datetime
from TS.Generador import Generator



class Analizador():

    def __init__(self):
        self.instrucciones=None
        self.errores=[]
        self.ast=None
        self.TSGlobal=None#sin nada creo porq esta en el ast
        self.grafo=''
        self.erroresSTR=[]
        self.TablaSimbolosREPORT=[]
        self.C3D =""
        self.genAux=None
        self.generator=None


        self.OptimizacionMirilla=''
        self.ErroresMirilla =[]
        

    

    def Main(self,entrada):
        self.genAux = Generator()
        self.genAux.ResetC3D()
        self.generator = self.genAux.getInstance()

        self.instrucciones = ParseJV(entrada)#obtengo el arbol ast      aqui se ejecuta PLY

        self.errores = getErrores()#obtengo la lista de errores lexicos,sintacticos,semanticos que me genero PLY
        self.ast = Arbol(self.instrucciones)
        self.TSGlobal = TablaSimbolos()
        self.ast.setTablaSimbolosGlobal(self.TSGlobal)

        
        #PARA TODAS LAS FUNCIONES NATIVAS
        crearNativas(self.ast)

        print("\nERRORES LEXICOS Y SINTACTICOS metidos al AST")
        #PASADA DE ERRORES LEXICOS,SINTACTICOS
        for error in self.errores:#scanner y parser errores al ast donde ya estan los semanticos
            self.ast.getExcepciones().append(error)
            self.ast.updateConsola(error.toString(),1)

        # pasada para recolectar solo los structs
        for struct in self.ast.getInstrucciones():
            
                if isinstance(struct,Struct):#si detecto una funcion la meto a la lista de funciones del AST
                    self.ast.addStruct(struct) 


        # pasada para recolectar solo las funciones falta para los structs
        for instruccion in self.ast.getInstrucciones():
            if isinstance(instruccion,FuncionSP):#si detecto una funcion la meto a la lista de funciones del AST
                self.ast.addFuncion(instruccion) 





        #PASADA DE DECLARACIONES Y ASIGNACIONES
        for instruccion in self.ast.getInstrucciones():#parser y realizar lo que van entre print ( expresionPrint )

            if not isinstance(instruccion,FuncionSP)and not isinstance(instruccion,Struct):#si NO detecto una funcion ,tonces las interpreto 
        
                self.generator.addCommit("-------------INICIO INSTRUCCION-----------------")
        
                value=instruccion.compilar(self.ast,self.TSGlobal)#aqui obtengo el valor que esta dentro de ( ) de un print pero por ser ejemplo los agrego a las excepciones(error)
                
                if isinstance(value, Excepcion):
                    self.ast.getExcepciones().append(value)
                    self.ast.updateConsola(value.toString(),1)

                if isinstance(value, Break):#para detectar los breaks como error afuera de whiles, falta continue y return
                    error = Excepcion("Semantico","Error semantico break fuera de ciclo",instruccion.fila,instruccion.columna)
                    self.ast.getExcepciones().append(error)#agregamos el error
                    self.ast.updateConsola(error.toString(),1)#e imprimimos 

                if isinstance(value, Continue):#para detectar los breaks como error afuera de whiles, falta continue y return
                    error = Excepcion("Semantico","Error semantico continue fuera de ciclo",instruccion.fila,instruccion.columna)
                    self.ast.getExcepciones().append(error)#agregamos el error
                    self.ast.updateConsola(error.toString(),1)#e imprimimos 


                if isinstance(value, Return):#para detectar los return como error afuera de whiles,funciones etc. falta continue
                    error = Excepcion("Semantico","Error semantico return fuera de ciclo o funcion",instruccion.fila,instruccion.columna)
                    self.ast.getExcepciones().append(error)#agregamos el error
                    self.ast.updateConsola(error.toString(),1)#e imprimimos 
                
        
        
        #EN ESTE PUNTO YA TENDRIA TODOS LOS ERRORES EN LA TB


        #ARBOL SINTACTICO--------------------------------------
        init =NodoAST("RAIZ")
        instr =NodoAST("INSTRUCCIONES")

        for instruccio in self.ast.getInstrucciones():
            instr.agregarHijoNodo(instruccio.getNodo())

        init.agregarHijoNodo(instr)


        
        self.grafo = self.ast.getDot(init)#retorna el AST graphviz
        '''
        dirname = os.path.dirname(__file__)#posiciono en lugar actual
        direcc=os.path.join(dirname,'ast.dot')
        arch = open(direcc,'w+')
        arch.write(self.grafo)
        arch.close()
        os.system("dot -T pdf -o ast.pdf ast.dot")#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ QUITAR COMMIT PARA HACER PDF
        '''
        #n16[label="tipo.ENTERO"]; hacerle un renplace para q salga int64
                
 
        print("\n\n************ CONSOLA ***********")
        print(self.ast.getConsola())
        print("\n\n--------------------------------------ERRORES----------------------------------")

        for excpt in self.ast.getExcepciones():

            now = datetime.now()
            DATE_TIME =str(now.day)+"/"+str(now.month)+"/"+str(now.year)+" "+str(now.hour)+":"+str(now.minute)       #SI NO LE SUMO +6 y-12 tambien, LAS HORAS SALE MAL EN HEROKU :'(
            #print(DATE_TIME)


            self.erroresSTR.append( {"tipo":str(excpt.tipo),"descripcion":str(excpt.descripcion),"fila":str(excpt.fila),"columna":str(excpt.columna),"tiempo":DATE_TIME  } )
            print(excpt.toString())
        
        
        print(str(len(self.erroresSTR)))
        print("[LISTA DE ERRORES LEX,SINTAC TAM]: "+str(len(self.errores)))      








        print("\n\n---------------------            FUNCIONES           -----------------------")
        print(self.ast.getFunciones())
        funcionesList =self.ast.getFunciones()
        for key in funcionesList:#itero el diccionario de cada funcion

            if isinstance(key, Uppercase) or isinstance(key,Lowercase) or isinstance(key,Length):
                print(str(key))

            if isinstance(key, FuncionSP) and not(    isinstance(key, Uppercase) or isinstance(key,Lowercase) or isinstance(key,Length)   ):
                ASH = {"tipo":"Funcion","nombre":str(key.nombre),"fila":str(key.fila),"columna":str(key.columna),"ambito":"global"  }
                self.TablaSimbolosREPORT.append(ASH)
                print(str(ASH)+"")
                #print(str(key))




        print("\n\n--------------------------------------TABLA SIMBOLOS DE FUNCIONES----------------------------------")#cada funcion posee su tabla de simbolos para si misma
        for key2 in funcionesList:#itero el diccionario de cada funcion

            if isinstance(key2, Uppercase) or isinstance(key2,Lowercase) or isinstance(key2,Length):
                print("No soy cannon :P"+str(key2))

            if isinstance(key2, FuncionSP) and not(    isinstance(key2, Uppercase) or isinstance(key2,Lowercase)  or isinstance(key2,Length)  ):
                tablaActual = key2.tablaSimbolosFuncion
                print(">>>FUNCION:"+key2.nombre)
                #print("tablaSimbolos:"+str(tablaActual))

                if tablaActual!=None:
                    for key in tablaActual.tabla:#itero el diccionario de cada tabla de simbolos
                        #print(str(key)+" : "+str(tablaActual.tabla[key]))
                        ASH = {"tipo":str(tablaActual.tabla[key].tipo),"nombre":str(tablaActual.tabla[key].id),"fila":str(tablaActual.tabla[key].fila),"columna":str(tablaActual.tabla[key].columna),"ambito":str(key2.nombre)  }
                        self.TablaSimbolosREPORT.append(ASH)
                        print(str(ASH)+"")
                            
                    #tablaActual = tablaActual.anterior

            print("\n------------------------------------------------------------------") 





        print("\n\n--------------------------------------TABLA SIMBOLOS DE STRUCTS----------------------------------")#cada funcion posee su tabla de simbolos para si misma
        
        StructList =self.ast.getStructssss()
        for key2 in StructList:#itero el diccionario de cada funcion

            if isinstance(key2, Uppercase) or isinstance(key2,Lowercase) or isinstance(key2,Length):
                print("No soy cannon :P"+str(key2))

            if isinstance(key2, Struct)  and not(    isinstance(key2, Uppercase) or isinstance(key2,Lowercase)  or isinstance(key2,Length)  ):
                tablaActual = key2.tablaSimbolosFuncion
                print(">>>FUNCION:"+key2.nombre)
                #print("tablaSimbolos:"+str(tablaActual))

                if tablaActual!=None:
                    for key in tablaActual.tabla:#itero el diccionario de cada tabla de simbolos
                        #print(str(key)+" : "+str(tablaActual.tabla[key]))
                        ASH = {"tipo":str(tablaActual.tabla[key].tipo),"nombre":str(tablaActual.tabla[key].id),"fila":str(tablaActual.tabla[key].fila),"columna":str(tablaActual.tabla[key].columna),"ambito":str(key2.nombre)  }
                        self.TablaSimbolosREPORT.append(ASH)
                        print(str(ASH)+"")
                            
                    #tablaActual = tablaActual.anterior

            print("\n------------------------------------------------------------------") 



        print("\n\n\n\n--------------------------------------TABLA SIMBOLOS GLOBAL----------------------------------")

        tablaActual = self.ast.getTablaSimbolosGlobal()
        #print(str(tablaActual))

        while tablaActual != None:

            #print(str(tablaActual.tabla))
            for key in tablaActual.tabla:#itero el diccionario de cada tabla de simbolos
                #print(str(key)+" : "+str(tablaActual.tabla[key]))

                if str(tablaActual.tabla[key].tipo)=="0":
                    ASH = {"tipo":"struct inmutable","nombre":str(tablaActual.tabla[key].id),"fila":str(tablaActual.tabla[key].fila),"columna":str(tablaActual.tabla[key].columna),"ambito":"global"  }
                
                elif str(tablaActual.tabla[key].tipo)=="1":
                    ASH = {"tipo":"struct mutable","nombre":str(tablaActual.tabla[key].id),"fila":str(tablaActual.tabla[key].fila),"columna":str(tablaActual.tabla[key].columna),"ambito":"global"  }
                
                else:
                    ASH = {"tipo":str(tablaActual.tabla[key].tipo),"nombre":str(tablaActual.tabla[key].id),"fila":str(tablaActual.tabla[key].fila),"columna":str(tablaActual.tabla[key].columna),"ambito":"global"  }
                self.TablaSimbolosREPORT.append(ASH)
                print(str(ASH)+"")
                    
            tablaActual = tablaActual.anterior 


        print(str(len(self.TablaSimbolosREPORT)))


        self.C3D = self.generator.getCodigo()




    def Mirilla(self,entrada):
        instructions = parseOP(entrada) 
        if instructions!=None:       
            instructions.Mirilla()
            out = instructions.getCode()
            self.ErroresMirilla = instructions.ReporteMirillaFull
            
            #aqui va el reset de ese array de errores sino se acumulan creo >:v

        print("OPTIMIZACION MIRILLA FINISH..........")
        #print(out)
        #f2222 = open("./salidaOptimizada.txt","w")
        #f2222.write(out)
        #f2222.close()
        self.OptimizacionMirilla=out
        