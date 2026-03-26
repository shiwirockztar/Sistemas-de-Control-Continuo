# Taller 1 - Sistema masa-resorte-amortiguador de 2 GDL con excitacion de base

## Descripcion

Este taller modela la dinamica vertical de un sistema mecanico de **dos grados de libertad (2 GDL)**, representativo de una suspension simplificada:

- `m1`: masa no suspendida (rueda/eje).
- `m2`: masa suspendida (chasis).
- `k1`: rigidez del neumatico respecto a la base.
- `k2`: rigidez de la suspension entre `m1` y `m2`.
- `c`: amortiguamiento viscoso de la suspension entre `m1` y `m2`.
- `U(x)`: perfil irregular del camino en funcion del espacio.
- `y(t)`: entrada de base en el tiempo, definida como `y(t)=U(x(t))`.

La entrada del sistema es el movimiento de base `y(t) = U(x(t))` y las salidas de interes son los desplazamientos `X(t)` y `Y(t)`.

## Esquema del sistema

Representacion conceptual:

```text
       Y(t)
        ^
       [m2]
        |
      [ c ]
      [k2 ]
        |
       [m1]  -> X(t)
        |
      [k1]
        |
      y(t) = U(x(t))
```

## Ecuaciones diferenciales del movimiento

Aplicando la segunda ley de Newton en cada masa:

### Para m1

\[
m_1 \ddot{X} + c(\dot{X} - \dot{Y}) + k_2(X - Y) + k_1(X - U(x(t))) = 0
\]

### Para m2

\[
m_2 \ddot{Y} + c(\dot{Y} - \dot{X}) + k_2(Y - X) = 0
\]

## Condiciones iniciales

En general, para simular desde reposo:

\[
X(0)=0,\quad \dot{X}(0)=0,\quad Y(0)=0,\quad \dot{Y}(0)=0
\]

## Forma matricial

Definiendo:

\[
\mathbf{X} = \begin{bmatrix} X \\ Y \end{bmatrix}, \quad
\dot{\mathbf{X}} = \begin{bmatrix} \dot{X} \\ \dot{Y} \end{bmatrix}, \quad
\ddot{\mathbf{X}} = \begin{bmatrix} \ddot{X} \\ \ddot{Y} \end{bmatrix}
\]

El sistema puede escribirse como:

\[
\mathbf{M}\ddot{\mathbf{X}} + \mathbf{C}\dot{\mathbf{X}} + \mathbf{K}\mathbf{X} = \mathbf{f}(t)
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
k_1 U(x(t)) \\
0
\end{bmatrix}
\]

## Objetivos del taller

1. Plantear correctamente el modelo dinamico en tiempo continuo.
2. Obtener y validar las ecuaciones diferenciales acopladas.
3. Simular la respuesta temporal para una entrada senoidal de base.
4. Analizar el efecto de `m1`, `m2`, `k1`, `k2` y `c` en el comportamiento del sistema.
5. Evaluar metricas de desempeno como amplitud, resonancia y confort (respuesta en `Y`).

## Sugerencia de flujo de trabajo

1. Definir parametros fisicos y condiciones iniciales.
2. Implementar el sistema en forma de estado o en forma matricial.
3. Simular en MATLAB/Simulink o Python.
4. Graficar `y(t)`, `X(t)`, `Y(t)` y, si aplica, aceleraciones.
5. Discutir resultados y conclusiones tecnicas.

## Entregables recomendados

- Desarrollo teorico del modelo.
- Simulacion y graficas principales.
- Analisis de sensibilidad de parametros.
- Conclusiones sobre el comportamiento dinamico del sistema.

## Nota

Si en el taller se usan valores numericos especificos de `m1`, `m2`, `k1`, `k2`, `c`, `A` y `omega`, agregalos en una tabla para facilitar la reproduccion de resultados.

## Interpretacion de graficas

La simulacion entrega dos bloques de resultados principales:

1. **Perfil del camino `u(x)` vs espacio `x`**  
   Esta grafica representa la irregularidad de la via que excita el sistema.  
  Es una entrada espacial, no temporal; por eso se convierte a `y(t)` usando la relacion `x(t)=v t` y `y(t)=U(x(t))`.

2. **Respuesta temporal `y(t)`, `X(t)` y `Y(t)`**

- `y(t)`: entrada de base (camino visto en el tiempo).
- `X(t)`: desplazamiento de la masa no suspendida (rueda/eje).
- `Y(t)`: desplazamiento de la masa suspendida (chasis).

En general, `X(t)` presenta variaciones mas rapidas y de mayor contenido en alta frecuencia, mientras que `Y(t)` es mas suave por efecto del amortiguamiento y la suspension.  
Si la amplitud de `Y(t)` es menor que la de `X(t)`, el sistema esta cumpliendo su funcion de aislamiento de vibraciones.

3. **Error de validacion (FT vs ODE)**  
  Se grafica `X_FT - X_ODE` y `Y_FT - Y_ODE`.  
   Valores cercanos a cero indican consistencia entre el enfoque por funcion de transferencia y el modelo en ecuaciones diferenciales, validando la implementacion numerica.

### Mensaje tecnico clave del taller

El modelo por funcion de transferencia permite describir la dinamica del sistema 2 GDL ante excitacion de base, y los resultados muestran como la suspension atenua la vibracion transmitida al chasis (`Y`) respecto a la masa no suspendida (`X`).
