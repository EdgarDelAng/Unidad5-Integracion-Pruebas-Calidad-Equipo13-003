# Unidad 5 — PetMarket | Equipo 13

Estructura del paquete:

```text
Unidad5_PetMarket_Equipo13/
├── 01_LABORATORIO_U5/
│   ├── datos/
│   ├── laboratorio_U5/
│   ├── recursos/
│   └── TDD_RED_BASELINE/
├── 02_PIA_PETMARKET/
├── 03_EVIDENCIAS/
├── Reporte_Cobertura/
├── docs/
│   ├── Matrices/
│   ├── Reporte/
│   └── Bitacora_IA/
├── README.md
└── .gitignore
```

## Qué contiene cada carpeta

- `datos/`: archivos CSV de prueba del laboratorio.
- `laboratorio_U5/`: proyecto Python base extraído del ZIP proporcionado para la actividad.
- `recursos/`: ZIP original del proyecto base, SQLite de demostración, script de carga, instrucciones y documentos del profesor.
- `TDD_RED_BASELINE/`: copia aislada con la prueba específica de confirmación duplicada para documentar TDD.
- `02_PIA_PETMARKET/`: archivos del PIA y documentos anteriores del equipo.
- `03_EVIDENCIAS/`: guía de capturas que el equipo debe producir al ejecutar cada actividad.
- `Reporte_Cobertura/`: reporte HTML existente y registro de resultados disponibles.
- `docs/`: matrices, reporte y bitácora.

## Separación de reglas

El proyecto de `laboratorio_U5/` es el ejercicio didáctico de la unidad. No se deben copiar automáticamente sus reglas como requisitos oficiales de PetMarket.

## Ejecución

Abrir una terminal en `01_LABORATORIO_U5/laboratorio_U5/`:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
pytest -v
pytest -v --cov=src --cov-report=html --cov-fail-under=80
ruff check src tests
```

## Estado de PetMarket

El ZIP U3 recibido no contiene `src/domain/`, aunque varios módulos y pruebas del proyecto dependen de ese paquete. Por ese motivo, la matriz PIA se conserva como trazabilidad propuesta y sus casos no se marcan como ejecutados hasta recuperar los módulos originales.

## Evidencias pendientes de captura real

- E03: RED, GREEN y REFACTOR.
- E07: cobertura y Ruff ejecutados en el equipo.
- E08: ejecuciones verde, roja y recuperada de GitHub Actions.
- E09: pruebas PIA ejecutadas tras recuperar `src/domain/`.

No se incluyen capturas inventadas ni se afirma que exista una ejecución remota de GitHub Actions.
