"""
session_store.py
────────────────
Gestión de estado global en memoria (page.session).
Vive mientras la app esté abierta. Se reinicia con la app.

  - Favoritos   : productos guardados por el usuario
  - Cotizaciones: últimos presupuestos calculados en MantenimientoView
"""
from datetime import datetime


# ─────────────────────────────────────────────────────────────────────────────
#  FAVORITOS
# ─────────────────────────────────────────────────────────────────────────────

def get_favoritos(page) -> list:
    return page.session.get("favoritos") or []


def toggle_favorito(page, producto: dict) -> bool:
    """
    Agrega o quita un producto de favoritos.
    Retorna True si quedó guardado, False si fue removido.
    """
    favs = get_favoritos(page)
    ids  = [f["id"] for f in favs]

    if producto["id"] in ids:
        favs = [f for f in favs if f["id"] != producto["id"]]
        page.session.set("favoritos", favs)
        return False   # removido
    else:
        favs.append(producto)
        page.session.set("favoritos", favs)
        return True    # guardado


def es_favorito(page, producto_id: str) -> bool:
    return any(f["id"] == producto_id for f in get_favoritos(page))


def limpiar_favoritos(page):
    page.session.set("favoritos", [])


# ─────────────────────────────────────────────────────────────────────────────
#  COTIZACIONES
# ─────────────────────────────────────────────────────────────────────────────

def guardar_cotizacion(page, servicios_seleccionados: list, total: int):
    """
    Guarda la cotización actual en sesión.

    servicios_seleccionados = [
        {"nombre": "Revisión", "precioBase": 25000},
        ...
    ]
    """
    cotizaciones = page.session.get("cotizaciones") or []

    cotizaciones.insert(0, {                      # más reciente primero
        "fecha"    : datetime.now().strftime("%d/%m/%Y %H:%M"),
        "servicios": servicios_seleccionados,
        "total"    : total,
    })

    # Conservar solo las últimas 10 cotizaciones
    page.session.set("cotizaciones", cotizaciones[:10])


def get_cotizaciones(page) -> list:
    return page.session.get("cotizaciones") or []


def limpiar_cotizaciones(page):
    page.session.set("cotizaciones", [])
