# PetMarket · Arquitectura de Software (Unidad 3)

Proyecto académico de **Componentes de Lógica de Negocio** para PetMarket, una tienda de productos para mascotas que coordina pedidos y preparación distribuida en **dos almacenes (A1 y A2)**. La arquitectura aplica Domain Model/DDD, Application Services, Repository/Unit of Work, CQRS básico, revisión SOLID y UML. La documentación conserva las reglas y criterios de aceptación de Unidad 2.

> **Alcance:** el código es un prototipo de referencia con persistencia en memoria. No hay plataforma de pagos, base de datos ni interfaz web productivas. Las funcionalidades parciales y no implementadas se identifican en la matriz de trazabilidad. Los ADR mantienen estado de propuesta hasta su ratificación.

## Estructura del repositorio

```text
PETMARKET_U3_ARQUITECTURA_CLNEG/
├── docs/
│   ├── ADR/               ADR_PetMarket.docx y ADR_PetMarket.pdf
│   ├── bitacora ia/        Bitacora_IA_PetMarket.docx y .pdf (18 iteraciones)
│   ├── informe/           Guia_Unidad_3_PetMarket.docx y .pdf (formato guía original)
│   ├── trazabilidad/      matriz-trazabilidad.xlsx y .pdf (56 CA / 18 US)
│   └── unidad 2/          Caso 13 y fuentes originales de BRD, historias, glosario y BPMN
├── diagramas/
│   ├── clases/            UML de clases: 4 vistas y archivo maestro
│   ├── dominio/           10 vistas DDD editables + PDF
│   └── secuencia/         2 secuencias UML individuales y archivo combinado
├── src/
│   ├── domain/            reglas, modelos, eventos y validaciones
│   ├── application/       contratos, CQRS, casos de uso y consultas
│   └── infrastructure/    repositorios, adaptadores, composición y UoW en memoria
├── tests/
│   ├── evidencias/        ejecucion-pruebas.txt y reporte Word/PDF
│   └── test_*.py          8 módulos de pruebas automatizadas
├── .github/workflows/     pipeline de unittest para cambios y pull requests
└── README.md
```

## Índice de documentación

| Artefacto | Fuentes |
|---|---|
| **Informe de arquitectura** | [Word](docs/informe/Guia_Unidad_3_PetMarket.docx) · [PDF](docs/informe/Guia_Unidad_3_PetMarket.pdf) |
| **Registros ADR** | [Word](docs/ADR/ADR_PetMarket.docx) · [PDF](docs/ADR/ADR_PetMarket.pdf) |
| **Bitácora de IA** | [Word](docs/bitacora%20ia/Bitacora_IA_PetMarket.docx) · [PDF](docs/bitacora%20ia/Bitacora_IA_PetMarket.pdf) |
| **Trazabilidad** | [Excel](docs/trazabilidad/matriz-trazabilidad.xlsx) · [PDF](docs/trazabilidad/matriz-trazabilidad.pdf) |
| **Unidad 2** | [Caso 13](docs/unidad%202/00_Caso_13_PetMarket.docx) · [BRD](docs/unidad%202/01_BRD_PetMarket.pdf) · [Historias + CA + Gherkin](docs/unidad%202/02_Historias_Criterios_Gherkin_PetMarket.pdf) · [Glosario](docs/unidad%202/03_Glosario_PetMarket.pdf) · [BPMN](docs/unidad%202/04_Modelo_BPMN_PetMarket.pdf) |
| **Mapa de dominio** | [Fuente draw.io](diagramas/dominio/mapa-dominio.drawio) · [PDF](diagramas/dominio/mapa-dominio.pdf) |
| **Clases UML** | [Vista maestra draw.io](diagramas/clases/clases_petmarket_todas_las_vistas.drawio) · [PDF](diagramas/clases/clases_petmarket_todas_las_vistas.pdf) |
| **Secuencia 1 — compra/pago** | [Draw.io](diagramas/secuencia/secuencia_1_compra_y_pago.drawio) · [PDF](diagramas/secuencia/secuencia_1_compra_y_pago.pdf) |
| **Secuencia 2 — cancelación** | [Draw.io](diagramas/secuencia/secuencia_2_cancelacion.drawio) · [PDF](diagramas/secuencia/secuencia_2_cancelacion.pdf) |
| **Evidencias de pruebas** | [Word](tests/evidencias/evidencia-pruebas.docx) · [PDF](tests/evidencias/evidencia-pruebas.pdf) · [Registro íntegro](tests/evidencias/ejecucion-pruebas.txt) |

## Correspondencia de actividades

| Etapa | Resultado documentado |
|---|---|
| 1 · Preparación del caso | Cinco casos de uso con flujo normal y alternativo derivados de U2. |
| 2 · Patrón | Domain Model comparado frente a Transaction Script y Table Module; ADR-000. |
| 3 · DDD | Agregados, entidades, VO, Domain Services y Events, límites y glosario. |
| 4 · Application Services | Contratos, coordinación, reglas delegadas y resultados. |
| 5 · Repository/UoW | Puertos, adaptadores de memoria y límites de transacción. |
| 6 · CQRS | Commands/Queries, handlers y DTO de lectura. |
| 7 · SOLID | Hallazgos, evidencia y ajustes propuestos. |
| 8 · UML/ADR | Clases, dos secuencias y cinco ADR. |
| 9 · Validación | Matriz por CA, evidencias de unittest y revisión de limitaciones. |

## Ejecución local

Requisitos: **Python 3.11 o posterior**; no se requieren dependencias externas para el prototipo.

**Windows PowerShell**, desde la raíz del repositorio:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

**Linux / macOS**:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Una validación local de esta versión ejecutó **66 pruebas: 66 correctas, 0 fallos y 0 errores**. Consulta el [registro original](tests/evidencias/ejecucion-pruebas.txt). GitHub Actions repite el comando cada vez que se publica un cambio o se abre una solicitud de incorporación.

### Qué comprueban las pruebas

- Reglas de pago, cancelación, despacho, inventario y estados del pedido.
- Distribución por almacenes, SKU repetidos y aislamiento del trabajo por almacén.
- Contratos de lectura, DTO, autorizaciones y resultados de error.
- Reversión de modificaciones en *snapshots* de repositorios en memoria.
- Estructura XML de fuentes draw.io y operaciones públicas de servicios.

**Límites:** estas pruebas no verifican una pasarela bancaria real, SQL/ORM, transacciones ACID, integración con paquetería, interfaces web ni comportamiento de múltiples usuarios concurrentes. `UnidadTrabajoSnapshot` restaura copias en memoria, no proporciona durabilidad o aislamiento de base de datos.

## Antes de publicar el repositorio públicamente

Los PDF originales de **Unidad 2 contienen nombres y matrículas personales**. Se incorporan por solicitud expresa de los integrantes, pero deben revisarse y, si corresponde, anonimizarse antes de publicar un repositorio público. Consulta `docs/unidad 2/AVISO_PUBLICACION.txt`.

También debe completarse la identificación de todos los integrantes y validarse el estado de los ADR. Los diagramas existentes conservaron sus fuentes originales editables; la reorganización no modifica su composición visual.

## Publicación en GitHub

Desde la carpeta raíz, después de revisar los datos personales:

```bash
git init
git add .
git commit -m "docs: arquitectura y pruebas PetMarket U3"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/TU-REPOSITORIO.git
git push -u origin main
```

Sustituir la URL por la del repositorio real. No se realizaron commits ni publicaciones remotas en nombre del equipo.
