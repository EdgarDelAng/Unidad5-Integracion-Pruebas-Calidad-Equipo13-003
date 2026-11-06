# Bitácora de uso de IA — Unidad 5

## Prompt utilizado

“Analiza el proyecto base y los criterios de Unidad 5. Propón pruebas pequeñas de éxito, error y límite; no inventes reglas. Señala supuestos, riesgos y archivos que falten. Explica qué contrato verifica cada prueba”.

## Propuesta aceptada

Se añadieron pruebas para descuento VIP y cliente regular con total de $200, confirmación duplicada, persistencia de un pedido de $250, rechazo de pago VIP verificando el importe enviado al mock, autorización administrativa y límite temporal exacto de 24 horas.

## Revisión humana

Se contrastaron los casos del laboratorio con el manual corregido. Se conservó el comportamiento de `security.py`: un pedido `SHIPPED` no se cancela ni siquiera por administrador; un administrador puede cancelar otros estados; el propietario dispone de menos de 24 horas. Se evitó cambiar esta regla por ejemplos distintos.

## Sugerencia corregida/rechazada

No se aceptó generar pruebas PIA ejecutables a partir de clases supuestas, porque el ZIP de PetMarket recibido no contiene `src/domain/`, que es importado por las pruebas y servicios U3. Se dejó una matriz trazable con estado pendiente, en lugar de reportar resultados inventados.

## Limitaciones

La suite ejecutada corresponde al proyecto base del laboratorio, no al PIA. El pipeline remoto y las capturas de E3/E8 requieren ejecución por el equipo.
