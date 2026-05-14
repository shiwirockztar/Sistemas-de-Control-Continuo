"""
Control Proporcional (P-only) con registro de datos
Adaptado para el Laboratorio de Control de Temperatura (TempLabUdeA)
"""

import tclab
import numpy as np
import time
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------------
# Conexión con el dispositivo Arduino + TCLab
# ------------------------------------------------------------------------------
lab = tclab.TCLab()

def save_txt(t, u1, u2, y1, y2, sp1, sp2, filename='data_ponly.txt'):
    data = np.vstack((t, u1, u2, y1, y2, sp1, sp2)).T
    encabezado = ('Tiempo (s), Cal1 (%), Cal2 (%), '
                  'Temp1 (°C), Temp2 (°C), Set1 (°C), Set2 (°C)')
    np.savetxt(filename, data, delimiter=',', header=encabezado, comments='')

print("Firmware:", lab.version)
lab.LED(100)

# ------------------------------------------------------------------------------
# Parámetros del Controlador P-only
# ------------------------------------------------------------------------------
tau_11 = 159.0457
K11 = 0.3271
Kc = K11
Q_bias = 0.0 # Definido por la guía para TempLABUdeA
# Pu = 43.84


# ku = 500
# Kp = 0.6*ku
# Ti = 0.5*Pu
# Td = 0.125*Pu 

# ------------------------------------------------------------------------------
# Parámetros de la prueba
# ------------------------------------------------------------------------------
duracion_min = 10.0             
ciclos = int(60 * duracion_min) 
t_array = np.zeros(ciclos)      

# Definir punto de consigna (Set-point) elevado para ver el offset
Tset1 = np.ones(ciclos) * 40.0  
Tset2 = np.ones(ciclos) * 40.0  

T1 = np.ones(ciclos) * lab.T1
T2 = np.ones(ciclos) * lab.T2
Q1 = np.zeros(ciclos)
Q2 = np.zeros(ciclos)

# Variables de estado del PID
ierr = 0.0      # Integral acumulada
prev_err = 0.0  # Error previo para la derivada 

print("Iniciando Control P-only. Ctrl-C para detener.")
print(f"{'t(s)':>6s} {'Q1(%)':>6s} {'T1(°C)':>7s} {'SP1(°C)':>7s} {'Err':>6s}")

plt.figure(figsize=(10, 7))
plt.ion()
plt.show()

# ------------------------------------------------------------------------------
# Bucle principal de control
# ------------------------------------------------------------------------------
t_inicio = time.time()
t_ant = t_inicio

try:
    for i in range(1, ciclos):
        dt = time.time() - t_ant
        time.sleep(max(0.0, 1.0 - dt))
        
        t_actual = time.time()
        t_array[i] = t_actual - t_inicio
        t_ant = t_actual
        
        # 1. Leer temperaturas actuales
        T1[i] = lab.T1
        
        # 2. Lógica de control P-only: Q = Q_bias + Kc * (SP - PV) 
        error1 = Tset1[i] - T1[i]
        
        # Términos PID
        # Integral
        ierr += error1 
        # Derivada
        deriv = error1 - prev_err
        
        # Ecuación de Control
        # Q1[i] = Q_bias + Kp * error1 + (Kp / Ti) * ierr + Kp * Td * deriv
        Q1[i] = Q_bias + Kc * error1 
        
        # Si se satura el actuador, se restaura la integral para evitar sobreimpulso excesivo
        if Q1[i] >= 100:
            Q1[i] = 100
            ierr -= error1
        elif Q1[i] <= 0:
            Q1[i] = 0
            ierr -= error1

        # 4. Enviar señales
        lab.Q1(Q1[i])
        prev_err = error1
        
        if i % 5 == 0: # Imprimir cada 5 iteraciones
            print(f"{t_array[i]:6.1f} {Q1[i]:6.2f} {T1[i]:7.2f} {Tset1[i]:7.2f} {error1:6.2f}")
        
        # Actualizar gráfico
        plt.clf()
        ax1 = plt.subplot(2,1,1)
        ax1.plot(t_array[:i], T1[:i], 'r-', label='T1 (PV)')
        ax1.plot(t_array[:i], Tset1[:i], 'k--', label='Set-point')
        plt.ylabel('Temperatura (°C)')
        plt.legend(loc='best')
        plt.grid(True)
        
        ax2 = plt.subplot(2,1,2)
        ax2.plot(t_array[:i], Q1[:i], 'b-', label='Señal Control (Q1)')
        plt.ylabel('Potencia (%)')
        plt.xlabel('Tiempo (s)')
        plt.legend(loc='best')
        plt.grid(True)
        plt.pause(0.05)
    
    lab.Q1(0); lab.Q2(0)
    save_txt(t_array, Q1, Q2, T1, T2, Tset1, Tset2)
    lab.close()

except KeyboardInterrupt:
    print("\nDetenido. Cerrando...")
    lab.Q1(0); lab.Q2(0); lab.close()
    save_txt(t_array[:i], Q1[:i], Q2[:i], T1[:i], T2[:i], Tset1[:i], Tset2[:i])