"""Adaptadores EN MEMORIA, únicamente demostración de arquitectura.
No simulan de forma segura atomicidad distribuida con un banco real.
"""
from __future__ import annotations
from copy import deepcopy
from domain.model import Pedido,ExistenciaInventario,OrdenPreparacion
class MemoriaPedidoRepository:
    def __init__(self):self.datos={}
    def guardar(self,pedido:Pedido):self.datos[pedido.id]=pedido
    def obtener(self,pedido_id):return self.datos.get(pedido_id)
    def listar(self):return list(self.datos.values())
class MemoriaInventarioRepository:
    def __init__(self,existencias=()):self.datos={(i.almacen_id,i.producto_sku):i for i in existencias}
    def guardar(self,ex):self.datos[ex.almacen_id,ex.producto_sku]=ex
    def obtener(self,almacen_id,sku):return self.datos.get((almacen_id,sku))
class MemoriaPreparacionRepository:
    def __init__(self):self.datos={}
    def guardar(self,orden):self.datos[orden.id]=orden
    def listar_por_pedido(self,pedido_id):return [o for o in self.datos.values() if o.pedido_id==pedido_id]
    def obtener(self,orden_id):return self.datos.get(orden_id)
class PasarelaSimulada:
    def __init__(self,aprobado=True):self.aprobado=aprobado;self.operaciones=[]
    def cobrar(self,pedido_id,monto):self.operaciones.append((pedido_id,monto));return self.aprobado
class UnitOfWorkEnMemoria:
    """Solo controla llamada conceptual; no es una transacción ACID."""
    def __init__(self):self.eventos=[]
    def iniciar(self):self.eventos.append('iniciar')
    def confirmar(self):self.eventos.append('confirmar')
    def revertir(self):self.eventos.append('revertir')
