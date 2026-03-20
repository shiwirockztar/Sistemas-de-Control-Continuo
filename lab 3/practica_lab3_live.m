% Practica Lab 3 - Simulacion de Sistemas de Control (MATLAB + Simulink)
 Curso: Sistemas de Control Continuo
 Objetivo:
- Preparar variables en MATLAB
 - Ejecutar un modelo de Simulink desde MATLAB
 - Exportar y analizar resultados
%
 Alcance de la practica:
 Esta practica NO busca cubrir toda la metodologia de Simulink para cualquier
 tipo de sistema. Se enfoca en introducir al estudiante en procedimientos
 comunes de modelado y simulacion para que, con apoyo del profesor y la ayuda
 oficial de MATLAB/Simulink, gane autonomia para resolver dificultades.
%
 Ayuda recomendada:
 - En la Ventana de Comandos de MATLAB: helpdesk
 - Para abrir Simulink desde comandos: simulink
 - Tambien puede abrirse desde el icono grafico de Simulink en MATLAB.
%
 Nota tecnica:
 Al guardar un modelo, se crea un archivo .slx con la estructura grafica del
 diagrama y la configuracion de sus bloques.
%
 Extension avanzada:
 Simulink puede ampliarse con Funciones S (S-Functions), que permiten crear
 bloques propios en lenguajes como MATLAB, C/C++, Fortran o Ada.

clc;
clear;
close all;

% 0) Procedimiento de arranque sugerido (segun guia)
 1. Escriba en MATLAB: simulink
 2. En la ventana de Simulink, abra: New > Blank Model
 3. Revise Library Browser y recorra rapidamente las bibliotecas principales.
 4. Identifique sublibrerias claves para esta practica:
    - Simulink: Commonly Used Blocks, Continuous, Sinks, Sources
    - Control System Toolbox
    - Simulink Extras (si esta disponible en su version)
 5. Parametrice bloques con doble click y use ayuda contextual (click derecho).

% 0.1) Procedimiento 4.2 - Construccion del modelo ejemplo1
 Objetivo del montaje:
 - Construir un Sistema de Control Retroalimentado (SCR)
 - Proceso: doble integrador (usar 2 bloques Integrator en cascada)
 - Controlador: subsistema compensador de adelanto (PD real)
%
 Pasos sugeridos:
 1. Desde Library Browser, cree/abra un modelo en blanco.
 2. Monte el diagrama de la guia (figura 1) en la ventana Untitled.
 3. Busque y agregue un "Floating Scope" escribiendo:
       floating scope
    en la barra de busqueda de Library Browser.
 4. Guarde el proyecto con el nombre:
       ejemplo1
%
 Dos formas de simulacion que exige la practica:
 A) Simulacion directa desde Simulink (secciones 4.3 a 4.5)
    - No requiere puertos Inport ni Outport en el diagrama.
    - Puede usar un bloque de entrada tipo Step para excitar el sistema.
%
 B) Simulacion desde la Ventana de Comandos de MATLAB, VCML
    (secciones 4.6 a 4.10)
    - Requiere puertos Inport y Outport para intercambiar datos con MATLAB.
    - No es necesario el bloque de senal Step dentro del modelo.

% 0.2) Procedimiento 4.3 - Scope, Logging y visualizacion de senales
 1. Abra el Floating Scope con doble click y recorra sus iconos de menu
    para reconocer su funcion.
 2. En la ventana del Scope, vaya a:
       View >> Configuration Properties
    y revise las pestanas de configuracion.
 3. En la pestana Logging, active el envio de datos al workspace de MATLAB.
    Formatos usuales de guardado:
    - Structure with time
    - Structure
    - Array
%
 Recomendacion de esta practica:
 Por ahora use Scope normal (no flotante) y agregue un bloque Mux con 3
 entradas para visualizar simultaneamente:
 - senal de entrada
 - senal de salida
 - accion de control
%
 Conexion sugerida:
 [entrada] ----\
 [salida ] ----- > Mux (3) --> Scope
 [control] ----/
%
 Ayuda adicional en MATLAB:
   doc scope
 y, en general, el comando doc para consultar bloques e iconos de Simulink.

% 0.3) Estudio de bloques In1, Out1 y To Workspace
 Actividad sugerida (preinforme):
 1. Abra la libreria de Simulink.
 2. Haga doble click en In1 (Inport), Out1 (Outport) y To Workspace.
 3. Revise parametros, formatos y opciones de cada bloque.
%
 Funcionalidad principal de cada bloque:
 - In1 (Inport): recibe una senal de entrada hacia un modelo o subsistema.
 - Out1 (Outport): entrega una senal de salida desde un modelo o subsistema.
 - To Workspace: exporta senales al workspace de MATLAB para analisis.
%
 Diferencia clave entre Out y To Workspace:
 - Out (Outport) define interfaz de salida del diagrama para interconexion
   entre bloques, jerarquia de subsistemas o comunicacion con sim(...).
 - To Workspace no define interfaz del modelo; solo registra/guarda datos
   de simulacion en el workspace (array, structure, structure with time).
%
 Conclusiones practicas:
 - Use Outport cuando la senal debe salir del subsistema/modelo como puerto.
 - Use To Workspace cuando necesita postprocesar, graficar o comparar datos
   en MATLAB despues de simular.
 - Ambas opciones pueden coexistir en un mismo modelo para fines distintos.

