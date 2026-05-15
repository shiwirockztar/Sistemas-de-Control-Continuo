"""
Control PID para canal Q2 (solo Q2)
Basado en a.py; usa parámetros del notebook Miniproyecto1_MIMO(Planta_termica).
"""

import tclab
import numpy as np
import time
import matplotlib.pyplot as plt

# Conexión
lab = tclab.TCLab()

def save_txt(t, u1, u2, y1, y2, sp1, sp2, filename='data_q2.txt'):
    data = np.vstack((t, u1, u2, y1, y2, sp1, sp2)).T
    encabezado = ('Tiempo (s), Cal1 (%), Cal2 (%), '
                  'Temp1 (°C), Temp2 (°C), Set1 (°C), Set2 (°C)')
    np.savetxt(filename, data, delimiter=',', header=encabezado, comments='')

print("Firmware:", lab.version)
lab.LED(100)
lab.Q1(0)  # asegurar Q1 apagado

# Parámetros PID (tomados de a.py)
tau_22 = 169.0153
K22 = 0.2931
Kp2 = 0.6 * 500.0
Ti2 = 0.5 * 93.47
Td2 = 0.125 * 93.47
Ki2 = Kp2 / Ti2
Kd2 = Kp2 * Td2
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
ierr2 = 0.0
prev_err2 = 0.0
deriv_filt2 = 0.0

print("Iniciando control solo Q2. Ctrl-C para detener.")
print(f"{'t(s)':>6s} {'Q2(%)':>6s} {'T2(°C)':>7s} {'SP2(°C)':>7s} {'Err':>6s}")

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

        # PID Q2
        error2 = Tset2[i] - T2[i]
        dt = max(1e-6, t_array[i] - t_array[i-1])
        ierr2 += error2 * dt
        deriv_raw2 = (error2 - prev_err2) / dt
        alpha = T_der / (T_der + dt)
        deriv_filt2 = alpha * deriv_filt2 + (1 - alpha) * deriv_raw2
        u2 = Q_bias + Kp2 * error2 + Ki2 * ierr2 + Kd2 * deriv_filt2
        if u2 > 100:
            u2 = 100
            ierr2 -= error2 * dt
        elif u2 < 0:
            u2 = 0
            ierr2 -= error2 * dt
        Q2[i] = u2
        prev_err2 = error2

        # Enviar señal (solo Q2)
        lab.Q2(Q2[i])

        if i % 5 == 0:
            print(f"{t_array[i]:6.1f} {Q2[i]:6.2f} {T2[i]:7.2f} {Tset2[i]:7.2f} {error2:6.2f}")

        # Graficas
        plt.clf()
        ax1 = plt.subplot(2,1,1)
        ax1.plot(t_array[:i], T2[:i], 'r-', label='T2 (PV)')
        ax1.plot(t_array[:i], Tset2[:i], 'k--', label='Set-point')
        plt.ylabel('Temperatura (°C)')
        plt.legend(loc='best')
        plt.grid(True)

        ax2 = plt.subplot(2,1,2)
        ax2.plot(t_array[:i], Q2[:i], 'b-', label='Señal Control (Q2)')
        plt.ylabel('Potencia (%)')
        plt.xlabel('Tiempo (s)')
        plt.legend(loc='best')
        plt.grid(True)
        plt.pause(0.05)

    lab.Q2(0)
    save_txt(t_array, Q1, Q2, T1, T2, Tset1, Tset2, filename='data_q2.txt')
    lab.close()

except KeyboardInterrupt:
    print("\nDetenido. Cerrando...")
    lab.Q2(0); lab.close()
    save_txt(t_array[:i], Q1[:i], Q2[:i], T1[:i], T2[:i], Tset1[:i], Tset2[:i], filename='data_q2_partial.txt')
