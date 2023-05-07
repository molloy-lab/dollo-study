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
MYMODL="$MODL,$NCHR,$REPL"

# Set outgroup based on model
if [ $MODL == "5taxa" ]; then
	OUTGROUP="Out"
elif [ $MODL == "6taxa" ]; then
	OUTGROUP="Out"
elif [ $MODL == "26taxa" ]; then
	OUTGROUP="TaxonU,TaxonV,TaxonW,TaxonX,TaxonY,TaxonZ"
elif [ $MODL == "Palaeognathae" ]; then
	OUTGROUP="galGal"
fi

# Paths
GROUPDIR="/fs/cbcb-lab/ekmolloy"
PROJDIR="$GROUPDIR/jdai123/dollo-study"
INOUTDIR="$PROJDIR/data/molloy2021theoretical-sim/$MODL-$NCHR/$REPL"

./d2_run_dollo_paup_bnb.sh $MYMODL $INOUTDIR $OUTGROUP
wait

