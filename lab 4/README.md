# Lab 4 - Control P/PID en TempLABUdeA

Este documento resume que se esta haciendo en el codigo y que se debe entregar en la practica.

## Objetivos de la practica

1. Desarrollar el modelo dinamico continuo de primer orden para cada zona termica, considerando conduccion, conveccion y radiacion.
2. Disenar y sintonizar controladores PID independientes para cada secuencia de temperatura, asegurando estabilidad y desempeno especificado.
3. Implementar el controlador en TempLABUdeA y validar el comportamiento experimental frente al modelo teorico.

## Codigo actual y alcance

El script [lab4.py](lab4.py) en esta carpeta esta enfocado en lazo para Q1/T1 y permite comparar P-only contra PID en el calculo de la accion de control.

- Lee temperatura medida T1.
- Calcula error e(t) = TSP - TPV(t).
- Aplica Q1 con saturacion 0 a 100 %.
- Registra datos en archivo y genera grafica final.

## Procedimiento A - Cuantificacion de offset con P-only

### Modelo de control P-only

Se usa:

$$Q(t) = Q_{bias} + K_c e(t), \quad e(t)=TSP-TPV(t)$$

Con este enfoque, en un proceso no integrador aparece error en estado estacionario:

$$e_{\infty} = TSP - TPV_{\infty}$$

En TempLABUdeA se toma normalmente $Q_{bias}=0$ al pasar de manual a automatico.

### Sintonia inicial P-only (ITAE)

Usar como punto de partida:

$$K_c = 0.20\left(\frac{\tau_p}{\theta_p}\right)^{1.22}$$

Luego ejecutar y medir $e_{\infty}$ experimental.

## Procedimiento B - PID por Ziegler-Nichols

1. Configurar lazo cerrado con accion proporcional pura (I=0, D=0).
2. Aumentar $K_c$ hasta oscilaciones sostenidas.
3. Medir:
   Ku = ganancia critica.
   Pu = periodo de oscilacion.
4. Calcular parametros PID:

$$K_p = 0.6Ku, \quad T_i = 0.5Pu, \quad T_d = 0.125Pu$$

5. Implementar:

$$u(t) = K_p\left[e(t) + \frac{1}{T_i}\int_0^t e(\tau)d\tau + T_d\frac{de}{dt}\right]$$

## Lo que se pide especificamente en lineas 90 a 93

En [lab4.py](lab4.py#L90) a [lab4.py](lab4.py#L93) esta el punto clave de la practica:

- [lab4.py](lab4.py#L90): formula PID completa (actualmente comentada).
- [lab4.py](lab4.py#L93): formula P-only activa para comparacion.

Trabajo solicitado sobre ese bloque:

1. Ejecutar pruebas con la ecuacion P-only (linea 93) y variar $K_c$.
2. Activar la ecuacion PID (linea 90), desactivar P-only y repetir barrido de $K_c$.
3. Usar parametros de Ziegler-Nichols como base y ajustar fino si hace falta.
4. Comparar P vs PID con metricas transitorias y estacionarias.

Sugerencia de barrido de ganancia:

- $0.5K_{c,nom}$
- $0.8K_{c,nom}$
- $1.0K_{c,nom}$
- $1.2K_{c,nom}$
- $1.5K_{c,nom}$

## Implementacion practica

1. Cargar firmware base en Arduino.
2. Ejecutar script Python para adquisicion y control.
3. Registrar tiempo, temperatura y potencia en CSV/TXT.
4. Hacer pruebas de escalon y distintas consignas.

Comando de ejecucion (simulacion):

```bash
python3 lab4.py --sim --min 6.2
```

## Validacion y analisis

Comparar respuesta experimental y simulada usando:

- Sobreimpulso (%).
- Tiempo de asentamiento.
- Error en estado estacionario.

Discutir discrepancias (modelo, parametros, ruido, saturacion) y proponer ajustes.

## Resultados de aprendizaje

Al finalizar, se espera que el estudiante pueda:

1. Modelar sistemas termicos de primer orden y derivar funciones de transferencia.
2. Disenar, simular e implementar controladores P/PID en sistema real.
3. Evaluar desempeno con indicadores clasicos de control.

## Entregables

1. Documento tecnico con:
   - Derivacion del modelo y funciones de transferencia.
   - Calculo y justificacion de parametros del controlador.
   - Comparacion grafica y cuantitativa entre simulacion y experimento.
2. Codigo fuente del controlador y scripts de adquisicion.
3. Datos crudos (CSV/TXT) y graficas finales.

## Rubrica (resumen)

| Criterio | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Precision del modelo | Ausente | Erroneo | Parcial | Funcional basico | Bueno | Excelente |
| Sintonia PID | Ausente | Incorrecta | Suboptima | Aceptable | Buena | Optima |
| Comparacion sim/exp | N/D | >25 % | 20-25 % | 15-20 % | 10-15 % | <10 % |
| Calidad de informe y codigo | Ausente | Muy deficiente | Deficiente | Aceptable | Buena | Excelente |

## Recomendaciones tecnicas

- Inicializar siempre $Q_{bias}$ e integral en cero.
- Mantener periodo de muestreo aproximadamente constante.
- Implementar anti-windup al saturar actuador.
- Cerrar en forma segura: $Q1=0$, $Q2=0$ y cierre de conexion.
