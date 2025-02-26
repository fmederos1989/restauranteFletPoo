import flet as ft

from restaurante import Restaurante
from mesa import Mesa
from cliente import Cliente

class RestauranteGUI:
    def __init__(self):
        self.restaurante = Restaurante()
        capacidades = [2, 2, 4, 4, 6, 6]
        for i in range(1, 7):
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
                       icon=ft.Icons.PERSON,
                       content=self.crear_vista_mesera()
                    ),
                ft.Tab(text='Cocina',
                       icon=ft.Icons.RESTAURANT,
                       # content=
                    ),
                ft.Tab(text='Caja',
                       icon=ft.Icons.POINT_OF_SALE,
                       # content=
                ),
                ft.Tab(text='Administración',
                       icon=ft.Icons.ADMIN_PANEL_SETTINGS,
                       # content=
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
            color = ft.Colors.GREEN_700 if not mesa.ocupado else ft.Colors.RED_700
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
                                        ft.Icon(ft.Icons.TABLE_RESTAURANT, color=ft.Colors.AMBER_400),
                                        ft.Text(f'Mesa {mesa.numero}', size=16, weight=ft.FontWeight.BOLD)
                                    ]
                                ),
                                ft.Text(f'Capacidad {mesa.tamaño} personas', size=14),
                                ft.Text(estado,
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE
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


    def seleccionar_mesa(self, e, numero_mesa):
        self.mesa_seleccionada = self.restaurante.buscar_mesa(numero_mesa)
        mesa = self.mesa_seleccionada

        #self.mesa_info.value = f'Mesa {mesa.numero} - Capacidad: {mesa.tamaño} personas'

        e.page.update()
        return None

    def crear_panel_gestion(self):
        self.mesa_seleccionada = None
        self.mesa_info =ft.Text('', size=16,weight=ft.FontWeight.BOLD)
        self.tamaño_grupo_input = ft.TextField(
            label='Tamaño del Grupo',
            input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.Icons.PEOPLE
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
                bgcolor=ft.Colors.GREEN_700,
                color=ft.Colors.WHITE
            )
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=self.mesa_info,
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        padding=10,
                        border_radius=10,
                    ),
                    ft.Container(height=20),
                    self.tamaño_grupo_input,
                    self.tipo_item_dropdown,
                    self.items_dropdown
                ]
            )
        )

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

def main():
    app = RestauranteGUI()
    ft.app(target=app.main)

if __name__ == '__main__':
    main()