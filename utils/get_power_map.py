import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import jobs
import scipy.ndimage as ndimage
#from jobs import get_power
#from jobs import get_gamma
power = np.zeros([32,32])
#thrust = np.zeros([32,32])
#tilt_torq = np.zeros([32,32])
#tilt_torq = 
# base_power = jobs.get_power('3wt-full-fine','0-0')
for i in range(0,32):
   print(i)
   for j in range(0,32):
       power[i,j] = jobs.get_power('3wt-wire01-3',str(i)+'-'+str(j))

#print(power.type)
#power = np.zeros([32,32])
#np.savetxt("foo.csv", power, delimiter=",")


  # X is an array
np.save('power_map.npy', np.asarray(power))
# print(power)
# power = (power - base_power)/(-base_power)
# initial = [0,0]
# p_history = initial[:]
# p_start = p_history[:]
# for i in range(0,6):
#     if i%2==0:
#         p_start[1] = np.argmax(-power[p_start[0],:])
#     else:
#         p_start[0] = np.argmax(-power[:,p_start[1]])
#     # print(p_start)
#     p_history = np.vstack((p_history, p_start))

# p_max = np.amax(-power)
# print(p_max)
# p_history2 = initial[:]
# p_start2 = p_history2[:]
# for i in range(0,6):
#     if i%2==0:
#         p_start2[0] = np.argmax(-power[:,p_start2[1]])
#     else:
#         p_start2[1] = np.argmax(-power[p_start2[0],:])
#     # print(p_start)
#     p_history2 = np.vstack((p_history2, p_start2))

# print(p_history[-1,:])

# print(get_power('3wt-full','12-7'))
# # point = [0,p2]
# # p3 = np.argmax(-power[:,p2])
# # print(p3)
# yaw = np.linspace(0,30,16)
# plt.contourf((-power+base_power)/-base_power,100)
# plt.axis('equal')
# # plt.plot(p_history[:,1],p_history[:,0])
# # plt.plot(p_history2[:,1],p_history2[:,0])
# plt.colorbar()
# plt.show()
