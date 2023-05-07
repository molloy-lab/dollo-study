#!/bin/bash

INDIR=$1
OUTDIR=$2
NCHR=$3

SEQTOOLS="/fs/cbcb-lab/ekmolloy/jdai123/dollo-study/tools/seqtools.py"

if [ ! -d $OUTDIR ]; then
    mkdir $OUTDIR
fi 
cd $OUTDIR

if [ ! -e mschars.nex ]; then
python3 $SEQTOOLS \
    -i $INDIR/mschars.nex \
    -r -e $NCHR \
    -f nexus \
    -o mschars.nex
fi

