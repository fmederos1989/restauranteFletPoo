class Mesa:
    def __init__(self, numero, tamaño):
        self.numero = numero
        self.tamaño = tamaño
        self.ocupado = False
        self.cliente = None
        self.pedido_actual = False

    def asignar_cliente(self, cliente):
        if cliente.tamaño_grupo <= self.tamaño:
            self.cliente = cliente
            self.ocupado = True
            return True
        return False

    def liberar(self):
        self.cliente = None
        self.ocupado = False
        self.pedido_actual = False

    def tiene_pedido_activo(self):
        return self.pedido_actual is not None