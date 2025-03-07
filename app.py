from logging import disable
from wsgiref.validate import validator

import flet as ft

from restaurante import Restaurante
from mesa import Mesa
from cliente import Cliente

class RestauranteGUI:
    def __init__(self):
        self.restaurante = Restaurante()
        capacidades = [2, 2, 2, 4, 4, 4, 6, 6, 6]
        for i in range(1, 10):
            self.restaurante.agregar_mesa(Mesa(i, capacidades[i-1]))

    def main(self, page: ft.Page):
        page.title = 'Sistema de Restaurante'
        page.padding = 20
        page.theme_mode = 'dark'

        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(text='Mesera',
                       icon=ft.icons.PERSON,
                       content=self.crear_vista_mesera()
                    ),
                ft.Tab(text='Cocina',
                       icon=ft.icons.RESTAURANT,
                       content=self.crear_vista_cocina()
                    ),
                ft.Tab(text='Caja',
                       icon=ft.icons.POINT_OF_SALE,
                       content=self.crear_vista_caja()
                ),
                ft.Tab(text='Administración',
                       icon=ft.icons.ADMIN_PANEL_SETTINGS,
                       content=self.crear_vista_adm()
                    ),
                ],
            expand=1,
        )

        page.add(self.tabs)

    #! Métodos de vistas
    def crear_vista_mesera(self):
        self.grid_container = ft.Container(
            content=self.crear_grid_mesas(),
            width=700,
            expand=True
        )
        return ft.Row(
            controls=[
                ft.Container(
                    width=700,
                    content=ft.Column([ft.Text('Mesas del Restaurante', size=20, weight=ft.FontWeight.BOLD),
                               self.grid_container
                              ], expand=True),
                    expand=True
                 ),
                ft.VerticalDivider(),
                ft.Container(
                    width=400,
                    content=self.crear_panel_gestion(),
                    expand=True
                )
            ],
            expand=True,
            spacing=0
        )

    def crear_vista_caja(self):
        self.lista_pedidos_caja = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
            auto_scroll=True
        )

        def marcar_como_pagado(e, pedido):
            pedido.cambiar_estado('Pagado')
            self.restaurante.pedidos_activos.remove(pedido)
            self.actualizar_vista_caja()
            self.actualizar_ui(e.page)
            e.page.update()

        def crear_item_pedido(pedido):
            return ft.Container(
                content=ft.Column([
                    ft.Text(f'Mesa {pedido.mesa.numero}', size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(pedido.obtener_resumen()),
                    ft.Row([
                        ft.ElevatedButton('Marcar como Pagado',
                                          on_click=lambda e, p=pedido: marcar_como_pagado(e, p),
                                          disabled=pedido.estado != 'Listo',
                                          style=ft.ButtonStyle(
                                            bgcolor=ft.colors.GREEN_700,
                                            color=ft.colors.WHITE
                                          )),
                        ft.Text(f'Total: ${pedido.calcular_total()}', 
                               size=16, 
                               weight=ft.FontWeight.BOLD,
                               color=ft.colors.AMBER_500)
                    ])
                ]),
                bgcolor=ft.colors.BLUE_GREY_900,
                padding=10,
                border_radius=10
            )

        def actualizar_vista_caja():
            self.lista_pedidos_caja.controls.clear()
            for pedido in self.restaurante.pedidos_activos:
                if pedido.estado == 'Listo':
                    self.lista_pedidos_caja.controls.append(crear_item_pedido(pedido))

        self.actualizar_vista_caja = actualizar_vista_caja
        self.actualizar_vista_caja()
        
        return ft.Container(
            content=ft.Column([
                ft.Text('Pedidos Listos para Cobrar', size=20, weight=ft.FontWeight.BOLD),
                self.lista_pedidos_caja
            ], expand=True),
            padding=20,
            expand=True
        )

    def crear_vista_cocina(self):
        self.lista_pedidos_cocina = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
            auto_scroll=True
        )

        def cambiar_estado_pedido(e,pedido, nuevo_estado):
            pedido.cambiar_estado(nuevo_estado)
            self.actualizar_vista_cocina()
            self.actualizar_vista_caja()
            self.actualizar_ui(e.page)
            e.page.update()

        def crear_item_pedido(pedido):
            return ft.Container(
                content=ft.Column([
                    ft.Text(f'Mesa {pedido.mesa.numero}', size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(pedido.obtener_resumen()),
                    ft.Row([
                        ft.ElevatedButton('En Preparacion',
                                          on_click= lambda  e, p=pedido: cambiar_estado_pedido(e,p, 'En Preparacion'),
                                          disabled=pedido.estado != 'Pendiente',
                                          style=ft.ButtonStyle(
                                            bgcolor=ft.colors.ORANGE_700,
                                            color=ft.colors.WHITE
                                          )),
                        ft.ElevatedButton('Listo',
                                          on_click=lambda e, p=pedido: cambiar_estado_pedido(e, p, 'Listo'),
                                          disabled=pedido.estado != 'En Preparacion',
                                          style=ft.ButtonStyle(
                                            bgcolor=ft.colors.GREEN_700,
                                            color=ft.colors.WHITE
                                          )),
                        ft.Text(f'Estado: {pedido.estado}', color=ft.colors.BLUE_200)
                    ])
                ]),
                bgcolor=ft.colors.BLUE_GREY_900,
                padding=10,
                border_radius=10
            )

        def actualizar_vista_cocina():
                self.lista_pedidos_cocina.controls.clear()
                for pedido in self.restaurante.pedidos_activos:
                    if pedido.estado in ['Pendiente', 'En Preparacion']:
                        self.lista_pedidos_cocina.controls.append(crear_item_pedido(pedido))

        self.actualizar_vista_cocina = actualizar_vista_cocina
        self.actualizar_vista_cocina()

        return ft.Container(
            content=ft.Column([
                ft.Text('Pedidos en Cocina', size=20, weight=ft.FontWeight.BOLD),
                self.lista_pedidos_cocina
            ], expand=True),
            padding=20,
            expand=True
        )

    #! Métodos internos de vistas
    def crear_grid_mesas(self):
        grid = ft.GridView(
            expand=1,
            runs_count=2,
            max_extent=200,
            child_aspect_ratio=1.0,
            spacing=10,
            run_spacing=10,
            padding=10
        )
        for mesa in self.restaurante.mesas:
            color = ft.colors.GREEN_700 if not mesa.ocupado else ft.colors.RED_700
            estado = 'Libre' if not mesa.ocupado else 'Ocupada'

            grid.controls.append(
                ft.Container(
                    content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Icon(ft.icons.TABLE_RESTAURANT, color=ft.colors.AMBER_400),
                                        ft.Text(f'Mesa {mesa.numero}', size=16, weight=ft.FontWeight.BOLD)
                                    ]
                                ),
                                ft.Text(f'Capacidad {mesa.tamaño} personas', size=14),
                                ft.Text(estado,
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.colors.WHITE
                                    )
                            ]
                        ),
                    bgcolor=color,
                    padding=5,
                    margin=5,
                    border_radius=5,
                    ink=True,
                    on_click= lambda e, num=mesa.numero: self.seleccionar_mesa(e, num)
                )
            )
        return grid

    def actualizar_ui(self, page):
        nuevo_grid = self.crear_grid_mesas()
        self.grid_container.content = nuevo_grid

        if self.mesa_seleccionada:
            if self.mesa_seleccionada.ocupado and self.mesa_seleccionada.pedido_actual:
                self.resumen_pedido.value = self.mesa_seleccionada.pedido_actual.obtener_resumen()
            else:
                self.resumen_pedido.value = ''

            self.asignar_btn.disabled = self.mesa_seleccionada.ocupado
            self.agregar_item_btn.disabled = not self.mesa_seleccionada.ocupado
            self.liberar_btn.disabled = not self.mesa_seleccionada.ocupado

            self.actualizar_vista_cocina()
            self.actualizar_vista_caja()

        page.update()


    def seleccionar_mesa(self, e, numero_mesa):
        self.mesa_seleccionada = self.restaurante.buscar_mesa(numero_mesa)
        mesa = self.mesa_seleccionada
        self.mesa_info.value = f'Mesa {mesa.numero} - Capacidad: {mesa.tamaño} personas'
        self.asignar_btn.disabled = mesa.ocupado
        self.agregar_item_btn.disabled = not mesa.ocupado
        self.liberar_btn.disabled = not mesa.ocupado

        if mesa.ocupado and mesa.pedido_actual:
            self.resumen_pedido.value = mesa.pedido_actual.obtener_resumen()
        else:
            self.resumen_pedido.value = ''

        self.actualizar_ui(e.page)

        e.page.update()
        return None

    def crear_panel_gestion(self):
        self.mesa_seleccionada = None
        self.mesa_info =ft.Text('', size=16,weight=ft.FontWeight.BOLD)
        self.tamaño_grupo_input = ft.TextField(
            label='Tamaño del Grupo',
            input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.PEOPLE
        )

        self.tipo_item_dropdown = ft.Dropdown(
            label='Tipo de Item',
            options=[
                ft.dropdown.Option('Entrada'),
                ft.dropdown.Option('Plato Principal'),
                ft.dropdown.Option('Postre'),
                ft.dropdown.Option('Bebida'),
            ],
            width=200,
            on_change=self.actualizar_items_menu
        )

        self.items_dropdown = ft.Dropdown(
            label='Seleccionar Item',
            width=200,
        )

        self.asignar_btn = ft.ElevatedButton(
            text='Asignar Cliente',
            on_click=self.asignar_cliente,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.GREEN_700,
                color=ft.colors.WHITE
            )
        )

        self.agregar_item_btn = ft.ElevatedButton(
            text='Agregar Item',
            on_click=self.agregar_item_pedido,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.BLUE_700,
                color=ft.colors.WHITE
            )
        )

        self.liberar_btn = ft.ElevatedButton(
            text='Liberar Mesa',
            on_click=self.liberar_mesa,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.RED_700,
                color=ft.colors.WHITE
            )
        )

        self.resumen_pedido = ft.Text(value='', size=14)

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=self.mesa_info,
                        bgcolor=ft.colors.BLUE_GREY_900,
                        padding=10,
                        border_radius=10,
                    ),
                    ft.Container(height=20),
                    self.tamaño_grupo_input,
                    self.asignar_btn,
                    ft.Divider(),
                    self.tipo_item_dropdown,
                    self.items_dropdown,
                    self.agregar_item_btn,
                    ft.Divider(),
                    self.liberar_btn,
                    ft.Divider(),
                    ft.Text(value='Resumen del Pedido:', size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=self.resumen_pedido,
                        bgcolor=ft.colors.BLUE_GREY_900,
                        padding=10,
                        border_radius=10,
                        width=350,
                    )
                ],
                spacing=10,
                expand=True
            ),
            padding=20,
            expand=True
        )

    def asignar_cliente(self, e):
        if not self.mesa_seleccionada:
            return
        try:
            tamaño_grupo = int(self.tamaño_grupo_input.value)
            if tamaño_grupo <= 0:
                return
            cliente = Cliente(tamaño_grupo)
            resultado = self.restaurante.asignar_mesa_cliente(cliente, self.mesa_seleccionada.numero)

            if 'asignado' in resultado:
                self.restaurante.crear_pedido(self.mesa_seleccionada.numero)
                self.tamaño_grupo_input.value = ''
                self.actualizar_ui(e.page)
        except ValueError:
            pass

    def actualizar_items_menu(self, e):
        tipo = self.tipo_item_dropdown.value
        self.items_dropdown.value = []

        if tipo == 'Entrada':
            items = self.restaurante.menu.entradas
        elif tipo == 'Plato Principal':
            items = self.restaurante.menu.plato_principal
        elif tipo == 'Postre':
            items = self.restaurante.menu.postres
        elif tipo == 'Bebida':
            items = self.restaurante.menu.bebidas
        else:
            items = []

        self.items_dropdown.options = [
            ft.dropdown.Option(item.nombre) for item in items
        ]
        if e and e.page:
            e.page.update()

    def agregar_item_pedido(self, e):
        if not self.mesa_seleccionada or not self.mesa_seleccionada.pedido_actual:
            return
        tipo = self.tipo_item_dropdown.value
        nombre_item = self.items_dropdown.value

        if tipo and nombre_item:
            item = self.restaurante.obtener_item_menu(tipo, nombre_item)
            if item:
                self.mesa_seleccionada.pedido_actual.agregar_item(item)
                self.actualizar_ui(e.page)

    def liberar_mesa(self,e):
        if self.mesa_seleccionada:
            self.restaurante.liberar_mesa(self.mesa_seleccionada.numero)
            self.actualizar_ui(e.page)
            
    def crear_vista_adm(self):
        self.nombre_item_input = ft.TextField(
            label='Nombre del Item',
            width=200
        )
        self.precio_item_input = ft.TextField(
            label='Precio',
            input_filter=ft.NumbersOnlyInputFilter(),
            width=200
        )
        self.tipo_item_adm_dropdown = ft.Dropdown(
            label='Tipo de Item',
            options=[
                ft.dropdown.Option('Entrada'),
                ft.dropdown.Option('Plato Principal'),
                ft.dropdown.Option('Postre'),
                ft.dropdown.Option('Bebida'),
            ],
            width=200
        )
        self.items_lista = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
            auto_scroll=True
        )

        def agregar_item(e):
            nombre = self.nombre_item_input.value
            try:
                precio = int(self.precio_item_input.value)
                tipo = self.tipo_item_adm_dropdown.value
                if nombre and precio > 0 and tipo:
                    if tipo == 'Entrada':
                        self.restaurante.menu.agregar_entrada(nombre, precio)
                    elif tipo == 'Plato Principal':
                        self.restaurante.menu.agregar_plato_principal(nombre, precio)
                    elif tipo == 'Postre':
                        self.restaurante.menu.agregar_postre(nombre, precio)
                    elif tipo == 'Bebida':
                        self.restaurante.menu.agregar_bebida(nombre, precio)
                    self.nombre_item_input.value = ''
                    self.precio_item_input.value = ''
                    actualizar_lista_items()
                    e.page.update()
            except ValueError:
                pass

        def eliminar_item(e, tipo, nombre):
            self.restaurante.menu.eliminar_item(tipo, nombre)
            actualizar_lista_items()
            e.page.update()

        def actualizar_lista_items():
            self.items_lista.controls.clear()
            for tipo, items in [
                ('Entrada', self.restaurante.menu.entradas),
                ('Plato Principal', self.restaurante.menu.plato_principal),
                ('Postre', self.restaurante.menu.postres),
                ('Bebida', self.restaurante.menu.bebidas)
            ]:
                if items:
                    self.items_lista.controls.append(
                        ft.Text(f'\n{tipo}s:', size=16, weight=ft.FontWeight.BOLD)
                    )
                    for item in items:
                        self.items_lista.controls.append(
                            ft.Container(
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(f'{item.nombre} - ${item.precio}'),
                                        ft.IconButton(
                                            icon=ft.icons.DELETE,
                                            icon_color=ft.colors.RED_400,
                                            on_click=lambda e, t=tipo, n=item.nombre: eliminar_item(e, t, n)
                                        )
                                    ]
                                ),
                                bgcolor=ft.colors.BLUE_GREY_900,
                                padding=10,
                                border_radius=10
                            )
                        )

        agregar_btn = ft.ElevatedButton(
            text='Agregar Item',
            on_click=agregar_item,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.GREEN_700,
                color=ft.colors.WHITE
            )
        )

        actualizar_lista_items()

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=300,
                        content=ft.Column([
                            ft.Text('Agregar Nuevo Item', size=20, weight=ft.FontWeight.BOLD),
                            self.tipo_item_adm_dropdown,
                            self.nombre_item_input,
                            self.precio_item_input,
                            agregar_btn
                        ], spacing=20),
                        padding=20
                    ),
                    ft.VerticalDivider(),
                    ft.Container(
                        expand=True,
                        content=ft.Column([
                            ft.Text('Items del Menú', size=20, weight=ft.FontWeight.BOLD),
                            self.items_lista
                        ]),
                        padding=20
                    )
                ],
                expand=True
            ),
            expand=True
        )


def main():
    app = RestauranteGUI()
    ft.app(target=app.main)

if __name__ == '__main__':
    main()