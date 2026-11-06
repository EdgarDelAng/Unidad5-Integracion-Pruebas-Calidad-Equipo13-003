"""Orquesta solicitud del cliente y autorización posterior del administrador."""
from domain.model import ReglaNegocioError
from .autorizacion import Actor,exigir_admin,exigir_cliente
from .contratos import ResultadoCancelacion
class CancelacionesApplicationService:
    def __init__(self,pedidos):self.pedidos=pedidos
    def solicitar(self,actor:Actor,pedido_id:str,motivo:str)->ResultadoCancelacion:
        pedido=self.pedidos.obtener(pedido_id)
        if pedido is None:raise ReglaNegocioError('Pedido inexistente')
        exigir_cliente(actor,pedido.cliente_id)
        pedido.solicitar_cancelacion(motivo)
        self.pedidos.guardar(pedido)
        return ResultadoCancelacion(pedido.id,pedido.estado.value,True)
    def autorizar(self,actor:Actor,pedido_id:str)->ResultadoCancelacion:
        exigir_admin(actor)
        pedido=self.pedidos.obtener(pedido_id)
        if pedido is None:raise ReglaNegocioError('Pedido inexistente')
        pedido.autorizar_cancelacion(actor.identificador)
        self.pedidos.guardar(pedido)
        return ResultadoCancelacion(pedido.id,pedido.estado.value,False)
