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
OLDMODL="model.$NTAX.$SHGHT.$SRATE"
NEWMODL="model-$NTAX-$SHGHT-$SRATE-$NCHR"

# Paths
PROJDIR="/fs/cbcb-lab/ekmolloy/jdai123/dollo-study"

# Input and output files
INDIR="$PROJDIR/data/mirarab2015astral2/$OLDMODL/$REPL"
OUTDIR="$PROJDIR/data/mirarab2015astral2/$NEWMODL"
if [ ! -d $OUTDIR ]; then
    mkdir $OUTDIR
fi
OUTDIR="$PROJDIR/data/mirarab2015astral2/$NEWMODL/$REPL"
if [ ! -d $OUTDIR ]; then
    mkdir $OUTDIR
    cp /fs/cbcb-lab/ekmolloy/group/data/mirarab2015astral2/$OLDMODL/$REPL/s_tree.trees $OUTDIR
fi

./b1_vary_nchars.sh $INDIR $OUTDIR $NCHR
wait

