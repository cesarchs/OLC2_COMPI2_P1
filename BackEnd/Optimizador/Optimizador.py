# INSTRUCCIONES GENERALES
from Optimizador.Instrucciones.Asignacion import *
from Optimizador.Instrucciones.LlamadaFuncion import *
from Optimizador.Instrucciones.Funcion import *
from Optimizador.Instrucciones.Label import *
from Optimizador.Instrucciones.Print import *
from Optimizador.Instrucciones.Return import *

# INSTRUCCIONES DE CAMBIO DE FLUJO
from Optimizador.Gotos.If import *
from Optimizador.Gotos.Goto   import *

# INSTRUCCIONES DE EXPRESION
from Optimizador.Expresiones.Acceso import *
from Optimizador.Expresiones.Expresiones import *
from Optimizador.Expresiones.Literal import *

class Optimizador:
    def __init__(self, packages, temps, code):
        self.packages = packages
        self.temps = temps
        self.code = code
        self.LabelABorrar={}
        self.FR3={}#para regla 3 solo xd

        self.banR3={}#para regla 3 solo xd

        '''self.ReporteR1=[]#solo por ahora para ver como se comporta todo, para luego unirlo todo en ReporteMirillaFull
        self.ReporteR2=[]
        self.ReporteR3=[]
        self.ReporteR4=[]
        self.ReporteR5=[]
        self.ReporteR6=[]
        self.ReporteR7=[]
        self.ReporteR8=[]'''


        self.ReporteMirillaFull=[]#usar solo este y descartar los demas para q vaya todo en uno
    
    def getCode(self):
        print("LISTA DE gotos Ls a borrar:\n"+str(self.LabelABorrar))
        self.borrarLabelsSueltas()#para q borre las Ls sueltas por regla 3
        self.LabelABorrar={}
        self.FR3={}
        print("label intocables:")
        print(str(self.banR3))
        self.banR3={}

        print("REPORTE INFORMACION DE BORRADOS:\n"+str(self.ReporteMirillaFull))

        '''print("REPORTE 1 INFORMACION DE BORRADOS:\n"+str(self.ReporteR1))
        print("REPORTE 2 INFORMACION DE BORRADOS:\n"+str(self.ReporteR2))
        print("REPORTE 3 INFORMACION DE BORRADOS:\n"+str(self.ReporteR3))
        print("REPORTE 4 INFORMACION DE BORRADOS:\n"+str(self.ReporteR4))
        print("REPORTE 5 INFORMACION DE BORRADOS:\n"+str(self.ReporteR5))
        print("REPORTE 6 INFORMACION DE BORRADOS:\n"+str(self.ReporteR6))
        print("REPORTE 7 INFORMACION DE BORRADOS:\n"+str(self.ReporteR7))
        print("REPORTE 8 INFORMACION DE BORRADOS:\n"+str(self.ReporteR8))'''

        ret = f'package main;\n\nimport (\n\t"{self.packages}"\n);\n'
        for temp in self.temps:
            ret = ret + f'var {temp}\n'
        ret = ret + '\n'
        
        for func in self.code:
            ret = ret + func.getCode() + '\n\n'
        return ret
    
    def Mirilla(self):
        
        self.ReporteMirillaFull=[]#reset de reporte de errores

        # Por cada funcion
        for func in self.code:
            
            self.Regla1(func.instr)# no bug T2=7 xd
            self.Regla2(func.instr)#mmmm
            self.Regla6(func.instr)# esq sino va antes nunca existiria la 6 xd
            self.Regla7(func.instr)#fijo sino F con los bools
            
            self.Regla3(func.instr)#mmmm

            self.Regla4(func.instr)#
            self.Regla5(func.instr)
            self.Regla8(func.instr)
            
            
                        
                        
                

#########################################################################################################E

    def Regla1(self, array):
        ret = False

        # Recorrer el arreglo de instrucciones C3D
        for i in range(len(array)):
            actual = array[i]
            # Si la instruccion es una Asignacion
            if type(actual) is Assignment and not actual.deleted and type(actual.exp) is not Expression:
                # Si se esta asignando a si mismo
                #print("*****************"+actual.place.getCode())
                #modificado=False
                for j in range(len(array)):
                    j = j+i
                    if j >=len(array):
                        break

                    
                    if array[j].getCode() != actual.getCode() and type(array[j]) is Assignment and not array[j].deleted:
                        #print(array[j].getCode())
                        if array[j].place.getCode()==actual.place.getCode():
                            #modificado=True
                            #print("BUUUUMMMM")
                            break
                        else:
                            if array[j].exp.getCode()==actual.place.getCode() and 'stack' not in array[j].place.getCode() and 'heap' not in array[j].place.getCode() and 'stack' not in array[j].exp.getCode() and 'heap' not in array[j].exp.getCode():# and modificado==False:
                                ret = True


                                ASH = {"tipo":"Mirilla","regla":" regla 1","original":array[j].getCode(),"optimizada":"eliminada","fila":array[j].line  }
                                self.ReporteMirillaFull.append(ASH)


                                #self.ReporteR1.append(array[j].getCode()+" Stack:"+str('stack' not in array[j].place.getCode())+" Heap:"+str('heap' not in array[j].place.getCode()))
                                array[j].deleted = True
                                
                        


        return ret



