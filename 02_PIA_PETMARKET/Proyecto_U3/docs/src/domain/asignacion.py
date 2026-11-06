"""Validación pura de subórdenes por almacén (CA-08.02/03)."""
from collections import Counter
from collections.abc import Mapping
from .model import DetallePedido,ReglaNegocioError

def validar_distribucion(lineas:tuple[DetallePedido,...], reparto:Mapping[str,Mapping[str,int]])->dict[str,int]:
    esperado=Counter()
    for linea in lineas:esperado[linea.producto_sku]+=linea.cantidad
    obtenido=Counter()
    for almacen,productos in reparto.items():
        if not almacen.strip() or not productos:raise ReglaNegocioError('Almacén sin asignación válida')
        for sku,cantidad in productos.items():
            if sku not in esperado or not isinstance(cantidad,int) or isinstance(cantidad,bool) or cantidad<=0:
                raise ReglaNegocioError('Cantidad o SKU inválido en asignación')
            obtenido[sku]+=cantidad
    if dict(obtenido)!=dict(esperado):raise ReglaNegocioError('Asignación no cubre el pedido')
    return dict(obtenido)
