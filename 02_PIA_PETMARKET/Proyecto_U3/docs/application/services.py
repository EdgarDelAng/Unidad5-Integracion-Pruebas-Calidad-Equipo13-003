"""Servicios de aplicación: orquestan; las reglas siguen en el dominio.

IMPORTANTE: pago externo y reserva local NO forman una transacción distribuida;
se necesita diseño de compensación real validado con stakeholder/pasarela.
"""
from dataclasses import dataclass
from decimal import Decimal
from uuid import uuid4
from domain.model import Pedido,DetallePedido,Domicilio,Dinero,ReglaNegocioError,ExistenciaInventario,OrdenPreparacion
from domain.ports import PedidoRepository,InventarioRepository,PreparacionRepository,PasarelaPago,UnitOfWork

@dataclass(frozen=True)
class ConfirmarCompraCommand:
    pedido_id:str
    cliente_id:str
    detalles:tuple[DetallePedido,...]
    domicilio:Domicilio
    metodo_entrega:str
    costo_entrega:Dinero

@dataclass(frozen=True)
class SolicitarCancelacionCommand:
    pedido_id:str
    cliente_id:str
    motivo:str

@dataclass(frozen=True)
class ConsultarPedidoQuery:
    pedido_id:str

@dataclass(frozen=True)
class ConsultarPreparacionQuery:
    pedido_id:str

@dataclass(frozen=True)
class PedidoDetalleDTO:
    id:str
    estado:str
    total:str
    cantidad_lineas:int

class ConsultaPedidoHandler:
    def __init__(self,repo:PedidoRepository):self.repo=repo
    def ejecutar(self,q:ConsultarPedidoQuery)->PedidoDetalleDTO|None:
        p=self.repo.obtener(q.pedido_id)
        return None if p is None else PedidoDetalleDTO(p.id,p.estado.value,str(p.total),len(p.detalles))

class ConsultaPreparacionHandler:
    def __init__(self,preparacion:PreparacionRepository):self.preparacion=preparacion
    def ejecutar(self,q:ConsultarPreparacionQuery)->list[dict]:
        return [{'almacen':o.almacen_id,'estado':o.estado.value,'lineas':dict(o.lineas)} for o in self.preparacion.listar_por_pedido(q.pedido_id)]

class SolicitarCancelacionHandler:
    def __init__(self,pedidos:PedidoRepository):self.pedidos=pedidos
    def ejecutar(self,c:SolicitarCancelacionCommand)->str:
        pedido=self.pedidos.obtener(c.pedido_id)
        if pedido is None or pedido.cliente_id!=c.cliente_id:raise ReglaNegocioError('Pedido no disponible para el cliente')
        pedido.solicitar_cancelacion(c.motivo)
        self.pedidos.guardar(pedido)
        return pedido.estado.value

class ConfirmarCompraHandler:
    def __init__(self,pedidos:PedidoRepository,almacenes:InventarioRepository,preparacion:PreparacionRepository,pagos:PasarelaPago,uow:UnitOfWork):
        self.pedidos,self.almacenes,self.preparacion,self.pagos,self.uow=pedidos,almacenes,preparacion,pagos,uow
    def ejecutar(self,c:ConfirmarCompraCommand,distribucion:dict[str,dict[str,int]])->str:
        """Distribución se obtiene de una política validada externamente, no se adivina.

        La reserva de existencias del prototipo ocurre después de la respuesta aprobada.
        No existe garantía de concurrencia ni idempotencia real en estos adaptadores.
        """
        pedido=Pedido(c.pedido_id,c.cliente_id,c.detalles,c.domicilio,c.metodo_entrega,c.costo_entrega)
        requerido: dict[str,int]={}
        for detalle in c.detalles:
            requerido[detalle.producto_sku]=requerido.get(detalle.producto_sku,0)+detalle.cantidad
        asignado={sku:0 for sku in requerido}
        for almacen,lineas in distribucion.items():
            for sku,qty in lineas.items():
                if sku not in asignado or qty<=0:raise ReglaNegocioError('Asignación inválida')
                asignado[sku]+=qty
        if asignado!=requerido:raise ReglaNegocioError('Asignación no cubre las líneas del pedido')
        # Validación completa antes de mutar inventario
        existencias=[]
        for almacen,lineas in distribucion.items():
            for sku,qty in lineas.items():
                ex=self.almacenes.obtener(almacen,sku)
                if ex is None or ex.disponible<qty:raise ReglaNegocioError('Inventario insuficiente')
                existencias.append((ex,qty))
        # 1) Fase local: registrar pedido pendiente antes del cobro remoto.
        # UnitOfWorkEnMemoria solo registra eventos: NO implementa ACID.
        self.uow.iniciar()
        try:
            self.pedidos.guardar(pedido)
            self.uow.confirmar()
        except Exception:
            self.uow.revertir()
            raise

        # 2) Cobro externo fuera de toda transacción de almacenamiento local.
        # Si no hay respuesta, el pedido sigue PENDIENTE_PAGO y se requiere
        # conciliación manual o un mecanismo idempotente que aquí no se simula.
        aprobado=self.pagos.cobrar(pedido.id,str(pedido.total))

        # 3) Nueva unidad local para aplicar el resultado del cobro.
        self.uow.iniciar()
        try:
            pedido.registrar_pago(aprobado)
            if aprobado:
                # La disponibilidad se revalida antes de actualizar existencias.
                # El tratamiento de conflictos posteriores a un cargo remoto
                # requiere conciliación, no reembolso implícito.
                for ex,qty in existencias:
                    if ex.disponible<qty:
                        raise ReglaNegocioError('Stock cambió después del cobro: requiere conciliación')
                for ex,qty in existencias:
                    ex.reservar(qty)
                    self.almacenes.guardar(ex)
                for almacen,lineas in distribucion.items():
                    self.preparacion.guardar(OrdenPreparacion(str(uuid4()),pedido.id,almacen,dict(lineas)))
            self.pedidos.guardar(pedido)
            self.uow.confirmar()
            return pedido.estado.value
        except Exception:
            self.uow.revertir()
            raise
