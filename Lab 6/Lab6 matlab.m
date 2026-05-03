% Lab6: Script de ejemplo para graficar una respuesta y definir una función local
% Autor: Generado por asistente

% Datos de ejemplo para la gráfica
t = linspace(0,10,1000);
y = 1.0*(1 - exp(-0.8*t).*(cos(2.0*t) + 0.4*sin(2.0*t))); % respuesta ejemplo

figure;
plot(t,y,'b','LineWidth',1.5); hold on;

% Límite de sobreimpulso (ejemplo)
overshoot_limit = 1.1; % valor de ejemplo
plot([t(1) t(end)],[overshoot_limit overshoot_limit],'r--','LineWidth',1.2);

% Tiempo de asentamiento (ejemplo)
settling_time = 5; % tiempo de asentamiento de ejemplo (s)
plot([settling_time settling_time],[min(y) max(y)],'g--','LineWidth',1.2);

xlabel('Tiempo (s)');
ylabel('Amplitud');
legend('Respuesta Simulada', 'Límite de Sobreimpulso', 'Tiempo de Asentamiento', 'Location', 'best');
grid on;
hold off;

% ==========================================
% FUNCIÓN LOCAL PARA EL SOLVER (Debe ir al final del archivo)
% ==========================================
function F = sistema_ecuaciones(vars, K, tau, sd)
    Kp_test = vars(1);
    Ti_test = vars(2);
    Td_test = vars(3);

    % Evaluamos G y Gpid en s = sd
    G_sd = K / (tau * sd + 1);
    Gpid_sd = Kp_test * (1 + 1/(Ti_test * sd) + Td_test * sd);

    % Lazo abierto evaluado en sd
    L_sd = Gpid_sd * G_sd;

    % Condición principal: L(sd) = -1 (que equivale a módulo 1 y fase -180)
    % Por lo tanto, L(sd) + 1 = 0
    error_ecuacion = L_sd + 1;

    % Separamos parte real e imaginaria para que fsolve resuelva 2 ecuaciones
    eq1 = real(error_ecuacion);
    eq2 = imag(error_ecuacion);

    % Necesitamos una tercera ecuación (restricción) porque tenemos 3 variables.
    % Usamos la relación heurística clásica de que Td es un cuarto de Ti.
    eq3 = Td_test - (Ti_test / 4.0);

    F = [eq1; eq2; eq3];
end