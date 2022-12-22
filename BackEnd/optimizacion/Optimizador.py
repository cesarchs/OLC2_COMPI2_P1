#saltos
#from ast import literal_eval
from optimizacion.Expresiones.Expresiones import Expresion
from optimizacion.Expresiones.Literal import Literal
from optimizacion.Instrucciones.asignacion import Asignacion
from optimizacion.Instrucciones.label import Label
from optimizacion.bloque import Bloque
from optimizacion.Gotos.Goto import Goto
from optimizacion.Gotos.If import If

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

  #*******************************************************************************************************************************        
    #***************************************************** REGLA_5 *****************************************************************
    #*******************************************************************************************************************************  
    
    def Regla5(self,array):
        'Optimizaciones de flujo de control'
        ret = False
        for i in range(len(array)):
            actual = array[i]
            actual.esLider=False#**
            if type(actual) is If and not actual.deleted:
                if i+1 < len(array):
                    ret=self.Regla5aux(actual,array[i+1:len(array)])
        return ret
    
    def Regla5aux(self,anterior,array):
        ret = False
        for i in range(len(array)):
            actual=array[i]
            actual.esLider=False#**
            if type(actual) is Label and not actual.deleted and actual.id==anterior.label:
                if not i+1 >= len(array):
                    if type(array[i+1]) is Goto:
                        #se genera copia de original
                        copia = anterior.getCode()
                        #->->->->->->->->->->->->->->
                        array[i+1].banderaGo = True
                        array[i+1].labelAux = anterior.label
                        anterior.label = array[i+1].label
                        self.ReporteMirilla.append({'regla':'Regla 5','ExpOr':str(copia),'ExpOp':str(anterior.getCode()),'fil':str(actual.line)})
                        ret = True
                        break
        return ret
        
    
    #*******************************************************************************************************************************        
    #***************************************************** REGLA_6 *****************************************************************
    #*******************************************************************************************************************************       
    
    def Regla6(self, array):
        'Simplificación algebraica y reducción por fuerza'
        ret = False
        # Recorrer el arreglo de instrucciones C3D
        for i in range(len(array)):
            actual = array[i]
            actual.esLider=False#**
            # Si la instruccion es una Asignacion
            if type(actual) is Asignacion and not actual.deleted:
                # Si se esta asignando a si mismo
                if type(actual.exp) is Expresion:
                    if(actual.selfAssignment()):
                    
                        actualOpt = actual.exp.neutralOps()
                        if actualOpt:
                            self.ReporteMirilla.append({'regla':'Regla 6','ExpOr':str(actual.getCode()),'ExpOp':'instruccion eliminada: '+str(actual.getCode()),'fil':str(actual.line)})
                            ret = True
                            actual.deleted = True
        return ret#ef Regla6(self,array):
    
    #*******************************************************************************************************************************        
    #***************************************************** REGLA_7 *****************************************************************
    #*******************************************************************************************************************************
    
    def Regla7(self, array):
        'Simplificación algebraica y reducción por fuerza'
        ret = False

        # Recorrer el arreglo de instrucciones C3D
        for i in range(len(array)):
            actual = array[i]
            actual.esLider=False#**
            # Si la instruccion es una Asignacion
            if type(actual) is Asignacion and not actual.deleted:
                if type(actual.exp) is Expresion:
                    if actual.validarRegla7():
                        #copia de actual antes de quitar ops
                        copia = actual.getCode()
                        actualOpt = actual.exp.OperandoOperador()
                        if actualOpt:
                            self.ReporteMirilla.append({'regla':'Regla 7','ExpOr':str(copia),'ExpOp':str(actual.getCode()),'fil':str(actual.line)})
                            ret = True
                            #actual.deleted = True
        return ret#ef Regla6(self,array):
    
    #*******************************************************************************************************************************        
    #***************************************************** REGLA_8 *****************************************************************
    #*******************************************************************************************************************************
    def Regla8(self, array):
        'Simplificación algebraica y reducción por fuerza'
        ret = False
        # Recorrer el arreglo de instrucciones C3D
        for i in range(len(array)):
            actual = array[i]
            actual.esLider=False#**
            # Si la instruccion es una Asignacion
            if type(actual) is Asignacion and not actual.deleted:
                flagReportar=False
                copia = actual.getCode()
                if type(actual.exp) is Expresion:
                    #x=y*0
                    if (actual.exp.left.getCode() == '0' and type(actual.exp.right) is Literal) or (type(actual.exp.left) is Literal and actual.exp.right.getCode() == '0'):
                        if actual.exp.typeOp == '*':
                            actual.exp.left = Literal('0',actual.line,actual.column)
                            actual.exp.right= Literal('',actual.line,actual.column)
                            actual.exp.typeOp = ''
                            flagReportar = True
                        #x=0/y
                        elif (actual.exp.left.getCode()=='0' and type(actual.exp.right) is Literal):
                            if actual.exp.typeOp == '/':
                                actual.exp.left = Literal('0',actual.line,actual.column)
                                actual.exp.right= Literal('',actual.line,actual.column)
                                actual.exp.typeOp = ''
                                flagReportar = True
                    #x=y*2
                    elif (actual.exp.left.getCode() == '2' and type(actual.exp.right) is Literal):
                        if actual.exp.typeOp == '*':
                            actual.exp.left = actual.exp.right 
                            actual.exp.typeOp = '+'
                            flagReportar = True
                    elif (type(actual.exp.left) is Literal and actual.exp.right.getCode() == '2'):
                        if actual.exp.typeOp == '*':
                            actual.exp.right = actual.exp.left 
                            actual.exp.typeOp = '+'
                            flagReportar = True
                if flagReportar:
                    self.ReporteMirilla.append({'regla':'Regla 8','ExpOr':str(copia),'ExpOp':str(actual.getCode()),'fil':str(actual.line)})
                    flagReportar=False
                    ret = True
        return ret
    
    def buscarGotoSueltos(self):
        'metodo para eliminar gotos de bools'
        for func in self.code:
            for goto in func.instr:
                if type(goto) is Goto:
                    if goto.label in self.gotoSueltos:
                        goto.deleted=True

    #*******************************************************************************************************************************        
    #***************************************************** OPTIMIZACION POR BLOQUES *****************************************************************
    #*******************************************************************************************************************************
    def Bloques(self):
        self.Lbloques=[]
        self.CrearBloques()
        for bloquesfunc in self.Lbloques:
            for bloque in bloquesfunc:
                self.Regla1Block(bloque.codigo)
        #while o for para aplicar reglas
        
        
        
        
        
    
    def CrearBloques(self):
        self.getLideres()#crea los lideres del bloque
        self.getBloques()#crea los lideres del bloque
        self.unirBloques()
    
    def getLideres(self):
        for funcion in self.code:
            #la primera cuadrupa es un lider
            funcion.instr[0].esLider = True
            ##el siguiente a un goto es lider
            bandera = False#bandera para una nueva funcion se coloca falsa
            for instruccion in funcion.instr:
                if bandera:#si la bandera es true se agrega lider
                    instruccion.esLider = True
                    bandera = False#se regresa a estado original hasta encontrar otro lider 
                if type(instruccion) is Goto or type(instruccion) is If:
                    bandera = True
                #las labels se dejan defaul como lider true
                #para cumplir la regla 
    
    def getBloques(self):
        for funcion in self.code:
            #creacion bloque de funcion
            bloques = []
            bloque = None #validador de bloque existente
            for instruccion in funcion.instr:
                if instruccion.esLider:
                    #si ya existe bloque solo se agrega
                    if bloque != None:
                        bloques.append(bloque)
                    bloque = Bloque(instruccion)
                bloque.codigo.append(instruccion)
            bloques.append(bloque)
            self.Lbloques.append(bloques)#se almacena cada bloque en la lista de bloques
    
    def unirBloques(self):
        #para almacenar lo de cada funcion que trae el c3d
        for funcion in self.Lbloques:
            bloqueanterior = None
            for bloque in funcion:
                if bloqueanterior == None:
                    bloqueanterior = bloque
                    continue
                bloqueanterior.siguientes.append(bloque)
                bloqueanterior = bloque
            
        for bloque in funcion:
            ultimaInstruccion = bloque.codigo[len(bloque.codigo)-1]
            if type(ultimaInstruccion) is Goto or type(ultimaInstruccion) is If:
                label = ultimaInstruccion.label
                
                for val in funcion:
                    if type(val.primertupla) is Label and val.primertupla.id == label:
                        bloque.siguientes.append(val)
                        break
        

    def Regla1Block(self,bloque):
        'Optimizaciones de flujo de control'
        ret = False
        for i in range(len(bloque)):
            actual = bloque[i]
            if type(actual) is Asignacion and actual.opt == False and 'stack' not in  actual.place.getCode() and 'heap' not in  actual.place.getCode() and 'stack' not in  actual.exp.getCode() and 'heap' not in  actual.exp.getCode():
                for j in range(len(bloque)):
                    j=j+(i+1)
                    if j >= len(bloque):
                        break
                    siguiente = bloque[j]
                    if type(siguiente) is Asignacion and siguiente.opt == False and 'stack' not in  siguiente.place.getCode() and 'heap' not in  siguiente.place.getCode() and 'stack' not in  siguiente.exp.getCode() and 'heap' not in siguiente.exp.getCode():
                        if type(siguiente.exp) is Expresion:
                            if actual.place.getCode() != siguiente.place.getCode() and actual.place.getCode() != siguiente.exp.left.getCode() and actual.place.getCode() != siguiente.exp.right.getCode():
                                if actual.exp.getCode() == siguiente.exp.getCode():
                                    copia=siguiente.getCode()
                                    siguiente.exp.left= Literal(actual.place.getCode(),siguiente.line,siguiente.column)
                                    siguiente.exp.right = Literal('',siguiente.line,siguiente.column)
                                    siguiente.exp.typeOp=''
                                    siguiente.opt = True
                                    self.ReporteBloques.append({'regla':'Regla 1','ExpOr':str(copia),'ExpOp':str(siguiente.getCode()),'fil':str(siguiente.line)})
                            else:
                                if actual.place.getCode() != siguiente.place.getCode() and actual.place.getCode() != siguiente.exp.getCode() :
                                    siguiente.exp= Literal(actual.place.getCode(),siguiente.line,siguiente.column)
                                
                                