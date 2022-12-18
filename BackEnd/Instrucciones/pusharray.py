from padres.instruccion import Instruccion
from padres.Nodo import NodoArbol
from almacenar.error import Error
from almacenar.tipo import Tipo

#from padres.instruccion import Instruccion
#from padres.Nodo import NodoArbol
#from almacenar.error import Error
#from almacenar.tipo import Tipo
import copy
class EmpujarArrayExp(Instruccion):
    def __init__(self, id,exps,fila, columna):
        self.identificador = id
        self.expresion=exps
        self.fila=fila
        self.columna=columna
    
    def compilar(self,arbol,tabla):
        #print("")
        self.valorpush=self.expresion.ejecutar(arbol,tabla)
        if isinstance(self.valorpush,Error):return self.valorpush
        
        #busco que el arreglo al que se le quiere hacer push exista
        arraysimbolo=tabla.getSimboloEnTs(self.identificador)
        if arraysimbolo == None:
            return Error("SEMANTICO","ARREGLO: "+self.identificador+ " NO ESTA DECLARADO",self.fila,self.columna)
        
        if not arraysimbolo.getArreglo():
            return Error("SEMANTICO", "ETIQUETA: "+self.identificador+" no es un arreglo",self.fila,self.columna)
        
        try:
            arraysimbolo.getValor().append(self.valorpush)
        except:
            return Error("SEMANTICO","NO SE PUEDE HACER PUSH A: "+self.identificador,self.fila,self.columna)
        print("")
        
    
    def getNode(self):
        nodoModArr= NodoArbol("PUSH_ARRAY")
        nodoModArr.agregarHijoSinNodo(str(self.identificador))
        nodoModArr.agregarHijoSinNodo(",")
        nodoModArr.agregarHijoSinNodo(str(self.valorpush))
        return nodoModArr


class EmpujarArray(Instruccion):
    def __init__(self, id,exps,fila, columna):
        self.identificador = id
        self.expresiones=exps
        self.fila=fila
        self.columna=columna
    
    def compilar(self,arbol,tabla):
        print("")
        self.valorpush=self.obtenerExp(self.expresiones,arbol,tabla)
        if isinstance(self.valorpush,Error):return self.valorpush
        
        #busco que el arreglo al que se le quiere hacer push exista
        arraysimbolo=tabla.getSimboloEnTs(self.identificador)
        if arraysimbolo == None:
            return Error("SEMANTICO","ARREGLO: "+self.identificador+ " NO ESTA DECLARADO",self.fila,self.columna)
        
        if not arraysimbolo.getArreglo():
            return Error("SEMANTICO", "ETIQUETA: "+self.identificador+" no es un arreglo",self.fila,self.columna)
        
        try:
            arraysimbolo.getValor().append(self.valorpush)
        except:
            return Error("SEMANTICO","NO SE PUEDE HACER PUSH A: "+self.identificador,self.fila,self.columna)
        #print("")
        
    
    def getNode(self):
        nodoModArr= NodoArbol("PUSH_ARRAY")
        nodoModArr.agregarHijoSinNodo(str(self.identificador))
        nodoModArr.agregarHijoSinNodo(",")
        nodoModArr.agregarHijoSinNodo(str(self.valorpush))
        return nodoModArr
    
    def obtenerExp(self,lista,arbol,tabla):
        lista_resul = []  # Lista que contendrea los resultados.
        for exp in lista:
            if isinstance(exp, list):  # Encontro una lista entre los itemas de la lista.
                lista_resul.append(self.obtenerExp(exp,arbol,tabla))  # lista_resul.append(otra lista), [5+8, False, True] -> [5+8, False, True, [[9*8, b]]]
            else:  # El item No es una lista.
                resExp = exp.ejecutar(arbol, tabla)
                if isinstance(resExp, Error):  # Es error, lo retornas. (Esto no se como funciona.)
                    return resExp
                else:  # exp, aqui puede ser Id, aritmetica, primitiva bool, etc. Ej: [] -> [5+8] -> [5+8, False] -> [5+8, False, True]; [] -> [9*8, b]
                    lista_resul.append(resExp) # lista_resul.apend(5+8), lista_resul.apend(True), etc.
        return lista_resul  # Retornas la lista actual con todas sus expresiones.
    
    
    
