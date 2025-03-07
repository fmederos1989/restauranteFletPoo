
import json
import os

class ItemMenu:
    def __init__(self, nombre, precio, cantidad=1):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def calcular_subtotal(self):
        return self.precio * self.cantidad

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'precio': self.precio,
            'cantidad': self.cantidad
        }

class Entrada(ItemMenu):
     def __init__(self, nombre, precio, cantidad=1):
        super().__init__(nombre, precio, cantidad)
        self.tipo = 'Entrada'

class PlatoPrincipal(ItemMenu):
     def __init__(self, nombre, precio, cantidad=1):
        super().__init__(nombre, precio, cantidad)
        self.tipo = 'Plato Principal'

class Postre(ItemMenu):
     def __init__(self, nombre, precio, cantidad=1):
        super().__init__(nombre, precio, cantidad)
        self.tipo = 'Postre'

class Bebida(ItemMenu):
     def __init__(self, nombre, precio, cantidad=1):
        super().__init__(nombre, precio, cantidad)
        self.tipo = 'Bebida'


class Menu:
    def __init__(self):
        self.entradas = []
        self.plato_principal = []
        self.bebidas = []
        self.postres = []
        self.archivo_menu = 'menu_data.json'
        self.cargar_menu()

    def guardar_menu(self):
        """Guarda el menú actual en un archivo JSON"""
        menu_data = {
            'entradas': [item.to_dict() for item in self.entradas],
            'plato_principal': [item.to_dict() for item in self.plato_principal],
            'bebidas': [item.to_dict() for item in self.bebidas],
            'postres': [item.to_dict() for item in self.postres]
        }
        
        try:
            with open(self.archivo_menu, 'w', encoding='utf-8') as archivo:
                json.dump(menu_data, archivo, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error al guardar el menú: {e}")

    def cargar_menu(self):
        """Carga el menú desde un archivo JSON si existe"""
        if not os.path.exists(self.archivo_menu):
            return
            
        try:
            with open(self.archivo_menu, 'r', encoding='utf-8') as archivo:
                menu_data = json.load(archivo)
                
                # Limpiar listas actuales
                self.entradas = []
                self.plato_principal = []
                self.bebidas = []
                self.postres = []
                
                # Cargar entradas
                for item_data in menu_data.get('entradas', []):
                    self.entradas.append(Entrada(
                        item_data['nombre'], 
                        item_data['precio'], 
                        item_data.get('cantidad', 1)
                    ))
                
                # Cargar platos principales
                for item_data in menu_data.get('plato_principal', []):
                    self.plato_principal.append(PlatoPrincipal(
                        item_data['nombre'], 
                        item_data['precio'], 
                        item_data.get('cantidad', 1)
                    ))
                
                # Cargar bebidas
                for item_data in menu_data.get('bebidas', []):
                    self.bebidas.append(Bebida(
                        item_data['nombre'], 
                        item_data['precio'], 
                        item_data.get('cantidad', 1)
                    ))
                
                # Cargar postres
                for item_data in menu_data.get('postres', []):
                    self.postres.append(Postre(
                        item_data['nombre'], 
                        item_data['precio'], 
                        item_data.get('cantidad', 1)
                    ))
        except Exception as e:
            print(f"Error al cargar el menú: {e}")

    def agregar_entrada(self, nombre, precio):
        entrada = Entrada(nombre, precio)
        self.entradas.append(entrada)
        self.guardar_menu()  # Guardar cambios
        return entrada

    def agregar_plato_principal(self, nombre, precio):
        plato_principal = PlatoPrincipal(nombre, precio)
        self.plato_principal.append(plato_principal)
        self.guardar_menu()  # Guardar cambios
        return plato_principal

    def agregar_bebida(self, nombre, precio):
        bebida = Bebida(nombre, precio)
        self.bebidas.append(bebida)
        self.guardar_menu()  # Guardar cambios
        return bebida

    def agregar_postre(self, nombre, precio):
        postre = Postre(nombre, precio)
        self.postres.append(postre)
        self.guardar_menu()  # Guardar cambios
        return postre

    def eliminar_item(self, tipo, nombre):
        if tipo == 'Entrada':
            items = self.entradas
        elif tipo == 'Plato Principal':
            items = self.plato_principal
        elif tipo == 'Postre':
            items = self.postres
        elif tipo == 'Bebida':
            items = self.bebidas
        else:
            return False

        for item in items[:]:
            if item.nombre == nombre:
                items.remove(item)
                self.guardar_menu()  # Guardar cambios
                return True
        return False

    def eliminar_entrada(self, nombre):
        return self.eliminar_item('Entrada', nombre)

    def eliminar_plato_principal(self, nombre):
        return self.eliminar_item('Plato Principal', nombre)

    def eliminar_postre(self, nombre):
        return self.eliminar_item('Postre', nombre)

    def eliminar_bebida(self, nombre):
        return self.eliminar_item('Bebida', nombre)

    def obtener_item(self, tipo, nombre):
        if tipo == 'Entrada':
            items = self.entradas
        elif tipo == 'Plato Principal':
            items = self.plato_principal
        elif tipo == 'Postre':
            items = self.postres
        elif tipo == 'Bebida':
            items = self.bebidas
        else:
            return None

        for item in items:
            if item.nombre == nombre:
                return item
        return None