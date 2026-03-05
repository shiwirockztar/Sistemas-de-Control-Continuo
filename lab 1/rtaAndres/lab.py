import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Cargar los datos
file_path = 'data_Q2.txt'
# Usamos 'latin1' porque el archivo viene de Windows/ANSI con símbolos de grado °
data = pd.read_csv(file_path, skipinitialspace=True, encoding='latin1')

# Limpiar nombres de columnas
data.columns = [c.strip() for c in data.columns]

t = data['Tiempo (s)'].values
u = data['Cal2 (%)'].values
y = data['Temp2 (°C)'].values

# 2. Identificar el escalón de entrada
idx_step = np.where(np.diff(u) > 0)[0][0] + 1
t_step = t[idx_step]
u_initial = u[0]
u_final = u[-1]
delta_u = u_final - u_initial

# 3. Regresión Polinómica (Grado 6 para capturar la curva en S)
# Ajustamos el modelo a los datos de temperatura
coefs = np.polyfit(t, y, 6)
poly_func = np.poly1d(coefs)
y_fit = poly_func(t)

# 4. Encontrar el punto de máxima pendiente usando la derivada de la regresión
poly_der = np.polyder(poly_func) # Derivada analítica del polinomio
pendientes = poly_der(t)

# Buscamos el máximo de la pendiente después de que inicia el escalón
idx_max_pendiente = idx_step + np.argmax(pendientes[idx_step:])
t_inflexion = t[idx_max_pendiente]
y_inflexion = y_fit[idx_max_pendiente]
m_max = pendientes[idx_max_pendiente] # La pendiente (m) en el punto de inflexión

# 5. Cálculos de Ziegler-Nichols
y_initial = np.mean(y[:idx_step])
y_final = np.mean(y[-20:]) # Promedio de los últimos puntos para el valor final
K = (y_final - y_initial) / delta_u

# Recta tangente: y = m(t - t_i) + y_i
# Intersección con y_initial (Tiempo muerto theta)
# y_initial = m_max * (t_base - t_inflexion) + y_inflexion
t_base = ((y_initial - y_inflexion) / m_max) + t_inflexion
theta = t_base - t_step

# Intersección con y_final (Para hallar constante de tiempo tau)
t_final_interseccion = ((y_final - y_inflexion) / m_max) + t_inflexion
tau = t_final_interseccion - t_base

print(f"--- Parámetros por Regresión Polinómica ---")
print(f"Ganancia (K): {K:.4f}")
print(f"Tiempo Muerto (theta): {theta:.4f} s")
print(f"Constante de Tiempo (tau): {tau:.4f} s")

# 5.1 Cálculos de Smith (28.3% y 63.2%)
def first_crossing_time(t_arr, y_arr, y_level, start_idx, direction=1):
	for i in range(start_idx + 1, len(t_arr)):
		y_prev = y_arr[i - 1]
		y_curr = y_arr[i]

		if direction >= 0:
			crossed = (y_prev <= y_level <= y_curr)
		else:
			crossed = (y_prev >= y_level >= y_curr)

		if crossed:
			if y_curr == y_prev:
				return t_arr[i]
			frac = (y_level - y_prev) / (y_curr - y_prev)
			return t_arr[i - 1] + frac * (t_arr[i] - t_arr[i - 1])

	return np.nan

direction = 1 if (y_final - y_initial) >= 0 else -1
y_28 = y_initial + 0.283 * (y_final - y_initial)
y_63 = y_initial + 0.632 * (y_final - y_initial)

t1 = first_crossing_time(t, y_fit, y_28, idx_step, direction)
t2 = first_crossing_time(t, y_fit, y_63, idx_step, direction)

if np.isnan(t1) or np.isnan(t2) or t2 <= t1:
	theta_smith = np.nan
	tau_smith = np.nan
else:
	tau_smith = max(1.5 * (t2 - t1), 1e-6)
	theta_smith = max((1.5 * t1 - 0.5 * t2) - t_step, 0.0)

