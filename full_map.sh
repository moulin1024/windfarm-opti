#!/bin/bash -l
#SBATCH --time 48:00:00
#SBATCH --exclusive 
#SBATCH --nodes 2
#This number is the number of jobs per nodes
# The real job array is this times the number of tasks per node
#SBATCH --array=1-32
total_job_num=32

module purge
module load intel
module load intel-mpi

ulimit -s unlimited
ulimit -c unlimited

echo "start: $(date)"
case_name=$1
search_type=$2
# Create case folder
if [[ ${CASE_ID} -eq 0 ]]
then
    mkdir ./case/${case_name}
    mkdir ./case/${case_name}/log
    mkdir ./case/${case_name}/plan
    cp -r ./config ./case/${case_name}
else
    echo ${CASE_ID}
fi

# python ./utils/preprocessing.py ${casename} ${total_job_num} 

./utils/grid_search.sh ${case_name} ${total_job_num} ${search_type}
