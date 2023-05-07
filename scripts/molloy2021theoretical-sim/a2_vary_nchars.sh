#!/bin/bash

CHARS=$1
OUTDIR=$2
NCHR=$3

SEQTOOLS="/fs/cbcb-lab/ekmolloy/jdai123/dollo-study/tools/seqtools.py"

if [ ! -d $OUTDIR ]; then
    mkdir $OUTDIR
fi 
cd $OUTDIR

if [ ! -e chardata.nex ]; then
python3 $SEQTOOLS \
    -i $CHARS \
    -r -e $NCHR \
    -f nexus \
    -o chardata.nex
fi

