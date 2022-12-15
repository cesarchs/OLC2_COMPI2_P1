from enum import Enum

from almacenar.generador import Generador

class Tipo(Enum):
    ENTERO    = 1
    DECIMAL   = 2
    BOOLEANO  = 3
    CARACTER  = 4
    CADENA    = 5
    NULO      = 6
    ARREGLO   = 7
    RANGO     = 8
    STRUCT    = 9

class OpsAritmetico(Enum):
    MAS    = 1
    COMA   = 2
    MENOS  = 3
    POR    = 4
    DIV    = 5
    MOD    = 6
    POT    = 7
    UMENOS = 8
    DP     = 9

class OpsRelacional(Enum):
    MAYORQ      = 1
    MENORQ      = 2
    MAYORIGUALQ = 3
    MENORIGUALQ = 4
    IGUALQ      = 5
    DIFERENTE   = 6

class OpsLogical(Enum):
    OR  = 1
    AND = 2
    NOT = 3

class Ambito(Enum):
    GLOBAL = 1
    LOCAL = 2

class Bandera(Enum):
    FALSO = 0
    VERDADERO = 1
    
#******************** RETORNO ************************************
class Return:
    def __init__(self,valor,tipoRetorno,esTemporal,auxTipo = ""):
        self.valor = valor
        self.tipo = tipoRetorno
        self.auxTipo = auxTipo
        self.esTemporal = esTemporal
        self.trueLbl = ''
        self.falseLbl = ''
        self.array = None
        self.dimensiones=None
        self.dimensionesenacceso=None
        self.LblsalirArray=None

    def getValor(self):
        genAux = Generador()
        generator = genAux.getInstance()
        generator.liberarTemporal(self.valor)
        return self.valor
    