#saltos
#from ast import literal_eval
from optimizacion.Expresiones.expresion import Expresion
from optimizacion.Expresiones.literal import Literal
from optimizacion.Instrucciones.asignacion import Asignacion
from optimizacion.Instrucciones.label import Label
from optimizacion.bloque import Bloque
from optimizacion.gotos.goto import Goto
from optimizacion.gotos.iff import If

class Optimizador:
    def __init__(self,packages,temps,code):
        self.packages = packages
        self.temps = temps
        self.code = code
        self.labelBlindados={}
        self.gotoSueltos={}
        self.ReporteMirilla=[]#reporte de optimizaciones por mirilla
        self.ReporteBloques=[]#reporte de optimizaciones por bloques
        
    def getReporte(self):
        return self.ReporteMirilla
    
    def getReporteBloques(self):
        return self.ReporteBloques
    
    def getCode(self):
        self.buscarGotoSueltos()
        ret = f'package main;\n\nimport (\n\t"{self.packages}"\n);\n'
        for temp in self.temps:
            ret = ret + f'var {temp}\n'
        ret = ret + '\n'
        
        for func in self.code:
            ret = ret + func.getCode() + '\n\n'
        return ret

    #*******************************************************************************************************************************        
    #***************************************************** OPTIMIZACION POR MIRILLA ************************************************
    #*******************************************************************************************************************************
    
