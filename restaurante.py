from menu import Menu
from mesa import Mesa

class Restaurante:
    def __init__(self):
        self.mesas = []
        self.clientes = []
        self.menu = Menu()
        self.pedidos_activos = []
        self._inicializar_menu()

    def _inicializar_menu(self):
        self.menu.agregar_entrada('Ensalada Cesar', 50)
        self.menu.agregar_entrada('Pasta Carbonara', 60)
        self.menu.agregar_plato_principal('Filete Mignon', 250)
        self.menu.agregar_plato_principal('Tacos de Carne', 200)
        self.menu.agregar_bebida('Cafe', 20)
        self.menu.agregar_bebida('Agua', 15)
        self.menu.agregar_postre('Flan', 30)
        self.menu.agregar_postre('Tiramisu', 40)

    def agregar_mesa(self, mesa):
        self.mesas.append(mesa)
        return f'Mesa {mesa.numero} (capacidad: {mesa.tamaño}) agregada exitosamente'