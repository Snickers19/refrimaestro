import flet as ft
from urllib.parse import quote

# ── Colores compartidos (importar desde tu constants.py o definir aquí) ───────
BG_COLOR        = "#0c0f14"
CONTAINER_COLOR = "#141821"
COFFEE_COLOR    = "#c29b76"
TEXT_PRIMARY    = "#f3f4f6"
TEXT_SECONDARY  = "#9ca3af"
ACCENT_BG       = "#1f2430"

# ── Datos de contacto ─────────────────────────────────────────────────────────
WHATSAPP_NRO  = "+56973982493"          # ← reemplaza con tu número
EMAIL_DESTINO = "ayuda.refrimaestro@gmail.com"     # ← reemplaza con tu correo


# ─────────────────────────────────────────────────────────────────────────────
#  Vista de detalle del producto
#  Uso:  abrir_detalle(page, producto_dict)
# ─────────────────────────────────────────────────────────────────────────────
def ProductoDetalleView(page: ft.Page, producto: dict) -> ft.View:
    """
    Empuja una nueva ft.View sobre el stack de navegación.
    El botón ← llama a page.views.pop() para volver.

    producto = {
        "id":          str,
        "nombre":      str,
        "descripcion": str,
        "precio":      str,
        "imagen":      str  (URL o ruta local)
    }
    """

    # ── Handlers de contacto ──────────────────────────────────────────────────
    def on_back(e):
        page.views.pop()
        page.update()

    def on_whatsapp(e):
        msg = (
            f"Hola, me interesa el refrigerador *{producto['nombre']}* "
            f"(Precio: {producto['precio']}). ¿Está disponible?"
        )
        url = f"https://wa.me/{WHATSAPP_NRO}?text={quote(msg)}"
        page.launch_url(url)

    def on_email(e):
        subject = quote(f"Consulta sobre {producto['nombre']}")
        body    = quote(
            f"Hola,\n\nMe interesa el modelo {producto['nombre']} "
            f"con precio {producto['precio']}.\n\nPor favor contáctenme.\n\nGracias."
        )
        page.launch_url(f"mailto:{EMAIL_DESTINO}?subject={subject}&body={body}")

    # ── Botón guardar en favoritos ────────────────────────────────────────────
    favoritos   = page.session.get("favoritos") or []
    ya_guardado = any(f["id"] == producto["id"] for f in favoritos)

    save_icon = ft.Ref[ft.IconButton]()

    def on_guardar(e):
        favs = page.session.get("favoritos") or []
        ids  = [f["id"] for f in favs]
        if producto["id"] not in ids:
            favs.append(producto)
            page.session.set("favoritos", favs)
            save_icon.current.icon       = ft.Icons.BOOKMARK
            save_icon.current.icon_color = COFFEE_COLOR
            save_icon.current.tooltip    = "Guardado en favoritos"
        else:
            favs = [f for f in favs if f["id"] != producto["id"]]
            page.session.set("favoritos", favs)
            save_icon.current.icon       = ft.Icons.BOOKMARK_BORDER
            save_icon.current.icon_color = TEXT_SECONDARY
            save_icon.current.tooltip    = "Guardar en favoritos"
        page.update()

    # ── UI ────────────────────────────────────────────────────────────────────
    top_bar = ft.Container(
        content=ft.Row(
            [
                # ← Volver
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                    icon_color=TEXT_PRIMARY,
                    icon_size=20,
                    tooltip="Volver",
                    on_click=on_back,
                ),
                # Título corto centrado
                ft.Text(
                    producto["nombre"],
                    size=16,
                    weight=ft.FontWeight.W_600,
                    color=TEXT_PRIMARY,
                    expand=True,
                    text_align=ft.TextAlign.CENTER,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                # Acciones rápidas
                ft.Row(
                    [
                        ft.IconButton(
                            ref=save_icon,
                            icon=ft.Icons.BOOKMARK if ya_guardado else ft.Icons.BOOKMARK_BORDER,
                            icon_color=COFFEE_COLOR if ya_guardado else TEXT_SECONDARY,
                            icon_size=22,
                            tooltip="Guardar en favoritos" if not ya_guardado else "Quitar de favoritos",
                            on_click=on_guardar,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CHAT_ROUNDED,
                            icon_color="#25D366",          # verde WhatsApp
                            icon_size=22,
                            tooltip="Consultar por WhatsApp",
                            on_click=on_whatsapp,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.EMAIL_OUTLINED,
                            icon_color=COFFEE_COLOR,
                            icon_size=22,
                            tooltip="Enviar correo",
                            on_click=on_email,
                        ),
                    ],
                    spacing=0,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=CONTAINER_COLOR,
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        border=ft.border.only(bottom=ft.BorderSide(1, "#2a2d36")),
    )

    # Imagen con zoom (fit=CONTAIN dentro de un contenedor grande)
    imagen_hero = ft.Container(
        content=ft.Image(
            src=producto.get("imagen", "https://via.placeholder.com/400x300"),
            fit=ft.ImageFit.CONTAIN,
            expand=True,
        ),
        bgcolor="#0a0d11",
        border_radius=ft.border_radius.only(bottom_left=16, bottom_right=16),
        height=320,
        margin=ft.margin.only(bottom=16),
    )

    info_card = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    producto["nombre"],
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY,
                ),
                ft.Container(height=6),
                ft.Text(
                    producto.get("descripcion", "Sin descripción disponible."),
                    size=14,
                    color=TEXT_SECONDARY,
                ),
                ft.Container(height=14),
                ft.Text(
                    producto["precio"],
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=COFFEE_COLOR,
                ),
            ]
        ),
        bgcolor=CONTAINER_COLOR,
        border_radius=16,
        padding=20,
        margin=ft.margin.symmetric(horizontal=16),
        border=ft.border.all(1, "#2a2d36"),
    )

    # Botones de acción principales (más visibles)
    action_buttons = ft.Container(
        content=ft.Row(
            [
                ft.ElevatedButton(
                    text="WhatsApp",
                    icon=ft.Icons.CHAT_ROUNDED,
                    on_click=on_whatsapp,
                    style=ft.ButtonStyle(
                        bgcolor="#1a3a22",
                        color="#25D366",
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.padding.symmetric(horizontal=20, vertical=14),
                        side=ft.border.BorderSide(1, "#25D366"),
                    ),
                    expand=True,
                ),
                ft.Container(width=12),
                ft.ElevatedButton(
                    text="Correo",
                    icon=ft.Icons.EMAIL_OUTLINED,
                    on_click=on_email,
                    style=ft.ButtonStyle(
                        bgcolor=ACCENT_BG,
                        color=COFFEE_COLOR,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.padding.symmetric(horizontal=20, vertical=14),
                        side=ft.border.BorderSide(1, COFFEE_COLOR),
                    ),
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        margin=ft.margin.symmetric(horizontal=16, vertical=16),
    )

    return ft.View(
        route=f"/producto/{producto['id']}",
        bgcolor=BG_COLOR,
        padding=0,
        controls=[
            ft.Column(
                [
                    top_bar,
                    imagen_hero,
                    info_card,
                    action_buttons,
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=0,
                expand=True,
            )
        ],
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Helper para abrir la vista desde cualquier lugar
# ─────────────────────────────────────────────────────────────────────────────
def abrir_detalle(page: ft.Page, producto: dict):
    """Llama esta función en on_click del container del producto."""
    page.views.append(ProductoDetalleView(page, producto))
    page.update()
