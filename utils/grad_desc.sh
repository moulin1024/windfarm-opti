#!/bin/bash -l
#SBATCH --time 04:00:00
#SBATCH --nodes 2
#This number is the number of jobs per nodes
# The real job array is this times the number of tasks per node
#SBATCH --array=1-32

module purge
module load intel
module load intel-mpi

ulimit -s unlimited
ulimit -c unlimited

echo "start: $(date)"

CASE_ID=$(( ( ${SLURM_ARRAY_TASK_ID} - 1 ) ))
echo "Case ${CASE_ID}"
case_name=$1
iter_count=0
for iter_count in {0..3}
do
    if [[ ${CASE_ID} -eq 0 ]]
    then
        python create.py ${case_name} ${iter_count}
    else
        echo "Pausing until case exists:"
        while : ; do
            [[ -f ${WIRELES}/job/${case_name}_${iter_count}_grad_${CASE_ID}/src/input/cl_cd.dat ]] && break
            sleep 1
        done
        echo "Case found"
    fi
    echo "${iter_count} ${SLURM_ARRAY_TASK_ID}"
    #determine a new output file for the fake_task
    OUTPUT_FILE=${SLURM_SUBMIT_DIR}/slurm-${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}_${iter_count}.out

    ### Add you script here with ${TASK_ID} as an argument
    ### the & at the end is important !!!
    cd ${WIRELES}/job/${case_name}_${iter_count}_grad_${CASE_ID}/src/
    make -j16 > compile_log
    srun -n 32 ${WIRELES}/job/${case_name}_${iter_count}_grad_${CASE_ID}/src/LES2  > ${OUTPUT_FILE} 2>&1

    cd ${WIRELES}/utils/optimization
    touch ${case_name}_${iter_count}_${CASE_ID}_done
    if [[ ${CASE_ID} -eq 0 ]]
    then
        echo "Check if other jobs have finished:"
        count=0
		while [[ ${count} -ne ${SLURM_ARRAY_TASK_MAX} ]]; do
            count=$(ls ./ | grep ${case_name}_${iter_count} | wc -l)
            sleep 10
        done
        echo "Other jobs done"
        python update.py ${case_name} ${iter_count}
    fi
done

echo "END: $(date)"
