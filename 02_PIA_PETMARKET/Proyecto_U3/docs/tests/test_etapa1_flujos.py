import unittest
from decimal import Decimal
from domain.model import *
from domain.asignacion import validar_distribucion
from domain.politicas import es_cancelable
from infrastructure.composicion import ContenedorAplicacion
from application.services import ConfirmarCompraCommand,ConfirmarCompraHandler
from application.autorizacion import Actor
from application.cancelaciones import CancelacionesApplicationService

def pedido(pid='PED-01'):
    return Pedido(pid,'CLI-01',(DetallePedido('SKU-A',2,Dinero(Decimal('50'))),),
                  Domicilio('Río','3','Centro','Monterrey','64000','MX'),'ESTANDAR',Dinero(Decimal('20')))
class CasosDeUso(unittest.TestCase):
    def test_compra_rechazada_mantiene_pendiente(self):
        c=ContenedorAplicacion([ExistenciaInventario('A1','SKU-A',2)])
        c.pasarela.aprobado=False
        p=pedido();c1=ConfirmarCompraCommand(p.id,p.cliente_id,p.detalles,p.domicilio,p.metodo_entrega,p.costo_entrega)
        r=ConfirmarCompraHandler(c.pedidos,c.inventario,c.preparacion,c.pasarela,c.uow).ejecutar(c1,{'A1':{'SKU-A':2}})
        self.assertEqual(r,'PENDIENTE_PAGO');self.assertEqual(len(c.preparacion.datos),0)
    def test_compra_dos_almacenes_genera_suborden_por_almacen(self):
        c=ContenedorAplicacion([ExistenciaInventario('A1','SKU-A',1),ExistenciaInventario('A2','SKU-A',1)])
        p=pedido();cmd=ConfirmarCompraCommand(p.id,p.cliente_id,p.detalles,p.domicilio,p.metodo_entrega,p.costo_entrega)
        estado=ConfirmarCompraHandler(c.pedidos,c.inventario,c.preparacion,c.pasarela,c.uow).ejecutar(cmd,{'A1':{'SKU-A':1},'A2':{'SKU-A':1}})
        self.assertEqual(estado,'PAGADO');self.assertEqual({o.almacen_id for o in c.preparacion.datos.values()},{'A1','A2'})
    def test_cu_cancelacion_solicitud_separada_aprobacion(self):
        c=ContenedorAplicacion();p=pedido();p.registrar_pago(True);c.pedidos.guardar(p)
        x=c.cancelaciones.solicitar(Actor('CLI-01','CLIENTE'),p.id,'Desistimiento')
        self.assertTrue(x.requiere_autorizacion);self.assertEqual(p.estado,EstadoPedido.CANCELACION_SOLICITADA)
        z=c.cancelaciones.autorizar(Actor('ADMIN-7','ADMINISTRADOR'),p.id)
        self.assertFalse(z.requiere_autorizacion);self.assertEqual(z.estado,'CANCELADO')
    def test_cancelacion_no_autoriza_cliente(self):
        c=ContenedorAplicacion();p=pedido();p.registrar_pago(True);p.solicitar_cancelacion('motivo');c.pedidos.guardar(p)
        with self.assertRaises(ReglaNegocioError):c.cancelaciones.autorizar(Actor('CLI-01','CLIENTE'),p.id)
    def test_cliente_no_accede_a_otros_pedidos(self):
        c=ContenedorAplicacion();p=pedido();p.registrar_pago(True);c.pedidos.guardar(p)
        with self.assertRaises(ReglaNegocioError):c.cancelaciones.solicitar(Actor('CLI-02','CLIENTE'),p.id,'otro')
    def test_estados_permitidos_literal_u2(self):
        self.assertEqual({e.value for e in EstadoPedido if es_cancelable(e)},{'PAGADO','PREPARADO','EMPACADO'})
    def test_asignacion_sku_repetido_suma(self):
        lineas=(DetallePedido('A',1,Dinero(Decimal('1'))),DetallePedido('A',3,Dinero(Decimal('1'))))
        self.assertEqual(validar_distribucion(lineas,{'A1':{'A':2},'A2':{'A':2}}),{'A':4})
    def test_asignacion_rechaza_sku_inexistente(self):
        with self.assertRaises(ReglaNegocioError):validar_distribucion(pedido().detalles,{'A1':{'SKU-X':2}})
    def test_asignacion_rechaza_cantidad_negativa(self):
        with self.assertRaises(ReglaNegocioError):validar_distribucion(pedido().detalles,{'A1':{'SKU-A':-2}})
    def test_asignacion_rechaza_cantidad_bool(self):
        with self.assertRaises(ReglaNegocioError):validar_distribucion(pedido().detalles,{'A1':{'SKU-A':True}})
    def test_asignacion_rechaza_almacen_vacio(self):
        with self.assertRaises(ReglaNegocioError):validar_distribucion(pedido().detalles,{'':{'SKU-A':2}})
    def test_total_positivo_con_entrega(self):
        self.assertEqual(pedido().total,Decimal('120'))
