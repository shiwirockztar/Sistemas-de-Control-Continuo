2. Stakeholder and Context Mapping
Direct User
El sistema está dirigido principalmente a personas con dificultades de movilidad que requieren apoyo para caminar o realizar procesos de rehabilitación. Entre los posibles usuarios se encuentran:
•	Personas de la tercera edad con pérdida de estabilidad o fuerza muscular.
•	Pacientes en procesos de rehabilitación física después de lesiones o cirugías.
•	Personas con enfermedades neuromotoras o psicomotoras que afectan la marcha.
•	Usuarios que requieren asistencia para corregir patrones de movimiento inadecuados.
Professional Actor
La implementación y operación del sistema requiere la participación de diferentes profesionales:
•	Fisioterapeutas y terapeutas de rehabilitación, encargados de supervisar las sesiones y ajustar los parámetros de uso.
•	Médicos especialistas (ortopedistas y neurólogos), responsables de evaluar la condición clínica del paciente.
•	Ingenieros electrónicos, mecánicos, biomédicos y de software, encargados del diseño, mantenimiento y mejora del sistema.
•	Personal administrativo y legal que garantice el cumplimiento de normativas de seguridad y regulación médica.
Indirect User
Existen actores que, aunque no interactúan directamente con el sistema, pueden beneficiarse de su implementación:
•	Familiares y cuidadores que apoyan el proceso de rehabilitación.
•	Instituciones hospitalarias y centros de rehabilitación.
•	Empresas con trabajadores que realizan esfuerzos físicos intensos, donde tecnologías similares podrían contribuir a la prevención de lesiones musculoesqueléticas.
•	Entidades aseguradoras interesadas en reducir costos asociados a tratamientos prolongados o incapacidades.
Environmental or Institutional Context
El sistema podría utilizarse en diferentes entornos:
•	Hospitales y clínicas de rehabilitación.
•	Centros especializados en terapia física.
•	Entornos domésticos para terapias supervisadas o continuas.
•	Espacios con diferentes condiciones ambientales, superficies y obstáculos que pueden afectar el desempeño del sistema.

3. Impact and Risk Analysis
1. Benefits in a Rehabilitation Context
El sistema puede proporcionar diversos beneficios:
•	Favorecer la recuperación de la movilidad en pacientes con limitaciones motoras.
•	Reducir el riesgo de futuras lesiones musculares o articulares mediante asistencia controlada al movimiento.
•	Corregir patrones de marcha inadecuados y posturas que podrían generar lesiones a largo plazo.
•	Permitir terapias más repetitivas y consistentes, mejorando la calidad del proceso de rehabilitación.
2. Technical Limitations Affecting Real-World Performance
Algunas limitaciones técnicas pueden afectar el desempeño del sistema:
•	Retardos entre la detección del movimiento y la acción del controlador, reduciendo la naturalidad de la asistencia.
•	Dificultad para diferenciar correctamente actividades como caminar, trotar o correr.
•	Variabilidad entre usuarios en peso, altura, fuerza y condiciones físicas, lo que puede disminuir la precisión del modelo utilizado para el control.
•	Posibles errores de medición debido a ruido en sensores o fallas de calibración.
3. Potential Failures Outside the Laboratory
Cuando el sistema se utiliza en condiciones reales pueden aparecer situaciones no contempladas durante las pruebas:
•	Usuarios con pesos o dimensiones corporales diferentes a los considerados durante el diseño pueden generar errores de control.
•	Temperaturas extremas, humedad o polvo pueden afectar sensores y actuadores.
•	Bloqueos mecánicos o fallas de los motores pueden limitar la asistencia al movimiento.
•	Uso inadecuado del sistema en actividades para las que no fue diseñado, como deportes de alto impacto o movimientos bruscos.
4. Assumptions About Users, Therapists, and Environment
El diseño del sistema asume que:
•	Los usuarios y terapeutas reciben capacitación adecuada para operar el dispositivo de forma segura.
•	El sistema se utiliza únicamente para actividades de rehabilitación y movilidad asistida.
•	El usuario cumple con los requisitos físicos establecidos para el funcionamiento seguro del dispositivo.
•	Las sesiones de terapia se realizan sobre superficies relativamente planas y controladas.
•	Existe supervisión profesional durante las etapas iniciales de uso.
•	roceso de rehabilitación.
•	Instituciones hospitalarias y centros de rehabilitación.
•	Empresas con trabajadores que realizan esfuerzos físicos intensos, donde tecnologías similares podrían contribuir a la prevención de lesiones musculoesqueléticas.
•	Entidades aseguradoras interesadas en reducir costos asociados a tratamientos prolongados o incapacidades.


## 4. Engineering Design Implications

| Sociotechnical Issue Identified                                | Engineering Decision                                                        | Technical Justification                                                                                  | Expected Benefit                                      |
| -------------------------------------------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Diferencias de peso, altura y condición física entre usuarios. | Implementar control adaptativo o ajuste automático de parámetros.           | El modelo dinámico cambia entre usuarios y puede afectar la estabilidad y el seguimiento de trayectoria. | Mayor precisión y seguridad para distintos pacientes. |
| Riesgo de aplicar fuerzas excesivas durante la rehabilitación. | Incorporar límites de torque y velocidad angular en los actuadores.         | Evita movimientos bruscos que puedan causar lesiones al usuario.                                         | Incremento de la seguridad durante la terapia.        |
| Posibles fallas o ruido en sensores.                           | Utilizar filtrado digital y redundancia de sensores críticos.               | Reduce errores en la estimación de estados utilizados por el controlador.                                | Mayor confiabilidad y robustez del sistema.           |
| Uso en superficies irregulares o condiciones no ideales.       | Incorporar sensores adicionales para detección de terreno y perturbaciones. | Permite ajustar la asistencia según el entorno.                                                          | Mejor desempeño fuera del laboratorio.                |
| Uso incorrecto por parte de usuarios o terapeutas.             | Diseñar una interfaz simple con alertas y modos de operación seguros.       | Disminuye errores humanos durante la configuración y operación.                                          | Mayor facilidad de uso y adopción clínica.            |


