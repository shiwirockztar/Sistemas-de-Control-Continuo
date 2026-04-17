# Laboratorio 5 - Lugar de las Raices

Este documento resume la actividad del laboratorio y deja la solucion teorica esperada a partir del enunciado del PDF incluido en esta carpeta.

## Objetivo del laboratorio

El laboratorio busca:

1. Usar Matlab para analizar sistemas de control realimentados.
2. Introducir el lugar de las raices como herramienta para estudiar la ubicacion de los polos de lazo cerrado.
3. Ver el efecto de agregar polos y ceros a la funcion de transferencia de lazo abierto sobre el LGR y la respuesta transitoria.

## Idea central

Para un sistema con realimentacion unitaria,

$$T(s)=\frac{G(s)}{1+G(s)H(s)}, \quad H(s)=1$$

los polos de lazo cerrado son las raices de la ecuacion caracteristica:

$$1+G(s)H(s)=0$$

El lugar de las raices muestra como se mueven esos polos cuando varia la ganancia del sistema.

## Sistemas pedidos en la actividad inicial

La guia propone tres sistemas a partir de un sistema base:

$$G_1(s)H_1(s)=\frac{k}{s(s+2)}$$

$$G_2(s)H_2(s)=\frac{k}{s(s+2)(\frac{s}{5}+1)}=\frac{5k}{s(s+2)(s+5)}$$

$$G_3(s)H_3(s)=\frac{k(\frac{s}{3}+1)}{s(s+2)(\frac{s}{5}+1)}=\frac{5k(s+3)}{3s(s+2)(s+5)}$$

En todos los casos se trabaja con retroalimentacion unitaria.

## Solucion teorica de la parte 4.1

### 4.1.1 Graficas separadas del LGR

Las graficas se obtienen en Matlab con `rlocus`, `rltool` o `rlocfind`.

Un ejemplo minimo en Matlab es:

```matlab
s = tf('s');
G1 = 1/(s*(s+2));
G2 = 1/(s*(s+2)*(s/5+1));
G3 = (s/3+1)/(s*(s+2)*(s/5+1));

figure; rlocus(G1); grid on;
figure; rlocus(G2); grid on;
figure; rlocus(G3); grid on;
```

### 4.1.2 Numero de ramas

- G1(s)H1(s): 2 ramas.
- G2(s)H2(s): 3 ramas.
- G3(s)H3(s): 3 ramas.

### 4.1.3 Efecto de agregar polo y cero

- Al agregar el polo en -5, el LGR gana una rama adicional y la dinamica tiende a hacerse mas lenta. La respuesta transitoria suele perder rapidez y puede volverse menos amortiguada.
- Al agregar el cero en -3, el LGR se desplaza hacia la izquierda en varias zonas y la respuesta suele mejorar en rapidez. Un cero en el semiplano izquierdo atrae las ramas y puede reducir el tiempo de establecimiento, aunque tambien puede aumentar el sobreimpulso si queda cerca de los polos dominantes.

### 4.1.4 Cual sistema podria tener polos inestables

El sistema mas sensible a inestabilidad es G2(s)H2(s).

Para retroalimentacion unitaria, su ecuacion caracteristica es:

$$s^3+7s^2+10s+k=0$$

El criterio de Routh muestra estabilidad para:

$$0<k<70$$

Por encima de ese valor, aparece inestabilidad.

En cambio:

$$G_1(s)H_1(s)\Rightarrow s^2+2s+k=0$$

es estable para k>0, y

$$G_3(s)H_3(s)\Rightarrow s^3+7s^2+(10+k)s+3k=0$$

permanece estable para k>0.

### 4.1.5 Si el sistema fuera inestable, que conviene agregar

En general es preferible agregar un cero bien ubicado en el semiplano izquierdo antes que agregar un polo, porque el cero puede mejorar la rapidez y empujar las ramas del LGR hacia la izquierda. Un polo adicional, por el contrario, suele empeorar el amortiguamiento y acercar el sistema a la inestabilidad.

## Solucion teorica de la parte 4.1.1 con wn y zeta

La guia tambien estudia el caso de segundo orden con wn=1 y:

$$T(s)=\frac{1}{s^2+2\zeta s+1}$$

Las raices son:

$$s=-\zeta \pm \sqrt{\zeta^2-1}$$

Interpretacion:

- Si 0 < zeta < 1, las raices son complejas conjugadas y hay oscilacion.
- Si zeta = 1, el sistema es criticamente amortiguado.
- Si zeta > 1, las raices son reales y negativas, con respuesta sobreamortiguada.

## Respuestas esperadas a los apartados de analisis

### 4.2 Agregar un cero real entre -5 y 5

- Un cero en el semiplano izquierdo suele mejorar la rapidez de la respuesta y atraer las ramas del LGR hacia la izquierda.
- Un cero muy cerca del origen puede cambiar mucho la forma del LGR y aumentar el sobreimpulso.
- Un cero en el semiplano derecho vuelve al sistema no minimo-fase, produce una respuesta inicial contraria a la entrada y deteriora el desempeno.

### 4.3 Agregar un polo real entre -5 y 0

- Un polo adicional desplaza el LGR hacia una dinamica mas lenta.
- Si el polo queda cerca del origen, el sistema pierde margen de estabilidad y aumenta el tiempo de establecimiento.
- Un polo en el semiplano izquierdo no implica automaticamente inestabilidad, pero si suele empeorar el transitorio.

### 4.4 Variar zeta entre 0 y 1.2 con wn=1

- A menor zeta, mayor sobreimpulso y mas oscilaciones.
- Al aumentar zeta, disminuye el sobreimpulso y la respuesta se vuelve mas amortiguada.
- El compromiso tipico para buen desempeno suele estar cerca de zeta = 0.6 a 0.8.
- Con zeta cercano a 1, la respuesta es mas lenta pero con poca o ninguna oscilacion.

## Codigo sugerido para reproducir la parte 4.4.1

```matlab
zeta = 0:0.1:1.2;
raices = [];

for i = 1:length(zeta)
    r = roots([1 2*zeta(i) 1]);
    raices = [raices; r.'];
end

figure;
plot(real(raices.'), imag(raices.'), 'o');
grid on;
xlabel('Parte real');
ylabel('Parte imaginaria');
title('Lugar de las raices manual para T(s)=1/(s^2+2 zeta s+1)');
```

## Codigo sugerido para la parte 4.4.2

```matlab
zeta = 0.5:0.1:1.2;
s = tf('s');

for i = 1:length(zeta)
    T = 1/(s^2 + 2*zeta(i)*s + 1);
    figure;
    step(T);
    grid on;
    title(['Respuesta al escalon, zeta = ', num2str(zeta(i))]);
end
```

## Conclusiones resumidas

1. El lugar de las raices permite predecir la estabilidad y el desempeno del sistema sin recalcular toda la ecuacion caracteristica para cada ganancia.
2. Agregar polos tiende a empeorar el transitorio; agregar ceros en el semiplano izquierdo puede mejorarlo.
3. El sistema G2(s)H2(s) es el mas propenso a inestabilidad al aumentar la ganancia, mientras que G3(s)H3(s) introduce una mejora por el cero en -3.
4. Para el sistema de segundo orden, zeta controla directamente el nivel de amortiguamiento y el numero de oscilaciones de la respuesta transitoria.

## Nota final

Las graficas finales del LGR y de las respuestas al escalon deben generarse en Matlab y anexarse al informe o al notebook que entregue el laboratorio.