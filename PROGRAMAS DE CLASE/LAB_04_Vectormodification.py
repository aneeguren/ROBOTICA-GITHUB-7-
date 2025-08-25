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


def fix_system(axis_length):
    # Fix system function 
    # Plots a 3D centered at [x,y,z] = [0,0,0]
    # -------------------------------------------------------------------
    # Arguments 
    # axis_length -> used to specify the length of the axis, in this case
    #                all axes are of the same length
    # -------------------------------------------------------------------
    x = [0, axis_length]
    y = [0, axis_length] 
    z = [0, axis_length]
    zp = [0, 0]
    ax.plot3D(x, zp, zp, color='red', linewidth=5) #linewidth es para hacer las lineas mas gruesas
    ax.plot3D(zp, y, zp, color='blue',linewidth=5)
    ax.plot3D(zp, zp, z, color='green',linewidth=5)
    

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


def RotZ(t):
    Rz = np.array(([cosd(t),-sind(t),0],[sind(t),cosd(t),0],[0,0,1]))
    return Rz

def drawVector(p_fin, p_init=[0,0,0], color='black',linewidth=1): #p_fin es el puto final, p_init es el punto inicial, luego el color y luego el ancho d linea
    deltaX = [p_init[0], p_fin[0]] #se coge el componente x del p_init, el cual se ha puesto en la linea anterior
    deltaY = [p_init[1], p_fin[1]] #se coge el componente y del p_init,  el cual se ha puesto dos lineas antes
    deltaZ = [p_init[2], p_fin[2]] #se coge el componente z del p_init, el cual se ha puesto tres lineas antes
    ax.plot3D(deltaX, deltaY, deltaZ,color=color, linewidth=linewidth)


# Set the view 
setaxis(0,2,0,2,0,2)

# plot the axis
fix_system(1)

# draw vector1
v1 = np.array([2,0,0])
drawVector(v1)

# draw vector2
v2 = RotZ(45).dot(v1) #v2 es el mismo vector q v1 pero rotau 45º
drawVector(v2,color="orange")

v2 = RotZ(45).dot(v2) #se crea un vector nuevo tambien llamado v2, es como se redibuja en la posicion nueva, pero el otro vector no se borra, va a haber dos
drawVector(v2,linewidth=4)

v3 = (RotZ(35).dot(RotZ(20))).dot(v1) #se rota el v1, pero el 35 y el 20 se suman, porq son rotaciones en el mismo eje, se redibuja
drawVector(v3,color="orange", linewidth=4)

v4 = (RotZ(15).dot(RotZ(10))).dot(v1)
drawVector(v4,color=(0.5, 0.5, 0.5), linewidth=4) #define el color en rgb, q es lo de los 0.5s.





# show image.
plt.draw()
plt.show()


