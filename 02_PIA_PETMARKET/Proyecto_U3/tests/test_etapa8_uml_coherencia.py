import unittest
from pathlib import Path
import xml.etree.ElementTree as ET
from application.cancelaciones import CancelacionesApplicationService
from application.preparacion import PreparacionApplicationService
from application.logistica import LogisticaApplicationService
from domain.model import EstadoPedido,EstadoPreparacion
ROOT=Path(__file__).resolve().parents[1]
class ValidacionArtefactos(unittest.TestCase):
    def test_mapadominio_fuente_valido(self):
        self.assertGreaterEqual(len(ET.parse(ROOT/'diagramas/dominio/mapa-dominio.drawio').getroot().findall('diagram')),1)
    def test_diagrama_clases_fuente_valido(self):
        self.assertGreaterEqual(len(ET.parse(ROOT/'diagramas/clases/clases_petmarket_todas_las_vistas.drawio').getroot().findall('diagram')),3)
    def test_dos_secuencias_en_archivos_individuales(self):
        archivos=sorted((ROOT/'diagramas/secuencia').glob('secuencia_[12]_*.drawio'))
        self.assertEqual(len(archivos),2)
        for p in archivos:ET.parse(p)
    def test_clases_servicios_publicos_existen(self):
        for clase,metodo in ((CancelacionesApplicationService,'solicitar'),(PreparacionApplicationService,'cambiar_estado'),(LogisticaApplicationService,'finalizar')):
            self.assertTrue(callable(getattr(clase,metodo)))
    def test_estados_u2(self):
        self.assertIn(EstadoPedido.CANCELACION_SOLICITADA,EstadoPedido)
        self.assertIn(EstadoPreparacion.EMPACADO,EstadoPreparacion)
