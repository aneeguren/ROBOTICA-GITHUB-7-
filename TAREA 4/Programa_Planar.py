import matplotlib.pyplot as plt
import numpy as np

def clamp(x, lo=-1.0, hi=1.0):
    return max(lo, min(hi, x))

# Normalizacion del angulo, para que quede etre -180º y 180º
def norm_ang(a):
    return (a + np.pi) % (2*np.pi) - np.pi

# Cinematica directa: Calculo la posición de cada articulación del brazo
def cinematica_directa(theta1, theta2, l1, l2):
    x1 = l1 * np.cos(theta1)
    y1 = l1 * np.sin(theta1)
    x2 = x1 + l2 * np.cos(theta1 + theta2)
    y2 = y1 + l2 * np.sin(theta1 + theta2)
    return (0,0), (x1,y1), (x2,y2)

# Cinematica inversa: Con el efector final calcula los angulos
def cinematica_inversa(Xf, Yf, l1, l2, codo):
    r2 = Xf**2 + Yf**2
    r = np.sqrt(r2)
    if r > l1 + l2 or r < abs(l1 - l2): # Si los brazos estirados no pueden llegar al efector final no funcionara
        return None

# Aplicar la ley del coseno
    cos_alpha2 = clamp((r2 - l1**2 - l2**2) / (2*l1*l2))
    alpha2 = np.arccos(cos_alpha2)
    cos_alpha1 = clamp((r2 + l1**2 - l2**2) / (2*l1*r))
    alpha1 = np.arccos(cos_alpha1)
    phi = np.arctan2(Yf, Xf)

# Calcular dos posibles soluciones para theta2 (codo hacia un lado o el otro)
    soluciones = [(alpha2, phi - np.arctan2(l2*np.sin(alpha2), l1 + l2*np.cos(alpha2))),
                  (-alpha2, phi - np.arctan2(l2*np.sin(-alpha2), l1 + l2*np.cos(-alpha2)))]

# Calcular codo para ambas soluciones
    candidatos = []
    for theta2, theta1 in soluciones:
        _, (x_codo, y_codo), (x_ef, y_ef) = cinematica_directa(theta1, theta2, l1, l2)
        candidatos.append((theta1, theta2, y_codo))

    if codo == "arriba":
# Elegir la solución con mayor Y del codo
        theta1_final, theta2_final, _ = max(candidatos, key=lambda x: x[2])
    else:
# Elegir la solución con menor Y del codo
        theta1_final, theta2_final, _ = min(candidatos, key=lambda x: x[2])

    return theta1_final, theta2_final

def dibujar_ejes(ax, longitud=5):
    # Eje X horizontal de color rojo con label
    ax.plot([-longitud, longitud], [0, 0], color="red", linewidth=2, label="X")
    # Eje Y vertical de color verde con label
    ax.plot([0, 0], [-longitud, longitud], color="green", linewidth=2, label="Y")
    
    # Añadir leyenda de los ejes
    ax.legend(loc="upper right")

# Dibujar los brazos y hacer que lleguen hasta el efector final
def dibujar_brazo(ax, theta1, theta2, l1, l2, efector_final=None):
    base, codo, ef = cinematica_directa(theta1, theta2, l1, l2)
    if efector_final is not None:
        ef = efector_final  # Forzar efector final exacto
    xs = [base[0], codo[0], ef[0]]
    ys = [base[1], codo[1], ef[1]]
    ax.plot(xs, ys, color="black", linewidth=3)
    ax.scatter(xs, ys, color="black", s=25)

# Interpolar los angulos para una mejor animacion
def interp_angulo(a0, a1, t):
    diff = (a1 - a0 + np.pi) % (2*np.pi) - np.pi
    return a0 + diff*t


def main():
    print("Animación planar de codo arriba o abajo")

# Preguntar si quieres que sea codo arriba o abajo
    codo = input("Elige que tipo de configuracion quieres, codo 'arriba' o 'abajo': ").strip().lower()
    if codo not in ["arriba","abajo"]:
        print("ERROR: La configuración debe ser 'arriba' o 'abajo'.")
        return

# Preguntar cuales son los datos que se van a querer utilizar
    l1 = float(input("Longitud l1: "))
    l2 = float(input("Longitud l2: "))
    Xf = float(input("Posición Xf: "))
    Yf = float(input("Posición Yf: "))

# Calcular los angluos finales y si el resultado no es alcanzable mandar un mensaje diciendolo
    sol = cinematica_inversa(Xf, Yf, l1, l2, codo)
    if sol is None:
        print("Objetivo no alcanzable.")
        return

    theta1_final, theta2_final = sol
    print(f"theta1 = {np.degrees(theta1_final):.2f}°, theta2 = {np.degrees(theta2_final):.2f}°")

# Animacion del brazo
    theta1_init, theta2_init = 0.0, 0.0
    pasos = 100
    fig, ax = plt.subplots(figsize=(6,6))
    lim = l1 + l2 + 1

# Interpolacion de los angulos
    for n in range(pasos+1):
        t = n/pasos
        th1 = interp_angulo(theta1_init, theta1_final, t)
        th2 = interp_angulo(theta2_init, theta2_final, t)

# Dibujar todo
        ax.cla()
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.set_title(f"Animacion planar - codo {codo}")
        ax.set_xlabel("Y")
        ax.set_ylabel("X")
        dibujar_ejes(ax, l1+l2)
        ax.scatter([Xf],[Yf], color="red", s=60)

# Forzar efector final exacto en la última iteración
        ef_final = (Xf, Yf) if n == pasos else None
        dibujar_brazo(ax, th1, th2, l1, l2, efector_final=ef_final)

        plt.pause(0.03)

    plt.show()

# Ejecutar el programa
if __name__=="__main__":
   main()
