class ReturnC3D:#para que mi c3d sea mas entendible y funcional
    def __init__(self, valor, tipoRet , esTemp, Array = [],posicion=-1,index=None):
        self.valor = valor
        self.tipo = tipoRet 
        self.Array = Array
        self.esTemporal = esTemp
        self.trueLbl = ''
        self.falseLbl = ''
        self.posicion=posicion
        self.index=index


    #def compilar(self):
    #    return self