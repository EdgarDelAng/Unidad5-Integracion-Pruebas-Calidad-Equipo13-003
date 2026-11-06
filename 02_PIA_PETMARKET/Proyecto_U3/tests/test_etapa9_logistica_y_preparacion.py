import unittest
from decimal import Decimal
from domain.model import *
from infrastructure.composicion import ContenedorAplicacion
from application.autorizacion import Actor
class PreparacionLogistica(unittest.TestCase):
    def test_suborden_cambia_estado_y_fecha(self):
        c=ContenedorAplicacion();o=OrdenPreparacion('O1','P1','A1',{'SKU-1':2});c.preparacion.guardar(o)
        r=c.preparar.cambiar_estado(Actor('OPER-1','ALMACEN','A1'),'O1',EstadoPreparacion.EN_PREPARACION)
        self.assertEqual(r.estado,'EN_PREPARACION');self.assertEqual(len(o.cambios),1)
    def test_operador_no_puede_modificar_otro_almacen(self):
        c=ContenedorAplicacion();o=OrdenPreparacion('O1','P1','A1',{'SKU-1':2});c.preparacion.guardar(o)
        with self.assertRaises(ReglaNegocioError):c.preparar.cambiar_estado(Actor('OPER-2','ALMACEN','A2'),'O1',EstadoPreparacion.EN_PREPARACION)
    def test_listado_suborden_solo_propio_almacen(self):
        c=ContenedorAplicacion();c.preparacion.guardar(OrdenPreparacion('O1','P1','A1',{'A':1}));c.preparacion.guardar(OrdenPreparacion('O2','P1','A2',{'B':1}))
        x=c.preparar.consultar_del_almacen(Actor('OPER','ALMACEN','A1'),'P1')
        self.assertEqual(len(x),1);self.assertEqual(x[0].almacen_id,'A1')
    def test_salto_empacado_rechazado(self):
        c=ContenedorAplicacion();c.preparacion.guardar(OrdenPreparacion('O1','P1','A1',{'A':1}))
        with self.assertRaises(ReglaNegocioError):c.preparar.cambiar_estado(Actor('OPER','ALMACEN','A1'),'O1',EstadoPreparacion.EMPACADO)
    def _pedido_preparado(self):
        p=Pedido('P1','C1',(DetallePedido('SKU',1,Dinero(Decimal('2'))),),Domicilio('A','1','B','Mty','64000','MX'),'EST',Dinero(Decimal('0')))
        p.registrar_pago(True);p.preparar();p.marcar_preparado();p.empacar();return p
    def test_envio_exitosa(self):
        c=ContenedorAplicacion();p=self._pedido_preparado();c.pedidos.guardar(p)
        c.logistica.despachar('P1','E1');estado=c.logistica.finalizar('P1','E1',True)
        self.assertEqual(estado.estado,'ENTREGADO');self.assertEqual(p.estado,EstadoPedido.ENTREGADO)
    def test_envio_fallida_incidente(self):
        c=ContenedorAplicacion();p=self._pedido_preparado();c.pedidos.guardar(p)
        c.logistica.despachar('P1','E1');estado=c.logistica.finalizar('P1','E1',False,'Destinatario ausente')
        self.assertEqual(estado.incidencias,1);self.assertEqual(c.consultas.incidencias_pendientes()[0]['envio_id'],'E1')
    def test_envio_no_permitido_sin_empaque(self):
        c=ContenedorAplicacion();p=Pedido('P1','C1',(DetallePedido('SKU',1,Dinero(Decimal('2'))),),Domicilio('A','1','B','Mty','64000','MX'),'EST',Dinero(Decimal('0')))
        c.pedidos.guardar(p)
        with self.assertRaises(ReglaNegocioError):c.logistica.despachar('P1','E1')
