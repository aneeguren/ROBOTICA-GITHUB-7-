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
    ax.plot3D(zp, y, zp, color='green',linewidth=linewidth)
    ax.plot3D(zp, zp, z, color='blue',linewidth=linewidth)

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

# DEFINIR LAS MATRICES QUE VOY A TENER QUE UTILIZAR LUEGO:
def TRy(t):
    Ry = np.array([[cosd(t), 0, sind(t), 0],
                   [0, 1, 0, 0],
                   [-sind(t), 0, cosd(t), 0],
                   [0, 0, 0, 1]])
    return Ry

def TRz(t):
    Rz = np.array([[cosd(t), -sind(t), 0, 0],
                   [sind(t),  cosd(t), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    return Rz

def TTx(L):
    Tx = np.array([[1, 0, 0, L],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    return Tx

def drawVector(p_fin, p_init=[0,0,0], color='black',linewidth=1):
    deltaX = [p_init[0], p_fin[0]]
    deltaY = [p_init[1], p_fin[1]]
    deltaZ = [p_init[2], p_fin[2]]
    ax.plot3D(deltaX, deltaY, deltaZ,color=color, linewidth=linewidth)

def getUnitaryVectorsFromMatrix(TM):
    x      = [TM[0][0], TM[1][0], TM[2][0]]
    y      = [TM[0][1], TM[1][1], TM[2][1]]
    z      = [TM[0][2], TM[1][2], TM[2][2]]
    origin = [TM[0][3], TM[1][3], TM[2][3]]
    return [x,y,z,origin]

def drawMobileFrame(origin, x, y, z):
    drawVector([origin[0]+x[0], origin[1]+x[1], origin[2]+x[2]], origin, "red")
    drawVector([origin[0]+y[0], origin[1]+y[1], origin[2]+y[2]], origin, "green")
    drawVector([origin[0]+z[0], origin[1]+z[1], origin[2]+z[2]], origin, "blue")

# DATOS:
beta_final = 30
theta1_final = 45
theta2_final = 30
theta3_final = 45
L1, L2, L3 = 10, 8, 6

# Set the view 
setaxis(-15,15,-15,15,-15,15)

# plot the axis
fix_system(10,linewidth=1)

#ANIMACION:
def animate_robot(steps=100):
    for n in range(steps+1):
        ax.cla()

        # Setear vista
        setaxis(-25, 25, -25, 25, -25, 25)

        # Dibujar ejes
        fix_system(10, 1)

        # Interpolation of joint angles
        beta   = beta_final   * n/steps
        theta1 = theta1_final * n/steps
        theta2 = theta2_final * n/steps
        theta3 = theta3_final * n/steps

        # Operation 1 - Rotate base Ry(beta)
        T1 = TRy(beta)
        [x1,y1,z1,origin1] = getUnitaryVectorsFromMatrix(T1)
        drawMobileFrame(origin1, x1, y1, z1)

        # Operation 2 - Rotate joint 1 Rz(theta1)
        T2 = T1.dot(TRz(theta1))
        [x2,y2,z2,origin2] = getUnitaryVectorsFromMatrix(T2)
        drawMobileFrame(origin2, x2, y2, z2)

        # Operation 3 - Translate along x (L1)
        T3 = T2.dot(TTx(L1))
        [x3,y3,z3,origin3] = getUnitaryVectorsFromMatrix(T3)
        drawMobileFrame(origin3, x3, y3, z3)
        drawVector(origin3, origin2, color="black", linewidth=3)

        # Operation 4 - Rotate joint 2 Rz(theta2)
        T4 = T3.dot(TRz(theta2))
        [x4,y4,z4,origin4] = getUnitaryVectorsFromMatrix(T4)
        drawMobileFrame(origin4, x4, y4, z4)

        # Operation 5 - Translate along x (L2)
        T5 = T4.dot(TTx(L2))
        [x5,y5,z5,origin5] = getUnitaryVectorsFromMatrix(T5)
        drawMobileFrame(origin5, x5, y5, z5)
        drawVector(origin5, origin3, color="black", linewidth=3)

        # Operation 6 - Rotate joint 3 Rz(theta3)
        T6 = T5.dot(TRz(theta3))
        [x6,y6,z6,origin6] = getUnitaryVectorsFromMatrix(T6)
        drawMobileFrame(origin6, x6, y6, z6)

        # Operation 7 - Translate along x (L3)
        T7 = T6.dot(TTx(L3))
        [x7,y7,z7,origin7] = getUnitaryVectorsFromMatrix(T7)
        drawMobileFrame(origin7, x7, y7, z7)
        drawVector(origin7, origin5, color="black", linewidth=3)

        # Plot joints
        ax.scatter([0, origin3[0], origin5[0], origin7[0]],
                   [0, origin3[1], origin5[1], origin7[1]],
                   [0, origin3[2], origin5[2], origin7[2]],
                   color="black", s=20)

        plt.draw()
        plt.pause(0.05)

# Run animation
animate_robot(100)
plt.show()
