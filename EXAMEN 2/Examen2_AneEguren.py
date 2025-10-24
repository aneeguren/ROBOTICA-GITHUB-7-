import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# ------------------ Parámetros del robot ------------------
A1 = 715.0          # Longitud primer brazo (mm)
A2 = 850.0          # Longitud segundo brazo (mm)
BASE_HEIGHT = 776.0 # Altura del eje del primer brazo
BAR_MIN = 418.5     # Altura mínima permitida
BAR_MAX = 880.0     # Altura máxima permitida
R_PLATILLO = 100.0  # Radio del platillo
L_BAR_YELLOW = 318.5  # Longitud FIJA de la barra amarilla
BRAZO_OFFSET_Z = -40.0  # Desnivel del segundo brazo

# ------------------ Cinemática directa con matrices ------------------
def fkine(theta1, theta2, delta_z, theta3):
    """Cinemática directa: calcula las posiciones clave de los puntos del robot."""
    # Conversión a radianes
    t1 = np.deg2rad(theta1)
    t2 = np.deg2rad(theta2)
    t3 = np.deg2rad(theta3)

    # Base y eje del primer brazo
    p_base = np.array([0, 0, 0])
    p_eje = np.array([0, 0, BASE_HEIGHT])

    # Brazo 1 (azul)
    p1 = p_eje + np.array([A1 * np.cos(t1), A1 * np.sin(t1), 0])

    # Brazo 2 (cian)
    p2 = p1 + np.array([A2 * np.cos(t1 + t2), A2 * np.sin(t1 + t2), BRAZO_OFFSET_Z])

    # --- Barra amarilla ---
    p_barra_bottom = np.array([p2[0], p2[1], BAR_MIN + delta_z])
    p_barra_top = p_barra_bottom + np.array([0, 0, L_BAR_YELLOW])

    # --- Platillo verde ---
    p_platillo = p_barra_bottom.copy()  # Usamos p_barra_bottom como la base para el platillo
    angs = np.linspace(0, 2 * np.pi, 60)
    circ_x = p_platillo[0] + R_PLATILLO * np.cos(angs + t3)
    circ_y = p_platillo[1] + R_PLATILLO * np.sin(angs + t3)
    circ_z = np.ones_like(circ_x) * p_platillo[2]

    # Punto rojo de la rotación
    punto_x = p_platillo[0] + R_PLATILLO * np.cos(t3)
    punto_y = p_platillo[1] + R_PLATILLO * np.sin(t3)
    punto_z = p_platillo[2]

    return p_base, p_eje, p1, p2, p_barra_bottom, p_barra_top, circ_x, circ_y, circ_z, punto_x, punto_y, punto_z

# ------------------ Dibujo del robot ------------------
def dibujar_robot(ax, p_base, p_eje, p1, p2, p_barra_bottom, p_barra_top, circ_x, circ_y, circ_z, punto_x, punto_y, punto_z):
    # Base
    ax.scatter(*p_base, color='red', s=60)
    ax.plot([p_base[0], p_eje[0]], [p_base[1], p_eje[1]], 
            [p_base[2], p_eje[2]], color='red', linewidth=3)

    # Brazos
    ax.plot([p_eje[0], p1[0]], [p_eje[1], p1[1]], 
            [p_eje[2], p1[2]], color='blue', linewidth=5)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 
            [p1[2], p2[2]], color='cyan', linewidth=5)

    # Barra amarilla
    ax.plot([p_barra_bottom[0], p_barra_top[0]], 
            [p_barra_bottom[1], p_barra_top[1]], 
            [p_barra_bottom[2], p_barra_top[2]], 
            color='orange', linewidth=4)

    # Platillo verde + punto rojo
    ax.plot(circ_x, circ_y, circ_z, color='green', linewidth=3)
    ax.scatter(punto_x, punto_y, punto_z, color='red', s=40)

# ------------------ Animación ------------------
def animar_robot(theta1_f, theta2_f, l1_f, theta3_f, frames=200):
    # Limitar el valor de l1_f para que se mantenga dentro de los límites
    l1_f = np.clip(l1_f, 0, L_BAR_YELLOW)

    # Estados iniciales
    theta1_i, theta2_i, dz_i, theta3_i = 0, 0, 0, 0

    # Interpolación de los parámetros
    t1_vals = np.linspace(theta1_i, theta1_f, frames)
    t2_vals = np.linspace(theta2_i, theta2_f, frames)
    dz_vals = np.linspace(dz_i, l1_f, frames)
    t3_vals = np.linspace(theta3_i, theta3_f, frames)

    # Crear la figura para la animación
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    lim = 1600
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(0, 1600)
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title("Animación Robot SCARA i4-850H")
    ax.view_init(elev=25, azim=45)

    def update(i):
        ax.cla()
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_zlim(0, 1600)
        ax.set_xlabel('X (mm)')
        ax.set_ylabel('Y (mm)')
        ax.set_zlabel('Z (mm)')
        ax.set_title("Animación Robot SCARA i4-850H")
        ax.view_init(elev=25, azim=45)

        # Calculando la posición del robot
        p_base, p_eje, p1, p2, p_barra_bottom, p_barra_top, circ_x, circ_y, circ_z, punto_x, punto_y, punto_z = fkine(
            t1_vals[i], t2_vals[i], dz_vals[i], t3_vals[i]
        )
        dibujar_robot(ax, p_base, p_eje, p1, p2, p_barra_bottom, p_barra_top, circ_x, circ_y, circ_z, punto_x, punto_y, punto_z)
        return []

    ani = animation.FuncAnimation(fig, update, frames=frames,
                                  interval=40, blit=False, repeat=False)
    plt.show()

# ------------------ Programa principal ------------------
if __name__ == "__main__":
    print("=== Animación Robot SCARA i4-850H ===")
    # Pedir las entradas antes de la animación
    theta1 = float(input("Introduce θ1 (brazo 1, grados): "))
    theta2 = float(input("Introduce θ2 (brazo 2, grados): "))
    l1 = float(input(f"Introduce l1 (distancia de subida de la barra, mm) [0–{L_BAR_YELLOW}]: "))
    theta3 = float(input("Introduce θ3 (rotación platillo, grados): "))

    # Ejecutar la animación con los valores dados
    animar_robot(theta1, theta2, l1, theta3)
