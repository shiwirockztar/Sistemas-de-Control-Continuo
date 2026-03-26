# Taller 1 - Sistema Masa-Resorte-Amortiguador de 2 GDL con Excitacion de Base

## Descripción General

Este taller modela la dinámica vertical de un sistema mecánico de **dos grados de libertad (2 GDL)**, representativo de una suspensión simplificada de un vehículo.

### Componentes del Sistema

- `m1`: masa no suspendida (rueda/eje)
- `m2`: masa suspendida (chasis)
- `k1`: rigidez del neumático respecto a la base
- `k2`: rigidez de la suspensión entre `m1` y `m2`
- `c`: amortiguamiento viscoso de la suspensión entre `m1` y `m2`
- `U(x)`: perfil irregular del camino en función del espacio
- `y(t)`: entrada de base en el tiempo, definida como `y(t) = U(x(t))`

---

## 1. Diagrama del Sistema

El sistema equivale a:

```
        ↑ Y(t)
        m2
        |
      [c] [k2]
        |
        m1   ↑ X(t)
        |
       [k1]
        |
    U(x)(t) = A sen(ωt)
```

La base (suelo) vibra con `y(t)`:
- `m1`: rueda
- `m2`: chasis

---

## 2. Ecuaciones Diferenciales

### Para m1 (masa no suspendida):
$$m_1 \ddot{X} + c(\dot{X} - \dot{Y}) + k_2(X - Y) + k_1(X - U(x)) = 0$$

### Para m2 (masa suspendida):
$$m_2 \ddot{Y} + c(\dot{Y} - \dot{X}) + k_2(Y - X) = 0$$

---

## 3. Condiciones Iniciales

Se asume que el sistema comienza en reposo:

$$X(0) = 0, \quad \dot{X}(0) = 0$$
$$Y(0) = 0, \quad \dot{Y}(0) = 0$$

---

## 4. Representación en Forma de Estado

### Vector de estado:
$$\mathbf{x} = \begin{bmatrix} X \\ Y \\ \dot{X} \\ \dot{Y} \end{bmatrix}$$

### Ecuación de estado:
$$\dot{\mathbf{x}} = A\mathbf{x} + B U(x)(t)$$

### Matriz A:
$$A = \begin{bmatrix} 
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1 \\
-\frac{k_1+k_2}{m_1} & \frac{k_2}{m_1} & -\frac{c}{m_1} & \frac{c}{m_1} \\
\frac{k_2}{m_2} & -\frac{k_2}{m_2} & \frac{c}{m_2} & -\frac{c}{m_2}
\end{bmatrix}$$

### Matriz B:
$$B = \begin{bmatrix} 0 \\ 0 \\ \frac{k_1}{m_1} \\ 0 \end{bmatrix}$$

### Matriz C (salida):
$$C = \begin{bmatrix} 0 & 1 & 0 & 0 \end{bmatrix}$$
(observando la posición del chasis `Y`)

### Matriz D:
$$D = 0$$

---

## 5. Función de Transferencia

### Entrada:
- `U(x)(t)`: desplazamiento de base (perfil del camino)

### Salida típica:
- `Y(t)`: movimiento del chasis

### Función de transferencia:
$$\frac{Y(s)}{U(x)(s)} = \frac{k_1 k_2(m_1 s^2 + cs + k_1 + k_2)}{(m_1 s^2 + cs + k_1 + k_2)(m_2 s^2 + cs + k_2) - (cs + k_2)^2}$$

**Nota:** Este es un sistema de 4º orden.

---

## 6. Objetivos del Taller

1. Plantear correctamente el modelo dinámico en tiempo continuo.
2. Obtener y validar las ecuaciones diferenciales acopladas.
3. Simular la respuesta temporal para una entrada senoidal de base.
4. Analizar el efecto de `m1`, `m2`, `k1`, `k2` y `c` en el comportamiento del sistema.
5. Evaluar métricas de desempeño como amplitud, resonancia y confort (respuesta en `y`).

---

## 7. Simulación en MATLAB

```matlab
% Parámetros del sistema
m1 = 10;
m2 = 50;
k1 = 1000;
k2 = 1500;
c = 100;

% Matrices de estado
A = [0 0 1 0;
     0 0 0 1;
     -(k1+k2)/m1 k2/m1 -c/m1 c/m1;
     k2/m2 -k2/m2 c/m2 -c/m2];

B = [0; 0; k1/m1; 0];
C = [0 1 0 0]; % salida x2
D = 0;

% Sistema en espacio de estado
sys = ss(A, B, C, D);

% Señal de entrada (excitación de base)
t = 0:0.01:10;
y = sin(2*t);

% Simulación
lsim(sys, y, t)
```

