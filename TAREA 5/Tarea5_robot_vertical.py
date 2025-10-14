import numpy as np
import matplotlib.pyplot as plt

# --- Cálculo de la posición del robot ---
def pos_robot(ang1, ang2, l1, l2):
    """Calcula la posición del robot de 2 eslabones en 3D (plano XZ)."""
    
    # Punto base
    origen = np.array([0, 0, 0])
    
    # Primer articulación
    p1 = np.array([
        l1 * np.sin(ang1),
        0,
        l1 * np.cos(ang1)
    ])
    
    # Posición del efector final
    p2 = p1 + np.array([
        l2 * np.sin(ang1 + ang2),
        0,
        l2 * np.cos(ang1 + ang2)
    ])
    
    return origen, p1, p2


# --- Dibujo del robot ---
def mostrar_robot(ax, base, junta1, efector):
    """Dibuja el robot articulado en el espacio 3D."""
    X = [base[0], junta1[0], efector[0]]
    Y = [base[1], junta1[1], efector[1]]
    Z = [base[2], junta1[2], efector[2]]

    ax.plot(X, Y, Z, 'o-', color='navy', linewidth=3)
    ax.scatter(X, Y, Z, color='crimson', s=45)


# --- Simulación y animación ---
def simular_movimiento(dest1, dest2, l1, l2):
    """Genera la animación del robot moviéndose entre los ángulos indicados."""
    frames = 80
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for paso in range(frames + 1):
        ax.cla()

        # Ajustes del gráfico
        ax.set_xlim(-l1 - l2, l1 + l2)
        ax.set_ylim(-l1 - l2, l1 + l2)
        ax.set_zlim(0, l1 + l2)
        ax.set_xlabel('Eje X')
        ax.set_ylabel('Eje Y')
        ax.set_zlabel('Eje Z')
        ax.view_init(elev=25, azim=40)
        ax.set_title("Simulación 3D: Robot de 2 eslabones (Plano XZ)")

        # Interpolación del movimiento angular
        t = paso / frames
        a1 = np.deg2rad(dest1 * t)
        a2 = np.deg2rad(dest2 * t)

        base, j1, ef = pos_robot(a1, a2, l1, l2)
        mostrar_robot(ax, base, j1, ef)

        plt.pause(0.05)

    plt.show()


# --- Programa principal ---
if __name__ == "__main__":
    print("=== Simulación de Cinemática Directa 3D ===")
    
    l1 = float(input("Introduce la longitud del primer eslabón (L1): "))
    l2 = float(input("Introduce la longitud del segundo eslabón (L2): "))
    ang1 = float(input("Introduce el ángulo θ1 (grados): "))
    ang2 = float(input("Introduce el ángulo θ2 (grados): "))

    simular_movimiento(ang1, ang2, l1, l2)
