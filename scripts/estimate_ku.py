#!/usr/bin/env python3
"""Graficador y estimador de Ku/Tu para datos de control.

Uso básico:
  python3 scripts/estimate_ku.py --file mimo/data_ponly_t2.txt --kc 1.5

El script carga un CSV, detecta picos en la señal de temperatura (por defecto `Temp2`),
estima el periodo de oscilación `Tu` y, si el usuario provee `--kc` y las oscilaciones
parecen sostenidas, reporta `Ku = kc`.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    from scipy.signal import find_peaks
    _HAS_SCIPY = True
except Exception:
    _HAS_SCIPY = False


def simple_find_peaks(y, distance=5, height=None):
    peaks = []
    n = len(y)
    for i in range(1, n - 1):
        if y[i] > y[i - 1] and y[i] > y[i + 1]:
            peaks.append(i)
    if not peaks:
        return np.array([], dtype=int)
    peaks = np.array(peaks)
    # enforce minimal distance
    if distance > 1:
        good = [peaks[0]]
        for p in peaks[1:]:
            if p - good[-1] >= distance:
                good.append(p)
        peaks = np.array(good)
    if height is not None:
        peaks = peaks[y[peaks] >= height]
    return peaks


def detect_peaks(t, y):
    # detrend a bit by subtracting median of last 20% to remove setpoint offset
    baseline = np.median(y[int(len(y) * 0.8) :]) if len(y) > 5 else np.median(y)
    yd = y - baseline
    sd = np.std(yd)
    height = max(sd * 0.3, 0.1)
    if _HAS_SCIPY:
        peaks, _ = find_peaks(yd, height=height, distance=max(1, int(0.5 / np.median(np.diff(t)))))
    else:
        peaks = simple_find_peaks(yd, distance=3, height=height)
    return peaks, yd


def estimate_Tu(t, peak_idx):
    if len(peak_idx) < 2:
        return None
    times = t[peak_idx]
    periods = np.diff(times)
    return np.mean(periods), periods


def main():
    p = argparse.ArgumentParser(description="Graficar datos y estimar Ku/Tu desde un CSV de tiempo-serie")
    p.add_argument("--file", "-f", required=True, help="Ruta al CSV de datos")
    p.add_argument("--kc", type=float, default=None, help="Valor de Kc usado en la prueba (opcional)")
    p.add_argument("--temp-col", default=None, help="Nombre (parcial) de la columna de temperatura a analizar (ej: Temp2)")
    p.add_argument("--save", default=None, help="Guardar figura a archivo (png) en vez de mostrar)")
    args = p.parse_args()

    fp = Path(args.file)
    if not fp.exists():
        print(f"Archivo no encontrado: {fp}")
        sys.exit(1)

    # leer CSV intentando detectar separador
    df = pd.read_csv(fp, sep=None, engine="python")
    print("Columnas detectadas:", list(df.columns))

    # detectar columna de tiempo
    time_col = None
    for c in df.columns:
        if "Tiempo" in c or "Time" in c or c.lower().startswith("t"):
            time_col = c
            break
    if time_col is None:
        time_col = df.columns[0]

    # detectar columna temperatura (preferir Temp2)
    temp_col = None
    if args.temp_col:
        for c in df.columns:
            if args.temp_col.lower() in c.lower():
                temp_col = c
                break
    if temp_col is None:
        for c in df.columns:
            if "Temp2" in c or "Temp 2" in c or "Temp2".lower() in c.lower():
                temp_col = c
                break
    if temp_col is None:
        for c in df.columns:
            if "Temp" in c or "temp" in c:
                temp_col = c
                break
    if temp_col is None:
        print("No se encontró columna de temperatura. Columnas:\n", df.columns)
        sys.exit(1)

    t = df[time_col].values.astype(float)
    y = df[temp_col].values.astype(float)

    peaks, yd = detect_peaks(t, y)
    est = estimate_Tu(t, peaks)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t, y, label=temp_col)
    ax.plot(t, yd + np.median(y), linestyle='--', alpha=0.6, label='detrended+median')
    if len(peaks) > 0:
        ax.scatter(t[peaks], y[peaks], color='C1', zorder=5, label='picos')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Temperatura')
    ax.grid(True)
    ax.legend(loc='upper left')

    # añadir señal de control si existe (Cal2 o Cal1)
    ctrl_col = None
    for c in df.columns:
        if c.lower().startswith('cal2') or 'cal2' in c.lower():
            ctrl_col = c
            break
    if ctrl_col is None:
        for c in df.columns:
            if c.lower().startswith('cal'):
                ctrl_col = c
                break
    if ctrl_col is not None:
        ax2 = ax.twinx()
        ax2.plot(t, df[ctrl_col].values, color='0.6', alpha=0.6, label=ctrl_col)
        ax2.set_ylabel(ctrl_col)
        ax2.legend(loc='upper right')

    title = f"{fp.name} — columna analizada: {temp_col}"
    if args.kc is not None:
        title += f" — Kc={args.kc}"
    ax.set_title(title)

    if est is None:
        print("No se detectaron suficientes picos para estimar Tu.")
    else:
        Tu, periods = est
        print(f"Periodo medio Tu = {Tu:.3f} s (n_picos={len(peaks)})")
        if args.kc is not None:
            # si las oscilaciones son aproximadamente periódicas y sostenidas
            if len(periods) >= 4 and (np.std(periods) / np.mean(periods)) < 0.25:
                print(f"Según la prueba, las oscilaciones parecen sostenidas. Se reporta Ku = {args.kc}")
            else:
                print("Las oscilaciones no parecen sostenidas o periódicas; no puedo asegurar que `kc` sea `Ku`.")

    if args.save:
        fig.savefig(args.save, dpi=150)
        print(f"Figura guardada en {args.save}")
    else:
        plt.show()


if __name__ == '__main__':
    main()
