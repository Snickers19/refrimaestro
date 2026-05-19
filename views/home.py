import flet as ft
from components.navbar import Navbar, Footer
from producto_detalle import abrir_detalle
from session_store import toggle_favorito, es_favorito

BG_COLOR = "#0c0f14"
CONTAINER_COLOR = "#141821"
NAV_COLOR = "#18191b"
COFFEE_COLOR = "#c29b76"
TEXT_PRIMARY = "#f3f4f6"
TEXT_SECONDARY = "#9ca3af"
ACCENT_BG = "#1f2430"

def HomeView(page: ft.Page):
    productos = [
        {
            "id": "daewoo_rf420s",
            "nombre": "DAEWOO RF-420S",
            "descripcion": "Sistema No Frost para evitar la acumulación de hielo. 312 L capacidad, 62 kg peso. Posee control electrónico de temperatura que permite ajustar frío de manera precisa en zonas de refrigeración y congelación. Diseñado para operación silenciosa y consumo eficiente. Dimensiones: 168 cm Alto, 60 cm Ancho, 65 cm Profundidad.",
            "precio": "$178,200",
            "imagen": "refrigerator-photos/Daewoo-RF-420S.jpeg"
        },
        {
            "id": "samsung_rt46",
            "nombre": "SAMSUNG RT46K6631SL",
            "descripcion": "Refrigerador de Sistema Inverter: Posee un control complejo que permite programar tecnologías Twin Cooling Plus, Power Cool y Freeze. 452 L capacidad, 111 L de freezer, 4 bandejas y 2 puertas, 75 kg peso. 182.5 cm Alto, 70 cm Ancho, 72.6 cm Profundidad.",
            "precio": "$344,500",
            "imagen": "refrigerator-photos/Samsung-2.jpeg"
        }
    ]

    def ProductoCard(page: ft.Page, producto: dict) -> ft.Container:
        save_ref = ft.Ref[ft.IconButton]()

        def on_tap(e):
            abrir_detalle(page, producto)

        def on_guardar(e):
            guardado = toggle_favorito(page, producto)
            save_ref.current.icon       = ft.Icons.BOOKMARK if guardado else ft.Icons.BOOKMARK_BORDER
            save_ref.current.icon_color = COFFEE_COLOR if guardado else TEXT_SECONDARY
            page.update()

        ya_guardado = es_favorito(page, producto["id"])

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Image(
                            src=producto.get("imagen", "https://via.placeholder.com/200"),
                            fit=ft.ImageFit.COVER,
                            expand=True,
                        ),
                        height=160,
                        border_radius=ft.border_radius.only(top_left=12, top_right=12),
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(producto["nombre"], color=TEXT_PRIMARY,
                                        size=14, weight=ft.FontWeight.W_600,
                                        overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(producto.get("descripcion", "")[:50],
                                        color=TEXT_SECONDARY, size=12,
                                        overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Row(
                                    [
                                        ft.Text(producto["precio"], color=COFFEE_COLOR,
                                                size=16, weight=ft.FontWeight.BOLD,
                                                expand=True),
                                        ft.IconButton(
                                            ref=save_ref,
                                            icon=ft.Icons.BOOKMARK if ya_guardado else ft.Icons.BOOKMARK_BORDER,
                                            icon_color=COFFEE_COLOR if ya_guardado else TEXT_SECONDARY,
                                            icon_size=20,
                                            tooltip="Guardar",
                                            on_click=on_guardar,
                                            padding=0,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ],
                            spacing=4,
                        ),
                        padding=ft.padding.symmetric(horizontal=12, vertical=10),
                    ),
                ],
                spacing=0,
            ),
            bgcolor=CONTAINER_COLOR,
            border_radius=12,
            border=ft.border.all(1, "#2a2d36"),
            ink=True,
            on_click=on_tap,
            shadow=ft.BoxShadow(blur_radius=8, color="#00000055", offset=ft.Offset(0, 3)),
        )

    return ft.Column(
        [
            Navbar(page, active_route="/"),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Nuestros Refrigeradores", size=32, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Text("Explora nuestra selección de refrigeradores, con los últimos modelos disponibles.", size=16, color=TEXT_SECONDARY),
                        ft.Container(height=20),
                        
                        ft.ResponsiveRow(
                            [
                                ft.Container(
                                    content=ProductoCard(page, prod),
                                    col={"xs": 12, "sm": 12, "md": 6, "lg": 4},
                                ) for prod in productos
                            ],
                            spacing=24,
                            run_spacing=24,
                        ),
                    ]
                ),
                padding=ft.padding.symmetric(horizontal=24, vertical=40),
                expand=True,
            ),
            Footer(),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
