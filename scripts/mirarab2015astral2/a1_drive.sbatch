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
MODL="model.$NTAX.$SHGHT.$SRATE"

# Paths
GROUPDIR="/fs/cbcb-lab/ekmolloy"
PROJDIR="$GROUPDIR/jdai123/dollo-study"

# Input files
INDIR="$GROUPDIR/group/data/mirarab2015astral2/$MODL/$REPL"
STRE_TRUE="$INDIR/s_tree.trees"

# Output files
OUTDIR="$PROJDIR/data/mirarab2015astral2/$MODL/$REPL"

cp $STRE_TRUE $OUTDIR
#cd $OUTDIR
#gzip mschars.nex

#./a1_run_ms_simulation.sh $STRE_TRUE $OUTDIR
wait

