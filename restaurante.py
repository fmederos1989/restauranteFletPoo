from menu import Menu
from mesa import Mesa
from pedido import Pedido
import os

class Restaurante:
    def __init__(self):
        self.mesas = []
        self.clientes = []
        self.menu = Menu()
        self.pedidos_activos = []
        
        # Solo inicializar el menú por defecto si no existe un archivo de menú guardado
        if not os.path.exists(self.menu.archivo_menu):
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

    def asignar_mesa_cliente(self, cliente, numero_mesa):
        mesa = self.buscar_mesa(numero_mesa)
        if not mesa:
            return f'Mesa {numero_mesa} no encontrada'
        if mesa.ocupado:
            return 'La mesa ya se encuentra ocupada'
        if cliente.tamaño_grupo > mesa.tamaño:
            return f'Grupo demasiado grande para ocupar esta mesa (capacidad maxima: {mesa.tamaño})'
        if mesa.asignar_cliente(cliente):
            return f'Cliente {cliente.id} ha sido asignado a la mesa {mesa.numero}'
        return 'No se pudo asignar el cliente a la mesa'
    def buscar_mesa(self, numero_mesa):
        for mesa in self.mesas:
            if mesa.numero == numero_mesa:
                return mesa
        return None

    def crear_pedido(self, numero_mesa):
        mesa = self.buscar_mesa(numero_mesa)
        if mesa and mesa.ocupado:
            pedido = Pedido(mesa)
            self.pedidos_activos.append(pedido)
            mesa.pedido_actual = pedido
            mesa.cliente.asignar_pedido(pedido)
            return pedido
        return None

    def liberar_mesa(self, numero_mesa):
        mesa = self.buscar_mesa(numero_mesa)
        if mesa:
            cliente = mesa.cliente
            if cliente:
                cliente.limpiar_pedido()
                if cliente in self.clientes:
                    self.clientes.remove(cliente)
                if mesa.pedido_actual in self.pedidos_activos:
                    self.pedidos_activos.remove(mesa.pedido_actual)
            mesa.liberar()
            return f'Mesa {numero_mesa} liberada exitosamente'
        return 'Mesa no encontrada'

    def obtener_item_menu(self, tipo, nombre):
        return self.menu.obtener_item(tipo, nombre)