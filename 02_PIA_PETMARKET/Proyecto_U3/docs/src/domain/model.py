"""PetMarket U3: reglas de U2 más decisiones técnicas del prototipo, no un sistema productivo."""
from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from datetime import datetime, timezone
import re
from typing import Iterable

class ReglaNegocioError(ValueError):
    pass

class EstadoPedido(str, Enum):
    PENDIENTE_PAGO='PENDIENTE_PAGO'
    PAGADO='PAGADO'
    EN_PREPARACION='EN_PREPARACION'
    PREPARADO='PREPARADO'
    EMPACADO='EMPACADO'
    EN_TRANSITO='EN_TRANSITO'
    ENTREGADO='ENTREGADO'
    ENTREGA_FALLIDA='ENTREGA_FALLIDA'
    CANCELACION_SOLICITADA='CANCELACION_SOLICITADA'
    CANCELADO='CANCELADO'

class EstadoPreparacion(str, Enum):
    PENDIENTE='PENDIENTE'
    EN_PREPARACION='EN_PREPARACION'
    PREPARADO='PREPARADO'
    EMPACADO='EMPACADO'

class EstadoPago(str, Enum):
    PENDIENTE='PENDIENTE'
    APROBADO='APROBADO'
    RECHAZADO='RECHAZADO'

class EstadoSolicitud(str, Enum):
    PENDIENTE='PENDIENTE'
    AUTORIZADA='AUTORIZADA'
    RECHAZADA='RECHAZADA'

@dataclass(frozen=True)
class Dinero:
    monto: Decimal
    moneda: str = 'MXN'
    def __post_init__(self):
        if not self.monto.is_finite() or self.monto < 0:
            raise ReglaNegocioError('El monto debe ser no negativo y finito')
        if not self.moneda.strip(): raise ReglaNegocioError('La moneda es obligatoria')

@dataclass(frozen=True)
class Domicilio:
    calle: str
    numero: str
    colonia: str
    ciudad: str
    codigo_postal: str
    pais: str
    def __post_init__(self):
        if any(not str(s).strip() for s in (self.calle,self.numero,self.colonia,self.ciudad,self.pais)):
            raise ReglaNegocioError('Domicilio incompleto')
        if re.fullmatch(r'\d{5}', self.codigo_postal) is None:
            raise ReglaNegocioError('El código postal debe contener 5 dígitos')

@dataclass(frozen=True)
class DetallePedido:
    producto_sku: str
    cantidad: int
    precio_unitario: Dinero
    def __post_init__(self):
        if not self.producto_sku.strip() or self.cantidad <= 0:
            raise ReglaNegocioError('SKU y cantidad positiva obligatorios')
    @property
    def subtotal(self)->Decimal:
        return self.precio_unitario.monto*self.cantidad

@dataclass
class SolicitudCancelacion:
    motivo: str
    estado: EstadoSolicitud=EstadoSolicitud.PENDIENTE
    solicitada_en: datetime=field(default_factory=lambda:datetime.now(timezone.utc))
    autorizada_por: str | None = None
    def decidir(self, administrador_id:str, autorizar:bool):
        if not administrador_id.strip():raise ReglaNegocioError('Se requiere administrador')
        if self.estado != EstadoSolicitud.PENDIENTE:raise ReglaNegocioError('Solicitud ya resuelta')
        self.estado=EstadoSolicitud.AUTORIZADA if autorizar else EstadoSolicitud.RECHAZADA
        self.autorizada_por=administrador_id

