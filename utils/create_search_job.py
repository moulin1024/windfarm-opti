import os
import pandas as pd
import numpy as np
from jobs import Job
from io import StringIO
import time
import sys
# Preprocessing
case_name = str(sys.argv[1])
total_job_count = int(sys.argv[2])
iter_num = int(sys.argv[3])
search_type = int(sys.argv[4])

max_yaw = -31
baseline_path = os.environ["WIRELES"]+"/case/"+case_name+"/config"
print(baseline_path)    
opti_mask = pd.read_csv(baseline_path+'/opti_wt_list.csv', header=None).to_numpy()

yaw_angle_history = pd.read_csv(baseline_path+'/yaw_angle_history.csv', header=None).to_numpy()
init_yaw_angle = yaw_angle_history[-1,:]
print("create yaw angle:",init_yaw_angle)
yaw_angle = np.zeros(init_yaw_angle.shape)
if search_type == 1:
    search_list = np.linspace(0,max_yaw,total_job_count)
    # Create the base case: greedy search
    for index,item in enumerate(search_list):
        yaw_angle[:] = init_yaw_angle[:]
        job_name = str(iter_num) + "-" + str(index)
        yaw_angle[iter_num%opti_mask.size] = item
        base_job = Job(case_name,job_name,yaw_angle,baseline_path)
        base_job.create_old()
elif search_type == 2:
    search_list = np.linspace(0,max_yaw,total_job_count)
    # Create the base case: greedy search
    for index,item in enumerate(search_list):
        yaw_angle[:] = init_yaw_angle[:]
        job_name = str(iter_num) + "-" + str(index)
        yaw_angle[opti_mask.size-iter_num%opti_mask.size-1] = item
        base_job = Job(case_name,job_name,yaw_angle,baseline_path)
        base_job.create_old()
elif search_type == 3:
    search_list = np.linspace(0,max_yaw,total_job_count)
    # Create case for 2-wt full search
    for index,item in enumerate(search_list):
        yaw_angle[:] = init_yaw_angle[:]
        job_name = str(iter_num) + "-" + str(index)
        yaw_angle[0] = -iter_num
        yaw_angle[1] = item
        base_job = Job(case_name,job_name,yaw_angle,baseline_path)
        base_job.create_old()
