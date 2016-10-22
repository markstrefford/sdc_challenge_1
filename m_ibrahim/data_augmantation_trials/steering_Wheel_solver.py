import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

deg_to_rad = np.pi/180.
rad_to_deg = 180./np.pi
steer_ratio = 14.8  
wheel_base = 2.85  
dt = 1.5 # sec
v = 5. # m/s 
phi_o = np.pi/2.
dx = -0.5

def F(x):
    return (v*dt/wheel_base)*np.sin(x) + x + phi_o - np.arccos(dx / (v*dt))

wheel_angle = scipy.optimize.broyden1(F, [0.1], f_tol=1e-5)
steering_angle = steer_ratio * wheel_angle 
print wheel_angle, steering_angle , steering_angle* rad_to_deg

x = [0]
y = [0]
phi = [phi_o]

steps = 2
small_dt = dt
for step in range(1,steps+1):
	x_new = x[-1]+ (v*small_dt*np.cos(phi[-1]+wheel_angle[0]))
	y_new = y[-1]+ (v*small_dt*np.sin(phi[-1]+wheel_angle[0]))
	phi_new = phi[-1]+ (v*small_dt*np.sin(wheel_angle[0])/wheel_base)
	x.append(x_new)
	y.append(y_new)
	phi.append(phi_new)

print np.array(phi)*rad_to_deg
print x 
print y
plt.plot(x,y)
plt.quiver(x, y, np.cos(phi), np.sin(phi), 
           color='Teal', 
           headlength=7)
plt.title('vehicle shift correction')
plt.xlim([-10,10])
plt.ylim([-10,20])
plt.show()