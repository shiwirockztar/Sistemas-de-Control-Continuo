"""
Control PID para canal Q1 (solo Q1)
Basado en a.py; usa parámetros del notebook Miniproyecto1_MIMO(Planta_termica).
"""

import tclab
import numpy as np
import time
import matplotlib.pyplot as plt

# Conexión
lab = tclab.TCLab()

def save_txt(t, u1, u2, y1, y2, sp1, sp2, filename='data_q1.txt'):
    data = np.vstack((t, u1, u2, y1, y2, sp1, sp2)).T
    encabezado = ('Tiempo (s), Cal1 (%), Cal2 (%), '
                  'Temp1 (°C), Temp2 (°C), Set1 (°C), Set2 (°C)')
    np.savetxt(filename, data, delimiter=',', header=encabezado, comments='')

print("Firmware:", lab.version)
lab.LED(100)
lab.Q2(0)  # asegurar Q2 apagado

# Parámetros PID (tomados de a.py)
tau_11 = 159.0457
K11 = 0.3271
Kp1 = 0.6 * 500.0
Ti1 = 0.5 * 43.84
Td1 = 0.125 * 43.84
Ki1 = Kp1 / Ti1
Kd1 = Kp1 * Td1
T_der = 0.005
Q_bias = 0.0

# Prueba
duracion_min = 10.0
ciclos = int(60 * duracion_min)
t_array = np.zeros(ciclos)

Tset1 = np.ones(ciclos) * 40.0
Tset2 = np.ones(ciclos) * 40.0

T1 = np.ones(ciclos) * lab.T1
T2 = np.ones(ciclos) * lab.T2
Q1 = np.zeros(ciclos)
Q2 = np.zeros(ciclos)

# Estados PID
ierr1 = 0.0
prev_err1 = 0.0
deriv_filt1 = 0.0

print("Iniciando control solo Q1. Ctrl-C para detener.")
print(f"{'t(s)':>6s} {'Q1(%)':>6s} {'T1(°C)':>7s} {'SP1(°C)':>7s} {'Err':>6s}")

plt.figure(figsize=(10,7))
plt.ion()
plt.show()

# Loop
t_inicio = time.time()
t_ant = t_inicio
try:
    for i in range(1, ciclos):
        dt = time.time() - t_ant
        time.sleep(max(0.0, 1.0 - dt))
        t_actual = time.time()
        t_array[i] = t_actual - t_inicio
        t_ant = t_actual

        # Lecturas
        T1[i] = lab.T1
        T2[i] = lab.T2

        # PID Q1
        error1 = Tset1[i] - T1[i]
        dt = max(1e-6, t_array[i] - t_array[i-1])
        ierr1 += error1 * dt
        deriv_raw1 = (error1 - prev_err1) / dt
        alpha = T_der / (T_der + dt)
        deriv_filt1 = alpha * deriv_filt1 + (1 - alpha) * deriv_raw1
        u1 = Q_bias + Kp1 * error1 + Ki1 * ierr1 + Kd1 * deriv_filt1
        if u1 > 100:
            u1 = 100
            ierr1 -= error1 * dt
        elif u1 < 0:
            u1 = 0
            ierr1 -= error1 * dt
        Q1[i] = u1
        prev_err1 = error1

        # Enviar señal (solo Q1)
        lab.Q1(Q1[i])

        if i % 5 == 0:
            print(f"{t_array[i]:6.1f} {Q1[i]:6.2f} {T1[i]:7.2f} {Tset1[i]:7.2f} {error1:6.2f}")

        # Graficas
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

    lab.Q1(0)
    save_txt(t_array, Q1, Q2, T1, T2, Tset1, Tset2, filename='data_q1.txt')
    lab.close()

except KeyboardInterrupt:
    print("\nDetenido. Cerrando...")
    lab.Q1(0); lab.close()
    save_txt(t_array[:i], Q1[:i], Q2[:i], T1[:i], T2[:i], Tset1[:i], Tset2[:i], filename='data_q1_partial.txt')
