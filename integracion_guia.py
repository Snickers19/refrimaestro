"""
GUÍA DE INTEGRACIÓN
═══════════════════
Muestra exactamente dónde y cómo conectar los archivos nuevos.

Archivos nuevos:
  - producto_detalle.py   → vista de detalle del producto
  - session_store.py      → gestión de estado en memoria
  - guardados_views.py    → vistas Favoritos y Cotizaciones
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1.  main.py  ─ registrar las rutas nuevas en el router
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from guardados_views import FavoritosView, CotizacionesView

def route_change(e):
    page.views.clear()

    if page.route == "/":
        page.views.append(HomeView(page))
    elif page.route == "/mantenimiento":
        page.views.append(MantenimientoView(page))
    elif page.route == "/favoritos":
        page.views.append(FavoritosView(page))
    elif page.route == "/cotizaciones":
        page.views.append(CotizacionesView(page))
    # /producto/{id} se maneja con page.views.append() directo,
    # no necesita estar aquí.

    page.update()

def view_pop(e):
    page.views.pop()
    top = page.views[-1]
    page.go(top.route)

page.on_route_change = route_change
page.on_view_pop     = view_pop
page.go(page.route)
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2.  Tu vista de productos  ─ card con on_click + botón guardar
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import flet as ft
from producto_detalle import abrir_detalle
from session_store    import toggle_favorito, es_favorito

BG_COLOR        = "#0c0f14"
CONTAINER_COLOR = "#141821"
COFFEE_COLOR    = "#c29b76"
TEXT_PRIMARY    = "#f3f4f6"
TEXT_SECONDARY  = "#9ca3af"


def ProductoCard(page: ft.Page, producto: dict) -> ft.Container:
    """
    Reemplaza tu card actual con este widget.
    Cada card tiene:
      - on_click → abre ProductoDetalleView
      - ícono bookmark → guarda/quita de favoritos
    """
    save_ref = ft.Ref[ft.IconButton]()

    def on_tap(e):
        abrir_detalle(page, producto)          # ← abre la vista de detalle

    def on_guardar(e):
        guardado = toggle_favorito(page, producto)
        save_ref.current.icon       = ft.Icons.BOOKMARK if guardado else ft.Icons.BOOKMARK_BORDER
        save_ref.current.icon_color = COFFEE_COLOR if guardado else TEXT_SECONDARY
        page.update()

    ya_guardado = es_favorito(page, producto["id"])

    return ft.Container(
        content=ft.Column(
            [
                # Imagen
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
                # Info
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
                                        icon=ft.Icons.BOOKMARK if ya_guardado
                                             else ft.Icons.BOOKMARK_BORDER,
                                        icon_color=COFFEE_COLOR if ya_guardado
                                                   else TEXT_SECONDARY,
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
        on_click=on_tap,                       # ← tap en toda la card
        shadow=ft.BoxShadow(blur_radius=8, color="#00000055", offset=ft.Offset(0, 3)),
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3.  MantenimientoView  ─ guardar cotización al generar resumen
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
# Agrega este import al inicio de mantenimiento.py:
from session_store import guardar_cotizacion

# Modifica la función generar_resumen():
def generar_resumen(e):
    total = 0
    seleccionados = []
    ...
    for cb in checkboxes:
        if cb.value:
            hay_seleccion = True
            total += cb.data["precioBase"]
            seleccionados.append(cb.data)       # ← agrega esta línea
            ...

    if hay_seleccion:
        guardar_cotizacion(page, seleccionados, total)   # ← guarda en sesión
    ...
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4.  Navbar  ─ botones de acceso a favoritos y cotizaciones
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
# Dentro de tu componente Navbar, agrega estos iconos al row de acciones:

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
"""
