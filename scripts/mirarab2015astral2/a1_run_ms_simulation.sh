#!/bin/bash

INTREE=$1
OUTDIR=$2

GROUPDIR="/fs/cbcb-lab/ekmolloy"
MS="$GROUPDIR/group/software/ms/msdir/ms"
RUNMS="$GROUPDIR/jdai123/dollo-study/tools/run_ms_simulation.py"

cd $OUTDIR

if [ ! -e mschars.nex ]; then
python3 $RUNMS \
    -m "$MS" \
    -i "$INTREE" \
    -o ""
fi

