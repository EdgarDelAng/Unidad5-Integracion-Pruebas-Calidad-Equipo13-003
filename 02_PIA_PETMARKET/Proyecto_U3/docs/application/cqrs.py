"""Separación entre comandos de escritura y consultas de lectura."""
from .services import (ConfirmarCompraCommand,ConfirmarCompraHandler,SolicitarCancelacionCommand,
                       SolicitarCancelacionHandler,ConsultarPedidoQuery,ConsultaPedidoHandler,
                       ConsultarPreparacionQuery,ConsultaPreparacionHandler)
__all__=[name for name in globals() if name.endswith(('Command','Handler','Query'))]
