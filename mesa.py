class Mesa:
    def __init__(self, numero, tamaño):
        self.numero = numero
        self.tamaño = tamaño
        self.ocupado = False
        self.cliente = None
        self.pedido_actual = False