#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=64gb
#SBATCH --partition=cbcb
#SBATCH --account=cbcb
#SBATCH --exclude=legacy[00-28]
#SBATCH --qos=highmem
#SBATCH --time=00:30:00

# Model condition
NEWMODL="$MODL-$NCHR"

# Paths
PROJDIR="/fs/cbcb-lab/ekmolloy/jdai123/dollo-study"

# Input files
INDIR="/fs/cbcb-lab/ekmolloy/group/data/molloy2021theoretical/retrosim-study/data/"
CHARS="$INDIR/input-data-sets/$MODL/$REPL.nex"
STRE_TRUE="$INDIR/model-trees/${MODL}_model.tre"

# Output files
OUTDIR="$PROJDIR/data/molloy2021theoretical-sim/$NEWMODL"
if [ ! -d $OUTDIR ]; then
    mkdir $OUTDIR
fi
OUTDIR="$PROJDIR/data/molloy2021theoretical-sim/$NEWMODL/$REPL"
if [ ! -d $OUTDIR ]; then
    mkdir $OUTDIR
    cp $STRE_TRUE $OUTDIR/model_species_tree.tre
fi

./a2_vary_nchars.sh $CHARS $OUTDIR $NCHR
wait

