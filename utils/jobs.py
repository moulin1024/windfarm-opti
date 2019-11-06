import os
import numpy as np
import pandas as pd
import time

class Job:
    def __init__(self,case,job,yaw_angle,config_path):
        self.finish_flag = 0
        self.iter = 0
        self.case = case
        self.job = job
        self.yaw_angle = yaw_angle
        self.config_path = config_path
        self.d_gamma=2
        
    def create(self):
    # --------------------------------------------------#
    # Create cases 
    # --------------------------------------------------#
        # Change to the wireles folder
        os.chdir(os.environ["WIRELES"])
        # Create the case folder
        os.system("python prc/wireles.py create " + self.job + "> opti_log" + self.job + ".txt")
        # Copy the config file to the case folder
        os.system("cp " + self.config_path +"/config " + os.environ["WIRELES"]+"/case/"+self.job+"/input")
        # Preprocessing the case
        os.system("python prc/wireles.py pre " + self.job + " >> opti_log" + self.job + ".txt")

        # Write the windfarm csv file and airfoil data to case/src/input
        wind_df = pd.read_csv(self.config_path +"/windfarm.csv")
        wind_df["gamma"] = self.yaw_angle
        wind_df.to_csv(os.environ["WIRELES"]+"/case/"+self.job+"/src/input/windfarm.csv",index=False)
        os.system("cp " + self.config_path +"/cl_cd.dat " + os.environ["WIRELES"]+"/case/"+self.job+"/src/input")
        return

    def create_old(self):
    # --------------------------------------------------#
    # Create cases 
    # --------------------------------------------------#
        # Change to the wireles folder
        os.chdir(os.environ["WIRELES"])
        # Create the case folder
        print(os.environ["WIRELES"]+"/case/"+self.case+"/"+self.job+"/")
        os.system("cp"+ " -r " +"solver " + os.environ["WIRELES"]+"/case/"+self.case+"/"+self.job+"/")
        # Preprocessing the case
        os.chdir(os.environ["WIRELES"] + "/case/" +self.case+"/"+ self.job)
        os.system("python parameter.py")
        os.chdir("src/")
        os.system("./config.sh")
        # Write the windfarm csv file and airfoil data to case/src/input
        wind_df = pd.read_csv(self.config_path +"/windfarm.csv")
        wind_df["gamma"] = self.yaw_angle
        wind_df.to_csv(os.environ["WIRELES"]+"/case/"+self.case+"/"+self.job+"/src/input/windfarm.csv",index=False)
        os.system("cp " + self.config_path +"/cl_cd.dat " + os.environ["WIRELES"]+"/case/"+self.case+"/"+self.job+"/src/input")
        return


def get_power(case_name,job_name):
    power_df = pd.read_csv(os.environ["WIRELES"]+"/case/"+case_name+"/"+job_name+"/src/output/power.out", 
                            header=None, sep='\s\s+', engine='python') 
    # Take the last 3/4 for averging
    data_array = power_df.iloc[power_df.shape[0]//4:power_df.shape[0]].mean().to_numpy()
    # Set to negative value for gradient descent
    total_power = -1*np.sum(data_array[0:power_df.shape[1]])
    return total_power 

def get_force(case_name,job_name):
    power_df = pd.read_csv(os.environ["WIRELES"]+"/case/"+case_name+"/"+job_name+"/src/output/power.out", 
                            header=None, sep='\s\s+', engine='python') 
    # Take the last 3/4 for averging
    data_array = power_df.iloc[power_df.shape[0]//4:power_df.shape[0]].mean().to_numpy()
    # Set to negative value for gradient descent
    total_thrust = -1*np.sum(data_array[0:power_df.shape[1]//3])
    total_tilt_torque = -1*np.sum(data_array[power_df.shape[1]//3:2*power_df.shape[1]//3])
    total_yaw_torque = -1*np.sum(data_array[2*power_df.shape[1]//3:3*power_df.shape[1]//3])
    
    return total_thrust,total_tilt_torque,total_yaw_torque


def get_gamma(case_name):
    os.chdir(os.environ["WIRELES"]+"/case/"+case_name+"/config")
    gamma_df = pd.read_csv("yaw_angle_history.csv", header=None) 
    # Take the last 1/4 for averging
    gamma_array = gamma_df.to_numpy()
    return gamma_array 