class EmpujarArrayD(Instruccion):
    def __init__(self, id,corch,exps,fila, columna):
        self.identificador = id
        self.corchetesexps = corch
        self.expresiones=exps
        self.fila=fila
        self.columna=columna
    
    def compilar(self,arbol,tabla):
       # print("")
        self.valorpush=self.obtenerExp(self.expresiones,arbol,tabla)
        if isinstance(self.valorpush,Error):return self.valorpush
        
        #busco que el arreglo al que se le quiere hacer push exista
        arraysimbolo=tabla.getSimboloEnTs(self.identificador)
        if arraysimbolo == None:
            return Error("SEMANTICO","ARREGLO: "+self.identificador+ " NO ESTA DECLARADO",self.fila,self.columna)
        
        if not arraysimbolo.getArreglo():
            return Error("SEMANTICO", "ETIQUETA: "+self.identificador+" no es un arreglo",self.fila,self.columna)
        

        #BUSQUEDA DE POSICION EN ARREGLO
        self.bandera=False
        valorasig = self.buscarCambiardimension(arbol,tabla,copy.copy(self.corchetesexps),arraysimbolo.getValor(),self.valorpush)
        if isinstance(valorasig,Error):return valorasig
        return valorasig
    
    def getNode(self):
        nodoModArr= NodoArbol("PUSH_ARRAY")
        nodoModArr.agregarHijoSinNodo(str(self.identificador))
        nodoModArr.agregarHijoSinNodo(",")
        nodoModArr.agregarHijoSinNodo(str(self.valorpush))
        return nodoModArr
    
    
    def buscarCambiardimension(self,arbol,tabla,expresiones,arreglo,valor):
        if len(expresiones) == 0:#si ya se obtuvo todo lo que venia en el acceso a arreglo -> push!(array[expresion])
            if isinstance(arreglo,list) and not isinstance(valor,list):
                return Error("SEMANTICO", "MODIFICACION A ARREGLO INCOMPLETO", self.fila, self.columna)
            else:
                self.bandera=True
            return valor
        
        if not isinstance(arreglo,list):
            return Error("SEMANTICO", "POSICION A ACCEDER NO EXISTE", self.fila,self.columna)
        dimension=expresiones.pop(0)
        num = dimension.ejecutar(arbol,tabla)#aqui puede devolver en valor un primitivo o un array
        if isinstance(num, Error): return num
        if num <=0: return Error("SEMANTICO", "POSICION A ACCEDER NO EXISTE", self.fila,self.columna)
        if dimension.tipo != Tipo.ENTERO:
            return Error("SEMANTICO","EXPRESION DEBE DE SER ENTERO PARA POSICION DE ARREGLO",self.fila,self.columna)
        try:
            value = self.buscarCambiardimension(arbol,tabla,copy.copy(expresiones),arreglo[num-1],valor)
        except:
            return Error("SEMANTICO", "POSICION A ACCEDER NO EXISTE", self.fila,self.columna)
        if isinstance(value, Error): return value
        if value != None and self.bandera==False:
            try:
                arreglo[num-1]= value
            except:
                return Error("SEMANTICO","NO SE PUEDE HACER PUSH EN ESTA POSICION,ESTA EXPRESION",self.fila,self.columna)
        elif value != None and self.bandera == True:
            try:
                arreglo[num-1].append(value)
            except:
                return Error("SEMANTICO","NO SE PUEDE HACER PUSH EN ESTA POSICION,ESTA EXPRESION!",self.fila,self.columna)
        return None
    
    def obtenerExp(self,lista,arbol,tabla):
        lista_resul = []  # Lista que contendrea los resultados.
        for exp in lista:
            if isinstance(exp, list):  # Encontro una lista entre los itemas de la lista.
                lista_resul.append(self.obtenerExp(exp,arbol,tabla))  # lista_resul.append(otra lista), [5+8, False, True] -> [5+8, False, True, [[9*8, b]]]
            else:  # El item No es una lista.
                resExp = exp.ejecutar(arbol, tabla)
                if isinstance(resExp, Error):  # Es error, lo retornas. (Esto no se como funciona.)
                    return resExp
                else:  # exp, aqui puede ser Id, aritmetica, primitiva bool, etc. Ej: [] -> [5+8] -> [5+8, False] -> [5+8, False, True]; [] -> [9*8, b]
                    lista_resul.append(resExp) # lista_resul.apend(5+8), lista_resul.apend(True), etc.
        return lista_resul  # Retornas la lista actual con todas sus expresiones.
