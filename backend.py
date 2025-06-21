import numpy as np
from scipy import signal
from math import pi

# Generar la señal analógica de acuerdo a los parámetros definidos por el usuario.
# Ahora recibe 'duracion' y 'frecuencia_predefinida' y los utiliza.
def generar_senal(tipo, funcion, fs, duracion, frecuencia_predefinida):
    # Aseguramos que num_puntos sea al menos 2 para evitar problemas con np.linspace y stepMode
    # y para que siempre haya al menos dos puntos para una línea o un escalón.
    num_puntos = int(fs * duracion)
    if num_puntos < 2:
        num_puntos = 2 # Mínimo de 2 puntos para poder graficar un segmento o escalón

    t = np.linspace(0, duracion, num_puntos, endpoint=False)

    if tipo == "Senoidal":
        senal = np.sin(2 * pi * frecuencia_predefinida * t) # Usa frecuencia_predefinida
    elif tipo == "Cuadrada":
        senal = signal.square(2 * pi * frecuencia_predefinida * t) # Usa frecuencia_predefinida
    elif tipo == "Triangular":
        senal = signal.sawtooth(2 * pi * frecuencia_predefinida * t, width=0.5) # Usa frecuencia_predefinida
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

    # Evitar división por cero si max_val y min_val son iguales (señal constante)
    if max_val == min_val:
        # Si la señal es constante, la cuantificación es simplemente el valor constante.
        # Aseguramos que el array no esté vacío antes de intentar acceder a senal[0]
        return np.full_like(senal, senal[0] if len(senal) > 0 else 0.0)

    # Normaliza la señal al rango [0, 1]
    senal_norm = (senal - min_val) / (max_val - min_val)
    # Escala y redondea
    senal_cuantizada = np.round(senal_norm * (niveles - 1)) / (niveles - 1)
    # Devuelve al rango original
    senal_cuantizada = senal_cuantizada * (max_val - min_val) + min_val
    return senal_cuantizada


# Procesa la señal, aplicando el proceso de muestreo y cuantización.
# Ahora recibe todos los argumentos necesarios y los pasa a generar_senal.
def procesar_senal(tipo, fs, bits, funcion, duracion, frecuencia_predefinida):
    # Pasa todos los parámetros relevantes a generar_senal
    t, analog = generar_senal(tipo, funcion, fs, duracion, frecuencia_predefinida)
    digital = cuantizar_senal(analog, bits)
    return t, analog, digital