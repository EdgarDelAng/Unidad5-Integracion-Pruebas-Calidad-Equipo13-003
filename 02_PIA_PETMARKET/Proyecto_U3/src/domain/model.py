from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from datetime import datetime, timezone

class ReglaNegocioError(ValueError):
    """Incumplimiento de una regla del dominio."""

class EstadoPedido(str, Enum):
    PENDIENTE_PAGO='PENDIENTE_PAGO'; PAGADO='PAGADO'; PREPARADO='PREPARADO'; EMPACADO='EMPACADO'; EN_TRANSITO='EN_TRANSITO'; ENTREGADO='ENTREGADO'; ENTREGA_FALLIDA='ENTREGA_FALLIDA'; CANCELACION_SOLICITADA='CANCELACION_SOLICITADA'; CANCELADO='CANCELADO'
class EstadoPago(str, Enum):
    PENDIENTE='PENDIENTE'; APROBADO='APROBADO'; RECHAZADO='RECHAZADO'
class EstadoPreparacion(str, Enum):
    PENDIENTE='PENDIENTE'; EN_PREPARACION='EN_PREPARACION'; PREPARADO='PREPARADO'; EMPACADO='EMPACADO'
class EstadoEnvio(str, Enum):
    PENDIENTE='PENDIENTE'; EN_TRANSITO='EN_TRANSITO'; ENTREGADO='ENTREGADO'; FALLIDO='FALLIDO'

@dataclass(frozen=True)
class Dinero:
    cantidad: Decimal
    def __post_init__(self):
        valor=Decimal(str(self.cantidad))
        if valor < 0: raise ReglaNegocioError('El dinero no puede ser negativo')
        object.__setattr__(self,'cantidad',valor.quantize(Decimal('0.01')))

@dataclass(frozen=True)
class Domicilio:
    calle:str; numero:str; colonia:str; ciudad:str; codigo_postal:str; pais:str
    def __post_init__(self):
        if len(str(self.codigo_postal).strip()) != 5 or not str(self.codigo_postal).isdigit(): raise ReglaNegocioError('Código postal inválido')

@dataclass(frozen=True)
class DetallePedido:
    producto_sku:str; cantidad:int; precio_unitario:Dinero
    def __post_init__(self):
        if not self.producto_sku or self.cantidad <= 0: raise ReglaNegocioError('Detalle de pedido inválido')

@dataclass
class Pedido:
    id:str; cliente_id:str; detalles:tuple[DetallePedido,...]; domicilio:Domicilio; metodo_entrega:str; costo_entrega:Dinero
    estado:EstadoPedido=EstadoPedido.PENDIENTE_PAGO
    def __post_init__(self):
        self.detalles=tuple(self.detalles)
        if not self.detalles: raise ReglaNegocioError('El pedido requiere al menos una línea')
        if not self.id or not self.cliente_id: raise ReglaNegocioError('Identificadores requeridos')
    @property
    def total(self): return sum((d.precio_unitario.cantidad*d.cantidad for d in self.detalles),Decimal('0'))+self.costo_entrega.cantidad
    def registrar_pago(self,aprobado:bool):
        if self.estado != EstadoPedido.PENDIENTE_PAGO: raise ReglaNegocioError('El pedido ya tiene respuesta de pago')
        if aprobado:self.estado=EstadoPedido.PAGADO
    def preparar(self):
        if self.estado!=EstadoPedido.PAGADO: raise ReglaNegocioError('El pedido debe estar pagado')
        self.estado=EstadoPedido.PREPARADO
    def marcar_preparado(self):
        if self.estado!=EstadoPedido.PREPARADO: raise ReglaNegocioError('Pedido no preparado')
    def empacar(self):
        if self.estado!=EstadoPedido.PREPARADO: raise ReglaNegocioError('El pedido debe estar preparado')
        self.estado=EstadoPedido.EMPACADO
    def registrar_salida(self):
        if self.estado!=EstadoPedido.EMPACADO: raise ReglaNegocioError('El pedido debe estar empacado')
        self.estado=EstadoPedido.EN_TRANSITO
    def solicitar_cancelacion(self,motivo:str):
        if not motivo.strip() or self.estado not in {EstadoPedido.PAGADO,EstadoPedido.PREPARADO,EstadoPedido.EMPACADO}: raise ReglaNegocioError('No es posible cancelar el pedido')
        self.estado=EstadoPedido.CANCELACION_SOLICITADA
    def autorizar_cancelacion(self,administrador_id:str):
        if self.estado!=EstadoPedido.CANCELACION_SOLICITADA or not administrador_id: raise ReglaNegocioError('Cancelación no autorizable')
        self.estado=EstadoPedido.CANCELADO

