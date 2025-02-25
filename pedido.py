from menu import ItemMenu

class Pedido:
    def __init__(self, mesa):
        self.mesa = mesa
        self.items = {
            'entradas': [],
            'platos_principal': [],
            'bebidas': [],
            'postres': []
        }
        self.estado = 'Pendiente'

    def agregar_item(self, item):
        if isinstance(item, ItemMenu):
            if item.tipo == 'Entrada':
                self.items['entradas'].append(item)
            elif item.tipo == 'Plato Principal':
                self.items['platos_principal'].append(item)
            elif item.tipo == 'Postre':
                self.items['postres'].append(item)
            elif item.tipo == 'Bebida':
                self.items['bebidas'].append(item)

    def calcular_total(self):
        total = 0
        for categoria in self.items.values():
            for item in categoria:
                total += item.calcular_subtotal()
        return round(total, 2)