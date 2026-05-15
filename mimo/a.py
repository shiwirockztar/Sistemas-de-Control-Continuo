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

# ----------------------------------------------------------------------------
# Parámetros del Controlador PID (forma paralela)
# Basados en los valores calculados en Miniproyecto1_MIMO(Planta_termica).ipynb
# Usamos los valores de sintonía (si no se dispone de soluciones LGR ejecutadas,
# se emplean los parámetros derivados por Ku/Pu presentes en la notebook).
tau_11 = 159.0457
K11 = 0.3271

# Valores de sintonía extraídos / calculados
# Para el subsistema 1
Kp1 = 0.6 * 500.0            # = 300.0 (Ku=500, Kp=0.6*Ku)
Ti1 = 0.5 * 43.84            # = 21.92
Td1 = 0.125 * 43.84          # = 5.48

# Para el subsistema 2
Kp2 = 0.6 * 500.0            # = 300.0
Ti2 = 0.5 * 93.47            # = 46.735
Td2 = 0.125 * 93.47          # = 11.68375

# Convertir a forma paralela usada en el notebook: Ci(s)=Kp + Ki/s + Kd*s
Ki1 = Kp1 / Ti1
Kd1 = Kp1 * Td1

Ki2 = Kp2 / Ti2
Kd2 = Kp2 * Td2

# Derivada filtrada (tiempo de filtrado continuo)
T_der = 0.005

# Bias inicial para Q (offset)
Q_bias = 0.0

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

# Variables de estado del PID (dos canales)
ierr1 = 0.0      # Integral acumulada canal 1
prev_err1 = 0.0  # Error previo canal 1
deriv_filt1 = 0.0

ierr2 = 0.0      # Integral acumulada canal 2
prev_err2 = 0.0  # Error previo canal 2
deriv_filt2 = 0.0

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
        
        # 2. Leer temperatura actual para canal 2 cuando exista
        T2[i] = lab.T2

        # Canal 1 - PID paralelo con derivada filtrada
        error1 = Tset1[i] - T1[i]
        dt = max(1e-6, t_array[i] - t_array[i-1]) if i > 0 else 1.0

        # Integral (rectangular) y anti-windup aplicado después de saturación
        ierr1 += error1 * dt

        # Derivada cruda
        deriv_raw1 = (error1 - prev_err1) / dt
        # Filtro discreto aproximado: alpha = T/(T+dt)
        alpha = T_der / (T_der + dt)
        deriv_filt1 = alpha * deriv_filt1 + (1 - alpha) * deriv_raw1

        # Señal de control (paralela): u = Kp*e + Ki*integral + Kd*deriv
        u1 = Q_bias + Kp1 * error1 + Ki1 * ierr1 + Kd1 * deriv_filt1

        # Saturación y anti-windup
        if u1 > 100:
            u1 = 100
            ierr1 -= error1 * dt
        elif u1 < 0:
            u1 = 0
            ierr1 -= error1 * dt

        Q1[i] = u1
        prev_err1 = error1

        # Canal 2 - PID paralelo (si se desea controlar canal 2 también)
        error2 = Tset2[i] - T2[i]
        ierr2 += error2 * dt
        deriv_raw2 = (error2 - prev_err2) / dt
        deriv_filt2 = alpha * deriv_filt2 + (1 - alpha) * deriv_raw2
        u2 = Q_bias + Kp2 * error2 + Ki2 * ierr2 + Kd2 * deriv_filt2
        if u2 > 100:
            u2 = 100
            ierr2 -= error2 * dt
        elif u2 < 0:
            u2 = 0
            ierr2 -= error2 * dt
        Q2[i] = u2

        # 4. Enviar señales
        lab.Q1(Q1[i])
        lab.Q2(Q2[i])
        
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