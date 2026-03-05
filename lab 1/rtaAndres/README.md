# README - Identificacion FOPDT y Sintonia PID

## 1. Objetivo del notebook `lab.ipynb`
Este notebook identifica un modelo de primer orden con tiempo muerto (FOPDT) a partir de datos experimentales de temperatura, y compara dos metodos de identificacion:

- Ziegler-Nichols por curva de reaccion (tangente en el punto de inflexion).
- Smith (niveles 28.3% y 63.2%).

Con los parametros del modelo (`K`, `tau`, `theta`) se puede obtener una sintonia inicial del controlador PID (`Kp`, `Ti`, `Td`) y luego optimizarla para mejorar desempeno.

## 2. Estructura y logica del notebook
El notebook esta separado por bloques para que cada etapa tenga una funcion clara.

### Celda 1-2: Importaciones y contexto
Se importan `pandas`, `numpy` y `matplotlib` para manejo de datos, calculo numerico y visualizacion.

### Celda 3-4: Carga y limpieza de datos
Se carga `data_Q2.txt`, se limpian encabezados y se extraen:

- `t`: tiempo (s)
- `u`: entrada (porcentaje de calentador)
- `y`: salida (temperatura)

### Celda 5: Deteccion del escalon
Se detecta el instante donde la entrada cambia (escalon) y se calcula `delta_u`.

Teoria: la identificacion FOPDT asume una excitacion tipo escalon para estimar dinamica dominante del proceso.

### Celda 6: Regresion y punto de inflexion
Se ajusta un polinomio de grado 6 para suavizar la salida y se deriva analiticamente para localizar la maxima pendiente.

Teoria: el punto de inflexion aproxima la zona de mayor sensibilidad dinamica de la curva de reaccion.

### Celda 7: Parametros por Ziegler-Nichols
Con la tangente en el punto de inflexion se obtienen:

- `K = (y_final - y_initial) / delta_u`
- `theta`: tiempo muerto aparente
- `tau`: constante de tiempo aparente

Modelo usado:

`G(s) = K * exp(-theta*s) / (tau*s + 1)`

### Celda 8: Parametros por Smith
Se calculan los tiempos `t1` y `t2` en 28.3% y 63.2% del cambio total de salida.

Formulas de Smith:

- `tau = 1.5 * (t2 - t1)`
- `theta = (1.5*t1 - 0.5*t2) - t0`

Teoria: esos porcentajes capturan la geometria de una respuesta de primer orden con retardo, permitiendo estimar `tau` y `theta` sin tangente explicita.

### Celda 9-11: Graficas
Se generan tres visualizaciones:

- Ajuste por tangente (ZN).
- Ajuste por Smith (incluye niveles 28.3% y 63.2%).
- Comparacion final de ambos modelos frente a datos reales.

Estas graficas permiten validar si el modelo identificado representa bien el proceso real.

## 3. Como calcular `Kp`, `Ti`, `Td` desde el modelo identificado
Una vez identificados `K`, `tau`, `theta`, se obtiene una sintonia inicial PID.

> Se recomienda iniciar con el metodo que mejor ajuste visual/numerico (ZN o Smith) y luego optimizar.

### 3.1 Sintonia inicial (ZN reaccion, PID ideal)
Para un PID en forma ideal/paralela:

`C(s) = Kp * (1 + 1/(Ti*s) + Td*s)`

Reglas Ziegler-Nichols (curva de reaccion):

- `Kp = 1.2 * tau / (K * theta)`
- `Ti = 2 * theta`
- `Td = 0.5 * theta`

Justificacion: estas reglas buscan respuesta rapida, pero suelen introducir sobreimpulso moderado/alto. Son un buen punto de partida, no el ajuste final.

## 4. Optimizacion de `Kp`, `Ti`, `Td` para desempeno
Para cumplir criterios de control (tiempo de asentamiento, sobreimpulso y error), se debe refinar la sintonia inicial.

### 4.1 Criterios de desempeno
En lazo cerrado, usar un escalon de referencia y medir:

- Tiempo de asentamiento `Ts` (banda tipica 2% o 5%).
- Sobreimpulso `Mp` (%).
- Error en regimen permanente `ess` o integral del error (`IAE`, `ISE`, `ITAE`).

### 4.2 Funcion de costo sugerida
Optimizar una combinacion ponderada:

`J = w1*Ts + w2*Mp + w3*IAE + w4*|ess|`

con `w1, w2, w3, w4` definidos segun prioridad del laboratorio.

### 4.3 Procedimiento recomendado
1. Identificar `K, tau, theta` (ya hecho en notebook).
2. Calcular `Kp, Ti, Td` iniciales con ZN.
3. Simular lazo cerrado con ese PID.
4. Medir `Ts`, `Mp`, `IAE`, `ess`.
5. Ajustar `Kp, Ti, Td` con optimizacion numerica (por ejemplo `scipy.optimize.minimize`) minimizando `J`.
6. Verificar robustez con pequenas variaciones de modelo (`K`, `tau`, `theta`).

## 5. Criterio de "parametros correctamente calculados, justificados y optimizados"
Se considera que `Kp`, `Ti`, `Td` estan correctamente reportados cuando:

- Se muestra origen de calculo: reglas y formulas usadas.
- Se indica el modelo base (`K`, `tau`, `theta`) del cual provienen.
- Se comparan resultados antes/despues de optimizacion.
- Se reportan metricas finales (`Ts`, `Mp`, `ess` o `IAE`).
- Se argumenta por que la sintonia final es mejor (por ejemplo: menor `Ts` con `Mp` aceptable y `ess` cercano a 0).

## 6. Recomendaciones practicas para tu entrega
- Reportar en tabla: metodo de identificacion, `K`, `tau`, `theta`, `Kp`, `Ti`, `Td`, `Ts`, `Mp`, `IAE`.
- Incluir graficas comparativas de salida real vs modelo y de respuesta en lazo cerrado.
- Si hay ruido, usar suavizado moderado y justificarlo.
- Evitar sintonias con `Mp` excesivo o accion derivativa demasiado alta (sensibilidad a ruido).

## 7. Conclusion tecnica
El notebook implementa correctamente la identificacion FOPDT por Ziegler-Nichols y Smith. Esos parametros son la base para calcular una sintonia inicial PID. La calidad final del controlador no depende solo de la formula inicial, sino de la optimizacion posterior con criterios de desempeno (`Ts`, `Mp`, `error`) y su validacion en simulacion/laboratorio.
