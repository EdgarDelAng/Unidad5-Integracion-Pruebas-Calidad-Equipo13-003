import unittest
from decimal import Decimal
from domain.model import *
from application.services import *
from infrastructure.memory import *

def pedido():
    dom=Domicilio('Río','120','Centro','Monterrey','64000','México')
    linea=DetallePedido('SKU-1',2,Dinero(Decimal('120.50')))
    return Pedido('PED-1','CLI-1',(linea,),dom,'Estándar',Dinero(Decimal('40.00')))

class DominioTests(unittest.TestCase):
    def test_cp01_domicilio_rechaza_cp_invalido(self):
        with self.assertRaises(ReglaNegocioError):Domicilio('A','1','B','C','123','MX')
    def test_cp02_pedido_sin_lineas(self):
        x=pedido()
        with self.assertRaises(ReglaNegocioError):Pedido('p','c',(),x.domicilio,'Estándar',x.costo_entrega)
    def test_cp03_total_incluye_entrega(self):self.assertEqual(pedido().total,Decimal('281.00'))
    def test_cp04_rechazo_permanece_pendiente(self):
        x=pedido();x.registrar_pago(False);self.assertEqual(x.estado,EstadoPedido.PENDIENTE_PAGO)
    def test_cp05_no_preparar_sin_pago(self):
        with self.assertRaises(ReglaNegocioError):pedido().preparar()
    def test_cp06_empaque_requiere_preparado(self):
        x=pedido();x.registrar_pago(True)
        with self.assertRaises(ReglaNegocioError):x.empacar()
    def test_cp07_envio_requiere_empacado(self):
        x=pedido();x.registrar_pago(True)
        with self.assertRaises(ReglaNegocioError):x.registrar_salida()
    def test_cp08_cancelacion_valida_requiere_autorizacion(self):
        x=pedido();x.registrar_pago(True);x.solicitar_cancelacion('Desistimiento');self.assertEqual(x.estado,EstadoPedido.CANCELACION_SOLICITADA)
        x.autorizar_cancelacion('ADMIN-1');self.assertEqual(x.estado,EstadoPedido.CANCELADO)
    def test_cp09_cancelacion_no_permitida_en_transito(self):
        x=pedido();x.registrar_pago(True);x.preparar();x.marcar_preparado();x.empacar();x.registrar_salida()
        with self.assertRaises(ReglaNegocioError):x.solicitar_cancelacion('Demasiado tarde')
    def test_cp10_inventario_sin_stock(self):
        ex=ExistenciaInventario('A1','SKU-1',1)
        with self.assertRaises(ReglaNegocioError):ex.reservar(2)
    def test_cp11_orden_registra_fechas(self):
        o=OrdenPreparacion('OP1','PED-1','A1',{'SKU-1':1});o.cambiar_estado(EstadoPreparacion.EN_PREPARACION)
        self.assertEqual(len(o.cambios),1)
    def test_cp12_pedido_dividido_dos_ordenes(self):
        p=pedido();pedidos=MemoriaPedidoRepository();inv=MemoriaInventarioRepository([ExistenciaInventario('A1','SKU-1',1),ExistenciaInventario('A2','SKU-1',1)])
        prep=MemoriaPreparacionRepository();gateway=PasarelaSimulada(True);uow=UnitOfWorkEnMemoria()
        c=ConfirmarCompraCommand(p.id,p.cliente_id,p.detalles,p.domicilio,p.metodo_entrega,p.costo_entrega)
        estado=ConfirmarCompraHandler(pedidos,inv,prep,gateway,uow).ejecutar(c,{'A1':{'SKU-1':1},'A2':{'SKU-1':1}})
        self.assertEqual(estado,'PAGADO');self.assertEqual(len(prep.listar_por_pedido(p.id)),2)
    def test_cp13_rechazo_no_crea_preparacion(self):
        p=pedido();pr=MemoriaPedidoRepository();inv=MemoriaInventarioRepository([ExistenciaInventario('A1','SKU-1',2)]);prep=MemoriaPreparacionRepository()
        c=ConfirmarCompraCommand(p.id,p.cliente_id,p.detalles,p.domicilio,p.metodo_entrega,p.costo_entrega)
        estado=ConfirmarCompraHandler(pr,inv,prep,PasarelaSimulada(False),UnitOfWorkEnMemoria()).ejecutar(c,{'A1':{'SKU-1':2}})
        self.assertEqual(estado,'PENDIENTE_PAGO');self.assertEqual(len(prep.listar_por_pedido(p.id)),0);self.assertEqual(inv.obtener('A1','SKU-1').disponible,2)
    def test_cp14_query_dto_no_devuelve_agregado(self):
        pr=MemoriaPedidoRepository();p=pedido();pr.guardar(p)
        dto=ConsultaPedidoHandler(pr).ejecutar(ConsultarPedidoQuery(p.id))
        self.assertIsInstance(dto,PedidoDetalleDTO)
    def test_cp15_asignacion_incompleta_bloquea_compra(self):
        p=pedido();c=ConfirmarCompraCommand(p.id,p.cliente_id,p.detalles,p.domicilio,p.metodo_entrega,p.costo_entrega)
        svc=ConfirmarCompraHandler(MemoriaPedidoRepository(),MemoriaInventarioRepository(),MemoriaPreparacionRepository(),PasarelaSimulada(),UnitOfWorkEnMemoria())
        with self.assertRaises(ReglaNegocioError):svc.ejecutar(c,{'A1':{'SKU-1':1}})


class DominioExtTests(unittest.TestCase):
    def test_cp16_pago_registra_respuesta(self):
        a=Pago('PA1','PED-1',Dinero(Decimal('10')),MetodoPago('TARJETA','Tarjeta'))
        a.registrar_respuesta(True)
        self.assertEqual(a.estado,EstadoPago.APROBADO)
        self.assertIsNotNone(a.registrado_en)
    def test_cp17_pago_no_repite_respuesta(self):
        a=Pago('PA1','PED-1',Dinero(Decimal('10')),MetodoPago('TARJETA','Tarjeta'))
        a.registrar_respuesta(False)
        with self.assertRaises(ReglaNegocioError): a.registrar_respuesta(True)
    def test_cp18_entrega_exitosa(self):
        a=pedido();a.registrar_pago(True);a.preparar();a.marcar_preparado();a.empacar()
        e=Envio('EN1',a.id);e.iniciar(a);e.completar(a)
        self.assertEqual(a.estado,EstadoPedido.ENTREGADO)
        self.assertIsNotNone(e.fecha_entrega)
    def test_cp19_entrega_fallida_genera_incidencia(self):
        a=pedido();a.registrar_pago(True);a.preparar();a.marcar_preparado();a.empacar()
        e=Envio('EN1',a.id);e.iniciar(a);e.registrar_falla(a,'DESTINATARIO AUSENTE')
        self.assertEqual(a.estado,EstadoPedido.ENTREGA_FALLIDA)
        self.assertEqual(len(e.incidencias),1)
    def test_cp20_devolucion_acepta_campos(self):
        x=SolicitudDevolucion('S1','PED-1','Producto defectuoso','CAMBIO','DEV-001')
        self.assertEqual(x.pedido_id,'PED-1')

if __name__=='__main__': unittest.main()
