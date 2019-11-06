import os
import pandas as pd
import numpy as np
from jobs import Job
from io import StringIO
import time
import sys
from sklearn.utils.extmath import cartesian

# Preprocessing
case_name = str(sys.argv[1])
total_job_count = int(sys.argv[2])
iter_num = int(sys.argv[3])

max_yaw = -30
baseline_path = os.environ["WIRELES"]+"/case/"+case_name+"/config"
print(baseline_path)    
opti_mask = pd.read_csv(baseline_path+'/opti_wt_list.csv', header=None).to_numpy()

yaw_angle_history = pd.read_csv(baseline_path+'/yaw_angle_history.csv', header=None).to_numpy()
init_yaw_angle = yaw_angle_history[-1,:]
print("create yaw angle:",init_yaw_angle)

search_list = np.linspace(0,max_yaw,total_job_count)
# Create the base case: greedy search
if iter_num == 0: 
    search_list = np.linspace(0,max_yaw,total_job_count)
    for index,item in enumerate(search_list):
        yaw_angle = np.zeros(init_yaw_angle.shape)
        job_name = str(iter_num) + "-" + str(index)
        yaw_angle[opti_mask] = yaw_angle[opti_mask] + item
        base_job = Job(case_name,job_name,yaw_angle,baseline_path)
        base_job.create_old()
else:
    root_yaw = np.unique(init_yaw_angle[opti_mask]) 
    for i in range(0,2*size(root_yaw)):        
        search_list = np.linspace(root_yaw[i//2]-2,root_yaw[i//2]+2,total_job_count)
        search_list_nd = cartesian([search_list]*(root_yaw.size*2))  # Attension: here is * is not product, but repetition!

for index,item in enumerate(search_list):
    yaw_angle = np.zeros(init_yaw_angle.shape)
    job_name = str(iter_num) + "-" + str(index)
    for i in range(0,2**)
        yaw_angle[iter_num] = yaw_angle[iter_num] + item
    base_job = Job(case_name,job_name,yaw_angle,baseline_path)
    base_job.create_old()


