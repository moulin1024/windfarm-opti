import numpy as np
import pandas as pd
import glob
import sys
import os
import re
import jobs
case_name = str(sys.argv[1])
job_name = str(sys.argv[2])

print(jobs.get_power(case_name,job_name))
#print(jobs.get_gamma(case_name))
