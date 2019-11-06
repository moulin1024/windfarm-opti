import os
import pandas as pd
import numpy as np
from jobs import Job
from io import StringIO
import derivative as de
import time
import sys
# Preprocessing
baseline_path = "/scratch/molin/optimization/config"    
content = np.genfromtxt(baseline_path+'/opti_wt_list.csv', delimiter=',')
if content.size == 1:
	opti_wt_list = np.asarray(list([[content]]))
else:
	opti_wt_list = np.asarray(list([content]))

d_gamma = 2
print(opti_wt_list)
yaw_angle_history = pd.read_csv(baseline_path+'/yaw_angle_history.csv', header=None).to_numpy()
yaw_angle = yaw_angle_history[-1,:]
print("create yaw angle:",yaw_angle)
iter_num = int(sys.argv[2])
case_name = str(sys.argv[1])

# Create the base case
base_job_name = case_name +"_" + str(iter_num) + "base"
base_job = Job(case_name,base_job_name,yaw_angle,baseline_path)
base_job.create_old()
# Create the gradient case
de.create_jobs_for_hessian(base_job,iter_num,opti_wt_list)
