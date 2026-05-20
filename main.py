import flet as ft
from views.home import HomeView
from views.mantenimiento import MantenimientoView
from views.contacto import ContactoView

def main(page: ft.Page):
    # Configuración principal de la página
    page.title = "Refri Maestro | Reparaciones y Ventas"
    page.padding = 0
    # CORRECCIÓN: ft.colors en minúsculas
    page.bgcolor = ft.colors.BLUE_GREY_50
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Configurar un tema "Premium App"
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.LIGHT_BLUE,
        font_family="Inter",
        visual_density=ft.ThemeVisualDensity.COMFORTABLE,
        page_transitions=ft.PageTransitionsTheme(
            windows=ft.PageTransitionTheme.FADE_UPWARDS,
            macos=ft.PageTransitionTheme.FADE_UPWARDS,
            linux=ft.PageTransitionTheme.FADE_UPWARDS,
            android=ft.PageTransitionTheme.FADE_UPWARDS,
            ios=ft.PageTransitionTheme.FADE_UPWARDS,
        ),
    )

    # Contenedor principal donde inyectaremos las vistas
    main_container = ft.AnimatedSwitcher(
        content=ft.Container(),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=300,
        reverse_duration=300,
        switch_in_curve=ft.AnimationCurve.EASE_IN_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN_OUT,
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
        else:
            view_content = HomeView(page)
            
        page.views.append(
            ft.View(
                route=page.route,
                controls=[view_content],
                padding=0,
                bgcolor=page.bgcolor,
                scroll=ft.ScrollMode.AUTO,
            )
        )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # CORRECCIÓN: Evitamos pasar None a page.go()
    page.go(page.route or "/")

# Lanzar la aplicación sirviendo la carpeta 'assets' local
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")