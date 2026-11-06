"""Pruebas de regresión del total de unidades por SKU en varias líneas."""
import unittest
from decimal import Decimal
from application.services import ConfirmarCompraCommand, ConfirmarCompraHandler
from domain.model import Dinero, Domicilio, DetallePedido, ExistenciaInventario, EstadoPedido, ReglaNegocioError
from infrastructure.memory import (
    MemoriaPedidoRepository, MemoriaInventarioRepository, MemoriaPreparacionRepository,
    PasarelaSimulada, UnitOfWorkEnMemoria
)

class RegresionSkuRepetido(unittest.TestCase):
    def crear(self, stock=5):
        detalles=(
            DetallePedido('SKU-1', 1, Dinero(Decimal('12.00'))),
            DetallePedido('SKU-1', 2, Dinero(Decimal('12.00'))),
        )
        solicitud=ConfirmarCompraCommand('PED-REP', 'CLI-REP', detalles,
            Domicilio('Calle', '123', 'Centro', 'Monterrey', '64000', 'México'),
            'Estandar', Dinero(Decimal('15.00')))
        pedidos=MemoriaPedidoRepository()
        inventario=MemoriaInventarioRepository([ExistenciaInventario('A1','SKU-1',stock)])
        preparacion=MemoriaPreparacionRepository()
        pagos=PasarelaSimulada(aprobado=True)
        servicio=ConfirmarCompraHandler(pedidos,inventario,preparacion,pagos,UnitOfWorkEnMemoria())
        return servicio,solicitud,pedidos,inventario,preparacion,pagos

    def test_dos_lineas_mismo_sku_suman_tres_unidades(self):
        servicio,solicitud,pedidos,inventario,preparacion,pagos=self.crear()
        estado=servicio.ejecutar(solicitud,{'A1':{'SKU-1':3}})
        self.assertEqual(estado,EstadoPedido.PAGADO.value)
        self.assertEqual(pedidos.obtener('PED-REP').total,Decimal('51.00'))
        self.assertEqual(inventario.obtener('A1','SKU-1').disponible,2)
        self.assertEqual(len(preparacion.listar_por_pedido('PED-REP')),1)
        self.assertEqual(len(pagos.operaciones),1)

    def test_stock_insuficiente_para_sku_repetido_no_cobra(self):
        servicio,solicitud,pedidos,inventario,preparacion,pagos=self.crear(stock=2)
        with self.assertRaises(ReglaNegocioError):
            servicio.ejecutar(solicitud,{'A1':{'SKU-1':3}})
        self.assertEqual(len(pagos.operaciones),0)
        self.assertIsNone(pedidos.obtener('PED-REP'))
