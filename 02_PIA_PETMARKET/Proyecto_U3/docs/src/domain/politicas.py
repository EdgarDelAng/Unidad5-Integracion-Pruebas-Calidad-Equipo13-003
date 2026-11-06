"""Reglas del ciclo de vida, separadas de la coordinación de la aplicación."""
from .model import EstadoPedido,EstadoPreparacion,ReglaNegocioError
ESTADOS_CANCELABLES=frozenset((EstadoPedido.PAGADO,EstadoPedido.PREPARADO,EstadoPedido.EMPACADO))
def es_cancelable(estado:EstadoPedido)->bool:
    return estado in ESTADOS_CANCELABLES
def validar_salida(estado:EstadoPedido)->None:
    if estado!=EstadoPedido.EMPACADO:raise ReglaNegocioError('El despacho requiere EMPACADO')
def validar_preparacion(estado:EstadoPedido)->None:
    if estado!=EstadoPedido.PAGADO:raise ReglaNegocioError('La preparación requiere pago aprobado')
def validar_empaque(estado:EstadoPreparacion)->None:
    if estado!=EstadoPreparacion.PREPARADO:raise ReglaNegocioError('El empaque requiere PREPARADO')
