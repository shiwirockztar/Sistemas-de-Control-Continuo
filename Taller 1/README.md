# Taller 1 - Sistema masa-resorte-amortiguador de 2 GDL con excitacion de base

## Descripcion

Este taller modela la dinamica vertical de un sistema mecanico de **dos grados de libertad (2 GDL)**, representativo de una suspension simplificada:

- `m1`: masa no suspendida (rueda/eje).
- `m2`: masa suspendida (chasis).
- `k1`: rigidez del neumatico respecto a la base.
- `k2`: rigidez de la suspension entre `m1` y `m2`.
- `c`: amortiguamiento viscoso de la suspension entre `m1` y `m2`.
- `y(t)`: excitacion de base (perfil del camino), tipicamente senoidal.

La entrada del sistema es el movimiento de base `y(t) = A sin(omega t)` y las salidas de interes son los desplazamientos `x1(t)` y `x2(t)`.

## Esquema del sistema

Representacion conceptual:

```text
       x2(t)
        ^
       [m2]
        |
      [ c ]
      [k2 ]
        |
       [m1]  -> x1(t)
        |
      [k1]
        |
      y(t) = A sin(omega t)
```

## Ecuaciones diferenciales del movimiento

Aplicando la segunda ley de Newton en cada masa:

### Para m1

\[
m_1 \ddot{x}\_1 + c(\dot{x}\_1 - \dot{x}\_2) + k_2(x_1 - x_2) + k_1(x_1 - y) = 0
\]

### Para m2

\[
m_2 \ddot{x}\_2 + c(\dot{x}\_2 - \dot{x}\_1) + k_2(x_2 - x_1) = 0
\]

## Condiciones iniciales

En general, para simular desde reposo:

\[
x_1(0)=0,\quad \dot{x}\_1(0)=0,\quad x_2(0)=0,\quad \dot{x}\_2(0)=0
\]

## Forma matricial

Definiendo:

\[
\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \end{bmatrix},
\quad
\dot{\mathbf{x}} = \begin{bmatrix} \dot{x}\_1 \\ \dot{x}\_2 \end{bmatrix},
\quad
\ddot{\mathbf{x}} = \begin{bmatrix} \ddot{x}\_1 \\ \ddot{x}\_2 \end{bmatrix}
\]

El sistema puede escribirse como:

\[
\mathbf{M}\ddot{\mathbf{x}} + \mathbf{C}\dot{\mathbf{x}} + \mathbf{K}\mathbf{x} = \mathbf{f}(t)
\]

donde:

\[
\mathbf{M} = \begin{bmatrix}
m_1 & 0 \\
0 & m_2
\end{bmatrix},
\quad
\mathbf{C} = \begin{bmatrix}
c & -c \\
-c & c
\end{bmatrix},
\quad
\mathbf{K} = \begin{bmatrix}
k_1 + k_2 & -k_2 \\
-k_2 & k_2
\end{bmatrix}
\]

\[
\mathbf{f}(t) = \begin{bmatrix}
k_1 y(t) \\
0
\end{bmatrix}
\]

## Objetivos del taller

1. Plantear correctamente el modelo dinamico en tiempo continuo.
2. Obtener y validar las ecuaciones diferenciales acopladas.
3. Simular la respuesta temporal para una entrada senoidal de base.
4. Analizar el efecto de `m1`, `m2`, `k1`, `k2` y `c` en el comportamiento del sistema.
5. Evaluar metricas de desempeno como amplitud, resonancia y confort (respuesta en `x2`).

## Sugerencia de flujo de trabajo

1. Definir parametros fisicos y condiciones iniciales.
2. Implementar el sistema en forma de estado o en forma matricial.
3. Simular en MATLAB/Simulink o Python.
4. Graficar `y(t)`, `x1(t)`, `x2(t)` y, si aplica, aceleraciones.
5. Discutir resultados y conclusiones tecnicas.

## Entregables recomendados

- Desarrollo teorico del modelo.
- Simulacion y graficas principales.
- Analisis de sensibilidad de parametros.
- Conclusiones sobre el comportamiento dinamico del sistema.

## Nota

Si en el taller se usan valores numericos especificos de `m1`, `m2`, `k1`, `k2`, `c`, `A` y `omega`, agregalos en una tabla para facilitar la reproduccion de resultados.
