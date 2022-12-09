from enum import Enum
#vamos a usar una estructura enum para tener un pull de palabras y opciones

class tipo(Enum):
    ENTERO=1
    DECIMAL=2
    BOOLEANO=3
    CHARACTER=4
    CADENA=5
    NULO=6
    ARREGLO=7


class operador_aritmetico(Enum):
    MAS=1
    MENOS=2
    POR=3
    DIV=4
    POTENCIA=5
    MODULO=6
    UMENOS=7#NEGATIVO
    COMA=8

class operador_relacional(Enum):
     MENOR=1
     MAYOR=2   
     MENORQUE=3
     MAYORQUE=4
     IGUALIGUAL=5
     DIFERENTE=6

class operador_logico(Enum):
        NOT=1
        AND=2
        OR=3

        