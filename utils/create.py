import os
import pandas as pd
import numpy as np
from jobs import Job
from io import StringIO
import time
import sys
# Preprocessing
baseline_path = "/scratch/molin/wireles/utils/optimization"    
content = np.genfromtxt('opti_wt_list.csv', delimiter=',')
if content.size == 1:
	opti_wt_list = np.asarray(list([[content]]))
else:
	opti_wt_list = np.asarray(list([content]))

d_gamma = 5
print(opti_wt_list)
yaw_angle_history = pd.read_csv('yaw_angle_history.csv', header=None).to_numpy()
yaw_angle = yaw_angle_history[-1,:]
print("create yaw angle:",yaw_angle)
iter_count = int(sys.argv[2])
case_name = str(sys.argv[1])

# Create the base case
base_job_name = case_name +"_" + str(iter_count) + "_grad_0"
base_job = Job(base_job_name,yaw_angle,baseline_path)
base_job.create()
# Create the gradient case
for index,item in enumerate(opti_wt_list[0,:]):
    grad_job_name = case_name +"_" + str(iter_count) + "_grad_" + str(index+1)
    grad_yaw_angle = np.asarray(list(yaw_angle))
    grad_yaw_angle[int(item)] = yaw_angle[int(item)] + d_gamma
    grad_job = Job(grad_job_name,grad_yaw_angle,baseline_path)
    grad_job.create()
    print(grad_job_name)


