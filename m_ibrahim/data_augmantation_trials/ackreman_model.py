import numpy as np
import matplotlib.pyplot as plt

deg_to_rad = np.pi/180.
rad_to_deg = 180./np.pi
steer_ratio = 14.8  
wheel_base = 2.85  


dt = 2 # sec
v = 5 # m/s 
steps = 2 
steering_angle = 9.4 # deg
wheel_angle = steering_angle * deg_to_rad / steer_ratio
x = [0]
y = [0]
phi = [(np.pi/2.0)]

for step in range(1,steps+1):
	x_new = x[-1]+ (v*dt*np.cos(phi[-1]+wheel_angle))
	y_new = y[-1]+ (v*dt*np.sin(phi[-1]+wheel_angle))
	phi_new = phi[-1]+ (v*dt*np.sin(wheel_angle)/wheel_base)
	x.append(x_new)
	y.append(y_new)
	phi.append(phi_new)

print np.array(phi)*rad_to_deg
print x , y 
plt.plot(x,y)
plt.quiver(x, y, np.cos(phi), np.sin(phi), 
           color='Teal', 
           headlength=7)

plt.title('ackreman steering model ')
plt.show()