% 0.4) Procedimiento 4.5 - Parametrizacion y corrida del modelo
 Antes de correr el modelo en Simulink, configure:
 Modeling > Model Settings > Model Settings
%
 Opciones clave a revisar:
 1) Solver
    - Tipo de paso: variable o fijo.
    - Metodo de solucion (solver numerico).
    - Tiempo de simulacion (Start time / Stop time).
%
 2) Data Import/Export
    - Entrada desde workspace (si usa In1).
    - Salida al workspace (si usa Out1 o registro global de simulacion).
    - Seleccione guardar: time, states y output.
    - Formato recomendado para esta practica: Array.
    - Puede dejar nombres por defecto de variables.
%
 3) Diagnostics
    - Defina alarmas/parada ante errores o inconsistencias de simulacion.

% 0.5) Verificacion previa del ETML (workspace)
 Objetivo: evitar mezclar resultados anteriores con la corrida actual.
%
 En la VCML, use:
   whos
 Si hay variables no deseadas, borrelas de forma selectiva.
 Evite clear all porque elimina estado util de trabajo.

 Ejemplo de limpieza selectiva (opcional):
 clearvars variable1 variable2

% 0.6) Resultados esperados y analisis posterior
 Luego de correr el modelo en SL:
 1. Active Scope y observe las senales.
 2. Haga un esquema de las senales (entrada, salida, control).
 3. Revise en workspace las variables generadas (whos).
 4. Verifique si existe alguna variable no esperada y documentela.
%
 Asociacion tipica de variables:
 - time   -> vector de tiempo de simulacion
 - states -> estados internos del modelo
 - output -> salidas del modelo

% 0.7) Como graficar cuando las variables estan en formato array
 Si una variable esta en formato matriz con tiempo en la primera columna:
   dato(:,1)  -> tiempo
   dato(:,2)  -> primera senal
   dato(:,3)  -> segunda senal, etc.
%
 Ejemplo generico (descomente y ajuste nombres segun su modelo):
%
 if exist('output','var') == 1
     t_out = output(:,1);
     y_out = output(:,2);
%
     figure('Name','Salida desde variable output');
     plot(t_out, y_out, 'LineWidth', 1.5);
     grid on;
     xlabel('Tiempo [s]');
     ylabel('Salida');
     title('Respuesta del sistema extraida desde output');
 else
     warning('No existe la variable output en el workspace.');
 end

% 1) Parametros del sistema
 Ajusta estos valores segun tu practica
t_sim = 20;               Tiempo total de simulacion [s]
Ts = 0.01;                Tiempo de muestreo para vectores en MATLAB
K = 1.0;                  Ganancia de ejemplo
tau = 2.0;                Constante de tiempo de ejemplo

 Vector de tiempo y entrada de ejemplo (escalon)
t = (0:Ts:t_sim).';
u = ones(size(t));

% 2) Modelo lineal en MATLAB (referencia para comparar)
 G(s) = K / (tau*s + 1)
num = K;
den = [tau 1];
G = tf(num, den);

 Simulacion con lsim
y_lsim = lsim(G, u, t);

figure('Name','Respuesta con lsim');
plot(t, y_lsim, 'LineWidth', 1.5);
grid on;
xlabel('Tiempo [s]');
ylabel('Salida');
title('Respuesta de G(s) usando lsim');

% 3) Simulacion de Simulink desde MATLAB
 Cambia este nombre por el .slx de tu practica
modelo_slx = 'ejemplo1';

 Opciones de simulacion (simset / simget)
opts = simset('SrcWorkspace', 'current');
opts_actuales = simget(opts); %#ok<NASGU>

 Nota:
 Si el modelo no existe aun, comenta este bloque temporalmente.
if exist([modelo_slx '.slx'], 'file') == 2
     Ejecuta el modelo con variables en el workspace actual
    out = sim(modelo_slx, 'StopTime', num2str(t_sim), opts);

     Si usas bloque "To Workspace", podras analizar aqui la senal exportada.
     Ejemplo esperado (ajusta el nombre):
     y_sl = y_out.signals.values;
     t_sl = y_out.time;

    disp('Simulacion en Simulink ejecutada correctamente.');
else
    warning('No se encontro %s.slx. Crea o ajusta el nombre del modelo.', modelo_slx);
end

% 4) Punto de equilibrio y linealizacion (referencia)
 trim y linmod requieren un modelo de Simulink adecuado y configurado.
 Descomenta y ajusta cuando tu modelo este listo.
%
 x0 = []; u0 = []; y0 = []; dx0 = [];
 [x_trim, u_trim, y_trim, dx_trim] = trim(modelo_slx, x0, u0, y0, dx0);
 [A, B, C, D] = linmod(modelo_slx, x_trim, u_trim);
%
 disp('Matrices del modelo linealizado:');
 A, B, C, D

% 5) Notas de practica
 - Define claramente que entra por Inport y que sale por Outport.
 - Usa To Workspace para exportar variables y compararlas con lsim.
 - Documenta cada prueba: parametros, cambios, resultado y conclusion.
 - Responde en el informe: que sublibrerias usaste y por que.
