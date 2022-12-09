from Expresiones.identificador import Identificador
from Expresiones.primitivos import Primitivos
from Instrucciones.Continue import Continue
from Abstract.NodoAST import NodoAST
from Instrucciones.Return import Return
from Instrucciones.Break import Break
from Abstract.instruccion import instruccion
from Instrucciones.asignacion import Asignacion
from TS.Excepcion import Excepcion
from TS.Generador import Generator
from TS.Tipo import tipo
from TS.TablaSimbolo import TablaSimbolos
from TS.Simbolo import Simbolo

class FuncionSP(instruccion):
            
    def __init__(self,tipo,nombre,parametros,instrucciones,fila,columna ):
        self.tipo=tipo#valor de return de una funcion

        
        self.nombre=nombre      #self.nombre=nombre.lower()#para ayudar en las funciones
        self.parametros=parametros#es un diccionario
        self.instrucciones=instrucciones
        self.fila=fila
        self.columna=columna
        #self.tipo=None

        self.tablaSimbolosFuncion=None
        
        #return
        

        self.returnVal=None#valor por si retorna algo


    def interpretar(self, tree, table):

        nuevaTabla =TablaSimbolos(table)#creamos un nueva tabla de simbolos para este ambito creo
        self.tablaSimbolosFuncion = nuevaTabla
        for instruccion in self.instrucciones:#recorre sus instrucciones

                value=instruccion.interpretar(tree,nuevaTabla)#si hay errores los guardamos

                if isinstance(value, Excepcion):
                    tree.getExcepciones().append(value)
                    tree.updateConsola(value.toString(),1)

                if isinstance(value, Break):#en main no se pueden poner breaks asiq aqui los detectamos como error
                    error = Excepcion("Semantico","Error semantico break fuera de ciclo",instruccion.fila,instruccion.columna)
                    tree.getExcepciones().append(error)
                    tree.updateConsola(error.toString(),1)

                if isinstance(value, Continue):#en main no se pueden poner continue asiq aqui los detectamos como error
                    error = Excepcion("Semantico","Error semantico continue fuera de ciclo",instruccion.fila,instruccion.columna)
                    tree.getExcepciones().append(error)
                    tree.updateConsola(error.toString(),1)


                if isinstance(value, Return):
                    self.tipo=value.tipo#tipo de return
                    #return self.result
                    return value.result
        #tree.setTablaSimbolosGlobal(nuevaTabla)#ANEXO LAS TABLAS DE UNA FUNCION A LA GENERAL LA TABLA PRINCIPAL

        
        return None

    def tipeof(self,num):
        
        switch={

        "tipo.ENTERO":'Int64',
        "tipo.DECIMAL":'Float64',
        "tipo.BOOLEANO":'Bool',
        "tipo.CHARACTER":'Char',
        "tipo.CADENA":'String',
        "tipo.NULO":'Nothing',
        "tipo.ARREGLO":'Arreglo'

        }

        return switch.get(num,"Invalid input")

        

    def getNodo(self):
        nodo = NodoAST("FUNCION")
        nodo.agregarHijo(str(self.nombre))#PUEDE COMO NO PUEDE VENIR JAVIER
        parametros = NodoAST("PARAMETROS")
        
        #VIDEO 15 MIN 51:40
        for param in self.parametros:
            parametro = NodoAST("PARAMETRO")
            #typeParam.agregarHijo(str(self.tipeof(str(param["tipo"]))))#que salga int,string etc. no 0,1,2,ETC.
            typeParam = NodoAST(str(self.tipeof(str(param["tipo"]))))
            typeParam.agregarHijo(param["identificador"])
            
            parametro.agregarHijoNodo(typeParam)
            parametros.agregarHijoNodo(parametro)

        nodo.agregarHijoNodo(parametros)

        instrucciones = NodoAST("INSTRUCCIONES")

        for instr in self.instrucciones:
            instrucciones.agregarHijoNodo(instr.getNodo())
        nodo.agregarHijoNodo(instrucciones)
        
        return nodo






    def compilar(self, tree, table):

        genAux = Generator()
        generator = genAux.getInstance()#obtengo mi static generator
        result2 = generator.getFuncion(self.nombre)
        generator.addCommit("_________INICIO DE FUNCION_________")
        RET=False
    
        nuevaTabla =TablaSimbolos(table)#creamos un nueva tabla de simbolos para este ambito creo
        self.tablaSimbolosFuncion = nuevaTabla

                #VERFICO SI YA ANTES HABIA CONPILADO LA MISMA FUNCION
        #ESTO PARA Q EN GO NO SE REPITA LA MISMA FUNCION Y DE ERROR
        if result2 ==True:#si encontro funcion no repito
            return None

        #if len(generator.temps_backUp)>0:
        #    generator.addCommit("\n\n\nMMMMMMMMMMMMMMMMMMMMMMMMMMMM\n\n")

        generator.inFunc = True#para q la escriba en la seccion de arriba
        generator.addBeginFunc(self.nombre)


        generator.GetTemporales()


        #AQUI DEBERIA HACER EL BCKUP DE LAS Ts q llevo para asi solo tener las q genere dentro del cuerpo

        #pasada para lo demas-------------------
        for instruccion in self.instrucciones:#recorre sus instrucciones
                if isinstance(instruccion, Return):
                    break
                else:
                    value=instruccion.compilar(tree,nuevaTabla)#si hay errores los guardamos
                    if isinstance(value, Excepcion):
                        tree.getExcepciones().append(value)





        



















        #pasada para definir el return-----------------------------------------------
        for instruccion in self.instrucciones:#recorre sus instrucciones
                if isinstance(instruccion, Return):
                    #print("ARELIS ~~~~")
                    value=instruccion.compilar(tree,nuevaTabla)#si hay errores los guardamos
                    if isinstance(value, Excepcion):
                        tree.getExcepciones().append(value)

                    #por defecto en la funcion meto el return como atributo 0
                    simbolo = Simbolo("RETURN_VALOR_funcion",value.tipo,None,self.fila,self.columna,value.valor,0,(value.tipo == tipo.CADENA or value.tipo == tipo.ARREGLO))
                    resultTablaS,newt = nuevaTabla.actualizarTabla(simbolo)#lo metemos a la tabla simbolos
                    if isinstance(resultTablaS,Excepcion): return resultTablaS#por si hubo error

                    #print("TELETUBIE "+str(newt.valor))
                    RET=True
                    self.tipo=value.tipo#tipo de return
                    break

        generator.addCommit("FIN DE FUNCION:"+self.nombre)
        generator.addEndFunc()
        
        generator.inFunc = False

        if generator.parImpar==True:
            generator.parImpar=False
            #funcion = generator.ambito2
            #if not isinstance(funcion,str) and not isinstance(funcion,Excepcion):
            #    value = funcion.compilar(tree, table)#ejecutar la funcion; enviamos la nueva tabla a la funcion para q no se pierdan los datos
            #    if isinstance(value, Excepcion):return value
            generator.ambito=""

        
        




        generator.GetTemporalesAgain()

        return RET














#[VIDEO 10]-------------------------------------------
#min 4 video para saber guardar funciones
#min 48 video para saber llamarlas
#-----------------------------------------------------

#video 11 ya hago lo de params






            