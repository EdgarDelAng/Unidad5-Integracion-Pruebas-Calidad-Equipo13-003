"""Construcción explícita de colaboradores; demuestra inversión de dependencias."""
from .memory import MemoriaPedidoRepository,MemoriaInventarioRepository,MemoriaPreparacionRepository,PasarelaSimulada
from .repositorios_memoria import MemoriaEnvioRepository
from .transacciones import UnidadTrabajoSnapshot
from application.cancelaciones import CancelacionesApplicationService
from application.preparacion import PreparacionApplicationService
from application.logistica import LogisticaApplicationService
from application.consultas import ConsultasApplicationService
from application.indicadores import IndicadoresApplicationService
class ContenedorAplicacion:
    def __init__(self,existencias=()):
        self.pedidos=MemoriaPedidoRepository()
        self.inventario=MemoriaInventarioRepository(existencias)
        self.preparacion=MemoriaPreparacionRepository()
        self.envios=MemoriaEnvioRepository()
        self.uow=UnidadTrabajoSnapshot(self.pedidos,self.inventario,self.preparacion,self.envios)
        self.pasarela=PasarelaSimulada()
        self.cancelaciones=CancelacionesApplicationService(self.pedidos)
        self.preparar=PreparacionApplicationService(self.preparacion)
        self.logistica=LogisticaApplicationService(self.pedidos,self.envios)
        self.consultas=ConsultasApplicationService(self.pedidos,self.envios)
        self.indicadores=IndicadoresApplicationService(self.pedidos)
