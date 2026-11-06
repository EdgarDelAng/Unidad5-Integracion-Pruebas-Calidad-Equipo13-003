"""Cálculos para indicadores agregados de pedidos (CA-18)."""
from collections import Counter
from datetime import datetime
from decimal import Decimal
from .model import Pedido

def calcular_indicadores(pedidos:list[Pedido],desde:datetime|None=None,hasta:datetime|None=None)->dict:
    seleccion=[]
    for pedido in pedidos:
        if not pedido.historial:continue
        creado=pedido.historial[0][0]
        if desde is not None and creado<desde:continue
        if hasta is not None and creado>hasta:continue
        seleccion.append(pedido)
    return {'total_pedidos':len(seleccion),'valor_pedidos':str(sum((p.total for p in seleccion),Decimal('0'))),
            'por_estado':dict(sorted(Counter(p.estado.value for p in seleccion).items()))}
