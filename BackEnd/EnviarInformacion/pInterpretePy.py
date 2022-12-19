import gramatica as gramatic
from almacenar.arbol import Arbol
from almacenar.ts import TablaSimbolos
from almacenar.error import Error
from almacenar.tipo import Tipo
from almacenar.generador import Generador
from padres.Nodo import NodoArbol
from EnviarInformacion.enviar import Informacion
from instrucciones.funcs import Funcion
from instrucciones.structss import NuevoStruct
from instrucciones.breeak import Break
from instrucciones.continuar import Continue
from instrucciones.retorn import Retorno
import time
#import gramatica as gramatic
#from   almacenar.arbol import Arbol
#from   almacenar.ts import TablaSimbolos
#from   almacenar.error import Error
#from   padres.Nodo import NodoArbol
#from   EnviarInformacion.enviar import Informacion
import os


class Analisis:
    def __init__(self):
        self.input = None
        self.instrucciones = None

    def principal(self, entrada):
        #print(entrada)
        genAux = Generador()
        genAux.limpiarTodo()
        generator = genAux.getInstance()
        e = str(entrada)
        e+='\n'
        # Aqui obtengo todos los objetos creados en el recorrido de la entrada vs gramtica
        self.instrucciones = gramatic.parse(e)
        # Creo arbol con la lista de instrucciones
        self.ast = Arbol(self.instrucciones)
        self.TsGlobal = TablaSimbolos(None)  # Creo una nueva tabla de símbolos global
        # Le añado la tabla de simbolos a el árbol creado.
        self.ast.setTsGlobal(self.TsGlobal)
        #AGREGO NATIVAS:
        #gramatic.getNativas(self.ast)
        # err lex y sin
        for error in gramatic.ListaErrores:  # para cada error en la lista de errores
            # lo agrego en la lista de errores del arbol
            self.ast.getListaErrores().append(error)
            # actualizo consola con error
            self.ast.actualizarConsola(error.toString())
