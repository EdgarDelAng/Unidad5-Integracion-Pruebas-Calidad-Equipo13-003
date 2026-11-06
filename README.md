# Unidad 5 — Integración, Pruebas y Calidad

**Equipo 13 · Componentes de Lógica de Negocios**  
**Proyecto de aplicación: PetMarket**

Este repositorio reúne los materiales de trabajo de la Unidad 5. La entrega está organizada en dos bloques independientes: el laboratorio guiado de pruebas y el Proyecto Integrador de Aprendizaje (PIA) PetMarket. Cada bloque conserva sus propios archivos, pruebas y resultados para evitar atribuir al PIA ejercicios que pertenecen únicamente al laboratorio.

El objetivo del trabajo es aplicar técnicas de pruebas de software para revisar reglas de negocio, persistencia dentro del alcance didáctico, simulación de servicios externos, autorización, cobertura e integración continua.

## Integrantes

- **Edgar Jesús Del Ángel Martínez** — 2160745
- **Israel Alejandro Pantoja Esquivel** — 2155971
- **Andrea Fernanda Rodríguez Niño** — 2160663

## Contenido

- [Estructura del repositorio](#estructura-del-repositorio)
- [1. Laboratorio guiado U5](#1-laboratorio-guiado-u5)
- [2. PIA PetMarket](#2-pia-petmarket)
- [3. Evidencias E01–E09](#3-evidencias-e01e09)
- [4. Matrices y documentación](#4-matrices-y-documentación)
- [5. Resultados de pruebas y cobertura](#5-resultados-de-pruebas-y-cobertura)
- [6. Integración continua con GitHub Actions](#6-integración-continua-con-github-actions)
- [7. Requisitos y ejecución local](#7-requisitos-y-ejecución-local)
- [8. Alcance y limitaciones](#8-alcance-y-limitaciones)

---

## Estructura del repositorio

```text
Unidad5-Integracion-Pruebas-Calidad-Equipo13-003/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── 01_LABORATORIO_U5/
│   ├── datos/
│   │   ├── casos_de_prueba.csv
│   │   ├── clientes_prueba.csv
│   │   └── pedidos_prueba.csv
│   │
│   ├── laboratorio_U5/
│   │   ├── src/
│   │   │   ├── application.py
│   │   │   ├── domain.py
│   │   │   ├── repository.py
│   │   │   └── security.py
│   │   ├── tests/
│   │   │   ├── test_order.py
│   │   │   ├── test_repository.py
│   │   │   ├── test_security.py
│   │   │   └── test_service.py
│   │   ├── pyproject.toml
│   │   ├── requirements.txt
│   │   └── README.md
│   │
│   ├── TDD_RED_BASELINE/
│   │   ├── src/
│   │   ├── tests/
│   │   ├── htmlcov/
│   │   ├── pyproject.toml
│   │   └── requirements.txt
│   │
│   └── recursos/
│       ├── documentos_profesor/
│       ├── cargar_datos_demo.py
│       ├── pedidos_prueba.sqlite3
│       └── archivos CSV y ZIP de apoyo
│
├── 02_PIA_PETMARKET/
│   ├── datos/
│   │   ├── actores.csv
│   │   ├── casos_prueba.csv
│   │   ├── catalogo.csv
│   │   ├── detalle_operaciones.csv
│   │   ├── operaciones.csv
│   │   └── transiciones_prueba.csv
│   ├── documentos_base/
│   │   ├── BRD_PetMarket.pdf
│   │   ├── Diagrama_BPMN_PetMarket.pdf
│   │   ├── Glosario_PetMarket.pdf
│   │   ├── Guia_Arquitectura_U3_PetMarket.pdf
│   │   └── Historias_Criterios_Gherkin_PetMarket.pdf
│   ├── Proyecto_U3/
│   │   ├── docs/
│   │   │   └── Matriz_E09_PetMarket.xlsx
│   │   ├── htmlcov/
│   │   ├── src/
│   │   ├── tests/
│   │   └── README.md
│   ├── tests_diseno/
│   ├── INSTRUCCIONES_ALUMNO.txt
│   ├── LEEME.txt
│   └── README_ESTADO_Y_ADAPTACION.md
│
├── 03_EVIDENCIAS/
│   ├── E01/
│   ├── E02/
│   ├── E03/
│   ├── E04/
│   ├── E05/
│   ├── E06/
│   ├── E07/
│   ├── E08/
│   └── E09/
│
├── docs/
│   ├── Bitacora_IA/
│   │   └── Bitacora_IA_U5.md
│   ├── Matrices/
│   │   ├── Matriz_Pruebas_Laboratorio_U5.csv
│   │   └── Matriz_Pruebas_PIA_PetMarket.csv
│   └── Reporte/
│       ├── Reporte_Unidad_5_PetMarket_Equipo13.docx
│       ├── Reporte_Unidad_5_PetMarket_Equipo13.pdf
│       └── Reflexion_Final_150_200_palabras.*
│
└── Reporte_Cobertura/
    ├── HTML_Laboratorio/
    └── RESULTADO_PRUEBAS_LOCAL.txt
```

> La estructura anterior representa las carpetas y archivos principales de la entrega. Se omitieron archivos auxiliares generados automáticamente, como cachés, archivos temporales y recursos internos del reporte HTML.

---

## 1. Laboratorio guiado U5

La carpeta `01_LABORATORIO_U5/` contiene el proyecto didáctico utilizado para practicar pruebas automatizadas y técnicas de calidad. Este proyecto es independiente de PetMarket.

### 1.1 Proyecto `laboratorio_U5`

La carpeta `laboratorio_U5/` contiene el proyecto base de gestión de pedidos.

| Ruta | Responsabilidad |
|---|---|
| `src/domain.py` | Reglas y validaciones del dominio de pedidos. |
| `src/application.py` | Operaciones y coordinación de la aplicación. |
| `src/repository.py` | Acceso a los datos y operaciones de persistencia del ejercicio. |
| `src/security.py` | Reglas de autorización y cancelación. |
| `tests/test_order.py` | Pruebas de reglas de pedidos y validaciones. |
| `tests/test_repository.py` | Pruebas de persistencia, confirmación y reversión. |
| `tests/test_security.py` | Pruebas de autorización. |
| `tests/test_service.py` | Pruebas de servicios y pasarela simulada. |

### 1.2 Copia de trabajo TDD

`TDD_RED_BASELINE/` conserva la versión utilizada para demostrar el ciclo **Red–Green–Refactor**, incluida la prueba específica de confirmación duplicada.

Esta carpeta tiene su propio código, pruebas y configuración. Se mantiene separada del proyecto base para que el ejercicio de TDD pueda revisarse sin confundirlo con el resto del laboratorio.

### 1.3 Datos y recursos

- `01_LABORATORIO_U5/datos/`: archivos CSV de clientes, pedidos y casos de prueba.
- `01_LABORATORIO_U5/recursos/`: script de carga, base SQLite de demostración, instrucciones, archivos base y documentos de apoyo.
- `01_LABORATORIO_U5/laboratorio_U5/requirements.txt`: dependencias del proyecto.
- `01_LABORATORIO_U5/laboratorio_U5/pyproject.toml`: configuración de herramientas y pruebas.

---

## 2. PIA PetMarket

La carpeta `02_PIA_PETMARKET/` reúne el material de referencia y el proyecto utilizado para revisar reglas de negocio del PIA.

PetMarket representa una tienda de productos para mascotas que coordina pedidos y preparación distribuida entre dos almacenes, identificados como **A1** y **A2**. La documentación del proyecto aborda compra y pago, inventario, preparación, autorización, logística y entrega.

### 2.1 Documentos base

La carpeta `documentos_base/` conserva los documentos funcionales y de arquitectura que sirven para interpretar las reglas del proyecto:

| Documento | Contenido |
|---|---|
| `BRD_PetMarket.pdf` | Requisitos y reglas de negocio. |
| `Diagrama_BPMN_PetMarket.pdf` | Representación de los procesos del negocio. |
| `Glosario_PetMarket.pdf` | Definiciones y términos del dominio. |
| `Guia_Arquitectura_U3_PetMarket.pdf` | Referencia de arquitectura del proyecto. |
| `Historias_Criterios_Gherkin_PetMarket.pdf` | Historias de usuario, criterios de aceptación y escenarios. |

### 2.2 Datos del PIA

La carpeta `datos/` incluye archivos CSV para representar actores, casos de prueba, catálogo, operaciones, detalle de operaciones y transiciones.

### 2.3 Proyecto y pruebas

Dentro de `Proyecto_U3/` se conservan el proyecto de referencia, los archivos de pruebas, la matriz E09 y el reporte HTML de cobertura. El README interno del PIA describe una arquitectura basada en Domain Model, Application Services, Repository/Unit of Work y CQRS básico.

### 2.4 Escenarios E09

La matriz `docs/Matriz_E09_PetMarket.xlsx` y el archivo general `docs/Matrices/Matriz_Pruebas_PIA_PetMarket.csv` permiten consultar las reglas seleccionadas y su relación con las pruebas.

Los nueve escenarios documentados se agrupan en tres procesos:

1. **Confirmación de compra y pago:** inventario distribuido, rechazo del cobro y validación de cantidades.
2. **Preparación por almacén:** actualización de subórdenes, autorización por almacén y transiciones permitidas.
3. **Entrega y logística:** entrega exitosa, intento fallido y rechazo de despacho sin empaque.

La evidencia de ejecución E09 se encuentra en `03_EVIDENCIAS/E09/`.

---

## 3. Evidencias E01–E09

La carpeta `03_EVIDENCIAS/` contiene las capturas que respaldan las actividades realizadas.

| Evidencia | Tema | Archivos principales |
|---|---|---|
| **E01** | Preparación del entorno y ejecución inicial | `E01_Entorno_Pruebas.png` |
| **E02** | Pruebas unitarias | `E02_Pruebas_Unitarias.png` |
| **E03** | Ciclo TDD | `E03_01_RED.png`, `E03_02_GREEN.png`, `E03_03_REFACTOR.png` |
| **E04** | Persistencia y transacciones del laboratorio | `E04_Integracion_SQLAlchemy.png` |
| **E05** | Mocks y simulación de pago | `E05_Mocks_Pago.png` |
| **E06** | Seguridad y autorización | `E06_Autorizacion.png` |
| **E07** | Cobertura y análisis estático | `E07_01_Cobertura.png`, `E07_02_Reporte_HTML.png`, `E07_03_Ruff.png` |
| **E08** | Integración continua | `E08_01_CI_VERDE.png`, `E08_02_CI_ROJO.png`, `E08_03_CI_RECUPERADO.png` |
| **E09** | Adaptación de pruebas al PIA PetMarket | Matriz, ejecución, cobertura, HTML y explicación |

### 3.1 Secuencia de CI documentada en E08

E08 conserva tres momentos del pipeline:

- **Ejecución verde:** el flujo termina correctamente.
- **Fallo controlado:** se introduce un cambio que provoca el fallo de una prueba.
- **Recuperación:** se corrige el cambio y el pipeline vuelve a finalizar correctamente.

Las capturas se encuentran en `03_EVIDENCIAS/E08/`.

---

## 4. Matrices y documentación

### 4.1 Matrices de pruebas

En `docs/Matrices/` se encuentran:

- `Matriz_Pruebas_Laboratorio_U5.csv`: casos del laboratorio guiado.
- `Matriz_Pruebas_PIA_PetMarket.csv`: escenarios relacionados con las reglas de PetMarket.

La matriz E09 también se conserva en `02_PIA_PETMARKET/Proyecto_U3/docs/Matriz_E09_PetMarket.xlsx`.

### 4.2 Reporte de Unidad 5

La carpeta `docs/Reporte/` contiene:

- `Reporte_Unidad_5_PetMarket_Equipo13.docx`: versión editable.
- `Reporte_Unidad_5_PetMarket_Equipo13.pdf`: versión para lectura y entrega.
- `Reflexion_Final_150_200_palabras.md` y `.docx`: reflexión final.

### 4.3 Bitácora de uso de IA

`docs/Bitacora_IA/Bitacora_IA_U5.md` contiene el registro de apoyo y uso de herramientas de IA durante el desarrollo de la unidad.

---

## 5. Resultados de pruebas y cobertura

Los resultados deben interpretarse por separado, porque el laboratorio y el PIA utilizan proyectos y conjuntos de pruebas distintos.

### 5.1 Laboratorio guiado

El registro `Reporte_Cobertura/RESULTADO_PRUEBAS_LOCAL.txt` documenta una ejecución de **20 pruebas aprobadas**. En ese registro, la cobertura del código fuente del laboratorio fue de **100% sobre 53 sentencias**.

El reporte HTML se puede consultar abriendo:

```text
Reporte_Cobertura/HTML_Laboratorio/index.html
```

### 5.2 PIA PetMarket

La evidencia E09 registra la ejecución de **66 pruebas**, con resultado `OK`, y una cobertura global de **95% sobre 475 sentencias**.

El reporte HTML del PIA se encuentra en:

```text
02_PIA_PETMARKET/Proyecto_U3/htmlcov/index.html
```

Los porcentajes de ambos proyectos no se combinan: corresponden a bases de código diferentes.

---

## 6. Integración continua con GitHub Actions

El workflow general se encuentra en:

```text
.github/workflows/ci.yml
```

Se activa ante eventos `push` y `pull_request`. Su configuración utiliza Ubuntu y Python 3.12.

El flujo realiza las siguientes tareas:

1. Descarga el repositorio con `actions/checkout`.
2. Configura Python mediante `actions/setup-python`.
3. Instala las dependencias del proyecto `01_LABORATORIO_U5/TDD_RED_BASELINE`.
4. Instala Ruff.
5. Ejecuta la revisión estática con `ruff check src tests`.
6. Ejecuta pytest con cobertura y un mínimo configurado de 80%.
7. Comprueba la compilación con `python -m compileall -q src`.

**Alcance del workflow:** el archivo está ubicado en la raíz del repositorio, pero sus comandos trabajan específicamente sobre `01_LABORATORIO_U5/TDD_RED_BASELINE`. Por lo tanto, el pipeline no representa la ejecución automática de todas las pruebas del PIA.

---

## 7. Requisitos y ejecución local

### 7.1 Laboratorio guiado

**Requisitos:** Python 3.11 o posterior y pip.

Abrir una terminal en:

```text
01_LABORATORIO_U5/TDD_RED_BASELINE/
```

Crear y activar un entorno virtual en Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

Instalar dependencias:

```cmd
pip install -r requirements.txt
```

Ejecutar las pruebas:

```cmd
python -m pytest -v
```

Ejecutar pruebas con cobertura:

```cmd
python -m pytest -v --cov=src --cov-report=term-missing --cov-fail-under=80
```

Revisar estilo:

```cmd
python -m ruff check src tests
```

Generar el reporte HTML:

```cmd
python -m pytest --cov=src --cov-report=html
```

Abrir `htmlcov/index.html` en el navegador.

### 7.2 PIA PetMarket

El README del proyecto indica que el prototipo utiliza Python 3.11 o posterior y no requiere dependencias externas para la suite de referencia.

Desde la carpeta `02_PIA_PETMARKET/Proyecto_U3/`, en Windows CMD:

```cmd
set PYTHONPATH=src
python -m unittest discover -s tests -v
```

En PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

Para ejecutar cobertura con `coverage.py`, si está instalado:

```cmd
python -m coverage run --source=src -m unittest discover -s tests -v
python -m coverage report -m
python -m coverage html
```

El reporte HTML se genera en `htmlcov/`.

---

## 8. Alcance y limitaciones

- El laboratorio guiado es un ejercicio didáctico independiente del PIA PetMarket.
- La persistencia con SQLAlchemy/SQLite y las verificaciones de commit/rollback pertenecen al laboratorio; no deben presentarse como persistencia productiva de PetMarket.
- PetMarket es un prototipo de referencia con repositorios y unidad de trabajo en memoria.
- La pasarela de pago utilizada en las pruebas es simulada; no se procesan cobros bancarios reales.
- Los resultados de las pruebas no demuestran integración real con paqueterías, operación de una interfaz web productiva ni concurrencia entre usuarios.
- La cobertura indica qué sentencias fueron ejecutadas durante las pruebas; no garantiza por sí sola que todos los comportamientos posibles estén libres de defectos.
- El pipeline de GitHub Actions configurado en la raíz ejecuta el laboratorio TDD indicado en su `working-directory`, no la suite completa del PIA.

Estas limitaciones forman parte del alcance técnico que debe considerarse al interpretar los resultados y proponer mejoras.

---

## Recomendaciones antes de publicar

1. Revisar que las matrículas y nombres de los integrantes sean correctos.
2. Confirmar que las capturas E01–E09 estén presentes en sus carpetas.
3. No incluir archivos `.env`, contraseñas, tokens ni credenciales reales.
4. Revisar los documentos base antes de hacer público el repositorio, ya que pueden contener datos personales o información académica del equipo.
5. Mantener los reportes HTML y las matrices junto con el código para facilitar la revisión de los resultados.

---

**Equipo 13 · Unidad 5 — Integración, Pruebas y Calidad**
