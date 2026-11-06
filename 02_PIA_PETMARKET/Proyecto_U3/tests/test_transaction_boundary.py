import unittest
from decimal import Decimal
from domain.model import Domicilio,Dinero,DetallePedido,ExistenciaInventario
from application.services import ConfirmarCompraCommand,ConfirmarCompraHandler
from infrastructure.memory import MemoriaPedidoRepository,MemoriaInventarioRepository,MemoriaPreparacionRepository,UnitOfWorkEnMemoria

class GatewayVerificador:
    def __init__(self,uow,ok=True):self.uow=uow;self.ok=ok;self.vio_fase=False
    def cobrar(self,pedido_id,monto):
        # La fase local PENDIENTE_PAGO ya terminó antes de llamar al gateway.
        self.vio_fase=self.uow.eventos==['iniciar','confirmar']
        return self.ok

class LimiteExterno(unittest.TestCase):
    def configurar(self,aprobado):
        repo=MemoriaPedidoRepository();inv=MemoriaInventarioRepository([ExistenciaInventario('A1','SKU-1',3)])
        prep=MemoriaPreparacionRepository();uow=UnitOfWorkEnMemoria();gateway=GatewayVerificador(uow,aprobado)
        cmd=ConfirmarCompraCommand('P01','C01',(DetallePedido('SKU-1',2,Dinero(Decimal('10'))),),Domicilio('A','1','B','C','64000','MX'),'Estándar',Dinero(Decimal('0')))
        app=ConfirmarCompraHandler(repo,inv,prep,gateway,uow)
        return cmd,app,gateway,uow,repo,prep
    def test_gateway_fuera_de_uow_compra_aprobada(self):
        cmd,app,gateway,uow,repo,prep=self.configurar(True)
        self.assertEqual(app.ejecutar(cmd,{'A1':{'SKU-1':2}}),'PAGADO')
        self.assertTrue(gateway.vio_fase)
        self.assertEqual(uow.eventos,['iniciar','confirmar','iniciar','confirmar'])
        self.assertEqual(len(prep.listar_por_pedido('P01')),1)
    def test_gateway_fuera_de_uow_pago_rechazado(self):
        cmd,app,gateway,uow,repo,prep=self.configurar(False)
        self.assertEqual(app.ejecutar(cmd,{'A1':{'SKU-1':2}}),'PENDIENTE_PAGO')
        self.assertTrue(gateway.vio_fase)
        self.assertEqual(len(prep.listar_por_pedido('P01')),0)
