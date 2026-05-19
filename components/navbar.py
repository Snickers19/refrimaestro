import flet as ft

BG_COLOR = "#0c0f14"
CONTAINER_COLOR = "#141821"
NAV_COLOR = "#18191b"
COFFEE_COLOR = "#c29b76"
TEXT_PRIMARY = "#f3f4f6"
TEXT_SECONDARY = "#9ca3af"

def Navbar(page: ft.Page, active_route: str = "/"):
    def navigate_to(e, route):
        page.go(route)

    def nav_button(text, icon, route):
        is_active = route == active_route
        return ft.TextButton(
            content=ft.Row(
                [
                    ft.Icon(icon, size=20, color=COFFEE_COLOR if is_active else TEXT_SECONDARY),
                    ft.Text(
                        text,
                        size=14,
                        weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.W_500,
                        color=COFFEE_COLOR if is_active else TEXT_SECONDARY,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                overlay_color="#2a2d36",
                bgcolor=CONTAINER_COLOR if is_active else "transparent",
            ),
            on_click=lambda e: navigate_to(e, route),
            height=45,
            expand=True if page.width and page.width < 600 else False,
        )

    top_header = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.AC_UNIT_ROUNDED, color=COFFEE_COLOR, size=32),
                        ft.Column(
                            [
                                ft.Text("Refri Maestro", weight=ft.FontWeight.BOLD, size=20, color=TEXT_PRIMARY),
                                ft.Text("Venta y Servicio Técnico", size=12, color=TEXT_SECONDARY),
                            ],
                            spacing=0,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.ResponsiveRow(
                    [
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Text("📞 +56 9 7398 2493", color=COFFEE_COLOR, weight=ft.FontWeight.W_600, size=13),
                                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                        bgcolor=CONTAINER_COLOR,
                                        border_radius=20,
                                        border=ft.border.all(1, "#2a2d36")
                                    ),
                                    ft.Container(
                                        content=ft.Text("✉️ ayuda.refrimaestro@gmail.com", color=COFFEE_COLOR, weight=ft.FontWeight.W_600, size=13),
                                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                        bgcolor=CONTAINER_COLOR,
                                        border_radius=20,
                                        border=ft.border.all(1, "#2a2d36")
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.BOOKMARK_OUTLINED,
                                        icon_color=TEXT_PRIMARY,
                                        tooltip="Guardados",
                                        on_click=lambda e: page.go("/favoritos"),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.RECEIPT_LONG_OUTLINED,
                                        icon_color=TEXT_PRIMARY,
                                        tooltip="Mis cotizaciones",
                                        on_click=lambda e: page.go("/cotizaciones"),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                            col={"xs": 0, "sm": 0, "md": 6, "lg": 6, "xl": 6},
                        )
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.END,
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=24, vertical=16),
        bgcolor=NAV_COLOR,
        border=ft.border.only(bottom=ft.border.BorderSide(1, "#2a2d36"))
    )

    nav_bar = ft.Container(
        content=ft.Row(
            [
                nav_button("Productos", ft.Icons.INVENTORY_2_OUTLINED, "/"),
                nav_button("Mantenimiento", ft.Icons.BUILD_CIRCLE_OUTLINED, "/mantenimiento"),
                nav_button("Contacto", ft.Icons.CONTACT_SUPPORT_OUTLINED, "/contacto"),
            ],
            alignment=ft.MainAxisAlignment.START if page.width and page.width >= 600 else ft.MainAxisAlignment.SPACE_AROUND,
            spacing=10,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=8),
        bgcolor=NAV_COLOR,
    )

    return ft.Column(
        [
            top_header,
            nav_bar,
        ],
        spacing=0,
    )

def Footer():
    return ft.Container(
        content=ft.Column(
            [
                ft.Divider(height=1, color="#2a2d36"),
                ft.Row(
                    [
                        ft.Text("© 2026 Refri Maestro | Reparaciones y Ventas en refrigeración", color=TEXT_SECONDARY, size=12),
                        ft.Row(
                            [
                                ft.Text("📞 +56 9 7398 2493", color=TEXT_SECONDARY, size=12),
                                ft.Text("✉️ ayuda.refrimaestro@gmail.com", color=TEXT_SECONDARY, size=12),
                            ],
                            spacing=15
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    wrap=True,
                )
            ]
        ),
        padding=ft.padding.symmetric(horizontal=24, vertical=24),
        bgcolor=NAV_COLOR,
        margin=ft.margin.only(top=40)
    )
