import flet as ft
from components.navbar import Navbar, Footer
from session_store import guardar_cotizacion

BG_COLOR = "#0c0f14"
CONTAINER_COLOR = "#141821"
NAV_COLOR = "#18191b"
COFFEE_COLOR = "#c29b76"
TEXT_PRIMARY = "#f3f4f6"
TEXT_SECONDARY = "#9ca3af"
ACCENT_BG = "#1f2430"

def MantenimientoView(page: ft.Page):
    servicios = [
        {"id": "revision", "nombre": "Visita Técnica / Revisión", "precioBase": 25000, "precioTxt": "$25.000"},
        {"id": "carga_gas", "nombre": "Recarga de Gas Refrigerante", "precioBase": 45000, "precioTxt": "$45.000"},
        {"id": "cambio_termostato", "nombre": "Cambio de Termostato", "precioBase": 35000, "precioTxt": "$35.000"},
        {"id": "limpieza", "nombre": "Mantenimiento y Limpieza Profunda", "precioBase": 30000, "precioTxt": "$30.000"},
        {"id": "cambio_motor", "nombre": "Cambio de Compresor (Motor)", "precioBase": 85000, "precioTxt": "Desde $85.000"},
    ]

    total_estimado = ft.Text("$0", size=24, weight=ft.FontWeight.BOLD, color=BG_COLOR,)  
    resumen_text = ft.Text("", font_family="monospace", size=13, color=TEXT_PRIMARY, selectable=True)
    resumen_container = ft.Container(
        content=resumen_text,
        bgcolor=ACCENT_BG,
        padding=20,
        border_radius=8,
        border=ft.border.all(1, "#2a2d36"),
        visible=False,
        margin=ft.margin.only(top=20)
    )

    checkboxes = []

    def format_clp(num):
        return f"${num:,.0f}".replace(",", ".")

    def calcular_total(e):
        total = 0
        for cb in checkboxes:
            if cb.value:
                total += cb.data["precioBase"]
        total_estimado.value = format_clp(total)
        page.update()

    def generar_resumen(e):
        total = 0
        seleccionados = []
        desglose = "Cotización de Servicio Técnico:\n"
        desglose += "-" * 40 + "\n"
        
        hay_seleccion = False
        for cb in checkboxes:
            if cb.value:
                hay_seleccion = True
                total += cb.data["precioBase"]
                seleccionados.append(cb.data)
                desglose += f"- {cb.data['nombre']}: {format_clp(cb.data['precioBase'])}\n"
        
        if not hay_seleccion:
            desglose = "Por favor selecciona al menos un servicio."
        else:
            guardar_cotizacion(page, seleccionados, total)
            desglose += "-" * 40 + "\n"
            desglose += f"Total Estimado: {format_clp(total)}\n\n"
            desglose += "*Nota: Estos valores son referenciales. El valor final depende de la visita técnica."
            
        resumen_text.value = desglose
        resumen_container.visible = True
        page.update()

    checkbox_controls = []
    for s in servicios:
        cb = ft.Checkbox(
            data=s,
            on_change=calcular_total,
            fill_color=COFFEE_COLOR,
            check_color=BG_COLOR,
        )
        checkboxes.append(cb)
        checkbox_controls.append(
            ft.Container(
                content=ft.Row(
                [cb,
                    ft.Text(f"{s['nombre']} ({s['precioTxt']})",
                        color=TEXT_PRIMARY,  # ✅ ahora sí se aplica
                        size=14,
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(horizontal=15, vertical=5),
                border=ft.border.all(1.5, "#2a2d36"),
                border_radius=8,
                bgcolor=BG_COLOR,
                margin=ft.margin.only(bottom=10),
            )
)


            

    pricing_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Servicio", weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("Descripción", weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)),
            ft.DataColumn(ft.Text("Valor Referencial", weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY)),
        ],
        rows=[
            ft.DataRow(cells=[ft.DataCell(ft.Text("Consulta base", color=TEXT_SECONDARY)), ft.DataCell(ft.Text("Evaluación y diagnóstico en domicilio.", color=TEXT_SECONDARY)), ft.DataCell(ft.Text("$15,000", color=COFFEE_COLOR, weight=ft.FontWeight.BOLD))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Cambio de filtro", color=TEXT_SECONDARY)), ft.DataCell(ft.Text("Cambio de pieza filtro para refrigeración", color=TEXT_SECONDARY)), ft.DataCell(ft.Text("$35,000", color=COFFEE_COLOR, weight=ft.FontWeight.BOLD))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Recarga de gas", color=TEXT_SECONDARY)), ft.DataCell(ft.Text("Detección/reparación de fugas y carga", color=TEXT_SECONDARY)), ft.DataCell(ft.Text("$45,000", color=COFFEE_COLOR, weight=ft.FontWeight.BOLD))]),
            ft.DataRow(cells=[ft.DataCell(ft.Text("Cambio de aceite", color=TEXT_SECONDARY)), ft.DataCell(ft.Text("Revisión de compresor y cambio de aceite", color=TEXT_SECONDARY)), ft.DataCell(ft.Text("$30,000", color=COFFEE_COLOR, weight=ft.FontWeight.BOLD))]),
        ],
        border=ft.border.all(1, "#2a2d36"),
        border_radius=12,
        heading_row_color=ACCENT_BG,
        expand=True,
    )

    return ft.Column(
        [
            Navbar(page, active_route="/mantenimiento"),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Servicio Técnico y Mantenimiento", size=32, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Text("Transparencia en nuestros precios. Conoce nuestras tarifas de revisión y reparación.", size=16, color=TEXT_SECONDARY),
                        ft.Container(height=20),
                        
                        ft.Container(
                            content=ft.Row([pricing_table], scroll=ft.ScrollMode.AUTO),
                            shadow=ft.BoxShadow(blur_radius=10, color="#000000"),
                            bgcolor=CONTAINER_COLOR,
                            border=ft.border.all(1, "#2a2d36"),
                            border_radius=12,
                            padding=10
                        ),
                        
                        ft.Container(height=40),
                        
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Cotizador Rápido", size=24, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                                    ft.Text("Selecciona los servicios para obtener un presupuesto aproximado.", color=TEXT_SECONDARY),
                                    ft.Container(height=10),
                                    
                                    ft.Column(checkbox_controls, spacing=0),
                                    
                                    ft.Container(
                                        content=ft.Row(
                                            [
                                                ft.Text("Total Estimado:", size=20, weight=ft.FontWeight.BOLD, color=BG_COLOR),
                                                total_estimado
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                        ),
                                        bgcolor=COFFEE_COLOR,
                                        padding=20,
                                        border_radius=12,
                                        margin=ft.margin.symmetric(vertical=20)
                                    ),
                                    
                                    ft.ElevatedButton(
                                        text="Obtener resumen",
                                        icon=ft.Icons.RECEIPT_LONG,
                                        on_click=generar_resumen,
                                        style=ft.ButtonStyle(
                                            bgcolor=ACCENT_BG,
                                            color=COFFEE_COLOR,
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.padding.all(20),
                                            side=ft.border.BorderSide(1, COFFEE_COLOR)
                                        ),
                                        width=float('inf')
                                    ),
                                    
                                    resumen_container
                                ]
                            ),
                            bgcolor=CONTAINER_COLOR,
                            padding=30,
                            border_radius=16,
                            border=ft.border.all(1, "#2a2d36"),
                            shadow=ft.BoxShadow(blur_radius=15, color="#000000", offset=ft.Offset(0, 4)),
                        )
                    ]
                ),
                padding=ft.padding.symmetric(horizontal=24, vertical=40),
            ),
            Footer(),
        ],
        scroll=ft.ScrollMode.AUTO,
    )
