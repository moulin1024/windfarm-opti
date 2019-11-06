import numpy as np
import pandas as pd
import glob
import sys
import os
import re
iter_count = int(sys.argv[2])
case_name = str(sys.argv[1])
d_gamma = 5 # TODO: Hard-coded value!
alpha = 500 # TODO: Hard-coded value!

def get_power(job_name):
    os.chdir(os.environ["WIRELES"]+"/job/"+job_name+"/src/output/")
    power_df = pd.read_csv("power.out", header=None, sep='\s\s+', engine='python') 
    # Take the last 1/4 for averging
    data_array = power_df.iloc[power_df.shape[0]//2:power_df.shape[0]].mean().to_numpy()
    # Set to negative value for gradient descent
    total_power = -1*np.sum(data_array[0:power_df.shape[1]])
    return total_power 

os.chdir(os.environ["WIRELES"]+"/job")
case_list = glob.glob(case_name+"_"+str(iter_count)+"*")
grad_power = np.zeros(len(case_list)-1)

# Extracting base power
base_power = get_power(case_name+"_"+str(iter_count)+"_grad_0")

# Extracting gradient power, be careful with the 0-based index    
for case in case_list:
   index = int(re.findall(r'\d+', case)[-1])       # get the last number in the case name
   if index != 0:
       grad_power[index-1] = (get_power(case) - base_power)/d_gamma

os.chdir(sys.path[0])
# Extract the yaw angle in the previous step
yaw_angle_history = pd.read_csv('yaw_angle_history.csv', header=None).to_numpy()
yaw_angle = np.copy(yaw_angle_history[-1,:]) # last line
# Mask with the list of chosen wind turbine for optimization
opti_mask = pd.read_csv('opti_wt_list.csv', header=None).to_numpy()
# Gradient desent
yaw_angle[0:4] = yaw_angle[0:4]-10#grad_power*alpha
# Update and Overwrite the yaw_angle
updated_yaw_angle_history = np.vstack((yaw_angle_history,yaw_angle))
np.savetxt('yaw_angle_history.csv',updated_yaw_angle_history,delimiter=",")
# Update and Overwrite the power
power_history = pd.read_csv('power_history.csv', header=None).to_numpy()
updated_power = np.vstack((power_history,base_power))
np.savetxt('power_history.csv',updated_power,delimiter=",")

