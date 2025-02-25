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
                ft.Tab(text='Administrracion',
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
        return ft.Container(
            content=ft.Column([ft.Text('Mesas del Restaurante', size=20, weight=ft.FontWeight.BOLD),
                               self.grid_container
        ])
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
                ft.Column(
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
                        )
                    ]
                )
            )
        return grid

def main():
    app = RestauranteGUI()
    ft.app(target=app.main)

if __name__ == '__main__':
    main()