print(f"\n--- Parámetros por Método de Smith ---")
print(f"t1 (28.3%): {t1:.4f} s")
print(f"t2 (63.2%): {t2:.4f} s")
print(f"Tiempo Muerto Smith (theta): {theta_smith:.4f} s")
print(f"Constante de Tiempo Smith (tau): {tau_smith:.4f} s")

if not np.isnan(theta_smith) and not np.isnan(tau_smith):
	tt_smith = t - (t_step + theta_smith)
	y_smith = y_initial + K * delta_u * np.where(tt_smith > 0, 1.0 - np.exp(-tt_smith / tau_smith), 0.0)
else:
	y_smith = np.full_like(t, np.nan, dtype=float)

# 6. Gráfica de resultados
plt.figure(figsize=(12, 7))
plt.plot(t, y, 'k.', alpha=0.2, label='Datos Originales')
plt.plot(t, y_fit, 'b-', label='Regresión Polinómica (Grado 6)')

# Dibujar la línea tangente
t_tangente = np.linspace(t_base, t_final_interseccion, 100)
y_tangente = m_max * (t_tangente - t_inflexion) + y_inflexion
plt.plot(t_tangente, y_tangente, 'r--', lw=2, label='Tangente en Inflexión')

# Guías visuales
plt.axhline(y_initial, color='green', linestyle=':', label='Valor Inicial')
plt.axhline(y_final, color='red', linestyle=':', label='Valor Final')
plt.axvline(t_step, color='black', alpha=0.5, label='Inicio Escalón')

plt.title('Ziegler-Nichols: Análisis por Regresión')
plt.xlabel('Tiempo (s)')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.grid(True)
plt.show()

# 7. Gráfica de Smith
plt.figure(figsize=(12, 7))
plt.plot(t, y, 'k.', alpha=0.2, label='Datos Originales')
plt.plot(t, y_fit, 'b-', lw=2, label='Regresión Polinómica (Grado 6)')

if not np.all(np.isnan(y_smith)):
	plt.plot(t, y_smith, 'm-', lw=2.5, label='Modelo FOPDT por Smith')

if not np.isnan(t1):
	plt.axvline(t1, color='orange', linestyle='--', alpha=0.7, label='t1 (28.3%)')
if not np.isnan(t2):
	plt.axvline(t2, color='red', linestyle='--', alpha=0.7, label='t2 (63.2%)')
if not np.isnan(theta_smith):
	plt.axvline(t_step + theta_smith, color='purple', linestyle=':', alpha=0.9, label='t0 + theta Smith')

plt.axhline(y_28, color='orange', linestyle=':', alpha=0.8, label='Nivel 28.3%')
plt.axhline(y_63, color='red', linestyle=':', alpha=0.8, label='Nivel 63.2%')
plt.axvline(t_step, color='black', alpha=0.5, label='Inicio Escalón')

plt.title('Método de Smith: Identificación FOPDT')
plt.xlabel('Tiempo (s)')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.grid(True)
plt.show()

# 8. Comparación: Ziegler-Nichols vs Smith
if not np.isnan(theta) and not np.isnan(tau):
	tt_zn = t - (t_step + theta)
	y_zn = y_initial + K * delta_u * np.where(tt_zn > 0, 1.0 - np.exp(-tt_zn / tau), 0.0)
else:
	y_zn = np.full_like(t, np.nan, dtype=float)

plt.figure(figsize=(12, 7))
plt.plot(t, y, 'k.', alpha=0.25, label='Datos Originales')

if not np.all(np.isnan(y_zn)):
	plt.plot(t, y_zn, 'c--', lw=2.5,
			 label=f'FOPDT Ziegler-Nichols (tau={tau:.2f}, theta={theta:.2f})')

if not np.all(np.isnan(y_smith)):
	plt.plot(t, y_smith, 'm-', lw=2.5,
			 label=f'FOPDT Smith (tau={tau_smith:.2f}, theta={theta_smith:.2f})')

plt.axvline(t_step, color='black', alpha=0.5, linestyle=':', label='Inicio Escalón')
plt.title('Comparación de Modelos FOPDT: Ziegler-Nichols vs Smith')
plt.xlabel('Tiempo (s)')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.grid(True)
plt.show()