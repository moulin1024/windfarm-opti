#!/bin/bash
CASE_ID=$(( ( ${SLURM_ARRAY_TASK_ID} - 1 ) ))
echo "Case ${CASE_ID}"

case_name=$1
total_job_num=$2
search_type=$3

OUTPUT_FILE=${WIRELES}/case/${case_name}/log/slurm-${SLURM_ARRAY_JOB_ID}-${iter_num}-${SLURM_ARRAY_TASK_ID}_solve.out
for iter_num in {0..10}
do
    if [[ ${CASE_ID} -eq 0 ]]
    then
        python ${WIRELES}/utils/create_search_job.py ${case_name} ${total_job_num} ${iter_num} ${search_type}
    else
        echo "Pausing until case exists:"
        while : ; do
            [[ -f ${WIRELES}/case/${case_name}/${iter_num}-${CASE_ID}/src/input/cl_cd.dat ]] && break
            sleep 1
        done
        echo "Case found"
    fi

    cd ${WIRELES}/case/${case_name}/${iter_num}-${CASE_ID}/src/
    echo ${WIRELES}/case/${case_name}/${iter_num}-${CASE_ID}/src/
    make -j16 > compile_log
    rm -rf *.f90
    rm -rf *.o
   	srun -n 32 LES2  > ${OUTPUT_FILE} 2>&1

    cd ${WIRELES}/case/${case_name}/log
    touch ${case_name}_${iter_num}_${CASE_ID}_done
    if [[ ${CASE_ID} -eq 0 ]]
    then
        echo "Check if other jobs have finished:"
        count=0
		while [[ ${count} -ne ${SLURM_ARRAY_TASK_MAX} ]]; do
            count=$(ls ./ | grep ${case_name}_${iter_num} | wc -l)
            sleep 10
        done
        echo "Other jobs done"
        python ${WIRELES}/utils/collect.py ${case_name} ${iter_num}
    fi
done
