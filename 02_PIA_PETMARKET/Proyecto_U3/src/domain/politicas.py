from .model import EstadoPedido
def es_cancelable(estado):
    return estado in {EstadoPedido.PAGADO,EstadoPedido.PREPARADO,EstadoPedido.EMPACADO}
