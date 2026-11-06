"""Implementaciones de referencia sin SQL ni acceso a red."""
from .memory import MemoriaPedidoRepository,MemoriaInventarioRepository,MemoriaPreparacionRepository
class MemoriaEnvioRepository:
    def __init__(self):self.datos={}
    def obtener(self,envio_id:str):return self.datos.get(envio_id)
    def guardar(self,envio):self.datos[envio.id]=envio
    def listar(self):return list(self.datos.values())
