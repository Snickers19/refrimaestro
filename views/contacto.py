import flet as ft
from components.navbar import Navbar, Footer
import urllib.request
import json

BG_COLOR = "#0c0f14"
CONTAINER_COLOR = "#141821"
NAV_COLOR = "#18191b"
COFFEE_COLOR = "#c29b76"
TEXT_PRIMARY = "#f3f4f6"
TEXT_SECONDARY = "#9ca3af"
ACCENT_BG = "#1f2430"

def ContactoView(page: ft.Page):
    WEBHOOK_URL = "https://connect.pabbly.com/workflow/sendwebhookdata/IjU3NjYwNTY4MDYzZjA0Mzc1MjZkNTUzNjUxMzMi_pc" 
    FORMSUBMIT_URL = "https://formsubmit.co/ajax/sebastian.fernandez.e@gmail.com"

    tf_nombre = ft.TextField(label="Nombre Completo", hint_text="Ej: Juan Pérez", border_radius=8, prefix_icon=ft.Icons.PERSON_OUTLINE, border_color="#2a2d36", focused_border_color=COFFEE_COLOR, color=TEXT_PRIMARY)
    tf_email = ft.TextField(label="Tu Correo Electrónico", hint_text="ejemplo@correo.com", border_radius=8, prefix_icon=ft.Icons.EMAIL_OUTLINED, border_color="#2a2d36", focused_border_color=COFFEE_COLOR, color=TEXT_PRIMARY)
    tf_telefono = ft.TextField(label="Teléfono (opcional)", hint_text="Ej: +56 9 1234 5678", border_radius=8, prefix_icon=ft.Icons.PHONE_OUTLINED, border_color="#2a2d36", focused_border_color=COFFEE_COLOR, color=TEXT_PRIMARY)
    tf_mensaje = ft.TextField(label="Mensaje o Consulta", multiline=True, min_lines=5, max_lines=8, border_radius=8, border_color="#2a2d36", focused_border_color=COFFEE_COLOR, color=TEXT_PRIMARY)

    def enviar_mensaje(e):
        if not tf_nombre.value or not tf_email.value or not tf_mensaje.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor completa todos los campos obligatorios.", color=TEXT_PRIMARY), bgcolor="#7f1d1d")
            page.snack_bar.open = True
            page.update()
            return

        btn_enviar.disabled = True
        btn_enviar.text = "Enviando..."
        page.update()

        data = {
            "nombre": tf_nombre.value,
            "email": tf_email.value,
            "telefono": tf_telefono.value,
            "mensaje": tf_mensaje.value,
            "_subject": "Nuevo mensaje desde la App Flet de Refrigeradores!"
        }

        url_destino = WEBHOOK_URL if WEBHOOK_URL else FORMSUBMIT_URL
        
        try:
            req = urllib.request.Request(url_destino)
            req.add_header('Content-Type', 'application/json')
            req.add_header('Accept', 'application/json')
            jsondata = json.dumps(data).encode('utf-8')
            
            urllib.request.urlopen(req, jsondata)
            
            tf_nombre.value = ""
            tf_email.value = ""
            tf_telefono.value = ""
            tf_mensaje.value = ""
            
            page.snack_bar = ft.SnackBar(
                ft.Text("¡Mensaje enviado con éxito! Te contactaremos a la brevedad.", color=BG_COLOR), 
                bgcolor=COFFEE_COLOR
            )
            page.snack_bar.open = True
            
        except Exception as ex:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Hubo un error al enviar: {str(ex)}", color=TEXT_PRIMARY), 
                bgcolor="#7f1d1d"
            )
            page.snack_bar.open = True
            
        finally:
            btn_enviar.disabled = False
            btn_enviar.text = "Enviar Mensaje ✉"
            page.update()

    btn_enviar = ft.ElevatedButton(
        text="Enviar Mensaje ✉",
        on_click=enviar_mensaje,
        style=ft.ButtonStyle(
            bgcolor=COFFEE_COLOR,
            color=BG_COLOR,
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.padding.all(20)
        ),
        width=float('inf')
    )

    info_directa = ft.Container(
        content=ft.Column(
            [
                ft.Text("Información Directa", size=20, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                ft.Text("Puedes escribirnos directamente a nuestro correo o llamarnos a nuestro número telefónico.", color=TEXT_SECONDARY),
                ft.Container(height=10),
                
                ft.Row([ft.Icon(ft.Icons.PHONE, color=COFFEE_COLOR), ft.Text("+56 9 7398 2493", size=16, weight=ft.FontWeight.W_600, color=TEXT_PRIMARY)]),
                ft.Row([ft.Icon(ft.Icons.EMAIL, color=COFFEE_COLOR), ft.Text("ayuda.refrimaestro@gmail.com", size=16, weight=ft.FontWeight.W_600, color=TEXT_PRIMARY)]),
                
                ft.Container(height=20),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Horario de atención:", weight=ft.FontWeight.BOLD, color=COFFEE_COLOR),
                            ft.Text("Lunes a Viernes: 09:30 - 18:00 hrs.", color=TEXT_PRIMARY),
                            ft.Text("Sábado: 10:00 - 14:00 hrs.", color=TEXT_PRIMARY),
                        ]
                    ),
                    bgcolor=ACCENT_BG,
                    padding=20,
                    border_radius=8,
                    border=ft.border.all(1, "#362b21")
                )
            ]
        ),
        bgcolor=CONTAINER_COLOR,
        padding=30,
        border_radius=16,
        border=ft.border.all(1, "#2a2d36"),
        shadow=ft.BoxShadow(blur_radius=15, color="#000000", offset=ft.Offset(0, 4)),
    )

    formulario = ft.Container(
        content=ft.Column(
            [
                ft.Text("Envíanos un Mensaje", size=20, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                ft.Container(height=10),
                tf_nombre,
                tf_email,
                tf_telefono,
                tf_mensaje,
                btn_enviar
            ]
        ),
        bgcolor=CONTAINER_COLOR,
        padding=30,
        border_radius=16,
        border=ft.border.all(1, "#2a2d36"),
        shadow=ft.BoxShadow(blur_radius=15, color="#000000", offset=ft.Offset(0, 4)),
    )

    return ft.Column(
        [
            Navbar(page, active_route="/contacto"),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Ponte en Contacto", size=32, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                        ft.Text("¿Tienes alguna duda o necesitas asistencia? Completa el formulario y te ayudaremos.", size=16, color=TEXT_SECONDARY),
                        ft.Container(height=20),
                        
                        ft.ResponsiveRow(
                            [
                                ft.Container(content=info_directa, col={"xs": 12, "md": 6}),
                                ft.Container(content=formulario, col={"xs": 12, "md": 6}),
                            ],
                            spacing=24,
                            run_spacing=24,
                        )
                    ]
                ),
                padding=ft.padding.symmetric(horizontal=24, vertical=40),
            ),
            Footer(),
        ],
        scroll=ft.ScrollMode.AUTO,
    )
