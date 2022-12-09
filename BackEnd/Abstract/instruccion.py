from abc import ABC,abstractmethod#crear clases y metodos abstractos


class instruccion(ABC):#sirve para q se hereden funcionalidades como imprimir,asignar declarar tener acceso
    def __init__(self,fila,columna):
        self.fila=fila#es parte de la gramatica entrada
        self.columna=columna#es parte de la gramatica entrada
        self.arreglo=False


        self.TMP=""#temporal
        self.C3D=""#Codigo 3 Direcciones
        self.LV=""#etiquetas verdaderas
        self.LF=""#etiquetas falsas
        self.LR=""#etiqueta de recurrencia para whiles,...etc
        
        self.LS=""#etiquetas de salidas



        super().__init__()#clases abstractas funcionen

    @abstractmethod
    def interpretar(self, tree, table):
        pass


    @abstractmethod
    def compilar(self, tree, table):
        pass

    
    @abstractmethod
    def getNodo(self):
        pass

        



































