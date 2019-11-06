import numpy as np
from jobs import Job
from abc import ABC, abstractmethod
from itertools import combinations_with_replacement


class AbstractDerivative:
    def __init__(self,x,dx,axis):
        self.x = x
        self.dx = dx
        self.axis = axis
    @abstractmethod    
    def create_plan(self):
        pass

class Dx(AbstractDerivative):
    def __init__(self,x,dx,axis):
        super().__init__(x,dx,axis)
        self.x_prime = np.zeros(1,self.x.size)
    def create_plan(self):
        self.x_prime[0,self.axis[0]] = self.x[0,self.axis[0]] - self.dx

class DxDx(AbstractDerivative):
    def __init__(self,x,dx,axis):
        super().__init__(x,dx,axis)
        self.x_prime = np.repeat([self.x],2,axis=0)
    def create_plan(self):
        self.x_prime[0,self.axis[0]] = self.x[self.axis[0]] - self.dx
        self.x_prime[1,self.axis[0]] = self.x[self.axis[0]] + self.dx
        
class DxDy(AbstractDerivative):
    def __init__(self,x,dx,axis):
        super().__init__(x,dx,axis)
        self.x_prime = np.repeat([self.x],4,axis=0)
    def create_plan(self):
        self.x_prime[0,[self.axis[0],self.axis[1]]] = self.x[[self.axis[0],self.axis[1]]] + [-self.dx,-self.dx]
        self.x_prime[1,[self.axis[0],self.axis[1]]] = self.x[[self.axis[0],self.axis[1]]] + [-self.dx,self.dx]
        self.x_prime[2,[self.axis[0],self.axis[1]]] = self.x[[self.axis[0],self.axis[1]]] + [self.dx,-self.dx]
        self.x_prime[3,[self.axis[0],self.axis[1]]] = self.x[[self.axis[0],self.axis[1]]] + [self.dx,self.dx]       

def create_jobs_for_hessian(base_job,iter_num,opti_wt_list):
    axis_list = combinations_with_replacement(list(opti_wt_list[0]), 2)
    case_list = []
    for axis in axis_list:
        axis = [int(i) for i in axis]
        if axis[0] == axis[1]:
            hessian_job = DxDx(base_job.yaw_angle,base_job.d_gamma,axis)
            hessian_job.create_plan()
            for i in range(2):
                job_name = str(iter_num) + "-d" + str(axis[0])+"d" + str(axis[1])+"-"+str(i) 
                case_list.append(job_name)
                job_yaw_angle = hessian_job.x_prime[i,:]
                job = Job(base_job.case,job_name,job_yaw_angle,base_job.config_path)
                job.create_old()
        else:
            hessian_job = DxDy(base_job.yaw_angle,base_job.d_gamma,axis)
            hessian_job.create_plan()
            for i in range(4):
                case_list.append(job_name)
                job_name = str(iter_num) + "-d" + str(axis[0])+"d" + str(axis[1])+"-"+str(i) 
                job_yaw_angle = hessian_job.x_prime[i,:]
                job = Job(base_job.case,job_name,job_yaw_angle,base_job.config_path)
                job.create_old()

def create_jobs_for_grad(base_job,iter_num,opti_wt_list):
    axis_list = combinations_with_replacement(list(opti_wt_list[0]), 2)
    case_list = []
    for axis in axis_list:
        axis = [int(i) for i in axis]
        if axis[0] == axis[1]:
            hessian_job = DxDx(base_job.yaw_angle,base_job.d_gamma,axis)
            hessian_job.create_plan()
            for i in range(2):
                job_name = str(iter_num) + "-d" + str(axis[0])+"d" + str(axis[1])+"-"+str(i) 
                case_list.append(job_name)
                job_yaw_angle = hessian_job.x_prime[i,:]
                job = Job(base_job.case,job_name,job_yaw_angle,base_job.config_path)
                job.create_old()
        else:
            hessian_job = DxDy(base_job.yaw_angle,base_job.d_gamma,axis)
            hessian_job.create_plan()
            for i in range(4):
                case_list.append(job_name)
                job_name = str(iter_num) + "-d" + str(axis[0])+"d" + str(axis[1])+"-"+str(i) 
                job_yaw_angle = hessian_job.x_prime[i,:]
                job = Job(base_job.case,job_name,job_yaw_angle,base_job.config_path)
                job.create_old()