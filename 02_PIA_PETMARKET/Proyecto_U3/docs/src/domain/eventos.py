"""Eventos registrados como hechos ocurridos, sin simular un bus distribuido."""
from dataclasses import dataclass,field
from datetime import datetime,timezone
from .identificadores import PedidoId
@dataclass(frozen=True)
class EventoPedido:
    pedido_id:PedidoId
    nombre:str="EventoPedido"
    ocurrido_en:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
@dataclass(frozen=True)
class PagoConfirmado(EventoPedido):
    nombre:str='PagoConfirmado'
@dataclass(frozen=True)
class CancelacionSolicitada(EventoPedido):
    nombre:str='CancelacionSolicitada'
@dataclass(frozen=True)
class EntregaFallida(EventoPedido):
    nombre:str='EntregaFallida'
