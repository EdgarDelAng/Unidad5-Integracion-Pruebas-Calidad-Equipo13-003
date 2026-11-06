"""Orquestación del registro de salida y resultado de entrega."""
from domain.model import Envio,ReglaNegocioError
from .contratos import EstadoEnvioDTO
class LogisticaApplicationService:
    def __init__(self,pedidos,envios):self.pedidos,self.envios=pedidos,envios
    def despachar(self,pedido_id:str,envio_id:str)->EstadoEnvioDTO:
        pedido=self.pedidos.obtener(pedido_id)
        if pedido is None:raise ReglaNegocioError('Pedido inexistente')
        envio=Envio(envio_id,pedido.id);envio.iniciar(pedido)
        self.pedidos.guardar(pedido);self.envios.guardar(envio)
        return EstadoEnvioDTO(envio.id,pedido.id,envio.estado,len(envio.incidencias))
    def finalizar(self,pedido_id:str,envio_id:str,exitosa:bool,motivo:str='')->EstadoEnvioDTO:
        pedido=self.pedidos.obtener(pedido_id);envio=self.envios.obtener(envio_id)
        if pedido is None or envio is None or envio.pedido_id!=pedido_id:
            raise ReglaNegocioError('No se localizó el envío del pedido')
        if exitosa:envio.completar(pedido)
        else:envio.registrar_falla(pedido,motivo)
        self.pedidos.guardar(pedido);self.envios.guardar(envio)
        return EstadoEnvioDTO(envio.id,pedido.id,envio.estado,len(envio.incidencias))
