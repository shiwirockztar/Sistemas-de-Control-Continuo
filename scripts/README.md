**Uso rápido**

- **Descripción:** Script para graficar series temporales desde un CSV y estimar el periodo de oscilación `Tu`. Si la prueba se hizo con un `Kc` que genera oscilaciones sostenidas, el usuario puede indicar `--kc` y el script reportará `Ku = Kc`.

- **Ejemplo:**

  `python3 scripts/estimate_ku.py --file mimo/data_ponly_t2.txt --kc 2.0`

- **Opciones importantes:**
  - `--file` o `-f`: ruta al archivo CSV (obligatorio).
  - `--kc`: valor de Kc usado en la prueba (opcional).
  - `--temp-col`: nombre parcial de la columna de temperatura a analizar (ej. `Temp2`).
  - `--save`: ruta PNG donde guardar la figura en vez de mostrarla.

- **Notas:**
  - El script intenta detectar automáticamente la columna de tiempo y temperatura.
  - Requiere `pandas`, `numpy` y `matplotlib`; si está disponible, usa `scipy` para mejor detección de picos.