import argparse
import time

import matplotlib.pyplot as plt
import numpy as np
import tclab


def save_txt(t, u1, y1, sp1, filename="data_PID_Q1.txt"):
    """Guarda los arrays de Q1 como columnas en un archivo CSV con cabecera."""
    data = np.vstack((t, u1, y1, sp1)).T
    header = "Tiempo_s,Cal1_pct,Temp1_C,Set1_C"
    np.savetxt(filename, data, delimiter=",", header=header, comments="")


def clamp_0_100(value):
    """Limita una señal al rango de actuacion [0, 100]."""
    return max(0.0, min(100.0, value))


def connect_lab(force_sim=False, speedup=10):
    """Conecta a TCLab real y, si falla o se fuerza, usa simulacion."""
    if force_sim:
        TCLab = tclab.setup(connected=False, speedup=speedup)
        return TCLab(), True

    try:
        return tclab.TCLab(), False
    except Exception as exc:
        print(f"No se pudo conectar al hardware real: {exc}")
        print("Se iniciara en modo simulacion.")
        TCLab = tclab.setup(connected=False, speedup=speedup)
        return TCLab(), True


def run_experiment(sim=False, duration_min=6.2):
    # Parametros del proceso y controlador PID
    taup = 111.0140
    tethap = 23.4411
    kc = 0.2 * (taup / tethap) ** 1.22
    tau_i = 175.0
    tau_d = 5.0
    q_bias = 0.0

    lab, is_sim = connect_lab(force_sim=sim, speedup=10)
    print("Modo simulacion." if is_sim else "Modo hardware real.")

    ciclos = int(60 * duration_min)
    t_array = np.zeros(ciclos)

    tset1 = np.ones(ciclos) * 23.0

    t1 = np.ones(ciclos) * lab.T1
    q1 = np.zeros(ciclos)

    error1_int = 0.0
    prev_error1 = 0.0

    print("Iniciando bucle principal. Ctrl-C para detener.")
    print(f"{'t(s)':>6s} {'Q1(%)':>7s} {'T1(C)':>8s}")
    print(f"{t_array[0]:6.1f} {q1[0]:7.2f} {t1[0]:8.2f}")

    plt.figure(figsize=(10, 7))
    plt.ion()
    plt.show()

    t_inicio = time.time()
    t_ant = t_inicio
    i_last = 0

    try:
        for i in range(1, ciclos):
            dt_loop = time.time() - t_ant
            time.sleep(max(0.0, 1.0 - dt_loop))

            t_actual = time.time()
            dt = t_actual - t_ant
            t_array[i] = t_actual - t_inicio
            t_ant = t_actual

            t1[i] = lab.T1

            error1 = tset1[i] - t1[i]

            error1_int += error1 * dt

            deriv1 = (error1 - prev_error1) / dt if dt > 1e-9 else 0.0
            prev_error1 = error1

            # u1 = q_bias + kc * error1 + (kc / tau_i) * error1_int + kc * tau_d * deriv1 # PID sin filtro derivativo
            # kc se varia con el proceso, pero tau_i y tau_d se pueden ajustar para mejorar la respuesta.
            # para calcular los parametros del PID se puede usar la formula de Ziegler-Nichols, pero es recomendable ajustar manualmente para mejorar el desempeño.
            u1 = q_bias + kc * error1 # P puro, para comparar con el PID completo

            q1[i] = clamp_0_100(u1)

            # Anti-windup simple: revierte la integral cuando la salida satura.
            if q1[i] != u1:
                error1_int -= error1 * dt

            lab.Q1(q1[i])
            lab.Q2(0)

            print(f"{t_array[i]:6.1f} {q1[i]:7.2f} {t1[i]:8.2f}")

            plt.clf()
            ax1 = plt.subplot(2, 1, 1)
            ax1.grid(True)
            ax1.plot(t_array[: i + 1], t1[: i + 1], "r-", label="T1")
            ax1.plot(t_array[: i + 1], tset1[: i + 1], "r--", label="SP1")
            ax1.set_ylabel("Temperatura (C)")
            ax1.legend(loc="best")

            ax2 = plt.subplot(2, 1, 2)
            ax2.grid(True)
            ax2.plot(t_array[: i + 1], q1[: i + 1], "r-", label="Q1")
            ax2.set_ylabel("Calentadores (%)")
            ax2.set_xlabel("Tiempo (s)")
            ax2.legend(loc="best")

            plt.pause(0.05)
            i_last = i

    except KeyboardInterrupt:
        print("\nDetencion por usuario.")
    finally:
        try:
            lab.Q1(0)
            lab.Q2(0)
        except Exception:
            pass

        try:
            lab.close()
        except Exception:
            pass

        n = i_last + 1
        save_txt(t_array[:n], q1[:n], t1[:n], tset1[:n])
        plt.savefig("resultado_PID_Q1.png", dpi=150, bbox_inches="tight")
        print("Datos guardados en data_PID_Q1.txt")
        print("Figura guardada en resultado_PID_Q1.png")


def parse_args():
    parser = argparse.ArgumentParser(description="PID para TCLab (Lab 4) - solo Q1")
    parser.add_argument(
        "--sim",
        action="store_true",
        help="Fuerza modo simulacion incluso si hay hardware disponible.",
    )
    parser.add_argument(
        "--min",
        type=float,
        default=6.2,
        help="Duracion del experimento en minutos (default: 6.2).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_experiment(sim=args.sim, duration_min=args.min)