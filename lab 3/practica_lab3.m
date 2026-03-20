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

% 0.8) Variables generadas en el ETML tras ejecutar la simulacion del ejemplo 1
 Luego de correr la simulacion desde MATLAB usando sim(...), se generan
 automaticamente las siguientes variables en el workspace (ETML):
%
 - tout
   Vector de tiempo de simulacion que contiene los instantes de tiempo
   en los que se registraron los datos.
%
 - xout e yout
   Vectores de senal correspondientes a los puertos de salida (Out1) del
   modelo. Representan los estados o variables de interes del sistema
   simulado.
%
 - simout
   Estructura o array que contiene los datos registrados por el bloque
   Scope durante la simulacion. Permite visualizar graficamente las
   senales sin necesidad de abrir el Scope en Simulink.
%
 - SimulationMetadata
   Variable que almacena toda la informacion de la corrida de simulacion,
   incluyendo parametros de configuracion, tiempos de ejecucion, metodo
   de resolucion numerica utilizado y otras caracteristicas tecnicas del
   proceso de simulacion.
%
 - ErrorMessage
   Campo que contiene mensajes de error generados durante la simulacion.
   En este caso esta vacio, ya que la simulacion se ejecuto sin problemas
   ni inconsistencias.
%
 Notas adicionales:
 - Estas variables pueden visualizarse con el comando 'whos' en MATLAB.
 - Los datos pueden ser procesados y graficados con plot() para analisis
   posterior.
 - El formato y nombres de variables pueden personalizarse en:
   Model Settings > Data Import/Export

% 0.9) Sublibrerías de Simulink, Control System Toolbox y Simulink Extras
 Las principales librerías disponibles en Simulink contienen las siguientes
 sublibrerías y bloques, accesibles desde el Library Browser:
%
 SIMULINK (libreria principal):
 - Commonly Used Blocks
   Contiene los bloques mas utilizados: Sum, Gain, Integrator, Derivative,
   Step, Constant, Mux, Demux, Scope.
%
 - Continuous
   Bloques para sistemas continuos: Integrator, Derivative, Transfer Fcn,
   State-Space, Zero-Pole, PID Controller.
%
 - Discrete
   Bloques para sistemas discretos: Discrete-Time Integrator, Transfer Fcn
   Discrete, Zero-Pole Discrete.
%
 - Sinks
   Bloques para visualizacion y registro de datos: Scope, To Workspace,
   Display, Floating Scope.
%
 - Sources
   Bloques de entrada: Step, Ramp, Sine Wave, Pulse Generator, Constant,
   Clock, From Workspace.
%
 - Math Operations
   Bloques de operaciones matematicas: Add, Multiply, Divide, Math Function.
%
 - Signal Routing
   Bloques para manejo de senales: Mux, Demux, Switch, Multi-port Switch.
%
 CONTROL SYSTEM TOOLBOX:
 - Classical Control Design
   Herramientas para control clasico: PID Controller, Transfer Function,
   State-Space, Zero-Pole placement.
%
 - Linear System Blocks
   Bloques para sistemas lineales: Transfer Fcn, State-Space, Zero-Pole.
%
 - Advanced Control
   Control avanzado: Adaptive Control, Robust Control, Optimizacion.
%
 SIMULINK EXTRAS (si esta disponible):
 - Additional Discrete
   Bloques discretos adicionales y variaciones.
%
 - Additional Sinks
   Sinks adicionales para registro y visualizacion extendida.
%
 - Additional Sources
   Fuentes de senal adicionales.
%
 Consejos practicos:
 - Para esta practica, enfoquese en: Commonly Used Blocks, Continuous,
   Sinks y Sources.
 - Explore los parametros de cada bloque con doble click para entender
   sus configuraciones.
 - Use la ayuda contextual (boton Help) dentro de cada bloque para mas
   detalles sobre funcionamiento y parametrizacion.
 - Anote los bloques que utilice para referencia en informes posteriores.

% 0.10) ¿Qué diferencia de funcionalidad existe entre Out y To Workspace?
 
 RESPUESTA SINTETICA:
 Out (Outport) y To Workspace tienen propositos distintos en Simulink,
 aunque ambos exportan datos. La diferencia radica en su funcion dentro
 de la arquitectura del modelo.
