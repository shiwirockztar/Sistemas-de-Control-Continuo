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

🏍️ 1. Diagrama del sistema

Tu sistema equivale a esto:

     ↑ x2(t)
     m2
     │
   [c] [k2]
     │
     m1   ↑ x1(t)
     │
    [k1]
     │
     y(t) = A sen(ωt)
La base (suelo) vibra con 
𝑦
(
𝑡
)
y(t)
𝑚
1
m
1
	​

: rueda
𝑚
2
m
2
	​

: chasis
📌 2. Ecuaciones diferenciales
Para 
𝑚
1
m
1
	​

𝑚
1
𝑥
¨
1
+
𝑐
(
𝑥
˙
1
−
𝑥
˙
2
)
+
𝑘
2
(
𝑥
1
−
𝑥
2
)
+
𝑘
1
(
𝑥
1
−
𝑦
)
=
0
m
1
	​

x
¨
1
	​

+c(
x
˙
1
	​

−
x
˙
2
	​

)+k
2
	​

(x
1
	​

−x
2
	​

)+k
1
	​

(x
1
	​

−y)=0
Para 
𝑚
2
m
2
	​

𝑚
2
𝑥
¨
2
+
𝑐
(
𝑥
˙
2
−
𝑥
˙
1
)
+
𝑘
2
(
𝑥
2
−
𝑥
1
)
=
0
m
2
	​

x
¨
2
	​

+c(
x
˙
2
	​

−
x
˙
1
	​

)+k
2
	​

(x
2
	​

−x
1
	​

)=0
🧾 3. Condiciones iniciales

Asumimos reposo:

𝑥
1
(
0
)
=
0
,
𝑥
˙
1
(
0
)
=
0
x
1
	​

(0)=0,
x
˙
1
	​

(0)=0
𝑥
2
(
0
)
=
0
,
𝑥
˙
2
(
0
)
=
0
x
2
	​

(0)=0,
x
˙
2
	​

(0)=0
📦 4. Forma matricial
𝑀
𝑥
¨
+
𝐶
𝑥
˙
+
𝐾
𝑥
=
𝐹
M
x
¨
+C
x
˙
+Kx=F
Matrices:
𝑀
=
[
𝑚
1
	
0


0
	
𝑚
2
]
M=[
m
1
	​

0
	​

0
m
2
	​

	​

]
𝐶
=
[
𝑐
	
−
𝑐


−
𝑐
	
𝑐
]
C=[
c
−c
	​

−c
c
	​

]
𝐾
=
[
𝑘
1
+
𝑘
2
	
−
𝑘
2


−
𝑘
2
	
𝑘
2
]
K=[
k
1
	​

+k
2
	​

−k
2
	​

	​

−k
2
	​

k
2
	​

	​

]
𝐹
=
[
𝑘
1
𝑦
(
𝑡
)


0
]
F=[
k
1
	​

y(t)
0
	​

]
🔄 5. Espacio de estados

Definimos estados:

𝑥
=
[
𝑥
1


𝑥
2


𝑥
˙
1


𝑥
˙
2
]
x=
	​

x
1
	​

x
2
	​

x
˙
1
	​

x
˙
2
	​

	​

	​

Sistema:
𝑥
˙
=
[
𝑥
˙
1


𝑥
˙
2


𝑥
¨
1


𝑥
¨
2
]
x
˙
=
	​

x
˙
1
	​

x
˙
2
	​

x
¨
1
	​

x
¨
2
	​

	​

	​

Forma final:
𝑥
˙
=
[
0
	
0
	
1
	
0


0
	
0
	
0
	
1


−
𝑘
1
+
𝑘
2
𝑚
1
	
𝑘
2
𝑚
1
	
−
𝑐
𝑚
1
	
𝑐
𝑚
1


𝑘
2
𝑚
2
	
−
𝑘
2
𝑚
2
	
𝑐
𝑚
2
	
−
𝑐
𝑚
2
]
⏟
𝐴
𝑥
+
[
0


0


𝑘
1
𝑚
1


0
]
⏟
𝐵
𝑦
(
𝑡
)
x
˙
=
A
	​

0
0
−
m
1
	​

k
1
	​

+k
2
	​

	​

m
2
	​

k
2
	​

	​

	​

