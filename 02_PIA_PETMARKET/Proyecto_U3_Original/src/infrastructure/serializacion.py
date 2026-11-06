"""Proyección de lectura sin serializar referencias internas de agregados."""
from dataclasses import asdict,is_dataclass
from decimal import Decimal
from datetime import datetime
from enum import Enum

def a_datos_lectura(obj):
    def normalizar(x):
        if isinstance(x,Decimal):return str(x)
        if isinstance(x,datetime):return x.isoformat()
        if isinstance(x,Enum):return x.value
        if isinstance(x,dict):return {k:normalizar(v) for k,v in x.items()}
        if isinstance(x,(list,tuple)):return [normalizar(v) for v in x]
        if is_dataclass(x):return normalizar(asdict(x))
        return x
    return normalizar(obj)