@dataclass
class Pedido:
    id: str
    cliente_id: str
    detalles: tuple[DetallePedido,...]
    domicilio: Domicilio
    metodo_entrega: str
    costo_entrega: Dinero
    estado: EstadoPedido=EstadoPedido.PENDIENTE_PAGO
    solicitud_cancelacion: SolicitudCancelacion|None=None
    historial: list[tuple[datetime,str]]=field(default_factory=list)
    def __post_init__(self):
        if not self.detalles:raise ReglaNegocioError('Pedido sin detalle')
        if not self.metodo_entrega.strip():raise ReglaNegocioError('Método de entrega obligatorio')
        self._registrar('Pedido creado')
    @property
    def total(self)->Decimal:
        return sum((d.subtotal for d in self.detalles),Decimal('0'))+self.costo_entrega.monto
    def _registrar(self,descripcion:str):
        self.historial.append((datetime.now(timezone.utc),descripcion))
    def registrar_pago(self,aprobado:bool):
        if self.estado != EstadoPedido.PENDIENTE_PAGO:raise ReglaNegocioError('Pago fuera de estado')
        if aprobado:
            self.estado=EstadoPedido.PAGADO
            self._registrar('Pago aprobado')
        else:self._registrar('Pago rechazado')
    def preparar(self):
        if self.estado != EstadoPedido.PAGADO:raise ReglaNegocioError('No preparar sin pago')
        self.estado=EstadoPedido.EN_PREPARACION;self._registrar('Preparación iniciada')
    def marcar_preparado(self):
        if self.estado != EstadoPedido.EN_PREPARACION:raise ReglaNegocioError('Pedido no está en preparación')
        self.estado=EstadoPedido.PREPARADO;self._registrar('Preparación terminada')
    def empacar(self):
        if self.estado != EstadoPedido.PREPARADO:raise ReglaNegocioError('Empaque requiere PREPARADO')
        self.estado=EstadoPedido.EMPACADO;self._registrar('Empaque registrado')
    def registrar_salida(self):
        if self.estado != EstadoPedido.EMPACADO:raise ReglaNegocioError('Envío requiere EMPACADO')
        self.estado=EstadoPedido.EN_TRANSITO;self._registrar('En tránsito')
    def registrar_entrega(self,exitosa:bool):
        if self.estado != EstadoPedido.EN_TRANSITO:raise ReglaNegocioError('Entrega requiere EN_TRANSITO')
        self.estado=EstadoPedido.ENTREGADO if exitosa else EstadoPedido.ENTREGA_FALLIDA
        self._registrar('Entrega exitosa' if exitosa else 'Entrega fallida')
    def solicitar_cancelacion(self,motivo:str):
        # CA-15.01 enumera PAGADO/PREPARADO/EMPACADO (no EN_PREPARACION).
        if self.estado not in (EstadoPedido.PAGADO,EstadoPedido.PREPARADO,EstadoPedido.EMPACADO):
            raise ReglaNegocioError('Cancelación no permitida en este estado')
        if not motivo.strip():raise ReglaNegocioError('Motivo obligatorio en propuesta de diseño')
        self.solicitud_cancelacion=SolicitudCancelacion(motivo=motivo)
        self.estado=EstadoPedido.CANCELACION_SOLICITADA;self._registrar('Cancelación solicitada')
    def autorizar_cancelacion(self,admin_id:str):
        if self.estado != EstadoPedido.CANCELACION_SOLICITADA or not self.solicitud_cancelacion:
            raise ReglaNegocioError('No existe solicitud pendiente')
        self.solicitud_cancelacion.decidir(admin_id,True)
        self.estado=EstadoPedido.CANCELADO;self._registrar('Cancelación autorizada')
        # Reembolso y liberación de stock: políticas pendientes, no se ejecutan silenciosamente.

@dataclass
class ExistenciaInventario:
    almacen_id: str
    producto_sku: str
    disponible: int
    reservado: int=0
    def __post_init__(self):
        if self.disponible<0 or self.reservado<0:raise ReglaNegocioError('Inventario negativo')
    def reservar(self,cantidad:int):
        if cantidad<=0 or cantidad>self.disponible:
            raise ReglaNegocioError('Existencias insuficientes')
        self.disponible-=cantidad;self.reservado+=cantidad
    def liberar(self,cantidad:int):
        if cantidad<=0 or cantidad>self.reservado:
            raise ReglaNegocioError('Cantidad a liberar inválida')
        self.reservado-=cantidad;self.disponible+=cantidad