# semant
        try:
            for instruccion in self.ast.getInstrucciones():  # realizar acciones #Para cada instruccion en arbol
                if isinstance(instruccion,Funcion):
                    resuladdFunc=instruccion.compilar(self.ast, self.TsGlobal)
                    if isinstance(resuladdFunc,Error):
                        self.ast.getListaErrores().append(resuladdFunc)
                        self.ast.actualizarConsola(resuladdFunc.toString())
                        
                    resuladdFunc=self.ast.agregarFuncs(instruccion)
                    if isinstance(resuladdFunc,Error):
                        self.ast.getListaErrores().append(resuladdFunc)
                        self.ast.actualizarConsola(resuladdFunc.toString())
                #if isinstance(instruccion,NuevoStruct):
                #    resuladdstruct=self.ast.agregarStruct(instruccion)
                #    if isinstance(resuladdstruct,Error):
                #        self.ast.getListaErrores().append(resuladdstruct)
                #        self.ast.actualizarConsola(resuladdstruct.toString())
                #    continue
                #retornoInstruccion = instruccion.ejecutar(self.ast, self.TsGlobal)
                #if isinstance(retornoInstruccion, Error):
                #    self.ast.getListaErrores().append(retornoInstruccion)
                #    self.ast.actualizarConsola(retornoInstruccion.toString())
                #if isinstance(retornoInstruccion,Break):
                #    repor=Error("SEMANTICO","INSTRUCCION BREAK FUERA DE LOOP",retornoInstruccion.fila,retornoInstruccion.columna)#///
                #    self.ast.getListaErrores().append(repor)#///
                #    self.ast.actualizarConsola(repor.toString())#///
                #if isinstance(retornoInstruccion,Continue):
                #    repor=Error("SEMANTICO","INSTRUCCION CONTINUE FUERA DE LOOP",retornoInstruccion.fila,retornoInstruccion.columna)#///
                #    self.ast.getListaErrores().append(repor)#///
                #    self.ast.actualizarConsola(repor.toString())#///
                #if isinstance(retornoInstruccion,Retorno):
                #    repor=Error("SEMANTICO","INSTRUCCION RETORNO FUERA DE FUNC",retornoInstruccion.fila,retornoInstruccion.columna)#///
                #    self.ast.getListaErrores().append(repor)#///
                #    self.ast.actualizarConsola(repor.toString())#///

            #print(self.ast.getFuncs())
            #print(self.ast.getConsola())
            for instruccion in self.ast.getInstrucciones():
                if isinstance(instruccion,NuevoStruct):
                    resuladdstruct=self.ast.agregarStruct(instruccion)
                    if isinstance(resuladdstruct,Error):
                        self.ast.getListaErrores().append(resuladdstruct)
                        self.ast.actualizarConsola(resuladdstruct.toString())
                    continue
                retornoInstruccion = instruccion.compilar(self.ast, self.TsGlobal)
                if isinstance(retornoInstruccion, Error):
                    self.ast.getListaErrores().append(retornoInstruccion)
                    self.ast.actualizarConsola(retornoInstruccion.toString())
                if isinstance(retornoInstruccion,Break):
                    repor=Error("SEMANTICO","INSTRUCCION BREAK FUERA DE LOOP",retornoInstruccion.fila,retornoInstruccion.columna)#///
                    self.ast.getListaErrores().append(repor)#///
                    self.ast.actualizarConsola(repor.toString())#///
                if isinstance(retornoInstruccion,Continue):
                    repor=Error("SEMANTICO","INSTRUCCION CONTINUE FUERA DE LOOP",retornoInstruccion.fila,retornoInstruccion.columna)#///
                    self.ast.getListaErrores().append(repor)#///
                    self.ast.actualizarConsola(repor.toString())#///
                if isinstance(retornoInstruccion,Retorno):
                    repor=Error("SEMANTICO","INSTRUCCION RETORNO FUERA DE FUNC",retornoInstruccion.fila,retornoInstruccion.columna)#///
                    self.ast.getListaErrores().append(repor)#///
                    self.ast.actualizarConsola(repor.toString())#///

            self.inicio = NodoArbol("INICIO")
            self.instrucs = NodoArbol("INSTRUCCIONES")

            for instruccion in self.ast.getInstrucciones():
                self.instrucs.agregarHijoConNodo(instruccion.getNode())

            self.inicio.agregarHijoConNodo(self.instrucs)
            grafo = self.ast.getDot(self.inicio)
            #self.generarDot(grafo)
            ts = self.reporteTs(self.ast,self.TsGlobal)
            lerror = self.reporteErrores(self.ast)
            enviar=Informacion(self.ast.getConsola(),generator.getCode(),grafo)
            #si existen variables en la TS agrego 
            if ts:
                enviar.setTs(ts)
            if lerror:
                enviar.setlError(lerror)
            #envio objeto
            return enviar
        except Exception as e:
            print(e)
            print("Error al ejecutar instrucciones")
            enviar = Informacion('ERROR AL EJECUTAR INSTRUCCIONES, VERIFIQUE SINTAXIS EN ENTRADA \n ERROR: '+str(e),'error','digraph{PYTHON->PyToPy}')
            return enviar


    def generarDot(self, t):
        if len(t) != 0:
            with open('arbol.txt', "w", encoding="utf-8") as f:
                f.write(t)
                os.system("dot -Tpng arbol.txt -o arbol.png")
                return t
        else:
            with open('reporteAST.dot', "w") as f:
                f.write('digraph G {\"No hay instrucciones\"}')
            return ""

    def reporteTs(self,arbol, tablaGlobal):
        reporte = []
        contador = 0
        arbol.ListaTablas.insert(0, ('GLOBAL', tablaGlobal))
        try:
            for tabla in arbol.getListaTablas():
                #print("aqui"+tabla[0])
                ambito=tabla[0]
                simbolos=tabla[1].getSimbolos()
                for simbolo in simbolos:
                    if simbolos[simbolo].getTipo()==Tipo.STRUCT:
                        valorret=self.desempaquetarvalor(simbolos[simbolo].getValor())
                        reporte.append({'no':str(contador),'id':str(simbolos[simbolo].getId()),'tipo':str(simbolos[simbolo].getTipo()),'ambito':ambito,'valor':str(valorret),'fil':str(simbolos[simbolo].getFil()),'col':str(simbolos[simbolo].getCol())})    
                    else:
                        reporte.append({'no':str(contador),'id':str(simbolos[simbolo].getId()),'tipo':str(simbolos[simbolo].getTipo()),'ambito':ambito,'params':'','posicion':str(simbolos[simbolo].getPosicion()),'fil':str(simbolos[simbolo].getFil()),'col':str(simbolos[simbolo].getCol())})
                    contador += 1
            for clave in arbol.getFuncs():
                #print("error aqui")
                if clave == 'uppercase' or clave == 'lowercase' or clave == 'float' or clave == 'string' or clave == 'typeof' or clave == 'sin' or clave == 'cos' or clave == 'tan' or clave == 'sqrt' or clave == 'pop!': continue
                valor = arbol.getFuncs()[clave]
                if isinstance(valor,Funcion):
                    parametros="SIN PARAMETROS"
                    if valor.parametros: 
                        parametros=str(valor.parametros)
                    reporte.append({'no':str(contador),'id':str(clave),'tipo':'FUNCION','ambito':'GLOBAL','params':'PARAMETROS: '+parametros,'posicion':'','fil':str(valor.fila),'col':str(valor.columna)}) 
                else:
                    reporte.append({'no':str(contador),'id':str(clave),'tipo':'FUNCION','ambito':'GLOBAL','params':'str()','posicion':'','fil':'','col':''})
                contador += 1
            
            if arbol.getStructs():
                diccionarioStrucds = arbol.getStructs()
                for clave in diccionarioStrucds:
                    valor=diccionarioStrucds[clave]
                    if isinstance(valor,NuevoStruct):
                        atributos='atributos: '
                        mutable=''
                        for atributo in valor.atributos:
                            atributos+='ID: ' +str(atributo.id)+' '+str(atributo.tipo)
                            if atributo != valor.atributos[-1]: atributos+=' , '
                        if valor.mutable == True:
                            mutable='mutable'
                        reporte.append({'no':str(contador),'id':str(clave),'tipo':'STRUCT '+mutable,'ambito':'GLOBAL','valor':atributos,'fil':str(valor.fila),'col':str(valor.columna)})
                    else:pass
                contador+=1
            #print(reporte)
            return reporte
        except:            
            return None



    def reporteErrores(self,arbol):
        ahora = time.strftime("%c")
        contador=0
        lisErrores=[]
        try:
            for error in arbol.getListaErrores():
                lisErrores.append({'no':str(contador),'tipo':str(error.getTipo()),'des':str(error.getDescripcion()),'fil':str(error.getFila()),'col':str(error.getCol()),'fecha':str(ahora)})
                contador+=1
            return lisErrores
        except:
            return None
    
    def desempaquetarvalor(self,diccionario):
        valor =""
        tamano=1
        valor=str(diccionario['##_nombre_padre_struct_##']['id'])+"("
        for key in diccionario:
            tamano+=1
            if  key != '##_nombre_padre_struct_##':
                if isinstance(diccionario[key]['valor'],dict):
                    valor+= self.desempaquetarvalor(diccionario[key]['valor'])
                else:
                    if diccionario[key]['valor']==None:
                        valor+='nothing'
                    else:
                        valor += str(diccionario[key]['valor'])
                    if tamano <= len(diccionario):valor += ','
        valor+=")"
        return valor
    
    
    # def enviarInformacion(self,consola,arbol):
    #    return Informacion(consola,arbol)