0
0
m
1
	​

k
2
	​

	​

−
m
2
	​

k
2
	​

	​

	​

1
0
−
m
1
	​

c
	​

m
2
	​

c
	​

	​

0
1
m
1
	​

c
	​

−
m
2
	​

c
	​

	​

	​

	​

	​

x+
B
	​

0
0
m
1
	​

k
1
	​

	​

0
	​

	​

	​

	​

y(t)
🔁 6. Función de transferencia

Entrada: 
𝑦
(
𝑡
)
y(t)
Salida típica: 
𝑥
2
(
𝑡
)
x
2
	​

(t) (movimiento del chasis)

Resultado general:
𝑋
2
(
𝑠
)
𝑌
(
𝑠
)
=
𝑘
1
𝑘
2
(
𝑚
1
𝑠
2
+
𝑐
𝑠
+
𝑘
1
+
𝑘
2
)
(
𝑚
2
𝑠
2
+
𝑐
𝑠
+
𝑘
2
)
−
(
𝑐
𝑠
+
𝑘
2
)
2
Y(s)
X
2
	​

(s)
	​

=
(m
1
	​

s
2
+cs+k
1
	​

+k
2
	​

)(m
2
	​

s
2
+cs+k
2
	​

)−(cs+k
2
	​

)
2
k
1
	​

k
2
	​

	​


👉 Es un sistema de 4º orden

💻 7. Simulación en MATLAB
m1 = 10;
m2 = 50;
k1 = 1000;
k2 = 1500;
c = 100;

A = [0 0 1 0;
     0 0 0 1;
     -(k1+k2)/m1 k2/m1 -c/m1 c/m1;
     k2/m2 -k2/m2 c/m2 -c/m2];

B = [0; 0; k1/m1; 0];
C = [0 1 0 0]; % salida x2
D = 0;

sys = ss(A,B,C,D);

t = 0:0.01:10;
y = sin(2*t);

lsim(sys,y,t)
🐍 8. Simulación en Python
import numpy as np
from scipy.signal import StateSpace, lsim
import matplotlib.pyplot as plt

m1, m2 = 10, 50
k1, k2 = 1000, 1500
c = 100

A = [[0,0,1,0],
     [0,0,0,1],
     [-(k1+k2)/m1, k2/m1, -c/m1, c/m1],
     [k2/m2, -k2/m2, c/m2, -c/m2]]

B = [[0],[0],[k1/m1],[0]]
C = [[0,1,0,0]]
D = [[0]]

sys = StateSpace(A,B,C,D)

t = np.linspace(0,10,1000)
y = np.sin(2*t)

t, response, _ = lsim(sys, y, t)

plt.plot(t, response)
plt.xlabel("Tiempo")
plt.ylabel("x2(t)")
plt.show()
🧠 9. Interpretación final
Si 
𝑐
↑
c↑ → menos vibración (más confort)
Si 
𝑘
2
↑
k
2
	​

↑ → más rígido (menos cómodo)
Si 
𝑚
2
↑
m
2
	​

↑ → más estable pero responde más lento
🚀 Si quieres subir de nivel

Puedo ayudarte a:

🔍 Sacar frecuencias naturales
📉 Analizar resonancia
🎯 Optimizar la suspensión (tipo ingeniería real)
🧪 Pasarlo a Simulink

Solo dime 👍

pasalo a simulink

Perfecto, vamos a llevar este modelo a Simulink paso a paso, como lo harías en una práctica o examen.

🧩 1. Idea general en Simulink

Vas a implementar las ecuaciones:

𝑥
¨
1
=
−
𝑘
1
(
𝑥
1
−
𝑦
)
−
𝑘
2
(
𝑥
1
−
𝑥
2
)
−
𝑐
(
𝑥
˙
1
−
𝑥
˙
2
)
𝑚
1
x
¨
1
	​

=
m
1
	​

−k
1
	​

(x
1
	​

−y)−k
2
	​

(x
1
	​

−x
2
	​

)−c(
x
˙
1
	​

−
x
˙
2
	​

)
	​

𝑥
¨
2
=
−
𝑘
2
(
𝑥
2
−
𝑥
1
)
−
𝑐
(
𝑥
˙
2
−
𝑥
˙
1
)
𝑚
2
x
¨
2
	​

