# TDD_RED_BASELINE

Copia aislada del proyecto pequeño del laboratorio para documentar el ejercicio Red–Green–Refactor.

- La prueba `tests/test_tdd_confirmar_dos_veces.py` comprueba que un pedido no se confirme dos veces.
- El código incluido contiene la validación y por eso la suite queda en estado GREEN.
- Para reproducir RED en clase, retirar temporalmente la condición `if self.status == "CONFIRMED":` de `src/domain.py`, ejecutar `pytest -q tests/test_tdd_confirmar_dos_veces.py` y conservar la salida fallida como evidencia.
- Restaurar inmediatamente la condición, volver a ejecutar y guardar la evidencia GREEN.
- La carpeta no contiene una captura RED fabricada; el equipo debe generarla ejecutando el procedimiento.
