import unittest
from decimal import Decimal
from domain.model import *
from infrastructure.composicion import ContenedorAplicacion
from application.autorizacion import Actor
from application.contratos import *
from application.errores import interpretar_error
from application.inventario import InventarioApplicationService
from application.auditoria import RegistroAccion,BitacoraOperaciones
from application.indicadores import IndicadoresApplicationService

def pedido(pid='P1',cliente='C1'):
    return Pedido(pid,cliente,(DetallePedido('A',1,Dinero(Decimal('10'))),),Domicilio('A','1','B','Mty','64000','MX'),'E',Dinero(Decimal('3')))
class CapaAplicacion(unittest.TestCase):
    def test_consulta_cliente_filtra_por_identidad(self):
        c=ContenedorAplicacion();c.pedidos.guardar(pedido('P1','C1'));c.pedidos.guardar(pedido('P2','C2'))
        self.assertEqual(len(c.consultas.pedidos_del_cliente('C1')),1)
    def test_busqueda_por_id_inexistente(self):
        self.assertIsNone(ContenedorAplicacion().consultas.buscar_por_id('SIN-PEDIDO'))
    def test_consulta_regresa_dto_no_agregado(self):
        c=ContenedorAplicacion();c.pedidos.guardar(pedido())
        dto=c.consultas.buscar_por_id('P1');self.assertEqual(dto.total,'13')
        self.assertFalse(hasattr(dto,'registrar_pago'))
    def test_indicadores_total_pedidos(self):
        c=ContenedorAplicacion();c.pedidos.guardar(pedido('P1'));c.pedidos.guardar(pedido('P2'))
        self.assertEqual(c.indicadores.consultar()['total_pedidos'],2)
    def test_indicadores_total_montos(self):
        c=ContenedorAplicacion();c.pedidos.guardar(pedido('P1'));c.pedidos.guardar(pedido('P2'))
        self.assertEqual(c.indicadores.consultar()['valor_pedidos'],'26')
    def test_indicadores_rechaza_rango_invalido(self):
        from datetime import datetime,timezone
        c=ContenedorAplicacion()
        with self.assertRaises(ValueError):c.indicadores.consultar(datetime(2026,12,2,tzinfo=timezone.utc),datetime(2026,1,2,tzinfo=timezone.utc))
    def test_inventario_dto_no_expone_reservar(self):
        c=ContenedorAplicacion([ExistenciaInventario('A1','A',4,1)])
        v=InventarioApplicationService(c.inventario).consultar('A1','A')
        self.assertEqual((v.disponible,v.reservado),(4,1));self.assertFalse(hasattr(v,'reservar'))
    def test_error_de_negocio_se_traduce_sin_sql(self):
        r=interpretar_error(ReglaNegocioError('Estado no permitido'))
        self.assertEqual(r.codigo,'REGLA_NEGOCIO')
    def test_error_tecnico_no_expone_interno(self):
        r=interpretar_error(RuntimeError('database password = demo'))
        self.assertEqual(r.mensaje,'Error interno')
    def test_bitacora_filtra_por_pedido(self):
        a=BitacoraOperaciones();a.agregar(RegistroAccion('cancelar','P1','A'));a.agregar(RegistroAccion('pagar','P2','A'))
        self.assertEqual(len(a.por_objeto('P1')),1)