---

## 8. Simulación en Python

```python
import numpy as np
from scipy.signal import StateSpace, lsim
import matplotlib.pyplot as plt

% Parámetros del sistema
m1, m2 = 10, 50
k1, k2 = 1000, 1500
c = 100

% Matrices de estado
A = [[0, 0, 1, 0],
     [0, 0, 0, 1],
     [-(k1+k2)/m1, k2/m1, -c/m1, c/m1],
     [k2/m2, -k2/m2, c/m2, -c/m2]]

B = [[0], [0], [k1/m1], [0]]
C = [[0, 1, 0, 0]]
D = [[0]]

% Sistema en espacio de estado
sys = StateSpace(A, B, C, D)

% Señal de entrada (excitación de base)
t = np.linspace(0, 10, 1000)
y = np.sin(2*t)

% Simulación
t, response, _ = lsim(sys, y, t)

% Gráfica
plt.plot(t, response)
plt.xlabel("Tiempo (s)")
plt.ylabel("x2(t) (m)")
plt.title("Respuesta del Chasis a Excitación de Base")
plt.grid(True)
plt.show()
```

---

## 9. Implementación en Simulink

### Ecuaciones a implementar en Simulink:

$$\ddot{x}_1 = \frac{-k_1(x_1 - y) - k_2(x_1 - x_2) - c(\dot{x}_1 - \dot{x}_2)}{m_1}$$

$$\ddot{x}_2 = \frac{-k_2(x_2 - x_1) - c(\dot{x}_2 - \dot{x}_1)}{m_2}$$

### Bloques necesarios:

- 4 bloques Integrator (para derivar aceleración a velocidad a posición)
- Bloques Sum (para las restas)
- Bloques Gain (para las ganancias/parámetros)
- 1 bloque Sine Wave (entrada `y(t)`)
- Bloques Scope (para visualizar)

### Construcción simplificada (recomendado):

Usa un **State-Space block** directamente:

1. Agrega bloque `State-Space` en Simulink
2. Configura las matrices A, B, C, D
3. Conecta entrada: Sine Wave
4. Conecta salida: Scope
5. Simula y observa

---

## 10. Parámetros de Ejemplo

| Parámetro | Valor |
|-----------|-------|
| m1        | 10 kg |
| m2        | 50 kg |
| k1        | 1000 N/m |
| k2        | 1500 N/m |
| c         | 100 N·s/m |

---

## 11. Interpretación de Resultados

### Comportamiento esperado:

- **x1(t)**: Vibra significativamente (masa no suspendida responde directamente a y(t))
- **x2(t)**: Oscilación más suave (la suspensión atenúa vibraciones)

### Métricas clave:

- Si `c ↑`: menos vibración → mayor confort
- Si `k2 ↑`: más rígido → menos cómodo
- Si `m2 ↑`: más estable pero responde más lentamente
- Si `c` es muy pequeño: resonancia pronunciada
- Si `c` es muy grande: amortiguamiento excesivo

### Validación:

Si `|x2(t)| < |x1(t)|` en general, el sistema está cumpliendo su función de aislamiento de vibraciones.

---

## 12. Flujo de Trabajo Recomendado

1. **Definir parámetros físicos y condiciones iniciales**
2. **Implementar el sistema** en forma de estado o matricial
3. **Simular en MATLAB/Simulink o Python**
4. **Graficar** `y(t)`, `x1(t)`, `x2(t)` y aceleraciones (si aplica)
5. **Analizar resultados** y conclusiones técnicas

---

## 13. Entregables Recomendados

- Desarrollo teórico del modelo
- Código de simulación (MATLAB/Python/Simulink)
- Gráficas principales comentadas
- Análisis de sensibilidad de parámetros
- Conclusiones sobre el comportamiento dinámico del sistema

---

## 14. Notas Adicionales

- Si el taller especifica valores numéricos particulares, agrégalos en una tabla para facilitar reproducción
- Verifica que las unidades sean consistentes (kg, N, m, s)
- Documenta todo paso en comentarios claros
- Guarda datos de simulación si necesitas validar múltiples escenarios

---

## Recursos Complementarios

- MATLAB/Simulink Documentation: Control System Toolbox
- Python: scipy.signal, numpy, matplotlib
- Conceptos: Dinámica de sistemas, análisis de vibraciones, teoría de suspensiones
