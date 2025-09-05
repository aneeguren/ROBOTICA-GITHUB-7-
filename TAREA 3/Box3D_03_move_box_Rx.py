# Import libraries and packages
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

# create the fig and ax objects to handle figure and axes of the fixed frame
fig,ax = plt.subplots()

# Use 3d view 
ax = plt.axes(projection = "3d")



def setaxis(x1, x2, y1, y2, z1, z2):
    # this function is used to fix the view to the values of input arguments
    # -----------------------------------------------------------------------
    # ARGUMENTS
    # x1, x2 -> numeric value
    # y1, y2 -> numeric value
    # y1, z2 -> numeric value
    # -----------------------------------------------------------------------
    ax.set_xlim3d(x1,x2)
    ax.set_ylim3d(y1,y2)
    ax.set_zlim3d(z1,z2)
    ax.view_init(elev=30, azim=40)


def fix_system(axis_length, linewidth=5):
    # Fix system function 
    # Plots a 3D centered at [x,y,z] = [0,0,0]
    # -------------------------------------------------------------------
    # Arguments 
    # axis_length -> used to specify the length of the axis, in this case
    #                all axes are of the same length
    # -------------------------------------------------------------------
    x = [-axis_length, axis_length]
    y = [-axis_length, axis_length] 
    z = [-axis_length, axis_length]
    zp = [0, 0]
    ax.plot3D(x, zp, zp, color='red', linewidth=linewidth)
    ax.plot3D(zp, y, zp, color='blue',linewidth=linewidth)
    ax.plot3D(zp, zp, z, color='green',linewidth=linewidth)
    

def sind(t):
    # sind function
    # Computes the sin() trigonometric function in degrees
    # ----------------------------------------------------------------------
    # Arguments
    # t -> Numeric, angle in degrees. 
    # ----------------------------------------------------------------------
    res = np.sin(t*np.pi/180)
    return res

def cosd(t):
    # sind function
    # Computes the cos() trigonometric function in degrees
    # ----------------------------------------------------------------------
    # Arguments
    # t -> Numeric, angle in degrees. 
    # ----------------------------------------------------------------------
    res = np.cos(t*np.pi/180)
    return res


def RotX(t):
    Rx = np.array(([1,0,0],[0,cosd(t),-sind(t)],[0,sind(t),cosd(t)]))
    return Rx

def drawVector(p_fin, p_init=[0,0,0], color='black',linewidth=1):
    deltaX = [p_init[0], p_fin[0]]
    deltaY = [p_init[1], p_fin[1]]
    deltaZ = [p_init[2], p_fin[2]]
    ax.plot3D(deltaX, deltaY, deltaZ,color=color, linewidth=linewidth)



def drawBox(p1, p2, p3, p4, p5, p6, p7, p8, color = 'black'):

    drawScatter(p1)
    drawScatter(p2)
    drawScatter(p3)
    drawScatter(p4)
    drawScatter(p5)
    drawScatter(p6)
    drawScatter(p7)
    drawScatter(p8)

    drawVector(p1,p2,color = color)
    drawVector(p2,p3,color = color)
    drawVector(p3,p4,color = color)
    drawVector(p4,p1,color = color)
    drawVector(p5,p6,color = color)
    drawVector(p6,p7,color = color)
    drawVector(p7,p8,color = color)
    drawVector(p8,p5,color = color)
    drawVector(p4,p8,color = color)
    drawVector(p1,p5,color = color)
    drawVector(p3,p7,color = color)
    drawVector(p2,p6,color = color)


def drawScatter(point,color='black',marker='o'):
    ax.scatter(point[0],point[1],point[2],marker='o')

def rotate_box(p1,p2,p3,p4,p5,p6,p7,p8,axis='x', angle = 0):
    rotation_matrix = np.eye(3)
    if axis=='x':
        rotation_matrix = RotX(angle)
    if axis=='y':
        pass 
    if axis=='z':
        pass

    p1_rot = rotation_matrix.dot(p1)
    p2_rot = rotation_matrix.dot(p2)
    p3_rot = rotation_matrix.dot(p3)
    p4_rot = rotation_matrix.dot(p4)
    p5_rot = rotation_matrix.dot(p5)
    p6_rot = rotation_matrix.dot(p6)
    p7_rot = rotation_matrix.dot(p7)
    p8_rot = rotation_matrix.dot(p8)

    return [p1_rot,p2_rot, p3_rot, p4_rot, p5_rot, p6_rot, p7_rot, p8_rot]



    
# Set the view 
setaxis(-15,15,-15,15,-15,15)

# plot the axis
fix_system(10,1)

p1_init = [0,0,0]
p2_init = [7,0,0]
p3_init = [7,0,3]
p4_init = [0,0,3]
p5_init = [0,2,0]
p6_init = [7,2,0]
p7_init = [7,2,3]
p8_init = [0,2,3]


drawBox(p1_init, p2_init, p3_init, p4_init,
        p5_init, p6_init, p7_init, p8_init)

[p1_rot, p2_rot, p3_rot, p4_rot, p5_rot, p6_rot, p7_rot, p8_rot] = rotate_box(p1_init, p2_init, p3_init, p4_init,
        p5_init, p6_init, p7_init, p8_init,axis='z', angle = 15) 



drawBox(p1_rot, p2_rot, p3_rot, p4_rot, p5_rot, p6_rot, p7_rot, p8_rot,color='red')


def animate_box_x(t):
    n = 0  # condición inicial
    while n < t: 
        ax.cla()  # limpiar pantalla

        # Setear vista
        setaxis(-15, 15, -15, 15, -15, 15)

        # Dibujar ejes
        fix_system(10, 1)

        # --- Traslación en eje X ---
        translation = np.array([n * 0.1, 0, 0])  # avanza en X

        # Trasladar los puntos de la caja
        p1_trans = np.array(p1_init) + translation
        p2_trans = np.array(p2_init) + translation
        p3_trans = np.array(p3_init) + translation
        p4_trans = np.array(p4_init) + translation
        p5_trans = np.array(p5_init) + translation
        p6_trans = np.array(p6_init) + translation
        p7_trans = np.array(p7_init) + translation
        p8_trans = np.array(p8_init) + translation

        # Dibujar la caja trasladada
        drawBox(p1_trans, p2_trans, p3_trans, p4_trans,
                p5_trans, p6_trans, p7_trans, p8_trans, color="red")

        n = n + 1
        plt.draw()
        plt.pause(0.05)  

# Ejecutar animación: trasladar en X
animate_box_x(90) 

# Mostrar figura
plt.draw()
plt.show()



