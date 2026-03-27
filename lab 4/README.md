# Lab 4 - Control de temperatura (solo Q1)

Este laboratorio implementa un controlador para el sistema TCLab usando **solo el calentador Q1** y la temperatura **T1**.

## 1) Que hace el codigo `lab4.py`

- Se conecta al TCLab real (o simulacion con `--sim`).
- Define un setpoint fijo para T1 (`tset1 = 23.0 C`).
- Ejecuta un lazo de control cada segundo.
- Calcula la accion de control `u1` y la aplica a Q1 (saturada entre 0 y 100%).
- Guarda resultados en `data_PID_Q1.txt` y una figura en `resultado_PID_Q1.png`.

## 2) Lo mas importante: que piden en las lineas 90 a 93

En ese bloque se compara:

- **Control PID completo** (comentado en la linea 90):

  ```python
  u1 = q_bias + kc * error1 + (kc / tau_i) * error1_int + kc * tau_d * deriv1
  ```

- **Control P puro** (activo en la linea 93):

  ```python
  u1 = q_bias + kc * error1
  ```

### Interpretacion de la tarea

Lo que normalmente te piden es:

1. Usar parametros iniciales tipo Ziegler-Nichols para el PID.
2. **Variar `kc`** para observar como cambia la respuesta del sistema.
3. Comparar desempeno entre P puro y PID completo.

## 3) Como variar `kc` correctamente

En `run_experiment`, `kc` se define al inicio:

```python
kc = 0.2 * (taup / tethap) ** 1.22
```

Para hacer el analisis, prueba varios valores alrededor de ese `kc` nominal:

- `0.5 * kc_nominal`
- `0.8 * kc_nominal`
- `1.0 * kc_nominal`
- `1.2 * kc_nominal`
- `1.5 * kc_nominal`

Manteniendo `tau_i` y `tau_d` fijos al inicio (segun tu sintonia base), evalua:

- tiempo de subida,
- sobreimpulso,
- tiempo de establecimiento,
- error en estado estacionario,
- saturacion de Q1.

## 4) Flujo recomendado para la practica

1. Ejecuta con **P puro** (linea 93 activa, linea 90 comentada).
2. Repite variando `kc` y guarda resultados.
3. Cambia a **PID completo** (linea 90 activa, linea 93 comentada).
4. Repite la misma variacion de `kc`.
5. Compara curvas T1 y Q1 para justificar cual ajuste funciona mejor.

## 5) Ejecucion

En la carpeta `lab 4`:

```bash
python3 lab4.py --sim --min 6.2
```

Sin `--sim`, el script intentara usar hardware real.

## 6) Entregable sugerido

Incluye una tabla como esta para cada prueba:

| Modo | kc usado | tau_i | tau_d | Sobreimpulso | t_establecimiento | Error final |
|---|---:|---:|---:|---:|---:|---:|
| P | ... | - | - | ... | ... | ... |
| PID | ... | ... | ... | ... | ... | ... |

Y concluye:

- que efecto tuvo aumentar/disminuir `kc`,
- en que punto el sistema mejora,
- cuando empieza a oscilar o saturar.