#########################################################################################################E

    def Regla2(self, array):
        ret = False
        #prev=None
        # Recorrer el arreglo de instrucciones C3D
        for i in range(len(array)):
            actual = array[i]
            if type(actual) is Goto and not actual.deleted:
                # Si se esta asignando a si mismo
                #print("====="+actual.getCode())
                #modificado=False
                for j in range(len(array)):
                    j = j+i+1
                    if j >=len(array):
                        break

                    #print("mikey")
                    #print(str(array[j].getCode()))
                    if type(array[j]) is Label and not array[j].deleted:
                        #actual.deleted=True   
                        break
                    else:
                        if not array[j].deleted and type(array[j]) is not Goto:
                            ret = True

                            ASH = {"tipo":"Mirilla","regla":" regla 2","original":array[j].getCode(),"optimizada":"eliminada","fila":array[j].line  }
                            self.ReporteMirillaFull.append(ASH)

                            array[j].deleted = True              
                        

            #prev = actual
        return ret



#########################################################################################################E

    def Regla3(self, array):
        # Auxiliar para verificar que la regla se implemento
        ret = False
        # Recorrer el arreglo de instrucciones C3D
        for i in range(len(array)):
            actual = array[i]
            #print("-"+array[i].getCode())
            # Si la instruccion es un If
            

            if type(actual) is If and not actual.deleted and i+2 < len(array) and i-1>=0:
                
                anterior = array[i-1]

                if type(anterior) is not If and not anterior.deleted:
                    
                    nextIns = array[i+1]
                    # Si el siguiente es un Goto
                    if type(nextIns) is Goto and not nextIns.deleted:


                        validador=False#hallar el L del goto sino F
                        for j in range(len(array)):
                            j = j+(i+2)
                            if j >=len(array):
                                break
                            if type(array[j]) is Label and  nextIns.label == array[j].id:#and not array[j].deleted:
                                validador=True
                                break
                                  
                        if validador==True:
                        
                                #habia for pero la cagaba xd
                                j = 0+(i+2)
                                if j >=len(array):
                                    #break
                                    pass
                                else:
                                    if type(array[j]) is Label and  actual.label == array[j].id and array[j].id not in self.banR3:#and not array[j].deleted:
                                            parche = actual.getCode()
                                            if actual.condition.left.value in self.FR3:
                                                pass
                                            else:
                                                print(">>"+str(actual.condition.left.value))
                                                actual.condition.getContrary()
                                            #print(":::::"+actual.getCode())
                                            self.LabelABorrar[actual.label]=1
                                            actual.label = nextIns.label                
                                            parche2 = nextIns.getCode()
                                            nextIns.deleted = True
                                            ret = True
                                            ASH = {"tipo":"Mirilla","regla":" regla 3","original":parche+"\n"+parche2+"\n"+array[j].getCode(),"optimizada":actual.getCode(),"fila":actual.line  }
                                            self.ReporteMirillaFull.append(ASH)
                                            array[j].deleted = True#LABEL ELIMINADO   #se elimina label que sige a goto : L1
                                            #break

                                    else:
                                        #print("fff"+actual.getCode()+"    -> if goto:"+str(actual.label)+' == label(i+2):'+ str(array[j].id)+"  in diccionario? "+str((array[j].id in self.banR3)))
                                            
                                        self.banR3[actual.label]=1#no se puede eliminar sino F
                                        #print("***"+actual.label)
                                      
            if type(actual) is If and not actual.deleted:
                self.banR3[actual.label]=1#no se puede eliminar sino F

        return ret
    
#########################################################################################################E

    def Regla4(self, array):
        ret = False
        prev=None
        # Recorrer el arreglo de instrucciones C3D
        for i in range(len(array)):
            actual = array[i]
            if type(actual) is Goto and not actual.deleted:
                # Si se esta asignando a si mismo
                #print("====="+actual.getCode())
                #modificado=False
                for j in range(len(array)):
                    j = j+i+1
                    if j >=len(array):
                        break

                    #print("mikey")
                    #print(str(array[j].getCode()))
                    if type(array[j]) is Label and not array[j].deleted and array[j].id==actual.label:
                        #actual.deleted=True
                        if not j+1 >=len(array):

                            if type(array[j+1]) is Goto:
                                #print("%%%%%%%%%"+array[j+1].label)
                                parche = actual.getCode()
                                
                                actual.auxR4="\n\t"+actual.getCode()
                                actual.label = array[j+1].label

                                ASH = {"tipo":"Mirilla","regla":" regla 4","original":parche,"optimizada":actual.getCode(),"fila":actual.line  }
                                self.ReporteMirillaFull.append(ASH)


                                break 
                        
                        
                                
                        

            prev = actual
        return ret