#    def Mirilla(self):
#        for funcion in self.code:
#            tamano = 10
#         
#            #ciclo par recorrer bloque de codigo    
#            while tamano <= len(funcion.instr):
#                banderaOptimizacion=False
#
#                for i in range(10):
#                    aux = 0
#                    # este ciclo genera una pasada completa
#                    while (tamano+aux) <= len(funcion.instr):
#                        #banderaOptimizacion = banderaOptimizacion or self.Regla1(funcion.instr[0+aux:tamano+aux])1-10 2-11
#                        banderaOptimizacion = banderaOptimizacion or self.Regla3(funcion.instr[0+aux:tamano+aux])
#                        banderaOptimizacion = banderaOptimizacion or self.Regla6(funcion.instr[0+aux:tamano+aux])
#                        #banderaOptimizacion = banderaOptimizacion or self.Regla7(funcion.instr[0+aux:tamano+aux])
#                        aux = aux+1
#
#                if not banderaOptimizacion:
#                    tamano = tamano+20

    def Mirilla(self):
        self.gotoSueltos={}
        for func in self.code:
            
            self.Regla1(func.instr)#1-100#Eliminación de instrucciones redundantes de carga y almacenamiento
            self.Regla2(func.instr)#Eliminación de código inalcanzable
            ###REGLA 6 Y 7 SON SIMILARES
            self.Regla6(func.instr)#Simplificación algebraica y reducción por fuerza
            self.Regla7(func.instr)#Simplificación algebraica y reducción por fuerza
            self.Regla8(func.instr)#Simplificación algebraica y reducción por fuerza
            ###REGLA 3 NECESITA IR POST DE 7
            self.Regla3(func.instr)#Optimizaciones de flujo de control
            self.Regla4(func.instr)#Optimizaciones de flujo de control
            self.Regla5(func.instr)#Optimizaciones de flujo de control
            
    #*******************************************************************************************************************************        
    #***************************************************** REGLA_1 *****************************************************************
    #*******************************************************************************************************************************
    
    def Regla1(self,array):
        'Eliminación de instrucciones redundantes de carga y almacenamiento'
        ret = False
        for i in range(len(array)):
            actual = array[i]
            if type(actual) is Asignacion and not actual.deleted and type(actual.exp) is not Expresion: 
                if i+1 < len(array):
                    ret=self.Regla1Aux(actual,array[i+1:len(array)])
        return ret
    
    def Regla1Aux(self,anterior,array):
        ret = False
        for i in range(len(array)):
            actual=array[i]
            actual.esLider=False#**
            if type(actual) is Label and not actual.deleted:
                break
            if actual.getCode()!=anterior.getCode() and type(actual) is Asignacion and not actual.deleted and type(actual.exp) is not Expresion:
                if actual.place.getCode() == anterior.place.getCode():
                    break
                else:
                    if actual.exp.getCode()==anterior.place.getCode() and 'stack' not in actual.place.getCode() and 'stack' not in actual.exp.getCode() and 'heap' not in actual.place.getCode() and 'heap' not in actual.exp.getCode():
                        if 'stack' not in anterior.place.getCode() and 'stack' not in anterior.exp.getCode() and 'heap' not in anterior.place.getCode() and 'heap' not in anterior.exp.getCode():
                            self.ReporteMirilla.append({'regla':'Regla 1','ExpOr':str(anterior.getCode()),'ExpOp':'Exp eliminada: '+str(actual.getCode()),'fil':str(actual.line)})
                            actual.deleted=True
                            ret = True   
                           
        return ret  
    
    #*******************************************************************************************************************************        
    #***************************************************** REGLA_2 *****************************************************************
    #*******************************************************************************************************************************   
    
    def Regla2(self,array):
        'Eliminación de código inalcanzable'
        ret = False
        for i in range(len(array)):
            actual = array[i]
            actual.esLider=False#**
            if type(actual) is Goto and not actual.deleted:
                if i+1 < len(array):
                    ret=self.Regla2aux(array[i+1:len(array)])
        return ret 
    
    def Regla2aux(self,array):
        ret = False
        for i in range(len(array)):
            actual=array[i]
            actual.esLider=False#**
            if type(actual) is Label and not actual.deleted:
                break
            else:
                if not actual.deleted and type(actual) is not Goto:
                    self.ReporteMirilla.append({'regla':'Regla 2','ExpOr':str(actual.getCode()),'ExpOp':'Exp eliminada: '+str(actual.getCode()),'fil':str(actual.line)})
                    actual.deleted=True;    
                    ret = True
        return ret
             
    #*******************************************************************************************************************************        
    #***************************************************** REGLA_3 *****************************************************************
    #*******************************************************************************************************************************
    
    def Regla3(self, array):
        'Optimizaciones de flujo de control'
        # Auxiliar para verificar que la regla se implemento
        ret = False
        # Recorrer el arreglo de instrucciones C3D
        for i in range(len(array)):
            actual = array[i]
            actual.esLider=False#**
            # Si la instruccion es un If
            if type(actual) is If and not actual.deleted and i+2 < len(array) and (i-1) >= 0:
                #con anterior se recoge la instruccion previa a actual
                anterior = array[i-1]
                
                if type(anterior) is not If and not anterior.deleted:
                
                    nextIns = array[i+1]
                    # Si el siguiente es un Goto
                    if type(nextIns) is Goto and not nextIns.deleted:
                        # SE DEBE ELIMINAR i+1 e i+2. Goto LBL y LBL:
                        #if a == 10 {goto L1}
                        #goto L2
                        #L1:
                        #<instrucciones1>
                        #L2:
                        #actual.condition.getContrary()              #if a == 10 -> if a != 10
                        #actual.label = nextIns.label                #if a != 10 {goto L1} -> if a != 10 {goto L2}
                        #nextIns.deleted = True#GOTO ELIMINADO       #se elimina :goto L2
                        #validar que sea la etiqueta lv
                        flag = False
                        for j in range(len(array)):
                            j = j+(i+2)
                            if j >= len(array):
                                break
                            
                            if type(array[j]) is Label and nextIns.label == array[j].id:#para encontrar label del goto
                                flag = True#si se encuentra el label del goto se activa bandera
                                break
                            
                        if flag == True:
                            j=0+(i+2)#j=i+2
                            if j >= len(array):
                                pass
                            else:
                                if type(array[j]) is Label and actual.label == array[j].id and array[j].id not in self.labelBlindados:
                            
                            #if type(array[j]) is Label :#and not array[j].deleted:
                                #if actual.label == array[j].id:
                                    #se hace una copia antes de cambiar el condicional
                                        copiaActual = actual.getCode()
                                        #->->->->->->->->-->->->_>->->->->->->->->->->->->->
                                        actual.condition.getContrary() 
                                        self.gotoSueltos[actual.label]='goto'#diccionario de goto
                                        actual.label = nextIns.label                #if a != 10 {goto L1} -> if a != 10 {goto L2}
                                        #se hace una copia del goto antes de eliminarlo
                                        gotoCopia = nextIns.getCode()
                                        #->->->->->->->->-->->->_>->->->->->->->->->->->->->
                                        nextIns.deleted = True#GOTO ELIMINADO       #se elimina :goto L2
                                        
                                        self.ReporteMirilla.append({'regla':'Regla 3','ExpOr':str(copiaActual)+"\n"+str(gotoCopia)+"\n"+array[j].getCode(),'ExpOp':str(actual.getCode()),'fil':str(actual.line)})
                                        array[j].deleted = True#LABEL ELIMINADO   #se elimina label que sige a goto : L1
                                        ret = True
                                        #break
                                else:
                                        self.labelBlindados[actual.label]=1
            if type(actual) is If and not actual.deleted:
                self.labelBlindados[actual.label]=1        
        return ret

    #*******************************************************************************************************************************        
    #***************************************************** REGLA_4 *****************************************************************
    #*******************************************************************************************************************************
    
    def Regla4(self,array):
        'Optimizaciones de flujo de control'
        ret = False
        for i in range(len(array)):
            actual=array[i]
            actual.esLider=False#**
            if type(actual) is Goto and not actual.deleted:
                #este sirve para recorrer instrucciones hasta llegar al label
                for j in range(len(array)):
                    j=j+(i+1)
                    if j >= len(array):
                        break
                    nextInst=array[j]
                    #si es label
                    if type(nextInst) is Label and not nextInst.deleted and nextInst.id == actual.label:
                        #y si el siguiente es goto
                        if not j+1 >= len(array):
                            if type(array[j+1]) is Goto:
                                copia=actual.getCode()
                                actual.banderaGo = True
                                actual.labelAux = actual.label
                                actual.label = array[j+1].label         
                                self.ReporteMirilla.append({'regla':'Regla 4','ExpOr':str(copia),'ExpOp':str(actual.getCode()),'fil':str(actual.line)})
                                ret = True               
                                break
        return ret    
    