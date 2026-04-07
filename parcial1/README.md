# Parcial - Punto 2

## Enunciado

Considere el sistema resorte-masa-polea de la figura. Si se tira de la masa m hacia abajo una distancia corta y se suelta, vibrara. Se pide obtener la frecuencia natural del sistema aplicando la ley de conservacion de la energia.

## Variables y relaciones cinematicas

Se definen las siguientes variables medidas desde el equilibrio:

- x: desplazamiento de la masa m.
- y: desplazamiento vertical de la polea.
- $\theta$: angulo de rotacion de la polea.

Relaciones geometricas del sistema:

$$
x = 2y
$$

$$
R\theta = x - y = y
$$

$$
J = \frac{1}{2}MR^2
$$

## Energia cinetica

La energia cinetica total del sistema es:

$$
T = \frac{1}{2}m\dot{x}^2 + \frac{1}{2}M\dot{y}^2 + \frac{1}{2}J\dot{\theta}^2
$$

Usando x = 2y y theta_dot = y_dot / R:

$$
T = \frac{1}{2}m\dot{x}^2 + \frac{1}{8}M\dot{x}^2 + \frac{1}{4}MR^2\left(\frac{\dot{y}}{R}\right)^2
$$

$$
T = \frac{1}{2}m\dot{x}^2 + \frac{3}{16}M\dot{x}^2
$$

## Energia potencial

En el estado de equilibrio:

$$
U_0 = \frac{1}{2}ky_\delta^2 + Mg(l-y_0) + mg(l-x_0)
$$

Cuando las masas se desplazan:

$$
U = \frac{1}{2}k(y_\delta + y)^2 + Mg(l-y_0-y) + mg(l-x_0-x)
$$

Al expandir:

$$
U = U_0 + \frac{1}{2}ky^2 + ky_\delta y - Mgy - mgx
$$

De la condicion de equilibrio estatico del resorte:

$$
ky_\delta = Mg + 2mg
$$

Multiplicando por y y usando x = 2y:

$$
ky_\delta y = Mgy + mgx
$$

Por tanto:

$$
U = U_0 + \frac{1}{2}ky^2 = U_0 + \frac{1}{8}kx^2
$$

## Conservacion de energia y ecuacion de movimiento

Aplicando conservacion de energia mecanica:

$$
T + U = \text{constante}
$$

$$
\frac{1}{2}m\dot{x}^2 + \frac{3}{16}M\dot{x}^2 + U_0 + \frac{1}{8}kx^2 = \text{constante}
$$

Derivando con respecto al tiempo:

$$
\left[\left(m + \frac{3}{8}M\right)\ddot{x} + \frac{1}{4}kx\right]\dot{x} = 0
$$

Como x_dot no es identicamente cero:

$$
\left(m + \frac{3}{8}M\right)\ddot{x} + \frac{1}{4}kx = 0
$$

Forma estandar:

$$
\ddot{x} + \frac{2k}{8m+3M}x = 0
$$

## Frecuencia natural

$$
\omega_n = \sqrt{\frac{2k}{8m+3M}}
$$

## Funcion de transferencia

La ecuacion obtenida corresponde a vibracion libre. Para definir funcion de transferencia se considera una fuerza externa de entrada $F(t)$ aplicada sobre la coordenada $x$:

$$
\left(m+\frac{3}{8}M\right)\ddot{x}+\frac{1}{4}kx = F(t)
$$

Aplicando transformada de Laplace con condiciones iniciales cero:

$$
\left[\left(m+\frac{3}{8}M\right)s^2+\frac{1}{4}k\right]X(s)=F(s)
$$

Por tanto, la funcion de transferencia desplazamiento-fuerza es:

$$
G(s)=\frac{X(s)}{F(s)}=\frac{1}{\left(m+\frac{3}{8}M\right)s^2+\frac{1}{4}k}
$$

Forma equivalente:

$$
G(s)=\frac{8}{(8m+3M)s^2+2k}
$$

Forma estandar de segundo orden:

$$
G(s)=\frac{1}{m_{eq}}\frac{1}{s^2+\omega_n^2}, \quad m_{eq}=m+\frac{3}{8}M
$$