@dataclass
class OrdenPreparacion:
    id: str
    pedido_id: str
    almacen_id: str
    lineas: dict[str,int]
    estado: EstadoPreparacion=EstadoPreparacion.PENDIENTE
    cambios: list[tuple[str,datetime]]=field(default_factory=list)
    def __post_init__(self):
        if not self.lineas or any(q<=0 for q in self.lineas.values()):
            raise ReglaNegocioError('Líneas de preparación inválidas')
    def cambiar_estado(self,nuevo:EstadoPreparacion):
        transiciones={EstadoPreparacion.PENDIENTE:{EstadoPreparacion.EN_PREPARACION},EstadoPreparacion.EN_PREPARACION:{EstadoPreparacion.PREPARADO},EstadoPreparacion.PREPARADO:{EstadoPreparacion.EMPACADO},EstadoPreparacion.EMPACADO:set()}
        if nuevo not in transiciones[self.estado]:raise ReglaNegocioError('Transición de preparación inválida')
        self.estado=nuevo;self.cambios.append((nuevo.value,datetime.now(timezone.utc)))

@dataclass(frozen=True)
class DomainEvent:
    nombre:str
    agregado_id:str
    registrado_en:datetime=field(default_factory=lambda:datetime.now(timezone.utc))

@dataclass(frozen=True)
class MetodoPago:
    codigo:str
    descripcion:str
    def __post_init__(self):
        if not self.codigo.strip():raise ReglaNegocioError('Código de método de pago obligatorio')

@dataclass
class Pago:
    id:str
    pedido_id:str
    monto:Dinero
    metodo:MetodoPago
    estado:EstadoPago=EstadoPago.PENDIENTE
    registrado_en:datetime|None=None
    def registrar_respuesta(self,aprobado:bool):
        if self.estado!=EstadoPago.PENDIENTE:raise ReglaNegocioError('Respuesta ya registrada')
        self.estado=EstadoPago.APROBADO if aprobado else EstadoPago.RECHAZADO
        self.registrado_en=datetime.now(timezone.utc)

@dataclass(frozen=True)
class IncidenciaEntrega:
    motivo:str
    fecha:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
    def __post_init__(self):
        if not self.motivo.strip():raise ReglaNegocioError('Motivo de incidencia obligatorio')

@dataclass
class Envio:
    id:str
    pedido_id:str
    numero_guia:str|None=None
    fecha_salida:datetime|None=None
    fecha_entrega:datetime|None=None
    estado:str='PENDIENTE'
    incidencias:list[IncidenciaEntrega]=field(default_factory=list)
    def iniciar(self,pedido:Pedido):
        # Alineación con CA-12.01. La regla primaria permanece en Pedido.
        pedido.registrar_salida()
        self.estado='EN_TRANSITO';self.fecha_salida=datetime.now(timezone.utc)
    def completar(self,pedido:Pedido):
        pedido.registrar_entrega(True)
        self.estado='ENTREGADO';self.fecha_entrega=datetime.now(timezone.utc)
    def registrar_falla(self,pedido:Pedido,motivo:str):
        incidencia=IncidenciaEntrega(motivo)
        pedido.registrar_entrega(False)
        self.incidencias.append(incidencia);self.estado='ENTREGA_FALLIDA'

@dataclass(frozen=True)
class SolicitudDevolucion:
    id:str
    pedido_id:str
    motivo:str
    opcion:str
    folio:str
    def __post_init__(self):
        if not all(x.strip() for x in (self.pedido_id,self.motivo,self.folio)):
            raise ReglaNegocioError('Devolución incompleta')
        if self.opcion not in ('REEMBOLSO','CAMBIO'):
            raise ReglaNegocioError('Opción de devolución inválida')