%
 DIFERENCIACION DETALLADA:
%
 OUT (Outport):
 - Define la INTERFAZ DE SALIDA del modelo o subsistema.
 - Permite que senales salgan del diagrama hacia bloques externos o hacia
   la ventana de comandos de MATLAB mediante sim(...).
 - Es obligatorio si se desea comunicacion estructurada entre:
   * Modelos jerarquicos (subsistemas que necesitan compartir senales)
   * La funcion sim(...) y el workspace de MATLAB
 - Los datos se retornan como variables con nombres predeterminados
   (yout, xout, etc.) o personalizables.
 - Ejemplo: Usar Out1 para obtener la salida del sistema que se usara
   en calculos posteriores o graficos en MATLAB.
%
 TO WORKSPACE:
 - NO define interfaz del modelo; es un bloque de REGISTRO O MONITOREO.
 - Guarda internamente los datos de la simulacion en el workspace sin
   necesidad de que salgan como puerto del diagrama.
 - Es OPCIONAL; su proposito es documental y de analisis posterior.
 - Permite elegir el formato de guardado:
   * Array (matriz con tiempo en columna 1)
   * Structure (estructura con campos etiquetados)
   * Structure with time (estructura con campo tiempo separado)
 - No interfiere con la comunicacion formal del modelo.
 - Ejemplo: Grabar internamente una senal intermedia (como un error de
   control) para inspeccionarla despues sin que sea una salida oficial.
%
 COMPARACION EN TABLA:
%
 Aspecto                | Out (Outport)         | To Workspace
 ---|---|---
 Funcion principal      | Interfaz de salida    | Registro de datos
 Obligatorio            | Si (para sim(...))    | No (opcional)
 Retorna datos a MATLAB | Si, automaticamente   | Si, por guardado interno
 Nombres de variables   | Predefinidos (yout)   | Personalizables
 Formatos disponibles   | Array                 | Array, Structure, etc.
 Jerarquia de bloques   | Define puertos        | Solo monitoreo
 Uso tipico             | Exportar datos        | Grabar senales internas
%
 CASO DE USO PRACTICO CON AMBOS:
%
 Escenario: Simulacion de un sistema de control con entrada, salida y
 senal de error de control.
%
 1. Use Out1 para la salida del sistema (y del modelo).
 2. Use Out2 para la accion de control (u) si es necesaria en MATLAB.
 3. Use "To Workspace" conectado al error (e = r - y) para grabar esta
    senal intermedia sin necesidad de puerto adicional.
%
 Resultado en workspace:
 - Automaticamente: yout, uout (si tiene Out2)
 - Grabado por To Workspace: error_signal (nombre personalizado)
%
 RECOMENDAZIONE PARA ESTA PRACTICA:
 - Use Outport (Out1, Out2) para senales que necesita en MATLAB.
 - Use To Workspace para senales internas que quiera analizar sin
   declararlas como puertos oficiales del modelo.
 - Ambas opciones PUEDEN COEXISTIR en el mismo modelo sin conflicto.
 
% 0.11) ¿Tiene alguna variable no esperada? (Analisis adicional)

 PREGUNTA:
 Despues de ejecutar la simulacion, al revisar el workspace con 'whos',
 aparecen variables como SimulationMetadata y ErrorMessage. ¿Son variables
 no esperadas o forman parte del proceso de simulacion?
%
 RESPUESTA:
 NO son variables inesperadas. SimulationMetadata y ErrorMessage son
 variables ESPERADAS y SON PARTE DEL FUNCIONAMIENTO NORMAL de la funcion
 sim(...) en Simulink. Aparecen automaticamente en el workspace.
%
 DESCRIPCION DETALLADA:
%
 SimulationMetadata:
 - Contenido: Variable de estructura que almacena TODA la informacion
   metadata de la corrida de simulacion.
 - Incluye:
   * Nombre y ruta del modelo simulado
   * Parametros del solver (tolerancia, tipo de paso, etc.)
   * Tiempos de inicio y fin de simulacion
   * Numero de pasos de integracion realizados
   * Informacion de compilacion y enlace del modelo
   * Configuracion de diagnosticos aplicados
   * Resumen de la ejecucion (exito, advertencias, etc.)
 - Proposito: Documento completo del entorno y condiciones en que se
   ejecuto la simulacion, util para reproducibilidad y auditorias.
 - Acceso: SimulationMetadata es una estructura; acceda a sus campos con
   punto: SimulationMetadata.ModelName, etc.