=
m
2
	​

−k
2
	​

(x
2
	​

−x
1
	​

)−c(
x
˙
2
	​

−
x
˙
1
	​

)
	​


👉 En Simulink:

Aceleración → Integrador → Velocidad → Integrador → Posición
🔧 2. Bloques que necesitas

En Simulink, usa:

2 bloques Integrator (para 
𝑥
1
x
1
	​

)
2 bloques Integrator (para 
𝑥
2
x
2
	​

)
Bloques Sum
Bloques Gain
1 bloque Sine Wave (entrada 
𝑦
(
𝑡
)
y(t))
1 bloque Scope
🏗️ 3. Construcción paso a paso
🔹 Parte de 
𝑚
1
m
1
	​

Ecuación:
𝑥
¨
1
=
−
𝑘
1
(
𝑥
1
−
𝑦
)
−
𝑘
2
(
𝑥
1
−
𝑥
2
)
−
𝑐
(
𝑥
˙
1
−
𝑥
˙
2
)
𝑚
1
x
¨
1
	​

=
m
1
	​

−k
1
	​

(x
1
	​

−y)−k
2
	​

(x
1
	​

−x
2
	​

)−c(
x
˙
1
	​

−
x
˙
2
	​

)
	​

En Simulink:
Restas:
𝑥
1
−
𝑦
x
1
	​

−y
𝑥
1
−
𝑥
2
x
1
	​

−x
2
	​

𝑥
˙
1
−
𝑥
˙
2
x
˙
1
	​

−
x
˙
2
	​

Multiplicas:
por 
𝑘
1
k
1
	​

, 
𝑘
2
k
2
	​

, 
𝑐
c
Sumas todo con signo negativo
Multiplicas por 
1
/
𝑚
1
1/m
1
	​

Resultado → Integrador → 
𝑥
˙
1
x
˙
1
	​

Otro integrador → 
𝑥
1
x
1
	​

🔹 Parte de 
𝑚
2
m
2
	​

Ecuación:
𝑥
¨
2
=
−
𝑘
2
(
𝑥
2
−
𝑥
1
)
−
𝑐
(
𝑥
˙
2
−
𝑥
˙
1
)
𝑚
2
x
¨
2
	​

=
m
2
	​

−k
2
	​

(x
2
	​

−x
1
	​

)−c(
x
˙
2
	​

−
x
˙
1
	​

)
	​

En Simulink:
Restas:
𝑥
2
−
𝑥
1
x
2
	​

−x
1
	​

𝑥
˙
2
−
𝑥
˙
1
x
˙
2
	​

−
x
˙
1
	​

Multiplicas por 
𝑘
2
k
2
	​

 y 
𝑐
c
Sumas (con signo negativo)
Multiplicas por 
1
/
𝑚
2
1/m
2
	​

Integrador → velocidad
Integrador → posición
🔌 4. Entrada sinusoidal

Usa bloque:

👉 Sine Wave

Configura:

Amplitud: 
𝐴
A
Frecuencia: 
𝜔
ω

Esto es 
𝑦
(
𝑡
)
y(t)

👀 5. Salida

Conecta al Scope:

𝑥
1
(
𝑡
)
x
1
	​

(t)
𝑥
2
(
𝑡
)
x
2
	​

(t)

👉 Así ves vibración de rueda vs chasis

🧱 6. Forma alternativa (MUCHO más fácil)

También puedes hacerlo con State-Space block:

Matrices:
A = [0 0 1 0;
     0 0 0 1;
     -(k1+k2)/m1 k2/m1 -c/m1 c/m1;
     k2/m2 -k2/m2 c/m2 -c/m2];

B = [0; 0; k1/m1; 0];

C = [0 1 0 0];

D = 0;
En Simulink:
Agrega bloque State-Space
Pegas matrices A, B, C, D
Entrada: Sine Wave
Salida: Scope

👉 listo en 30 segundos 😄

⚙️ 7. Valores de ejemplo
m1 = 10
m2 = 50
k1 = 1000
k2 = 1500
c = 100
🧠 8. Qué deberías observar
𝑥
1
x
1
	​

: vibra mucho (rueda)
𝑥
2
x
2
	​

: más suave (suspensión funciona)
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
