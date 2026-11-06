"""Clasificación del resultado sin filtrar excepciones tecnológicas al negocio."""
from dataclasses import dataclass
@dataclass(frozen=True)
class ErrorAplicacion:
    codigo:str
    descripcion:str
ERRORES={
 'PAGO_RECHAZADO':ErrorAplicacion('PAGO_RECHAZADO','Pago no aprobado; el pedido permanece pendiente.'),
 'STOCK_INSUFICIENTE':ErrorAplicacion('STOCK_INSUFICIENTE','No se cubren las cantidades solicitadas.'),
 'CANCELACION_NO_PERMITIDA':ErrorAplicacion('CANCELACION_NO_PERMITIDA','El estado del pedido no permite cancelarlo.'),
 'AUTORIZACION_DENEGADA':ErrorAplicacion('AUTORIZACION_DENEGADA','El actor no está autorizado.'),
 'RESULTADO_INCIERTO':ErrorAplicacion('RESULTADO_INCIERTO','No se confirmó el resultado de la operación externa.'),
}