#########################################################################################################E

    def Regla5(self, array):
        # Auxiliar para verificar que la regla se implemento
        ret = False
        # Recorrer el arreglo de instrucciones C3D
        for i in range(len(array)):
            actual = array[i]
            # Si la instruccion es un If
            if type(actual) is If and not actual.deleted:
                for j in range(len(array)):
                    j = j+i+1
                    if j >=len(array):
                        break

                    if type(array[j]) is Label and not array[j].deleted and array[j].id==actual.label:
                        #actual.deleted=True
                        if not j+1 >=len(array):

                            if type(array[j+1]) is Goto and not array[j+1].deleted:
                                #print("%%%%%%%%%"+array[j+1].label)
                                parche = actual.getCode()

                                array[j].R5="goto "+actual.label+";//para q no de clavos goolang\n\t"
                                actual.label = array[j+1].label


                                ASH = {"tipo":"Mirilla","regla":" regla 5","original":parche,"optimizada":actual.getCode(),"fila":actual.line  }
                                self.ReporteMirillaFull.append(ASH)


                                break

                

        return ret



#########################################################################################################E

    def Regla6(self, array):#aun tiene bugs al haber 1 funcion :/ como sumaSC
        ret = False

        # Recorrer el arreglo de instrucciones C3D
        for i in range(len(array)):
            actual = array[i]
            # Si la instruccion es una Asignacion
            if type(actual) is Assignment and not actual.deleted:
                # Si se esta asignando a si mismo
                if(actual.selfAssignment() and type(actual.exp) is Expression):
                    actualOpt = actual.exp.neutralOps()
                    if actualOpt:
                        ret = True
                        ASH = {"tipo":"Mirilla","regla":" regla 6","original":actual.getCode(),"optimizada":"eliminada","fila":actual.line  }
                        self.ReporteMirillaFull.append(ASH)
                        actual.deleted = True
                        
        return ret

#########################################################################################################E

    def Regla7(self, array):#aun tiene bugs al haber 1 funcion :/ como sumaSC
        ret = False
        # Recorrer el arreglo de instrucciones C3D
        for i in range(len(array)):
            actual = array[i]
            # Si la instruccion es una Asignacion
            if type(actual) is Assignment and not actual.deleted:
                # Si se esta asignando a si mismo
                if(actual.selfAssignmentR7()):
                    #print("HULK!")
                    actualOpt = actual.exp.neutralOps2()
                    if actualOpt:
                     #   print("HOGAN :/")
                        ret = True
                        parche = actual.getCode()
                        if actual.exp.left.getCode()=="0" and actual.exp.right.getCode()!="0":
                            if actual.exp.typeOp=="+":
                                actual.exp.left=actual.exp.right
                            elif actual.exp.typeOp=="-":
                                actual.exp.right.value="-"+str(actual.exp.right.value)
                                actual.exp.left=actual.exp.right
                                self.FR3[actual.place.value]=1#meto porq es negativo y no cambio signo
                                print("puta xd"+str(self.FR3))

                            
                        actual.exp.right=Literal('',actual.exp.right.line,actual.exp.right.column)
                        actual.exp.typeOp=''

                        ASH = {"tipo":"Mirilla","regla":" regla 7","original":parche,"optimizada":actual.getCode(),"fila":actual.line  }
                        self.ReporteMirillaFull.append(ASH)
                        #actual.deleted = True
        return ret

#########################################################################################################E

    def Regla8(self, array):#aun tiene bugs al haber 1 funcion :/ como sumaSC
        ret = False

        # Recorrer el arreglo de instrucciones C3D
        for i in range(len(array)):
            actual = array[i]
            # Si la instruccion es una Asignacion
            if type(actual) is Assignment and not actual.deleted:
                # Si se esta asignando a si mismo
                if(type(actual.exp) is Expression):
                    actualOpt = actual.exp.Rule8()
                    if actualOpt:
                        ret = True
                        parche = actual.getCode()
                        if actual.exp.left.getCode()=="0" and actual.exp.typeOp == '/':
                            actual.exp.typeOp =''
                            actual.exp.right=Literal('',actual.exp.right.line,actual.exp.right.column)
                        
                        elif actual.exp.right.getCode()=="0" and actual.exp.typeOp == '*':
                            actual.exp.typeOp =''
                            actual.exp.left=Literal('',actual.exp.right.line,actual.exp.right.column)
                               
                        elif actual.exp.right.getCode()=="2" and actual.exp.typeOp == '*':
                            actual.exp.typeOp ='+'
                            actual.exp.right=actual.exp.left
                             
                        #actual.exp.right=Literal('',actual.exp.right.line,actual.exp.right.column)
                        #actual.exp.typeOp=''

                        ASH = {"tipo":"Mirilla","regla":" regla 8","original":parche,"optimizada":actual.getCode(),"fila":actual.line  }
                        self.ReporteMirillaFull.append(ASH)
                        
        return ret

    def borrarLabelsSueltas(self):#pero en Gotos XD
        for func in self.code:
            for func2 in func.instr:
                if type(func2) is Goto:
                    if func2.label in self.LabelABorrar:
                        func2.deleted=True
                        #print("label:"+func2.id)
