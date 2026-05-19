import flet as ft
from views.home import HomeView
from views.mantenimiento import MantenimientoView
from views.contacto import ContactoView
from guardados_views import FavoritosView, CotizacionesView

# Paleta de colores globales
BG_COLOR = "#0c0f14"
CONTAINER_COLOR = "#141821"
NAV_COLOR = "#18191b"
COFFEE_COLOR = "#c29b76" # Un color café elegante
TEXT_PRIMARY = "#f3f4f6"
TEXT_SECONDARY = "#9ca3af"

def main(page: ft.Page):
    # Configuración principal de la página
    page.title = "Refri Maestro | Reparaciones y Ventas"
    page.favicon = "refrigerator-photos/Refrimaestro.png" 
    page.padding = 0
    page.spacing = 0
    page.bgcolor = BG_COLOR
    
    # Configurar un tema "Premium App"
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(thumb_color=COFFEE_COLOR),
        font_family="Inter",
    )

    def route_change(route):
        page.views.clear()
        
        # Enrutamiento tipo aplicación
        if page.route == "/":
            view_content = HomeView(page)
        elif page.route == "/mantenimiento":
            view_content = MantenimientoView(page)
        elif page.route == "/contacto":
            view_content = ContactoView(page)
        elif page.route == "/favoritos":
            view_content = FavoritosView(page)
        elif page.route == "/cotizaciones":
            view_content = CotizacionesView(page)
        else:
            view_content = HomeView(page)
            
        if isinstance(view_content, ft.View):
            page.views.append(view_content)
        else:
            page.views.append(
                ft.View(
                    route=page.route,
                    controls=[view_content],
                    padding=0,
                    bgcolor=BG_COLOR,
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Inicializar la ruta en la raíz
    page.go(page.route)

# Lanzar la aplicación sirviendo la carpeta 'assets' local
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
