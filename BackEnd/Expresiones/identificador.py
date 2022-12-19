from Expresiones.primitivos import Primitivos
from TS.Generador import Generator
from TS.Return2 import ReturnC3D
from TS.Tipo import tipo
from Abstract.NodoAST import NodoAST
from Abstract.instruccion import instruccion
from TS.Excepcion import Excepcion


class Identificador(instruccion):
    def __init__(self, identificador,fila,columna):
        self.identificador =identificador
        self.fila=fila
        self.columna=columna
        self.tipo=None

        self.LV=""
        self.LF=""

        
#estp es para obtener el valor de por ejemplo A que vale 4 y mostrarlo por ejemplo en print
    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador )

        if simbolo==None:
            return Excepcion("Semantico","Variable "+self.identificador+"  no encontrada en TablaSimbolos", self.fila,self.columna)

        self.tipo=simbolo.getTipo()#necesitamos no solo saber el valor sino tambien su tipo ej: 90 tipo entero

        


       
        return simbolo.getValor()



    def getNodo(self):
        nodo = NodoAST("IDENTIFICADOR")
        nodo.agregarHijo(str(self.identificador))
        return nodo





    def compilar(self, tree, table):
        genAux = Generator()
        generator = genAux.getInstance()
        generator.addCommit("Compilacion de Acceso")


        simbolo = table.getTabla(self.identificador)

        if simbolo==None:
            return Excepcion("Semantico","Variable "+self.identificador+"  no encontrada en TablaSimbolos", self.fila,self.columna)

        self.tipo=simbolo.getTipo()#necesitamos no solo saber el valor sino tambien su tipo ej: 90 tipo entero

        # Temporal para guardar variable
        temp = generator.addTemporal()

        # Obtencion de posicion de la variable
        tempPos = simbolo.size
        if(not simbolo.global1):
            tempPos = generator.addTemporal()
            generator.addExp(tempPos, 'P', simbolo.size, "+")
        generator.getStack(temp, tempPos)

        if simbolo.tipo != tipo.BOOLEANO and simbolo.tipo != tipo.NULO:
            generator.addCommit("Fin compilacion acceso")
            generator.addSaltoLinea()

            #print("=================================>"+str(simbolo.id)+"|"+str(simbolo.index))
            return ReturnC3D(temp, simbolo.tipo, True,simbolo.valor.Array,-1,simbolo.index)

        if simbolo.tipo == tipo.BOOLEANO:
            #si ya es bool entonces

            if self.LV == '':
                self.LV = generator.newLabel()
            if self.LF == '':
                self.LF = generator.newLabel()
            
            generator.addIf(temp, '1', '==', self.LV)
            generator.addGoto(self.LF)

            generator.addCommit("Fin compilacion acceso")
            generator.addSaltoLinea()

            ret = ReturnC3D(None, tipo.BOOLEANO, False,-1,simbolo.index)
            ret.trueLbl = self.LV
            ret.falseLbl = self.LF

            return ret


        #si ya es nothing entonces

        if self.LV == '':
            self.LV = generator.newLabel()
        if self.LF == '':
            self.LF = generator.newLabel()
        
        generator.addIf(temp, '00000000', '==', self.LV)
        generator.addGoto(self.LF)

        generator.addCommit("Fin compilacion acceso")
        generator.addSaltoLinea()

        ret = ReturnC3D('00000000.0', tipo.NULO, False,-1,simbolo.index)
        ret.trueLbl = self.LV
        ret.falseLbl = self.LF

        return ret
        



    '''
    def imprimirC3DPrimi(self,value, tree, table):
                                                                                                                                                                                                                                                                                                                                                         
        tree.contador=tree.contador+1

        if value.tipo == tipo.CADENA:

            cadena = "T"+str(tree.contador)+" = stack[int("+str(value.posicionSTACKoHEAP)+")]"+";\nfmt.Printf(\"%c\", ASCII);\n"#valor del primitivo a mostrar

        elif value.tipo == tipo.ENTERO:
    
            cadena = "T"+str(tree.contador)+" = stack[int("+str(value.posicionSTACKoHEAP)+")]"+";\nfmt.Printf(\"%d\", int("+ "T"+str(tree.contador)+"));\n"#valor del primitivo a mostrar

        elif value.tipo == tipo.DECIMAL:
        
            cadena = "T"+str(tree.contador)+" = stack[int("+str(value.posicionSTACKoHEAP)+")]"+";\nfmt.Printf(\"%f\", "+ "T"+str(tree.contador)+");\n"#valor del primitivo a mostrar

        elif value.tipo == tipo.CHARACTER:#char
        
            cadena = "T"+str(tree.contador)+" = stack[int("+str(value.posicionSTACKoHEAP)+")]"+";\nfmt.Printf(\"%c\", ASCII);\n"#valor del primitivo a mostrar

        elif value.tipo == tipo.BOOLEANO:# van a ser 0,1
        
            cadena = "T"+str(tree.contador)+" = stack[int("+str(value.posicionSTACKoHEAP)+")]"+";\nfmt.Printf(\"%d\", int("+ "T"+str(tree.contador)+"));\n"#valor del primitivo a mostrar


        return cadena'''