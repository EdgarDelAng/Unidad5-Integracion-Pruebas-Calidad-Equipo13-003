"""DTO de entrada y salida, diferentes de las entidades mutables."""
from dataclasses import dataclass
@dataclass(frozen=True)
class ResultadoCancelacion:
    pedido_id:str
    estado:str
    requiere_autorizacion:bool
@dataclass(frozen=True)
class ResumenPreparacion:
    orden_id:str
    almacen_id:str
    estado:str
    total_lineas:int
@dataclass(frozen=True)
class EstadoEnvioDTO:
    envio_id:str
    pedido_id:str
    estado:str
    incidencias:int
@dataclass(frozen=True)
class ExistenciaDTO:
    almacen_id:str
    sku:str
    disponible:int
    reservado:int
