from collections import Counter
from .model import ReglaNegocioError

def validar_distribucion(detalles, distribucion):
    requerido = Counter()
    for detalle in detalles:
        requerido[detalle.producto_sku] += detalle.cantidad

    asignado = Counter()
    for almacen_id, lineas in distribucion.items():
        if not isinstance(almacen_id, str) or not almacen_id.strip():
            raise ReglaNegocioError("El almacén es obligatorio")
        if not isinstance(lineas, dict) or not lineas:
            raise ReglaNegocioError("Cada almacén debe tener productos asignados")
        for sku, cantidad in lineas.items():
            if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
                raise ReglaNegocioError("Asignación inválida")
            asignado[sku] += cantidad

    if dict(requerido) != dict(asignado):
        raise ReglaNegocioError("Asignación incompleta, excedida o con SKU inexistente")
    return dict(asignado)
