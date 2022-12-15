
class SimboloFun:
    'ESTA CLASE SIRVE PARA DEFINIR UN SIMBOLO DE FUNCION EN LA TS'
    def __init__(self,func,idunico, esNative):
        self.Id = func.id
        self.IdUnico = idunico
        self.tipo = func.tipo
        self.tamano = len(func.parametros)
        self.parametros = func.parametros
        self.fila = func.fila
        self.columna = func.columna
        self.listatemps = None
        self.esNativa = esNative
        #self.ref 
        