#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=64gb
#SBATCH --partition=cbcb
#SBATCH --account=cbcb
##SBATCH --exclude=legacy[00-28]
#SBATCH --qos=highmem
#SBATCH --time=01:00:00

./a5_run_dollo_cdp.sh 
wait

./b5_run_dollo_cdp_fast.sh
wait

./c5_run_dollo_paup_hsearch.sh
wait

./d5_run_dollo_paup_bnb.sh
wait

