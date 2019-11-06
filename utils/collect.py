import numpy as np
import pandas as pd
import glob
import sys
import os
import re
from jobs import get_power
case_name = str(sys.argv[1])
iter_num = int(sys.argv[2])

# print(get_power("test","0-0"))

os.chdir(os.environ["WIRELES"]+"/case/"+case_name)
job_list = glob.glob("*-*")
power_list = np.zeros(len(job_list))

# Extracting power from different case   
for idx,item in enumerate(job_list):
    iter_count = int(re.findall(r'\d+', item)[0])       # get the first number in the case name
    if iter_count == iter_num:
        power_list[idx] = get_power(case_name,item)

max_power = np.amin(power_list)
max_idx = np.where(power_list == max_power)
listOfCordinates = list(max_idx[0])
max_case = job_list[listOfCordinates[0]]

# Get yaw angle
wind_df = pd.read_csv(os.environ["WIRELES"]+"/case/"+case_name+"/"+max_case+"/src/input/windfarm.csv")
max_yaw_angle = wind_df["gamma"].to_numpy()
print(job_list)

os.chdir(os.environ["WIRELES"]+"/case/"+case_name+"/config")
# Extract the yaw angle in the previous step
yaw_angle_history = pd.read_csv('yaw_angle_history.csv', header=None).to_numpy()
# Update and Overwrite the yaw_angle
updated_yaw_angle_history = np.vstack((yaw_angle_history,max_yaw_angle))
np.savetxt('yaw_angle_history.csv',updated_yaw_angle_history,delimiter=",")
# Update and Overwrite the power
power_history = pd.read_csv('power_history.csv', header=None).to_numpy()
updated_power = np.vstack((power_history,max_power))
np.savetxt('power_history.csv',updated_power,delimiter=",")

