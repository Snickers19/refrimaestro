import flet as ft
from views.home import HomeView
from views.mantenimiento import MantenimientoView
from views.contacto import ContactoView

def main(page: ft.Page):
    page.title = "Refri Maestro | Reparaciones y Ventas"
    page.padding = 0
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.theme_mode = ft.ThemeMode.LIGHT

    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.LIGHT_BLUE,
        font_family="Inter",
        visual_density=ft.VisualDensity.COMFORTABLE,
        page_transitions=ft.PageTransitionsTheme(
            windows=ft.PageTransitionTheme.FADE_UPWARDS,
            macos=ft.PageTransitionTheme.FADE_UPWARDS,
            linux=ft.PageTransitionTheme.FADE_UPWARDS,
            android=ft.PageTransitionTheme.FADE_UPWARDS,
            ios=ft.PageTransitionTheme.FADE_UPWARDS,
        ),
    )

    def route_change(route):
        page.views.clear()
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
    page.go(page.route or "/")

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")