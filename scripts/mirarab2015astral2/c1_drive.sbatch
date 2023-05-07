#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=64gb
#SBATCH --partition=cbcb
#SBATCH --account=cbcb
#SBATCH --exclude=legacy[00-28]
#SBATCH --qos=highmem
#SBATCH --time=24:00:00

##module load Python3/3.8.15

# Model condition
TMP=$(echo $MODL | sed 's/-/,/g' | sed 's/model-//g')  # Line in CSV 
MYMODL="$TMP,$REPL"

# Paths
GROUPDIR="/fs/cbcb-lab/ekmolloy"
PROJDIR="$GROUPDIR/jdai123/dollo-study"
INOUTDIR="$PROJDIR/data/mirarab2015astral2/$MODL/$REPL"

./c1_run_dollo_cdp_fast.sh $MYMODL $INOUTDIR
wait

