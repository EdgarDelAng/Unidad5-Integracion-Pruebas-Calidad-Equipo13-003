import unittest
from decimal import Decimal
from domain.model import *
from infrastructure.memory import *
from infrastructure.transacciones import UnidadTrabajoSnapshot
from infrastructure.pasarelas import PasarelaSinRespuesta
from infrastructure.serializacion import a_datos_lectura
from infrastructure.reloj import RelojFijo
from datetime import datetime,timezone
class PersistenciaYFallos(unittest.TestCase):
    def test_rollback_restaura_repositorio(self):
        pr=MemoriaPedidoRepository();uow=UnidadTrabajoSnapshot(pr)
        uow.iniciar();pr.datos['X']='nuevo';uow.revertir()
        self.assertNotIn('X',pr.datos)
    def test_commit_conserva_cambios(self):
        pr=MemoriaPedidoRepository();uow=UnidadTrabajoSnapshot(pr)
        uow.iniciar();pr.datos['X']='nuevo';uow.confirmar()
        self.assertEqual(pr.datos['X'],'nuevo')
    def test_rollback_restauracion_con_variados_repos(self):
        inv=MemoriaInventarioRepository([ExistenciaInventario('A','SKU',3)]);pr=MemoriaPedidoRepository();uow=UnidadTrabajoSnapshot(inv,pr)
        uow.iniciar();inv.obtener('A','SKU').reservar(1);pr.datos['P']=1;uow.revertir()
        self.assertEqual(inv.obtener('A','SKU').disponible,3);self.assertNotIn('P',pr.datos)
    def test_no_permite_doble_begin(self):
        a=UnidadTrabajoSnapshot();a.iniciar()
        with self.assertRaises(RuntimeError):a.iniciar()
    def test_no_permite_commit_sin_iniciar(self):
        with self.assertRaises(RuntimeError):UnidadTrabajoSnapshot().confirmar()
    def test_gateway_timeout_explicito(self):
        with self.assertRaises(TimeoutError):PasarelaSinRespuesta().cobrar('P','10')
    def test_serializacion_dinero_a_str(self):
        self.assertEqual(a_datos_lectura(Dinero(Decimal('10.25')))['monto'],'10.25')
    def test_reloj_inyectable_reproducible(self):
        fecha=datetime(2026,10,10,tzinfo=timezone.utc);self.assertEqual(RelojFijo(fecha).ahora(),fecha)
