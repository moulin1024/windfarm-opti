from abc import ABC, abstractmethod

class AbstractPlan(ABC):
    def __init__(self,wt_list,max_yaw,total_job_num):
        self.plan = []
        self.max_yaw = max_yaw
        self.total_job_num = total_job_num
    @abstractmethod
    def create_plan(self):
        pass

class Greedy(AbstractPlan):
    def create_plan(self):
        for idx,item in enumerate(self.wt_list):
            
    


search_list = np.linspace(0,max_yaw,total_job_count)
# Create the base case: greedy search
for index,item in enumerate(search_list):
    yaw_angle = np.zeros(init_yaw_angle.shape)
    job_name = str(iter_num) + "-" + str(index)
    yaw_angle[0:5-iter_num] = yaw_angle[0:5-iter_num] + item
    base_job = Job(case_name,job_name,yaw_angle,baseline_path)
    base_job.create_old()



# class InverseGreedy():

# class BinarySearch():
