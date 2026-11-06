"""Pasarela determinista para pruebas, no gateway comercial real."""
from .memory import PasarelaSimulada
class PasarelaSinRespuesta:
    def cobrar(self,pedido_id:str,monto:str):
        raise TimeoutError('La pasarela no confirmó el cobro')
