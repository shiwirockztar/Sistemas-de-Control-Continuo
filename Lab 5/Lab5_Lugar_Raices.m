%% Laboratorio 5 - Lugar de las Raices
% Curso: Sistemas de Control Continuo
%
% Este Live Script resume el contenido teorico y practico descrito en el
% README del laboratorio. Incluye los sistemas pedidos, analisis basico del
% lugar de las raices y el caso de segundo orden con wn = 1 y zeta variable.

%% Objetivos
% 1. Usar Matlab para analizar sistemas de control realimentados.
% 2. Introducir el lugar de las raices como herramienta para estudiar la
%    ubicacion de los polos de lazo cerrado.
% 3. Ver el efecto de agregar polos y ceros a la funcion de transferencia
%    de lazo abierto sobre el LGR y la respuesta transitoria.

%% Idea central
% Para un sistema con realimentacion unitaria:
%
% T(s) = G(s) / (1 + G(s)H(s)),    H(s) = 1
%
% Los polos de lazo cerrado son las raices de la ecuacion caracteristica:
%
% 1 + G(s)H(s) = 0
%
% El lugar de las raices muestra como se mueven esos polos cuando varia la
% ganancia del sistema.

%% Sistemas base de la actividad
% G1(s)H1(s) = k / (s(s+2))
% G2(s)H2(s) = k / (s(s+2)(s/5 + 1)) = 5k / (s(s+2)(s+5))
% G3(s)H3(s) = k(s/3 + 1) / (s(s+2)(s/5 + 1)) = 5k(s+3) / (3s(s+2)(s+5))

s = tf('s');

G1 = 1/(s*(s+2));
G2 = 1/(s*(s+2)*(s/5+1));
G3 = (s/3 + 1)/(s*(s+2)*(s/5+1));

%% 4.1 Graficas separadas del LGR
figure('Name','LGR G1');
rlocus(G1);
grid on;
title('Lugar de las raices para G1(s)H1(s) = k/[s(s+2)]');

figure('Name','LGR G2');
rlocus(G2);
grid on;
title('Lugar de las raices para G2(s)H2(s) = k/[s(s+2)(s/5+1)]');

figure('Name','LGR G3');
rlocus(G3);
grid on;
title('Lugar de las raices para G3(s)H3(s) = k(s/3+1)/[s(s+2)(s/5+1)]');

%% Numero de ramas
% G1(s)H1(s): 2 ramas.
% G2(s)H2(s): 3 ramas.
% G3(s)H3(s): 3 ramas.

%% Efecto de agregar polo y cero
% - El polo en -5 agrega una rama y suele hacer la dinamica mas lenta.
% - El cero en -3 atrae el LGR hacia la izquierda y suele mejorar la rapidez.

%% Analisis de estabilidad con polinomios caracteristicos
% G1: s^2 + 2s + k = 0
% G2: s^3 + 7s^2 + 10s + k = 0
% G3: s^3 + 7s^2 + (10+k)s + 3k = 0
%
% Para inspeccionar el comportamiento, se pueden evaluar polos para varios
% valores de k.

kValues = [1 10 30 50 70 90];

figure('Name','Polos de lazo cerrado para G2');
hold on;
for k = kValues
    polesG2 = roots([1 7 10 k]);
    plot(real(polesG2), imag(polesG2), 'o', 'DisplayName', ['k = ' num2str(k)]);
end
xline(0, '--k');
yline(0, '--k');
grid on;
axis equal;
title('Polos de lazo cerrado de G2(s)H2(s) para varios valores de k');
xlabel('Parte real');
ylabel('Parte imaginaria');
legend('Location','bestoutside');
hold off;

figure('Name','Polos de lazo cerrado para G3');
hold on;
for k = kValues
    polesG3 = roots([1 7 10 + k 3*k]);
    plot(real(polesG3), imag(polesG3), 'o', 'DisplayName', ['k = ' num2str(k)]);
end
xline(0, '--k');
yline(0, '--k');
grid on;
axis equal;
title('Polos de lazo cerrado de G3(s)H3(s) para varios valores de k');
xlabel('Parte real');
ylabel('Parte imaginaria');
legend('Location','bestoutside');
hold off;

%% Caso de segundo orden con wn = 1
% T(s) = 1 / (s^2 + 2*zeta*s + 1)
% Raices: s = -zeta +/- sqrt(zeta^2 - 1)

zeta = 0:0.1:1.2;
raices = [];

for i = 1:length(zeta)
    raices = [raices; roots([1 2*zeta(i) 1]).']; %#ok<AGROW>
end

figure('Name','Lugar de las raices manual para wn=1');
plot(real(raices.'), imag(raices.'), 'o', 'MarkerSize', 5);
grid on;
axis equal;
xline(0, '--k');
yline(0, '--k');
title('Raices para T(s) = 1/(s^2 + 2 zeta s + 1)');
xlabel('Parte real');
ylabel('Parte imaginaria');

%% Respuesta al escalon para varios valores de zeta
zetaStep = 0.5:0.1:1.2;

figure('Name','Respuesta al escalon para zeta variable');
for i = 1:length(zetaStep)
    T = 1/(s^2 + 2*zetaStep(i)*s + 1);
    subplot(2, 4, i);
    step(T);
    grid on;
    title(['zeta = ' num2str(zetaStep(i))]);
end
sgtitle('Respuesta al escalon para wn = 1 y zeta variable');

%% Agregar cero y polo reales como ejemplo visual
% Cero en el semiplano izquierdo: tiende a acelerar la respuesta.
% Polo adicional: tiende a hacer la respuesta mas lenta.

G_with_zero = (s + 3)/(s*(s+2)*(s/5+1));
G_with_pole = 1/(s*(s+2)*(s/5+1)*(s+1));

figure('Name','Comparacion LGR con cero y con polo');
subplot(1,2,1);
rlocus(G_with_zero);
grid on;
title('LGR con cero en -3');

subplot(1,2,2);
rlocus(G_with_pole);
grid on;
title('LGR con polo en -1');

%% Conclusiones resumidas
% 1. El lugar de las raices permite predecir estabilidad y desempeno sin
%    recalcular toda la ecuacion caracteristica para cada ganancia.
% 2. Agregar polos tiende a empeorar el transitorio; agregar ceros en el
%    semiplano izquierdo puede mejorarlo.
% 3. G2(s)H2(s) es el sistema mas sensible a inestabilidad al aumentar k.
% 4. zeta controla el amortiguamiento y el nivel de oscilacion del sistema
%    de segundo orden.
