class Bloque:

    def __init__(self, primertupla):
        # Primera instruccion del codigo
        self.primertupla = primertupla
        # Bloques siguientes a este
        self.siguientes = []
        self.codigo = []