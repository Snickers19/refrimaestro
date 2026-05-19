import flet as ft
from session_store import get_favoritos, limpiar_favoritos, get_cotizaciones, limpiar_cotizaciones
from producto_detalle import abrir_detalle

BG_COLOR        = "#0c0f14"
CONTAINER_COLOR = "#141821"
COFFEE_COLOR    = "#c29b76"
TEXT_PRIMARY    = "#f3f4f6"
TEXT_SECONDARY  = "#9ca3af"
ACCENT_BG       = "#1f2430"


# ─────────────────────────────────────────────────────────────────────────────
#  VISTA DE FAVORITOS
# ─────────────────────────────────────────────────────────────────────────────
def FavoritosView(page: ft.Page):
    favoritos = get_favoritos(page)

    def on_back(e):
        page.go("/")

    def on_limpiar(e):
        limpiar_favoritos(page)
        page.go("/")

    if not favoritos:
        cuerpo = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.BOOKMARK_BORDER, size=64, color=TEXT_SECONDARY),
                    ft.Text("No tienes productos guardados.", color=TEXT_SECONDARY, size=16),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
        )
    else:
        cards = []
        for p in favoritos:
            def make_on_tap(producto):
                def handler(e):
                    abrir_detalle(page, producto)
                return handler

            cards.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Image(
                                src=p.get("imagen", "https://via.placeholder.com/80"),
                                width=80, height=80,
                                fit=ft.ImageFit.COVER,
                                border_radius=ft.border_radius.all(8),
                            ),
                            ft.Column(
                                [
                                    ft.Text(p["nombre"], color=TEXT_PRIMARY, size=14,
                                            weight=ft.FontWeight.W_600,
                                            overflow=ft.TextOverflow.ELLIPSIS),
                                    ft.Text(p.get("descripcion", "")[:60] + "...",
                                            color=TEXT_SECONDARY, size=12,
                                            overflow=ft.TextOverflow.ELLIPSIS),
                                    ft.Text(p["precio"], color=COFFEE_COLOR,
                                            size=16, weight=ft.FontWeight.BOLD),
                                ],
                                expand=True,
                                spacing=4,
                            ),
                            ft.Icon(ft.Icons.CHEVRON_RIGHT, color=TEXT_SECONDARY),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=12,
                    ),
                    bgcolor=CONTAINER_COLOR,
                    border_radius=12,
                    padding=12,
                    border=ft.border.all(1, "#2a2d36"),
                    margin=ft.margin.only(bottom=10),
                    ink=True,
                    on_click=make_on_tap(p),
                )
            )

        cuerpo = ft.Column(cards, scroll=ft.ScrollMode.AUTO, expand=True)

    top_bar = ft.Container(
        content=ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                    icon_color=TEXT_PRIMARY, icon_size=20,
                    on_click=on_back,
                ),
                ft.Text("Guardados", size=18, weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY, expand=True),
                ft.TextButton(
                    "Limpiar", style=ft.ButtonStyle(color=ft.Colors.RED_400),
                    on_click=on_limpiar,
                    visible=bool(favoritos),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=CONTAINER_COLOR,
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        border=ft.border.only(bottom=ft.BorderSide(1, "#2a2d36")),
    )

    return ft.View(
        route="/favoritos",
        bgcolor=BG_COLOR,
        padding=0,
        controls=[
            ft.Column(
                [
                    top_bar,
                    ft.Container(content=cuerpo, padding=16, expand=True),
                ],
                expand=True,
                spacing=0,
            )
        ],
    )


# ─────────────────────────────────────────────────────────────────────────────
#  VISTA DE HISTORIAL DE COTIZACIONES
# ─────────────────────────────────────────────────────────────────────────────
def CotizacionesView(page: ft.Page):
    cotizaciones = get_cotizaciones(page)

    def on_back(e):
        page.go("/")

    def on_limpiar(e):
        limpiar_cotizaciones(page)
        page.go("/")

    def format_clp(num):
        return f"${num:,.0f}".replace(",", ".")

    if not cotizaciones:
        cuerpo = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.RECEIPT_LONG_OUTLINED, size=64, color=TEXT_SECONDARY),
                    ft.Text("No hay cotizaciones guardadas.", color=TEXT_SECONDARY, size=16),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
        )
    else:
        tarjetas = []
        for c in cotizaciones:
            servicios_texto = ft.Column(
                [
                    ft.Text(
                        f"• {s['nombre']}: {format_clp(s['precioBase'])}",
                        color=TEXT_SECONDARY, size=13,
                    )
                    for s in c["servicios"]
                ],
                spacing=2,
            )

            tarjetas.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.ACCESS_TIME, size=14, color=TEXT_SECONDARY),
                                    ft.Text(c["fecha"], color=TEXT_SECONDARY, size=12),
                                ],
                                spacing=6,
                            ),
                            ft.Divider(color="#2a2d36", height=10),
                            servicios_texto,
                            ft.Divider(color="#2a2d36", height=10),
                            ft.Row(
                                [
                                    ft.Text("Total:", color=TEXT_PRIMARY, size=15,
                                            weight=ft.FontWeight.W_600),
                                    ft.Text(format_clp(c["total"]), color=COFFEE_COLOR,
                                            size=18, weight=ft.FontWeight.BOLD),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                        ],
                        spacing=4,
                    ),
                    bgcolor=CONTAINER_COLOR,
                    border_radius=12,
                    padding=16,
                    border=ft.border.all(1, "#2a2d36"),
                    margin=ft.margin.only(bottom=12),
                )
            )

        cuerpo = ft.Column(tarjetas, scroll=ft.ScrollMode.AUTO, expand=True)

    top_bar = ft.Container(
        content=ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                    icon_color=TEXT_PRIMARY, icon_size=20,
                    on_click=on_back,
                ),
                ft.Text("Mis Cotizaciones", size=18, weight=ft.FontWeight.BOLD,
                        color=TEXT_PRIMARY, expand=True),
                ft.TextButton(
                    "Limpiar",
                    style=ft.ButtonStyle(color=ft.Colors.RED_400),
                    on_click=on_limpiar,
                    visible=bool(cotizaciones),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=CONTAINER_COLOR,
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        border=ft.border.only(bottom=ft.BorderSide(1, "#2a2d36")),
    )

    return ft.View(
        route="/cotizaciones",
        bgcolor=BG_COLOR,
        padding=0,
        controls=[
            ft.Column(
                [
                    top_bar,
                    ft.Container(content=cuerpo, padding=16, expand=True),
                ],
                expand=True,
                spacing=0,
            )
        ],
    )
