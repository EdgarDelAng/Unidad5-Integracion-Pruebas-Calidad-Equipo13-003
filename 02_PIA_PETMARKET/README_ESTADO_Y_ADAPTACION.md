# Adaptación U5 al PIA PetMarket — Equipo 13

## Alcance usado

La matriz `../../docs/Matrices/Matriz_Pruebas_PIA_PetMarket.csv` se deriva del BRD, las historias de usuario y los criterios de aceptación de PetMarket. Se seleccionaron tres reglas: validación de inventario, procesamiento del pago y cancelación antes del envío.

## Hallazgo técnico que impide declarar E9 terminado

El ZIP U3 recibido contiene módulos de `src/application/` y `src/infrastructure/`, además de pruebas que importan `domain.model`, `domain.ports`, `domain.asignacion`, `domain.politicas` y `domain.metricas`. Sin embargo, la carpeta `src/domain/` no está incluida en el ZIP. El README del proyecto original también describe esa carpeta, pero el contenido no está en el archivo entregado.

Por ese motivo, el código U3 no puede importarse ni ejecutarse de forma íntegra con el ZIP recibido. No se añadieron implementaciones ficticias de esos módulos ni se marcaron pruebas PIA como aprobadas. La matriz de nueve casos es una propuesta trazable; sus pruebas ejecutables deben incorporarse cuando el equipo recupere el `src/domain/` completo y confirme la regla PIA-09.

## Qué sí se puede afirmar

- El proyecto U3 recibido declara persistencia en memoria, no SQL/ORM productivo.
- La pasarela incluida es simulada; no procesa pagos bancarios reales.
- El flujo de compra contempla pago, validación de inventario y preparación por almacén.
- Los documentos de U2 indican que un pago rechazado mantiene el pedido en `PENDIENTE_PAGO` y bloquea la preparación.
- La cancelación se contempla antes del envío; después de enviar, la situación se trata como incidencia o devolución.

## Próximo paso requerido para cerrar E9

Recuperar desde el repositorio GitHub la carpeta completa `src/domain/` y ejecutar la suite U3 original. Después, implementar los nueve casos como pruebas pytest sobre las clases y servicios reales, no sobre dobles que sustituyan la lógica de negocio.