%
 ErrorMessage:
 - Contenido: Campo de la salida de sim(...) que REGISTRA ERRORES de
   simulacion si los hay.
 - Caracteristicas:
   * Si NO hay errores => está VACÍA (variable string vacío '')
   * Si hay errores => contiene descripcion del problema
   * Incluye linea de ejecucion donde ocurrio el error
   * Facilita diagnostico rapido de problemas
 - Proposito: Mecanismo automatico de reporte de anomalias sin necesidad
   de capturar excepciones manualmente en try-catch.
 - En la practica actual está VACIA porque la simulacion fue EXITOSA.
%
 VERIFICACION EN EL WORKSPACE:
 
 Comando recomendado para revisar:
   whos SimulationMetadata ErrorMessage
   
 Si ejecuta:
   SimulationMetadata
   
 MATLAB mostrara una estructura con todos sus campos.
 
 Para ver el ErrorMessage:
   ErrorMessage
   
 Si esta vacio, vera: ans = [] (conjunto vacio) o '' (string vacio).
%
 RECOMENDACION PARA LA PRACTICA:
 - Estas variables SON NORMALES y ESPERADAS.
 - No las elimine a menos que necesite limpiar el workspace.
 - Si desea evitarlas en futuras simulaciones, use la opcion 'ReturnWorkspaceOutputs'
   en sim(...) con valor false (pero esto es avanzado).
 - Para esta practica, DOCUMENTELAS en sus informes mencionando que fueron
   generadas automaticamente por el proceso de simulacion y que su presencia
   indica que la simulacion se ejecuto correctamente.
%
 CONCLUSION:
 SimulationMetadata y ErrorMessage NO son variables inesperadas o problematicas.
 Son INDICADORES DE EXITO de la simulacion. Su presencia confirma que:
 1. sim(...) se ejecuto correctamente
 2. No hubo errores en la ejecucion
 3. Toda la informacion de la corrida fue registrada para auditoria

% 0.12) Graficar la respuesta del sistema con variables del ETML (plot)
 PREGUNTA:
 Con la informacion contenida en las variables del ETML, grafique la
 respuesta del sistema usando plot. Recuerde que las variables estan en
 formato arreglo (con tiempo), por lo que primero debe extraer columnas.
%
 RESPUESTA:
 Cuando una variable esta en formato arreglo, MATLAB la guarda como una
 matriz donde cada columna representa una senal distinta.
%
 Extraccion de columnas (indexacion):
 - Sintaxis general: matriz(:,columna)
 - Ejemplo:
   * t = datos(:,1);   % primera columna: tiempo
   * y = datos(:,2);   % segunda columna: salida
%
 Esto significa:
 - ':'  toma todas las filas
 - '1'  toma la columna 1
 - '2'  toma la columna 2
%
 EJEMPLO PRACTICO (variable output):
%
 if exist('output','var') == 1
     t = output(:,1);    % columna de tiempo
     y = output(:,2);    % columna de salida

     figure('Name','Respuesta del sistema');
     plot(t, y, 'b', 'LineWidth', 1.5);
     grid on;
     xlabel('Tiempo [s]');
     ylabel('Salida y(t)');
     title('Respuesta temporal del sistema');
 else
     warning('No existe la variable output en el workspace.');
 end
%
 EJEMPLO SI USA yout/tout:
%
 if exist('tout','var') == 1 && exist('yout','var') == 1
     t2 = tout;
     y2 = yout(:,1);     % primera salida (si yout tiene varias columnas)

     figure('Name','Respuesta desde yout/tout');
     plot(t2, y2, 'r', 'LineWidth', 1.5);
     grid on;
     xlabel('Tiempo [s]');
     ylabel('Salida y(t)');
     title('Respuesta del sistema (yout vs tout)');
 end
%
 RESUMEN:
 Para extraer una columna de una matriz en MATLAB use indexacion:
   variable(:,n)
 donde n es el numero de columna. Luego grafique con:
   plot(t, y)

