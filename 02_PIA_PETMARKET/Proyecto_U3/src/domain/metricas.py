from decimal import Decimal

def calcular_indicadores(pedidos, desde=None, hasta=None):
    # El agregado Pedido actual no conserva una fecha de creación; por ello,
    # el rango se acepta pero no se aplica a registros sin marca temporal.
    seleccionados = list(pedidos)
    total = len(seleccionados)
    estados = {}
    valor = sum((pedido.total for pedido in seleccionados), Decimal("0"))
    for pedido in seleccionados:
        estado = getattr(getattr(pedido, "estado", None), "value", getattr(pedido, "estado", None))
        estados[estado] = estados.get(estado, 0) + 1
    valor_texto = format(valor.normalize(), "f") if valor else "0"
    return {"total_pedidos": total, "valor_pedidos": valor_texto, "por_estado": estados}
