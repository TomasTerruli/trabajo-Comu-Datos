import numpy as np
from scipy import signal
from math import pi

def generar_senal(tipo, funcion, fs, duracion, frecuencia_predefinida):
    num_puntos = int(fs * duracion)
    if num_puntos < 2:
        num_puntos = 2 # Mínimo de 2 puntos para poder graficar un segmento o escalón

    t = np.linspace(0, duracion, num_puntos, endpoint=False)

    if tipo == "Senoidal":
        senal = np.sin(2 * pi * frecuencia_predefinida * t)
    elif tipo == "Cuadrada":
        senal = signal.square(2 * pi * frecuencia_predefinida * t)
    elif tipo == "Triangular":
        senal = signal.sawtooth(2 * pi * frecuencia_predefinida * t, width=0.5)
    elif tipo == "Personalizada":
        try:
            if not funcion.strip():
                raise ValueError("No se ingresó una función para la señal personalizada.")
            senal = eval(funcion, {"t": t, "pi": pi, "sin": np.sin, "cos": np.cos, "exp": np.exp, "np": np})
        except Exception as e:
            raise ValueError(f"Error al evaluar función personalizada: {e}")

    else:
        senal = np.zeros_like(t)

    return t, senal


def cuantizar_senal(senal, bits):
    niveles = 2 ** bits
    min_val = np.min(senal)
    max_val = np.max(senal)

    if max_val == min_val:
        return np.full_like(senal, senal[0] if len(senal) > 0 else 0.0)

    senal_norm = (senal - min_val) / (max_val - min_val)
    senal_cuantizada = np.round(senal_norm * (niveles - 1)) / (niveles - 1)
    senal_cuantizada = senal_cuantizada * (max_val - min_val) + min_val
    return senal_cuantizada


def procesar_senal(tipo, fs, bits, funcion, duracion, frecuencia_predefinida):
    t, analog = generar_senal(tipo, funcion, fs, duracion, frecuencia_predefinida)
    digital = cuantizar_senal(analog, bits)
    return t, analog, digital