@dataclass(frozen=True)
class MetodoPago:
    codigo:str; nombre:str
@dataclass
class Pago:
    id:str; pedido_id:str; monto:Dinero; metodo:MetodoPago
    estado:EstadoPago=EstadoPago.PENDIENTE
    registrado_en:datetime|None=None
    def registrar_respuesta(self,aprobado:bool):
        if self.estado!=EstadoPago.PENDIENTE: raise ReglaNegocioError('El pago ya fue respondido')
        self.estado=EstadoPago.APROBADO if aprobado else EstadoPago.RECHAZADO
        self.registrado_en=datetime.now(timezone.utc)

@dataclass
class ExistenciaInventario:
    almacen_id:str; producto_sku:str; disponible:int; reservado:int=0
    def __post_init__(self):
        if self.disponible<0 or self.reservado<0: raise ReglaNegocioError('Existencia inválida')
    def reservar(self,cantidad:int):
        if cantidad<=0 or self.disponible<cantidad: raise ReglaNegocioError('Inventario insuficiente')
        self.disponible-=cantidad; self.reservado+=cantidad

@dataclass
class OrdenPreparacion:
    id:str; pedido_id:str; almacen_id:str; lineas:dict
    estado:EstadoPreparacion=EstadoPreparacion.PENDIENTE
    cambios:list=field(default_factory=list)
    def cambiar_estado(self,nuevo:EstadoPreparacion):
        permitidos={EstadoPreparacion.PENDIENTE:{EstadoPreparacion.EN_PREPARACION},EstadoPreparacion.EN_PREPARACION:{EstadoPreparacion.PREPARADO},EstadoPreparacion.PREPARADO:{EstadoPreparacion.EMPACADO}}
        if nuevo not in permitidos.get(self.estado,set()): raise ReglaNegocioError('Cambio de estado de preparación inválido')
        self.estado=nuevo; self.cambios.append(datetime.now(timezone.utc))

@dataclass
class Envio:
    id:str; pedido_id:str
    estado:str='PENDIENTE'; fecha_entrega:datetime|None=None; incidencias:list=field(default_factory=list)
    def iniciar(self,pedido:Pedido):
        if pedido.id!=self.pedido_id or pedido.estado!=EstadoPedido.EMPACADO: raise ReglaNegocioError('Pedido no listo para envío')
        pedido.registrar_salida(); self.estado=EstadoEnvio.EN_TRANSITO.value
    def completar(self,pedido:Pedido):
        if pedido.id!=self.pedido_id or pedido.estado!=EstadoPedido.EN_TRANSITO: raise ReglaNegocioError('Envío no está en tránsito')
        pedido.estado=EstadoPedido.ENTREGADO; self.estado=EstadoEnvio.ENTREGADO.value; self.fecha_entrega=datetime.now(timezone.utc)
    def registrar_falla(self,pedido:Pedido,motivo:str):
        if pedido.id!=self.pedido_id or pedido.estado!=EstadoPedido.EN_TRANSITO or not motivo: raise ReglaNegocioError('No se puede registrar la incidencia')
        pedido.estado=EstadoPedido.ENTREGA_FALLIDA; self.estado=EstadoEnvio.FALLIDO.value; self.incidencias.append(motivo)

@dataclass(frozen=True)
class SolicitudDevolucion:
    id:str; pedido_id:str; motivo:str; tipo:str; folio:str
